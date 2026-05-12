from app.api.extract_content.services.extraction_pipeline import ExtractionPipeline


def get_extraction_pipeline() -> ExtractionPipeline:
    return ExtractionPipeline()
