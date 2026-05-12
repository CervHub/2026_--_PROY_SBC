from fastapi import FastAPI
from app.config.config import Settings
from app.api import routes

def get_settings():
	return Settings()

app = FastAPI(title="SBC Content Extraction API")

# Incluir rutas
app.include_router(routes.router)

# export GOOGLE_APPLICATION_CREDENTIALS="/Users/cerv/Projects/2026_--_Proy_SBC/sbc-contentextraction-9cf6e2740a0d.json"