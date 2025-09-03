from fastapi import APIRouter

from .models import (
    HealthResponse, 
    AssetUploadRequest, 
    AssetUploadResponse, 
    AssetsListResponse, 
    AssetResponse,
    AssetId
)
from .utils import save_asset, get_asset_by_id, get_all_assets

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def root():
    return HealthResponse(
        status="ok",
        message="Algorand Hackathon API is running"
    )

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        message="API server is operational"
    )

@router.post("/upload", response_model=AssetUploadResponse)
async def upload_asset(asset: AssetUploadRequest):
    asset_id = save_asset(asset)
    return AssetUploadResponse(
        success=True,
        asset_id=asset_id,
        message="Asset uploaded successfully"
    )

@router.get("/assets", response_model=AssetsListResponse)
async def list_assets():
    assets = get_all_assets()
    return AssetsListResponse(
        success=True,
        assets=assets,
        message="Assets retrieved successfully"
    )

@router.get("/assets/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: str):
    try:
        asset_id_obj = AssetId.from_string(asset_id)
        asset = get_asset_by_id(asset_id_obj)
    except ValueError:
        return AssetResponse(
            success=False,
            asset=None,
            message="Invalid asset ID format"
        )
    if asset is None:
        return AssetResponse(
            success=False,
            asset=None,
            message="Asset not found"
        )
    
    return AssetResponse(
        success=True,
        asset=asset,
        message="Asset retrieved successfully"
    )