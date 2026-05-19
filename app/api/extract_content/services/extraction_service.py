import os
import numpy as np
from app.config.config import settings
from app.api.extract_content.domain.models.model import Model
from app.infrastructure.parallel.parallel_task_queue import ParallelTaskQueue
from app.api.extract_content.services.vision_service import VisionService

class ExtractionService:
    @staticmethod
    def align_and_crop(input_path: str, template_path: str, data: Model, output_dir: str):
        """Alinea la imagen de entrada con la plantilla usando la función especificada y recorta las regiones."""
        # Importar OpenCV de forma perezosa para evitar overhead en cold-start
        import cv2
        # Leer imágenes
        img = cv2.imread(input_path, 0)
        template = cv2.imread(template_path, 0)

        if img is None or template is None:
            raise ValueError(f"Unable to read input or template image: {input_path}, {template_path}")

        # Seleccionar función de alineamiento
        try:
            aligned = ExtractionService.align_by_feature_matching(img, template)
        except Exception as e:
            print(f"[align_and_crop][WARN] Alignment failed for {input_path}: {e}")
            return False

        ExtractionService.crop_regions(aligned, data, output_dir)
        return True

    @staticmethod
    def align_by_feature_matching(img: 'np.ndarray', template: 'np.ndarray') -> 'np.ndarray':
        """Alinea img con template usando feature matching y retorna la imagen alineada."""
        import cv2
        orb = cv2.ORB_create(10000)
        kp1, des1 = orb.detectAndCompute(template, None)
        kp2, des2 = orb.detectAndCompute(img, None)

        if des1 is None or des2 is None:
            raise ValueError(f"No descriptors found (des1_found={des1 is not None}, des2_found={des2 is not None})")

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        try:
            matches = bf.match(des1, des2)
        except cv2.error as e:
            raise ValueError(f"Feature matching failed: {e}")

        if not matches:
            raise ValueError("No matches found between image and template.")

        matches = sorted(matches, key=lambda x: x.distance)
        if len(matches) < 4:
            raise ValueError("No hay suficientes matches para calcular la homografía.")

        num_good_matches = max(4, min(100, int(len(matches) * 0.15)))
        good_matches = matches[:num_good_matches]

        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)
        H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
        if H is None:
            raise ValueError("Homography could not be computed.")

        # template may be grayscale (h, w) or color (h, w, c)
        h, w = template.shape[:2]
        aligned = cv2.warpPerspective(img, H, (w, h))
        return aligned

    @staticmethod
    def crop_regions(aligned: 'np.ndarray', data: Model, output_dir: str):
        """Recorta y guarda las regiones de interés de la imagen alineada."""
        import cv2

        region_dir = os.path.join(output_dir, "regions")
        os.makedirs(region_dir, exist_ok=True)
        for idx, region in enumerate(data.iter_regions()):
            y1, y2, x1, x2 = region.as_tuple()
            crop = aligned[y1:y2, x1:x2]
            out_path = os.path.join(region_dir, f"region_{idx}.png")
            cv2.imwrite(out_path, crop)
            region.image_path = out_path

    @staticmethod
    def resolve(data: Model):
        """
        Procesa todas las regiones usando ParallelTaskQueue.
        Cada región válida se resuelve en paralelo y se espera a que todas terminen.
        """
        futures = []

        def process_region(region):
            try:
                if hasattr(region, 'fixed_value') and region.fixed_value is not None:
                    value = region.fixed_value
                elif region.resolver.value == "OCR":
                    value = ""
                    # value = VisionService.ocr(region.image_path)
                elif region.resolver.value == "OMR":
                    value = bool(VisionService.omr(region.image_path))
                elif region.resolver.value == "HW":
                    value = VisionService.hw(region.image_path)
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

