from fastapi import APIRouter
from app.api.extract_content.api.endpoints import extract_content

router = APIRouter()

router.add_api_route("/api/sbc/extract-content", extract_content, methods=["POST"])