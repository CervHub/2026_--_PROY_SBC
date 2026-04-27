import copy
import json
import cv2
import os
import numpy as np
import threading
import lib.models.ilo_abastecimientos_almacenes_y_trafico_v01 as ilo_aayt_v01
import lib.models.ilo_ferrocarril_industrial_v02 as ilo_fi_v02
from lib.resolver import Resolver
from lib.debug import Debug
from lib.parallel_task_queue import ParallelTaskQueue

def align_and_crop(input_path, template_path, data, output_dir="outputs"):
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
        region_dir = os.path.join(output_dir, "regions")
        os.makedirs(region_dir, exist_ok=True)
        out_path = os.path.join(region_dir, f"region_{idx}.png")
        cv2.imwrite(out_path, crop)
        region.image_path = out_path

def resolve(data):
    """
    Procesa todas las regiones usando ParallelTaskQueue.
    Cada región válida se resuelve en paralelo y se espera a que todas terminen.
    """
    futures = []

    def process_region(region):
        try:
            if region.resolver.value == "OCR":
                value = Resolver.ocr(region.image_path)
            elif region.resolver.value == "OMR":
                value = str(Resolver.omr(region.image_path))
            elif region.resolver.value == "HW":
                value = Resolver.hw(region.image_path)
            else:
                print(f"[resolve][ERROR] Unknown resolver {region.resolver} for region {region.as_tuple()}")
                value = None
        except Exception as e:
            print(f"[resolve][ERROR] {region.image_path}: {e}")
            value = None
        return value

    for region in data.iter_regions():
        if not hasattr(region, 'resolver') or region.resolver is None:
            continue
        if not hasattr(region, 'image_path') or region.image_path is None:
            continue
        future = ParallelTaskQueue.submit(process_region, region)
        futures.append((region, future))

    # Esperar a que todas las tareas terminen y asignar el resultado
    for region, future in futures:
        region.extracted_value = future.result()

def main():
    input_dir = "inputs"
    corporation_dir = "ilo"
    management_dir = "ferrocarril_industrial"
    version = "v02"

    target_dir = os.path.join(input_dir, corporation_dir, management_dir)
    target_base_path = f"{corporation_dir}.{management_dir}.{version}"
    target_template_path = os.path.join(target_dir, f"{target_base_path}.jpg")
    target_template_mapping_path = os.path.join(target_dir, f"data/{target_base_path}.json")

    # Lista de sufijos para los archivos de entrada
    input_suffixes = ["001.png", "002.jpeg", "003.jpeg", "004.jpeg", "005.jpeg"]
    input_paths = [os.path.join(target_dir, f"{target_base_path}.eg{suffix}") for suffix in input_suffixes]

    # Paso 0: Cargar datos (una vez) --------------------------------------------------------------
    with open(target_template_mapping_path, "r") as f:
        raw_data = json.load(f)
    template_data = ilo_fi_v02.IloFerrocarrilIndustrialV02.from_json(raw_data)    
    data_list = [copy.deepcopy(template_data) for _ in input_paths]

    # Paso 1: Segmentar la imagen en regiones (en paralelo) --------------------------------------------------------------
    align_futures = []
    for input_path, data, suffix in zip(input_paths, data_list, input_suffixes):
        output_dir = os.path.join("outputs", f"output_{suffix}")
        future = ParallelTaskQueue.submit(align_and_crop, input_path, target_template_path, data, output_dir)
        align_futures.append(future)
    for future in align_futures:
        future.result()

    # Paso 2: Resolver valores de cada región (en paralelo por documento) --------------------------------------------------------------
    resolve_threads = []
    for data in data_list:
        t = threading.Thread(target=resolve, args=(data,))
        t.start()
        resolve_threads.append(t)
    for t in resolve_threads:
        t.join()

    # Paso 3: Guardar resultados --------------------------------------------------------------
    for data, suffix in zip(data_list, input_suffixes):
        output_dir = os.path.join("outputs", f"output_{suffix}")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "result.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data.to_json(), f, indent=4, ensure_ascii=False)
        print(f"Resultados guardados en {output_path}")


if __name__ == "__main__":
    Debug.time(lambda: main(), "Tiempo de ejecución total")

# export GOOGLE_APPLICATION_CREDENTIALS="/Users/cerv/Projects/2026_--_Proy_SBC/sbc-contentextraction-9cf6e2740a0d.json"