from fastapi import APIRouter
from app.presentation.api.v1.endpoints.patients import router as patients_router

api_v1_router = APIRouter()
api_v1_router.include_router(patients_router)
