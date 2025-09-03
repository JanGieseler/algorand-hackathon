from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import hashlib
import json

app = FastAPI(
    title="Algorand Hackathon API",
    description="FastAPI backend for Algorand hackathon project",
    version="0.1.0",
)

class HealthResponse(BaseModel):
    status: str
    message: str

class GPSCoordinates(BaseModel):
    latitude: float
    longitude: float

class AssetUploadRequest(BaseModel):
    description: str
    content: str
    location: GPSCoordinates
    timestamp: datetime
    creator: str
    publisher: str

class AssetUploadResponse(BaseModel):
    success: bool
    asset_id: Optional[str] = None
    message: str

class AssetSummary(BaseModel):
    asset_id: str
    description: str

class AssetsListResponse(BaseModel):
    success: bool
    assets: List[AssetSummary]
    message: str

class Asset(BaseModel):
    asset_id: str
    description: str
    content: str
    location: GPSCoordinates
    timestamp: datetime
    creator: str
    publisher: str

class AssetResponse(BaseModel):
    success: bool
    asset: Optional[Asset] = None
    message: str

def generate_asset_id(asset: AssetUploadRequest) -> str:
    data_to_hash = {
        "content": asset.content,
        "location": {"latitude": asset.location.latitude, "longitude": asset.location.longitude},
        "timestamp": asset.timestamp.isoformat(),
        "creator": asset.creator,
        "publisher": asset.publisher
    }
    
    hash_string = json.dumps(data_to_hash, sort_keys=True)
    return hashlib.sha256(hash_string.encode()).hexdigest()

@app.get("/", response_model=HealthResponse)
async def root():
    return HealthResponse(
        status="ok",
        message="Algorand Hackathon API is running"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        message="API server is operational"
    )

@app.post("/upload", response_model=AssetUploadResponse)
async def upload_asset(asset: AssetUploadRequest):
    asset_id = generate_asset_id(asset)
    return AssetUploadResponse(
        success=True,
        asset_id=asset_id,
        message="Asset uploaded successfully"
    )

@app.get("/assets", response_model=AssetsListResponse)
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

@app.get("/assets/{asset_id}", response_model=AssetResponse)
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