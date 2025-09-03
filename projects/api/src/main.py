from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
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