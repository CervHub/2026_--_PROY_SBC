import json
import time
import cv2
import numpy as np
import os
import lib.models.ilo_abastecimientos_almacenes_y_trafico_v01 as ilo_aayt_v01
import lib.models.ilo_ferrocarril_industrial_v02 as ilo_fi_v02
from lib.resolver import Resolver
from lib.debug import Debug

def align_and_crop(input_path, template_path, data, output_dir="outputs/regions"):
    """"Alinea la imagen de entrada con la plantilla y recorta las regiones especificadas."""
    # Leer imágenes
    img = cv2.imread(input_path, 0)
    template = cv2.imread(template_path, 0)

    # Detectar puntos clave y descriptores
    orb = cv2.ORB_create(10000)
    kp1, des1 = orb.detectAndCompute(template, None)
    kp2, des2 = orb.detectAndCompute(img, None)

    # Hacer matching de puntos
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    # Calcular homografía
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1,1,2)
    H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

    # Alinear imagen
    h, w = template.shape
    aligned = cv2.warpPerspective(img, H, (w, h))

    # Crear carpeta de salida
    os.makedirs(output_dir, exist_ok=True)

    # Recorrer todas las regiones en profundidad y guardar cada crop
    for idx, region in enumerate(data.iter_regions()):
        y1, y2, x1, x2 = region.as_tuple()
        crop = aligned[y1:y2, x1:x2]
        # Nombre único para cada región
        out_path = os.path.join(output_dir, f"region_{idx}.png")
        cv2.imwrite(out_path, crop)
        region.image_path = out_path


def resolve(data, max_workers=8):
    """
    Procesa todas las regiones usando una cola de trabajo y un pool de threads.
    Cada thread toma una región, la procesa según su tipo (OCR, DENSITY, HW)
    y continúa hasta vaciar la cola.
    """
    import threading
    import queue

    q = queue.Queue()

    # Cargar regiones válidas en la cola
    for region in data.iter_regions():
        if not hasattr(region, 'resolver') or region.resolver is None:
            continue
        if not hasattr(region, 'image_path') or region.image_path is None:
            continue
        q.put(region)

    # Worker que consume de la cola
    def worker():
        while True:
            try:
                region = q.get(timeout=1)  # evita bloqueo infinito
            except queue.Empty:
                return  # cola vacía → thread termina

            start = time.time()

            try:
                if region.resolver.value == "OCR":
                    value = Resolver.ocr(region.image_path)

                elif region.resolver.value == "DENSITY":
                    value = str(Resolver.density(region.image_path))

                elif region.resolver.value == "HW":
                    value = Resolver.hw(region.image_path)

                else:
                    print(f"Unknown resolver {region.resolver} for region {region.as_tuple()}")
                    value = None

            except Exception as e:
                print(f"[resolve][ERROR] {region.image_path}: {e}")
                value = None

            end = time.time()

            region.extracted_value = value
            Debug.print_timed(f"[resolve][{region.resolver.value}] {region.image_path}", end - start)

            q.task_done()

    # Lanzar workers
    threads = []
    for _ in range(max_workers):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)

    # Esperar a que la cola se vacíe
    q.join()

    # Esperar a que terminen los threads
    for t in threads:
        t.join()

def main():
    t0 = time.time()
    # dir = "inputs/ilo/abastecimientos"
    # file = "ilo.abastecimientos_almacenes_y_trafico.v01"
    dir = "inputs/ilo/ferrocarril_industrial"
    file = "ilo.ferrocarril_industrial.v02"
    data_dir = os.path.join(dir, "data")

    # Paso 0: Cargar datos --------------------------------------------------------------
    t_load0 = time.time()
    json_path = os.path.join(data_dir, f"{file}.json")
    with open(json_path, "r") as f:
        raw_data = json.load(f)
    data = ilo_fi_v02.IloFerrocarrilIndustrialV02.from_json(raw_data)
    t_load1 = time.time()
    Debug.print_timed("[step][0] Carga de datos", t_load1 - t_load0)

    # Paso 1: Segmentar la imagen en regiones --------------------------------------------------------------
    template_path = os.path.join(dir, f"{file}.jpg")
    # input_path    = os.path.join(dir, f"{file}.jpg")
    # input_path    = os.path.join(dir, f"{file}.eg001.png")
    input_path    = os.path.join(dir, f"{file}.eg002.jpeg")
    # input_path    = os.path.join(dir, f"{file}.eg003.jpeg")
    # input_path    = os.path.join(dir, f"{file}.eg004.jpeg")

    t_crop0 = time.time()
    align_and_crop(input_path, template_path, data)
    t_crop1 = time.time()
    Debug.print_timed("[step][1] Segmentación y crop", t_crop1 - t_crop0)

    # Paso 2: Resolver valores de cada región --------------------------------------------------------------
    t_resolve0 = time.time()
    resolve(data)
    t_resolve1 = time.time()
    Debug.print_timed("[step][2] Resolución de regiones", t_resolve1 - t_resolve0)

    # Tiempo total --------------------------------------------------------------
    t1 = time.time()
    Debug.print_timed("Tiempo de ejecución total", t1-t0)

    # Guardar resultados --------------------------------------------------------------                                    
    output_path = os.path.join("outputs", f"{file}.result.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data.to_json(), f, indent=4, ensure_ascii=False)
    print(f"Resultados guardados en {output_path}")


if __name__ == "__main__":
    main()

# export GOOGLE_APPLICATION_CREDENTIALS="/Users/cerv/Projects/2026_--_Proy_SBC/sbc-contentextraction-9cf6e2740a0d.json"