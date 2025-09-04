from typing import List, Optional, Tuple

from .generate_asset_id import generate_asset_id
from .models import AssetUploadRequest, Asset, AssetSummary, AssetId, AssetVerifyRequest
from .storage import storage



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

def verify_asset(asset_request: AssetVerifyRequest) -> bool:
    """Verify an asset"""

    storage.retrieve(asset_id)
    asset_id = generate_asset_id(asset_request)
    transaction_id = storage.save_and_link(asset_request, asset_id)
    return asset_id, transaction_id