from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from .models import Asset, AssetUploadRequest, AssetSummary

class AssetStorage(ABC):
    """Abstract base class for asset storage implementations"""
    
    @abstractmethod
    def save(self, asset_request: AssetUploadRequest, asset_id: str) -> str:
        """
        Save an asset and return its ID
        
        Args:
            asset_request: The asset upload request data
            asset_id: The generated asset ID
            
        Returns:
            The asset ID
        """
        pass
    
    @abstractmethod
    def list(self) -> List[AssetSummary]:
        """
        List all assets with summary information
        
        Returns:
            List of asset summaries
        """
        pass
    
    @abstractmethod
    def retrieve(self, asset_id: str) -> Optional[Asset]:
        """
        Retrieve a specific asset by its ID
        
        Args:
            asset_id: The ID of the asset to retrieve
            
        Returns:
            The asset if found, None otherwise
        """
        pass

class InMemoryAssetStorage(AssetStorage):
    """In-memory implementation of asset storage"""
    
    def __init__(self):
        self._storage: Dict[str, Asset] = {}
    
    def save(self, asset_request: AssetUploadRequest, asset_id: str) -> str:
        """Save an asset in memory"""
        asset = Asset(
            asset_id=asset_id,
            description=asset_request.description,
            content=asset_request.content,
            location=asset_request.location,
            timestamp=asset_request.timestamp,
            creator=asset_request.creator,
            publisher=asset_request.publisher
        )
        
        self._storage[asset_id] = asset
        return asset_id
    
    def list(self) -> List[AssetSummary]:
        """List all assets with summary information"""
        return [
            AssetSummary(asset_id=asset.asset_id, description=asset.description)
            for asset in self._storage.values()
        ]
    
    def retrieve(self, asset_id: str) -> Optional[Asset]:
        """Retrieve a specific asset by its ID"""
        return self._storage.get(asset_id)

# Global storage instance (in production, this would be configured via dependency injection)
storage: AssetStorage = InMemoryAssetStorage()