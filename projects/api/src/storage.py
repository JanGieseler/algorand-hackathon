from abc import ABC, abstractmethod
from algosdk.v2client import algod
from typing import Dict, List, Optional
import hashlib

from .asset_create import create_asset
from .models import Asset, AssetUploadRequest, AssetSummary, AssetId
            
from algosdk import transaction
import json
import os
from dotenv import load_dotenv

class AssetStorage(ABC):
    """Abstract base class for asset storage implementations"""
    
    @abstractmethod
    def save(self, asset_request: AssetUploadRequest, transaction_id: str) -> Optional[str]:
        """
        Save an asset and return its ID
        
        Args:
            asset_request: The asset upload request data
            transaction_id: The generated transaction ID
            
        Returns:
            The transactoin Id if there is any
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
    def retrieve(self, transaction_id: str) -> Optional[Asset]:
        """
        Retrieve a specific asset by its ID
        
        Args:
            asset_id: The ID of the asset to retrieve
            
        Returns:
            The asset if found, None otherwise
        """
        pass

    @abstractmethod
    def link_transaction(self, asset_id: AssetId, transaction_id: str):
        """
        Link an asset to a transaction
        
        Args:
            asset_id: The asset id
            transaction_id: The generated transaction ID
            
        """
        pass


class InMemoryAssetStorage(AssetStorage):
    """In-memory implementation of asset storage"""
    
    def __init__(self):
        self._storage: Dict[AssetId, Asset] = {}
        self._links: Dict[AssetId, str] = {}
    
    def save(self, asset_request: AssetUploadRequest, asset_id: AssetId) -> Optional[str]:
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
        
    
    def list(self) -> List[AssetSummary]:
        """List all assets with summary information"""
        return [
            AssetSummary(asset_id=asset.asset_id, description=asset.description)
            for asset in self._storage.values()
        ]
    
    def retrieve(self, asset_id: AssetId) -> Optional[Asset]:
        """Retrieve a specific asset by its ID"""
        return self._storage.get(asset_id)

    def link_transaction(self, asset_id: AssetId, transaction_id: str):
        """
        Link an asset to a transaction
        
        Args:
            asset_id: The asset id
            transaction_id: The generated transaction ID
            
        """
        self._links[asset_id] = transaction_id

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


class AlgorandStorage:
    """
    Pure Algorand blockchain storage implementation.
    
    This class handles blockchain operations:
    - Recording asset IDs on Algorand blockchain
    - Using transaction note field to store metadata
    - Account management for blockchain transactions
    - Implements AssetStorage interface for blockchain-only storage
    """
    
    def __init__(self, network: str = "localnet"):
        self.network = network
        
        # Load environment variables
        load_dotenv()
        self.algo_account = os.getenv('ALGO_ACCOUNT')
        if not self.algo_account:
            print("⚠️ ALGO_ACCOUNT not found in environment variables")

        self.sender_address = self.algo_account
        
        
        with open(f"data/keys/{self.algo_account}.key", 'r') as f:
            private_key = f.read().strip()
        self.sender_private_key = private_key

        self.algod_client = self._setup_algorand_client()
    
    def _setup_algorand_client(self) -> Optional[algod.AlgodClient]:
        """Set up Algorand client connection"""
        
        if self.network == "testnet":
            # TestNet configuration
            self.algod_address = "https://testnet-api.algonode.cloud"
            self.algod_token = ""  # AlgoNode doesn't require a token
        elif self.network == "mainnet":
            # MainNet configuration  
            self.algod_address = "https://mainnet-api.algonode.cloud"
            self.algod_token = ""
        else:
            # Local development (AlgoKit LocalNet)
            self.algod_address = "http://localhost:4001"
            self.algod_token = "a" * 64  # Default LocalNet token
        
        try:
            algod_client = algod.AlgodClient(self.algod_token, self.algod_address)
            # Test connection
            algod_client.status()
            print(f"✅ Connected to Algorand {self.network}")
        except Exception as e:
            print(f"⚠️ Algorand connection failed: {e}")
            print("📝 Blockchain storage will not be available")
            algod_client = None
        return algod_client
    
    
    def record_asset(self, asset_id: AssetId, asset_request: AssetUploadRequest) -> Optional[str]:
        """Record asset ID on Algorand blockchain"""
        if not self.algod_client:
            print("⚠️ Blockchain not available, skipping blockchain record")
            return None
        

        # Create metadata to store in note field (max 1KB)
        note_data = {
            "type": "asset_registry",
            "asset_id": asset_id.value,
            "description": asset_request.description[:100],  # Truncate if too long
            "creator": asset_request.creator,
            "publisher": asset_request.publisher,
            "timestamp": asset_request.timestamp.isoformat()
        }
        
        metadata_json = json.dumps(note_data, separators=(',', ':'))
        metadata_hash = hashlib.sha256(metadata_json.encode('utf-8')).digest()
        
        # Ensure note is under 1KB limit
        # if len(note_bytes) > 1024:
        #     # Truncate description further if needed
        #     note_data["description"] = asset_request.description[:50] + "..."
        #     note_bytes = json.dumps(note_data, separators=(',', ':')).encode('utf-8')
        
        # Create an asset with proper length limits
        # asset_name: max 32 bytes, unit_name: max 8 bytes
        asset_name = asset_request.description[:32] if asset_request.description else "Asset"
        unit_name = asset_request.description[:8] if asset_request.description else "ASSET"
        
        txn = create_asset(
            algod_client=self.algod_client,
            creator_address=self.sender_address,
            creator_private_key=self.sender_private_key,
            asset_name=asset_name,
            unit_name=unit_name,
            metadata_hash=metadata_hash
        )
        print(f"✅ Asset {asset_id.short_id()}... recorded on blockchain: {txn}")
        return txn
    
    def save(self, asset_request: AssetUploadRequest, asset_id: AssetId) -> AssetId:
        """Save an asset by recording it on the blockchain"""
        self.record_asset(asset_id, asset_request)
        return asset_id
    
    def list(self) -> List[AssetSummary]:
        """List all assets - not supported for pure blockchain storage"""
        # Pure blockchain storage doesn't support efficient listing
        # In a real implementation, you'd need to scan all transactions
        print("⚠️ Asset listing not supported for pure blockchain storage")
        return []
    
    def retrieve(self, asset_id: AssetId) -> Optional[Asset]:
        """Retrieve a specific asset - not supported for pure blockchain storage"""
        # Pure blockchain storage doesn't support efficient retrieval
        # In a real implementation, you'd need to scan transactions for the asset_id
        print("⚠️ Asset retrieval not supported for pure blockchain storage")
        return None


class HybridAssetStorage:
    """
    Hybrid asset storage that combines local storage with blockchain registry.
    
    This implementation:
    1. Stores asset data locally for performance
    2. Records asset IDs on Algorand blockchain for immutability
    3. Provides graceful fallback when blockchain is unavailable
    """
    
    def __init__(self, network: str = "localnet", local_storage: AssetStorage = InMemoryAssetStorage()):
        self.local_storage = local_storage
        self.blockchain_storage = AlgorandStorage(network)
    
    def save_and_link(self, asset_request: AssetUploadRequest, asset_id: AssetId) -> str:
        """Save asset locally and record on blockchain"""
        # Save to local storage first
        self.local_storage.save(asset_request, asset_id)
        
        # Record on blockchain (doesn't block if it fails)
        blockchain_txid = self.blockchain_storage.record_asset(asset_id, asset_request)

        # Link the transaction to the asset in the local storage
        self.local_storage.link_transaction(asset_id=asset_id, transaction_id=blockchain_txid)
        
        if blockchain_txid:
            print(f"🔗 Asset {asset_id.short_id()}... linked to blockchain tx: {blockchain_txid}")
        
        return blockchain_txid
    
    def list(self) -> List[AssetSummary]:
        """List assets from local storage"""
        return self.local_storage.list()
    
    def retrieve(self, asset_id: AssetId) -> Optional[Asset]:
        """Retrieve asset from local storage"""
        return self.local_storage.retrieve(asset_id)

# Global storage instance (in production, this would be configured via dependency injection)
# storage: AssetStorage = InMemoryAssetStorage()
# storage: AssetStorage = FileSystemAssetStorage()
# storage: AssetStorage = AlgorandStorage()  # Pure blockchain storage
storage: HybridAssetStorage = HybridAssetStorage()  # InMemory + Blockchain