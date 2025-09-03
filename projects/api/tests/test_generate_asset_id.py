import pytest
from datetime import datetime
from src.utils import generate_asset_id
from src.models import AssetUploadRequest, GPSCoordinates

class TestGenerateAssetId:
    
    def test_generate_asset_id_consistency(self):
        """Test that the same input always generates the same asset ID"""
        asset = AssetUploadRequest(
            description="Test asset",
            content="This is test content",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="creator123",
            publisher="publisher456"
        )
        
        asset_id_1 = generate_asset_id(asset)
        asset_id_2 = generate_asset_id(asset)
        
        assert asset_id_1 == asset_id_2
    
    def test_generate_asset_id_format(self):
        """Test that the generated asset ID is a valid SHA-256 hex string"""
        asset = AssetUploadRequest(
            description="Test asset",
            content="This is test content",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="creator123",
            publisher="publisher456"
        )
        
        asset_id = generate_asset_id(asset)
        
        # SHA-256 hex string should be 64 characters long
        assert len(asset_id) == 64
        # Should only contain hexadecimal characters
        assert all(c in "0123456789abcdef" for c in asset_id)
    
    def test_generate_asset_id_different_content(self):
        """Test that different content generates different asset IDs"""
        base_asset = AssetUploadRequest(
            description="Test asset",
            content="This is test content",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="creator123",
            publisher="publisher456"
        )
        
        modified_asset = AssetUploadRequest(
            description="Test asset",
            content="This is different test content",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="creator123",
            publisher="publisher456"
        )
        
        asset_id_1 = generate_asset_id(base_asset)
        asset_id_2 = generate_asset_id(modified_asset)
        
        assert asset_id_1 != asset_id_2
    
    def test_generate_asset_id_different_location(self):
        """Test that different location generates different asset IDs"""
        base_asset = AssetUploadRequest(
            description="Test asset",
            content="This is test content",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="creator123",
            publisher="publisher456"
        )
        
        modified_asset = AssetUploadRequest(
            description="Test asset",
            content="This is test content",
            location=GPSCoordinates(latitude=37.7749, longitude=-122.4194),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="creator123",
            publisher="publisher456"
        )
        
        asset_id_1 = generate_asset_id(base_asset)
        asset_id_2 = generate_asset_id(modified_asset)
        
        assert asset_id_1 != asset_id_2
    
    def test_generate_asset_id_different_timestamp(self):
        """Test that different timestamp generates different asset IDs"""
        base_asset = AssetUploadRequest(
            description="Test asset",
            content="This is test content",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="creator123",
            publisher="publisher456"
        )
        
        modified_asset = AssetUploadRequest(
            description="Test asset",
            content="This is test content",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-02T12:00:00"),
            creator="creator123",
            publisher="publisher456"
        )
        
        asset_id_1 = generate_asset_id(base_asset)
        asset_id_2 = generate_asset_id(modified_asset)
        
        assert asset_id_1 != asset_id_2
    
    def test_generate_asset_id_different_creator(self):
        """Test that different creator generates different asset IDs"""
        base_asset = AssetUploadRequest(
            description="Test asset",
            content="This is test content",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="creator123",
            publisher="publisher456"
        )
        
        modified_asset = AssetUploadRequest(
            description="Test asset",
            content="This is test content",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="different_creator",
            publisher="publisher456"
        )
        
        asset_id_1 = generate_asset_id(base_asset)
        asset_id_2 = generate_asset_id(modified_asset)
        
        assert asset_id_1 != asset_id_2
    
    def test_generate_asset_id_different_publisher(self):
        """Test that different publisher generates different asset IDs"""
        base_asset = AssetUploadRequest(
            description="Test asset",
            content="This is test content",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="creator123",
            publisher="publisher456"
        )
        
        modified_asset = AssetUploadRequest(
            description="Test asset",
            content="This is test content",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="creator123",
            publisher="different_publisher"
        )
        
        asset_id_1 = generate_asset_id(base_asset)
        asset_id_2 = generate_asset_id(modified_asset)
        
        assert asset_id_1 != asset_id_2
    
    def test_generate_asset_id_expected_value(self):
        """Test that the function generates the expected asset ID for known input"""
        asset = AssetUploadRequest(
            description="Test asset",
            content="This is test content",
            location=GPSCoordinates(latitude=40.7128, longitude=-74.0060),
            timestamp=datetime.fromisoformat("2024-01-01T12:00:00"),
            creator="creator123",
            publisher="publisher456"
        )
        
        asset_id = generate_asset_id(asset)
        
        # This is the expected hash for the specific input above
        expected_id = "e872179dc951d84997944d378116e9d0906dcb127aa6a00c1d122dd180a003ad"
        assert asset_id == expected_id