#!/usr/bin/env python3
"""
Script to create a new asset on Algorand LocalNet blockchain.
Uses the account from .env file and loads the private key from data/keys.
Returns the transaction ID of the asset creation transaction.
"""

import hashlib
import os
from algosdk import transaction, account
from algosdk.v2client import algod
from dotenv import load_dotenv
# from projects.api.scripts.setup_demo_account import get_localnet_client, ensure_account_funded


def load_account_from_env() -> tuple[str, str]:
    """
    Load account address from .env and corresponding private key from data/keys.
    
    Returns:
        Tuple of (address, private_key)
    """
    load_dotenv()
    
    # Get account address from environment
    account_address = os.getenv('ALGO_ACCOUNT')
    if not account_address:
        raise ValueError("ALGO_ACCOUNT not found in .env file")
    
    # Load private key from file
    key_file_path = f"data/keys/{account_address}.key"
    if not os.path.exists(key_file_path):
        raise FileNotFoundError(f"Private key file not found: {key_file_path}")
    
    with open(key_file_path, 'r') as f:
        private_key = f.read().strip()
    
    # Verify the private key matches the address
    derived_address = account.address_from_private_key(private_key)
    if derived_address != account_address:
        raise ValueError("Private key does not match the account address from .env")
    
    print(f"✅ Loaded account: {account_address}")
    return account_address, private_key


def create_asset(
    algod_client:algod.AlgodClient, 
    creator_address: str,
    creator_private_key: str,
    asset_name: str = "My Asset",
    unit_name: str = "MYASSET",
    total: int = 1,
    decimals: int = 0,
    url: str = "",
    metadata_hash: bytes = None,
    freeze_addr: str = None,
    clawback_addr: str = None,
    manager_addr: str = None,
    reserve_addr: str = None
) -> transaction.GenericSignedTransaction:
    """
    Create a new asset on the Algorand blockchain.
    
    Args:
        creator_address: Address of the asset creator
        creator_private_key: Private key of the asset creator
        asset_name: Full name of the asset (max 32 bytes)
        unit_name: Short name/ticker of the asset (max 8 bytes)
        total: Total supply of the asset
        decimals: Number of decimal places for the asset
        url: Optional URL for asset metadata
        metadata_hash: Optional 32-byte hash of asset metadata
        freeze_addr: Address that can freeze/unfreeze holdings of this asset
        clawback_addr: Address that can clawback holdings of this asset
        manager_addr: Address that can manage asset configuration
        reserve_addr: Address that holds non-minted assets
        
    Returns:
        Transaction ID
    """
    
    # Get network parameters
    params = algod_client.suggested_params()
    
    # Create asset creation transaction
    txn = transaction.AssetConfigTxn(
        sender=creator_address,
        sp=params,
        total=total,
        decimals=decimals,
        default_frozen=False,
        unit_name=unit_name,
        asset_name=asset_name,
        manager=manager_addr or creator_address,
        reserve=reserve_addr or creator_address,
        freeze=freeze_addr,
        clawback=clawback_addr,
        url=url,
        metadata_hash=metadata_hash,
        strict_empty_address_check=False
    )
    
    # Sign transaction
    signed_txn = txn.sign(creator_private_key)
    
    # Send transaction
    txid = algod_client.send_transaction(signed_txn)
    print(f"📤 Asset creation transaction sent: {txid}")
    
    # Wait for confirmation
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)

    print(f"📤 Asset creation transaction confimed: {confirmed_txn}")
    
    # Extract asset ID from the confirmed transaction
    asset_id = confirmed_txn["asset-index"]
    
    print(f"✅ Asset created successfully!")
    print(f"   Asset ID: {asset_id}")
    print(f"   Transaction ID: {txid}")
    print(f"   Asset Name: {asset_name}")
    print(f"   Unit Name: {unit_name}")
    print(f"   Total Supply: {total}")
    print(f"   Decimals: {decimals}")
    
    return txid


# def main():
#     """Main function to create a sample asset"""
#     print("🚀 Creating New Asset on Algorand LocalNet")
#     print("=" * 50)
    
#     try:
#         # Load account from .env and key file
#         creator_address, creator_private_key = load_account_from_env()
        
#         # Ensure the account has enough ALGOs for transaction fees
#         ensure_account_funded(creator_address, min_balance_algos=1.0)
        
#         print(f"💼 Using creator account: {creator_address}")
        

#         message = "hellosdsafdaf"

#         hash_value = hashlib.sha256(message.encode()).digest()

#         # Get LocalNet client
#         algod_client = get_localnet_client()
#         # Create the asset
#         result = create_asset(
#             algod_client=algod_client,
#             creator_address=creator_address,
#             creator_private_key=creator_private_key,
#             asset_name="Hackathon Test",
#             unit_name="HACK",
#             total=1,  # 1 million tokens
#             decimals=0,     # 6 decimal places (like ALGO)
#             url="https://somethisnd.asdas.de",
#             # You can add these optional parameters:
#             freeze_addr=creator_address,  # Allow freezing
#             clawback_addr=creator_address,  # Allow clawback
#             manager_addr=creator_address,  # Allow management changes
#             metadata_hash=hash_value
#         )
        
#         print("\n🎉 Asset Creation Complete!")
#         print(f"Asset ID: {result['asset_id']}")
#         print(f"Transaction: {result['transaction_id']}")
        
#         return result
        
#     except Exception as e:
#         print(f"❌ Error creating asset: {e}")
#         print("\n💡 Troubleshooting:")
#         print("   1. Make sure LocalNet is running on localhost:4001")
#         print("   2. Ensure ALGO_ACCOUNT is set in .env file")
#         print("   3. Check that the private key file exists in data/keys/")
#         print("   4. Verify the account has sufficient ALGOs")
#         raise


# if __name__ == "__main__":
#     main()