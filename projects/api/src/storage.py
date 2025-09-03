from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from .models import Asset, AssetUploadRequest, AssetSummary, AssetId

class AssetStorage(ABC):
    """Abstract base class for asset storage implementations"""
    
    @abstractmethod
    def save(self, asset_request: AssetUploadRequest, asset_id: AssetId) -> AssetId:
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
    def retrieve(self, asset_id: AssetId) -> Optional[Asset]:
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
        self._storage: Dict[AssetId, Asset] = {}
    
    def save(self, asset_request: AssetUploadRequest, asset_id: AssetId) -> AssetId:
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
    
    def retrieve(self, asset_id: AssetId) -> Optional[Asset]:
        """Retrieve a specific asset by its ID"""
        return self._storage.get(asset_id)

class FileSystemAssetStorage(AssetStorage):
    """File system implementation of asset storage"""
    
    def __init__(self, storage_dir: str = "data/assets"):
        import os
        self.storage_dir = storage_dir
        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
    
    def _get_asset_path(self, asset_id: AssetId) -> str:
        """Get the file path for an asset"""
        return f"{self.storage_dir}/{asset_id.value}.json"
    
    def save(self, asset_request: AssetUploadRequest, asset_id: AssetId) -> AssetId:
        """Save an asset to disk"""
        import json
        
        asset = Asset(
            asset_id=asset_id,
            description=asset_request.description,
            content=asset_request.content,
            location=asset_request.location,
            timestamp=asset_request.timestamp,
            creator=asset_request.creator,
            publisher=asset_request.publisher
        )
        
        # Convert to dictionary for JSON serialization
        asset_data = {
            "asset_id": asset.asset_id.value,
            "description": asset.description,
            "content": asset.content,
            "location": {
                "latitude": asset.location.latitude,
                "longitude": asset.location.longitude
            },
            "timestamp": asset.timestamp.isoformat(),
            "creator": asset.creator,
            "publisher": asset.publisher
        }
        
        # Write to file
        asset_path = self._get_asset_path(asset_id)
        with open(asset_path, 'w') as f:
            json.dump(asset_data, f, indent=2)
        
        return asset_id
    
    def list(self) -> List[AssetSummary]:
        """List all assets from disk"""
        import os
        import json
        
        assets = []
        
        # Check if storage directory exists
        if not os.path.exists(self.storage_dir):
            return assets
        
        # Read all JSON files in the storage directory
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                asset_path = os.path.join(self.storage_dir, filename)
                try:
                    with open(asset_path, 'r') as f:
                        asset_data = json.load(f)
                        assets.append(AssetSummary(
                            asset_id=AssetId.from_string(asset_data['asset_id']),
                            description=asset_data['description']
                        ))
                except (json.JSONDecodeError, KeyError, IOError):
                    # Skip corrupted files
                    continue
        
        return assets
    
    def retrieve(self, asset_id: AssetId) -> Optional[Asset]:
        """Retrieve a specific asset from disk"""
        import json
        from datetime import datetime
        from .models import GPSCoordinates
        
        asset_path = self._get_asset_path(asset_id)
        
        try:
            with open(asset_path, 'r') as f:
                asset_data = json.load(f)
                
                return Asset(
                    asset_id=AssetId.from_string(asset_data['asset_id']),
                    description=asset_data['description'],
                    content=asset_data['content'],
                    location=GPSCoordinates(
                        latitude=asset_data['location']['latitude'],
                        longitude=asset_data['location']['longitude']
                    ),
                    timestamp=datetime.fromisoformat(asset_data['timestamp']),
                    creator=asset_data['creator'],
                    publisher=asset_data['publisher']
                )
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return None

# Global storage instance (in production, this would be configured via dependency injection)
# storage: AssetStorage = InMemoryAssetStorage()
storage: AssetStorage = FileSystemAssetStorage()