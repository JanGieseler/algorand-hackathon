from fastapi import APIRouter
from datetime import datetime

from .models import (
    HealthResponse, 
    AssetUploadRequest, 
    AssetUploadResponse, 
    AssetsListResponse, 
    AssetSummary,
    AssetResponse,
    Asset,
    GPSCoordinates
)
from .utils import generate_asset_id

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
    asset_id = generate_asset_id(asset)
    return AssetUploadResponse(
        success=True,
        asset_id=asset_id,
        message="Asset uploaded successfully"
    )

@router.get("/assets", response_model=AssetsListResponse)
async def list_assets():
    dummy_assets = [
        AssetSummary(asset_id="a7e59cf752cd9cf52a016d79f56ef4986132c889b198a97e4e63f5346ad1ed11", description="Sample asset 1"),
        AssetSummary(asset_id="08d1eed0344be85ec7cb37e7e244327b424d92e09a6c4a4facc4d98fb227c27b", description="Sample asset 2"),
        AssetSummary(asset_id="91b1f3f26882f6db4c2e427c3dbf7f76e7fb493b7c4866812395ef00a6834515", description="Sample asset 3")
    ]
    return AssetsListResponse(
        success=True,
        assets=dummy_assets,
        message="Assets retrieved successfully"
    )

@router.get("/assets/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: str):
    dummy_asset = Asset(
        asset_id=asset_id,
        description="Sample asset description",
        content="This is the sample content of the asset",
        location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
        timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
        creator="creator123",
        publisher="publisher456"
    )
    return AssetResponse(
        success=True,
        asset=dummy_asset,
        message="Asset retrieved successfully"
    )