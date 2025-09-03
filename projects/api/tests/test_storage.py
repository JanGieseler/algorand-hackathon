import pytest
from datetime import datetime
from src.storage import InMemoryAssetStorage
from src.models import AssetUploadRequest, GPSCoordinates

class TestInMemoryAssetStorage:
    
    def setup_method(self):
        """Set up a fresh storage instance for each test"""
        self.storage = InMemoryAssetStorage()
    
    def test_empty_storage_initially(self):
        """Test that storage starts empty"""
        assets = self.storage.list()
        assert len(assets) == 0
    
    def test_add_two_assets_returns_list_length_two(self):
        """Test that adding two assets results in a list of length 2"""
        # Create first asset
        asset1 = AssetUploadRequest(
            description="First test asset",
            content="Content of first asset",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="creator1",
            publisher="publisher1"
        )
        
        # Create second asset
        asset2 = AssetUploadRequest(
            description="Second test asset", 
            content="Content of second asset",
            location=GPSCoordinates(latitude=37.7749, longitude=-122.4194),
            timestamp=datetime.fromisoformat("2024-01-02T15:30:00"),
            creator="creator2",
            publisher="publisher2"
        )
        
        # Start with empty storage
        initial_assets = self.storage.list()
        assert len(initial_assets) == 0
        
        # Add first asset
        asset_id_1 = self.storage.save(asset1, "test_id_1")
        assert asset_id_1 == "test_id_1"
        
        # Check we have one asset
        assets_after_first = self.storage.list()
        assert len(assets_after_first) == 1
        assert assets_after_first[0].asset_id == "test_id_1"
        assert assets_after_first[0].description == "First test asset"
        
        # Add second asset
        asset_id_2 = self.storage.save(asset2, "test_id_2")
        assert asset_id_2 == "test_id_2"
        
        # Check we have two assets
        all_assets = self.storage.list()
        assert len(all_assets) == 2
        
        # Verify both assets are in the list
        asset_ids = [asset.asset_id for asset in all_assets]
        assert "test_id_1" in asset_ids
        assert "test_id_2" in asset_ids
        
        descriptions = [asset.description for asset in all_assets]
        assert "First test asset" in descriptions
        assert "Second test asset" in descriptions
    
    def test_retrieve_saved_assets(self):
        """Test that saved assets can be retrieved by ID"""
        asset = AssetUploadRequest(
            description="Retrievable asset",
            content="Content for retrieval test",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="test_creator",
            publisher="test_publisher"
        )
        
        # Save asset
        asset_id = self.storage.save(asset, "retrieve_test_id")
        
        # Retrieve asset
        retrieved_asset = self.storage.retrieve("retrieve_test_id")
        
        # Verify retrieved asset matches original
        assert retrieved_asset is not None
        assert retrieved_asset.asset_id == "retrieve_test_id"
        assert retrieved_asset.description == "Retrievable asset"
        assert retrieved_asset.content == "Content for retrieval test"
        assert retrieved_asset.creator == "test_creator"
        assert retrieved_asset.publisher == "test_publisher"
        assert retrieved_asset.location.latitude == 40.7128
        assert retrieved_asset.location.longitude == -74.0060
    
    def test_retrieve_nonexistent_asset_returns_none(self):
        """Test that retrieving a non-existent asset returns None"""
        result = self.storage.retrieve("nonexistent_id")
        assert result is None