from fastapi import Depends
from app.api.extract_content.api.request_dto import ExtractRequest
from app.api.extract_content.api.request_validator import RequestValidator
from app.api.extract_content.api.dependencies import get_extraction_pipeline
from app.api.extract_content.services.extraction_pipeline import ExtractionPipeline


async def extract_content(
    request: ExtractRequest = Depends(RequestValidator.validate),
    pipeline: ExtractionPipeline = Depends(get_extraction_pipeline),
):
    return await pipeline.execute(
        images=request.images,
        reference_form=request.reference_form,
        bounding_boxes=request.bounding_boxes,
    )