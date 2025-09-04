import hashlib
import json
from typing import List, Optional, Tuple
from .models import AssetUploadRequest, Asset, AssetSummary, AssetId
from .storage import storage

def generate_asset_id(asset: AssetUploadRequest) -> AssetId:
    """The Asset ID hashes the content and meta data of the asset and thereby gives it a unique representation"""
    data_to_hash = {
        "content": asset.content,
        "location": {"latitude": asset.location.latitude, "longitude": asset.location.longitude},
        "timestamp": asset.timestamp.isoformat(),
        "creator": asset.creator,
        "publisher": asset.publisher
    }
    
    hash_string = json.dumps(data_to_hash, sort_keys=True)
    hash_value = hashlib.sha256(hash_string.encode()).hexdigest()
    return AssetId.from_string(hash_value)

def save_asset(asset_request: AssetUploadRequest) -> Tuple[AssetId, str]:
    """Save an asset and return its generated ID"""
    asset_id = generate_asset_id(asset_request)
    transaction_id = storage.save_and_link(asset_request, asset_id)
    return asset_id, transaction_id

def get_asset_by_id(asset_id: AssetId) -> Optional[Asset]:
    """Retrieve an asset by its ID"""
    return storage.retrieve(asset_id)

def get_all_assets() -> List[AssetSummary]:
    """Get a list of all assets with summary information"""
    return storage.list()