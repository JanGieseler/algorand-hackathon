from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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