import os

import numpy as np
import cv2
import pytesseract
from google.cloud import vision

class Resolver:
    @staticmethod
    def ocr(image_path):
        """
        Realiza OCR en la imagen dada y retorna el texto extraído.
        """
        config = "--oem 1 --psm 6"
        img = cv2.imread(image_path, 0)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        return pytesseract.image_to_string(img, lang="spa", config=config)

    client = vision.ImageAnnotatorClient()
    @staticmethod
    def hw(image_path):
        """"
        Realiza OCR (Especializado en Hand Writing) usando Google Cloud Vision API y retorna el texto extraído.
        """
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = Resolver.client.document_text_detection(image=image)
        return response.full_text_annotation.text

    @staticmethod
    def density(image_path, threshold=35, debug_dir="outputs/debug"):
        """
        Heurística modificada: ignora el borde de la casilla y analiza solo el interior.
        Ahora compara la cantidad absoluta de píxeles negros con el umbral.
        """
        # Leer imagen
        img = cv2.imread(image_path, 0)
        # Binarizar (invertida, umbral fijo bajo)
        # Solo los píxeles realmente oscuros se consideran "marcados"
        _, thresh = cv2.threshold(img, 70, 255, cv2.THRESH_BINARY_INV)
        # Cantidad de píxeles negros
        black_pixels = np.sum(thresh > 0)
        # Guardar para debug con black_pixels en el nombre
        # os.makedirs(debug_dir, exist_ok=True)
        # base, ext = os.path.splitext(os.path.basename(image_path))
        # debug_filename = f"{base}_black_{black_pixels}{ext}"
        # debug_path = os.path.join(debug_dir, debug_filename)
        # cv2.imwrite(debug_path, thresh)
        return black_pixels > threshold