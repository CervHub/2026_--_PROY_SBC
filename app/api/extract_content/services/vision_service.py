import os


class VisionService:
    _client = None

    @staticmethod
    def get_client():
        """Inicializa el cliente de Google Vision de forma perezosa.

        También asegura que las credenciales GCP estén disponibles llamando
        a `ensure_gcp_credentials()` sólo cuando sea necesario.
        """
        if VisionService._client is None:
            # Cargar credenciales GCP de forma perezosa
            from app.utils.gcp_credentials import ensure_gcp_credentials

            ensure_gcp_credentials()
            # Importar el cliente de Vision sólo cuando se vaya a usar
            from google.cloud import vision

            VisionService._client = vision.ImageAnnotatorClient()
        return VisionService._client

    @staticmethod
    def hw(image_path: str) -> str:
        """Realiza OCR (Hand Writing) usando Google Cloud Vision API.

        Carga sólo las dependencias necesarias en tiempo de ejecución para
        reducir el tiempo de cold-start.
        """
        client = VisionService.get_client()
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        from google.cloud import vision

        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)
        return response.full_text_annotation.text

    @staticmethod
    def omr(image_path: str, temp_dir: str = None) -> bool:
        # Importar OpenCV y numpy de forma perezosa
        import cv2
        import numpy as np

        # Lee la imagen
        img = cv2.imread(image_path, 0)

        # preparar directorio de debug dentro del temp_dir del pipeline
        image_dir = os.path.dirname(image_path)
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        if temp_dir:
            debug_dir = os.path.join(temp_dir, "debug")
        else:
            # fallback legacy: Si la imagen está en outputs/output_xxx/regions/region_N.png, guardar en outputs/output_xxx/debug/
            if os.path.basename(image_dir) == "regions":
                parent_dir = os.path.dirname(image_dir)
                debug_dir = os.path.join(parent_dir, "debug")
            else:
                debug_dir = os.path.join(image_dir, "debug")
        os.makedirs(debug_dir, exist_ok=True)
        base_name = image_name
        cv2.imwrite(os.path.join(debug_dir, f"{base_name}_0_original.png"), img)

        # 1. Recorte interno del 10%
        h, w = img.shape
        pad = int(min(h, w) * 0.1)
        inner = img[pad:h-pad, pad:w-pad]
        cv2.imwrite(os.path.join(debug_dir, f"{base_name}_1_inner10.png"), inner)
        if inner.size == 0:
            return False

        # 2. Binarización adaptativa según iluminación
        mean_val = np.mean(inner)
        min_thresh = 80
        max_thresh = 180
        offset = -50
        thresh_val = int(np.clip(mean_val + offset, min_thresh, max_thresh))
        _, thresh = cv2.threshold(inner, thresh_val, 255, cv2.THRESH_BINARY_INV)
        cv2.imwrite(os.path.join(debug_dir, f"{base_name}_2_thresh_{thresh_val}.png"), thresh)

        # 3. Recorte cuadrado centrado en los componentes
        # Encontrar bounding box de todos los componentes
        coords = cv2.findNonZero(thresh)
        if coords is None:
            return False
        x, y, w_box, h_box = cv2.boundingRect(coords)
        # Hacer el recorte cuadrado centrado
        cx = x + w_box // 2
        cy = y + h_box // 2
        min_side = 10
        side = max(max(w_box, h_box), min_side)
        # Definir los límites del recorte cuadrado
        half = side // 2
        start_x = max(cx - half, 0)
        start_y = max(cy - half, 0)
        end_x = min(start_x + side, thresh.shape[1])
        end_y = min(start_y + side, thresh.shape[0])
        # Ajustar si el recorte se sale de la imagen
        if end_x - start_x < side:
            start_x = max(end_x - side, 0)
        if end_y - start_y < side:
            start_y = max(end_y - side, 0)
        square = thresh[start_y:end_y, start_x:end_x]
        # Si el recorte es menor a 10x10, rellenar con ceros para que sea 10x10
        sh, sw = square.shape
        if sh < min_side or sw < min_side:
            padded = np.zeros((max(sh, min_side), max(sw, min_side)), dtype=square.dtype)
            padded[:sh, :sw] = square
            square = padded
        cv2.imwrite(os.path.join(debug_dir, f"{base_name}_3_square.png"), square)
        if square.size == 0:
            return False

        # 4. Calcular densidad
        density = np.sum(square > 0) / square.size

        # 5. Calcular componentes
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(square, 8)
        areas = stats[1:, cv2.CC_STAT_AREA]

        # 6. Calcular peso por píxel respecto al centro
        center_y, center_x = square.shape[0] / 2, square.shape[1] / 2
        yy, xx = np.indices(square.shape)
        dist = np.sqrt(((xx - center_x) / center_x) ** 2 + ((yy - center_y) / center_y) ** 2)
        mask = (square > 0)
        pixel_weights = (1 - dist) * mask
        center_weight = np.sum(pixel_weights) / np.sum(mask) if np.sum(mask) > 0 else 0

        # 7. Calcular peso por cantidad de componentes
        valid_areas = [a for a in areas if 5 < a < (square.size * 0.5)]
        n_components = len(valid_areas)

        # 8. Calcular ponderación final
        score = (
            0.6 * density +           # densidad tiene más peso
            0.2 * center_weight +     # peso por píxel respecto al centro
            0.0 * (n_components / 10) # más componentes suma peso, normalizado
        )

        # 9. Calcular threshold adaptativo: decae suavemente con el área, nunca menor a 0.05 ni mayor a 0.3
        area = square.size
        _min = 0.05
        _max = 0.3
        smooth_factor = 0.005
        threshold = _max / (1 + smooth_factor * area) + _min
        threshold = min(max(threshold, _min), _max)

        return score > threshold