from fastapi import File, HTTPException, UploadFile, status
from app.api.extract_content.api.request_dto import ExtractRequest

class RequestValidator:
    async def validate(
        images: list[UploadFile] = File(...),
        reference_form: UploadFile = File(...),
        bounding_boxes: UploadFile = File(...),
    ) -> ExtractRequest:

        # Validar imágenes
        if len(images) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe enviar al menos una imagen",
            )

        # Validar reference_form
        if not reference_form.filename.lower().endswith(".jpg"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reference_form debe ser una imagen",
            )

        # Validar bounding_boxes
        if not bounding_boxes.filename.lower().endswith(".json"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="bounding_boxes debe ser un JSON",
            )

        return ExtractRequest(
            images=images,
            reference_form=reference_form,
            bounding_boxes=bounding_boxes,
        )