from fastapi import FastAPI
from app.config.config import Settings
from app.api import routes
from mangum import Mangum

import os
import json
import logging

import boto3
from botocore.exceptions import ClientError

def get_settings():
	return Settings()

app = FastAPI(title="SBC Content Extraction API")

# Incluir rutas
app.include_router(routes.router)

async def startup_event():
	"""At startup, try to fetch GCP service account JSON from AWS Secrets Manager
	and write it to a file under /tmp, then set GOOGLE_APPLICATION_CREDENTIALS.
	This allows the container to obtain GCP credentials securely via Secrets Manager.
	"""
	secret_name = os.environ.get("GCP_SECRET_NAME", "sbc-contentextraction-9cf6e2740a0d")
	region_name = os.environ.get("AWS_REGION", "us-east-1")

# export GOOGLE_APPLICATION_CREDENTIALS="/Users/cerv/Projects/2026_--_Proy_SBC/sbc-contentextraction-9cf6e2740a0d.json"