from pydantic import BaseModel, Field
from typing import Optional, List, NewType
from datetime import datetime

class AssetId(BaseModel):
    """
    Type-safe Asset ID representation.
    
    Provides validation and type safety for asset identifiers,
    ensuring they are valid SHA-256 hashes.
    """
    
    value: str = Field(..., min_length=64, max_length=64, pattern=r'^[a-f0-9]{64}$')
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"AssetId('{self.value}')"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, AssetId):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return False
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    @classmethod
    def from_string(cls, asset_id: str) -> 'AssetId':
        """Create AssetId from string with validation"""
        return cls(value=asset_id)
    
    def short_id(self, length: int = 8) -> str:
        """Get shortened version for display purposes"""
        return self.value[:length]

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
    asset_id: Optional[AssetId] = None
    message: str

class AssetSummary(BaseModel):
    asset_id: AssetId
    description: str

class AssetsListResponse(BaseModel):
    success: bool
    assets: List[AssetSummary]
    message: str

class Asset(BaseModel):
    asset_id: AssetId
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