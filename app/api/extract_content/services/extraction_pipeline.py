

import os
import json
import copy
from typing import List, Any
from fastapi import UploadFile
from app.api.extract_content.domain.models.model import Model
from app.infrastructure.storage.file_manager import FileManager
from app.api.extract_content.services.pdf_service import PDFService
from app.api.extract_content.services.extraction_service import ExtractionService

class ExtractionPipeline:
	@staticmethod
	async def execute(images: List[UploadFile], reference_form: UploadFile, bounding_boxes: UploadFile) -> Any:
		# 1. Crear directorio temporal único
		file_manager = FileManager()
		temp_dir = file_manager.create_temp_dir()
		print(f"[execute] Temporary directory created: {temp_dir}")

		# 2. Guardar archivos de template
		reference_form_path = await file_manager.save_uploaded_file(reference_form, prefix="reference_form")
		bounding_boxes_path = await file_manager.save_uploaded_file(bounding_boxes, prefix="bounding_boxes")

		# 3. Guardar imágenes subidas (pueden ser imágenes o PDFs)
		input_paths = []
		pdf_service = PDFService()
		for idx, img in enumerate(images):
			ext = img.filename.lower().split('.')[-1]
			if ext == 'pdf':
				# Convertir PDF a imágenes
				pdf_img_dir = os.path.join(temp_dir, f"pdf_{idx}")
				os.makedirs(pdf_img_dir, exist_ok=True)
				pdf_image_paths = await pdf_service.convert_to_images(img, pdf_img_dir)
				input_paths.extend(pdf_image_paths)
			else:
				img_path = await file_manager.save_uploaded_file(img, prefix=f"img_{idx}")
				input_paths.append(img_path)

		# 4. Cargar el template/modelo desde bounding_boxes
		with open(bounding_boxes_path, "r") as f:
			raw_data = json.load(f)
		template_data = Model.from_json(raw_data)

		# 5. Para cada imagen, clonar el template y segmentar/extraer.
		# Si la imagen no se puede alinear, la saltamos.
		data_list = []
		for input_path in input_paths:
			data = copy.deepcopy(template_data)
			output_dir = os.path.join(temp_dir, f"output_{os.path.basename(input_path)}")
			try:
				success = ExtractionService.align_and_crop(input_path, reference_form_path, data, output_dir)
			except Exception as e:
				print(f"[execute][WARN] Error processing {input_path}: {e}")
				continue
			if not success:
				print(f"[execute][INFO] Skipping {input_path} because alignment failed.")
				continue
			data_list.append(data)

		# 6. Resolver regiones (OCR/OMR/HW)
		for data in data_list:
			ExtractionService.resolve(data)

		# 7. Limpiar directorio temporal
		file_manager.delete_temp_dir()

		# 8. Devolver resultados serializados
		results = [data.to_json() for data in data_list]
		return results
