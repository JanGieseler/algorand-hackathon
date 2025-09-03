import hashlib
import json
from .models import AssetUploadRequest

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