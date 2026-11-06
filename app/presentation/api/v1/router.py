from fastapi import APIRouter
from app.presentation.api.v1.endpoints.ppr1001 import router as ppr1001_router

api_v1_router = APIRouter()
api_v1_router.include_router(ppr1001_router)
