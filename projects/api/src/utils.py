import hashlib
import json
from typing import List, Optional
from .models import AssetUploadRequest, Asset, AssetSummary
from .storage import storage

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

def save_asset(asset_request: AssetUploadRequest) -> str:
    """Save an asset and return its generated ID"""
    asset_id = generate_asset_id(asset_request)
    return storage.save(asset_request, asset_id)

def get_asset_by_id(asset_id: str) -> Optional[Asset]:
    """Retrieve an asset by its ID"""
    return storage.retrieve(asset_id)

def get_all_assets() -> List[AssetSummary]:
    """Get a list of all assets with summary information"""
    return storage.list()