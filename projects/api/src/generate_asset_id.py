import hashlib
import json
from typing import List, Optional, Tuple
from .models import AssetUploadRequest, Asset, AssetSummary, AssetId, AssetVerifyRequest


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