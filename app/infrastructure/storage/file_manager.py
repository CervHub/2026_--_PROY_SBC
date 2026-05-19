
import os
import uuid
import shutil
from fastapi import UploadFile
from typing import List, Optional
from app.config.config import settings


class FileManager:
    def __init__(self):
        unique_id = str(uuid.uuid4())
        # Use /tmp in AWS Lambda (writable). Allow override via TMP_DIR env var for local testing.
        base_root = os.environ.get("TMP_DIR", "/tmp")
        self.base_dir = os.path.join(base_root, unique_id)
        os.makedirs(self.base_dir, exist_ok=True)

    def create_temp_dir(self) -> str:
        os.makedirs(self.base_dir, exist_ok=True)
        return self.base_dir

    async def save_uploaded_file(self, file: UploadFile, prefix: Optional[str] = None) -> str:
        filename = file.filename
        if prefix:
            filename = f"{prefix}_{filename}"
        save_path = os.path.join(self.base_dir, filename)
        with open(save_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        return save_path

    async def save_multiple_files(self, files: List[UploadFile], prefix: Optional[str] = None) -> List[str]:
        paths = []
        for idx, file in enumerate(files):
            pfx = f"{prefix}_{idx}" if prefix else str(idx)
            path = await self.save_uploaded_file(file, prefix=pfx)
            paths.append(path)
        return paths

    def delete_temp_dir(self):
        if os.path.exists(self.base_dir):
            shutil.rmtree(self.base_dir)