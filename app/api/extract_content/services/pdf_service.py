import os
from fastapi import UploadFile
from typing import List


class PDFService:
    @staticmethod
    async def convert_to_images(pdf_file: UploadFile, output_dir: str) -> List[str]:
        """
        Convierte un archivo PDF (UploadFile) en imágenes y las guarda en output_dir.
        Retorna la lista de rutas de las imágenes generadas.
        """
        # Importar pdf2image sólo cuando se vaya a convertir
        from pdf2image import convert_from_bytes

        os.makedirs(output_dir, exist_ok=True)
        content = await pdf_file.read()
        pages = convert_from_bytes(content)
        image_paths = []
        for page_num, page in enumerate(pages):
            img_path = os.path.join(output_dir, f"page_{page_num+1}.jpg")
            page.save(img_path, 'JPEG')
            image_paths.append(img_path)
        return image_paths