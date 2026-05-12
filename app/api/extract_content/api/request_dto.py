from dataclasses import dataclass
from fastapi import UploadFile


@dataclass
class ExtractRequest:
    images: list[UploadFile]
    reference_form: UploadFile
    bounding_boxes: UploadFile