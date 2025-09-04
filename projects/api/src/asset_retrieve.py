#!/usr/bin/env python3
"""
Script to retrieve asset information from a transaction ID.
Takes a transaction ID as input and returns the asset information.
"""

import sys
from algosdk.v2client import algod

from .dev_tools import get_localnet_client
from .models import AssetId



def get_hash_from_transaction(algod_client:algod.AlgodClient, transaction_id: str) -> str:
    """
    Retrieve asset information from a transaction ID.
    
    Args:
        transaction_id: The transaction ID of the asset creation transaction
        
    Returns:
        Dictionary containing asset information
    """
    
    try:
        # Get transaction information
        txn_info = algod_client.pending_transaction_info(transaction_id)
        
        # If transaction is not pending, try to get it from confirmed transactions
        if not txn_info:
            # For confirmed transactions, we need to search through recent blocks
            # This is a simplified approach - in production you'd use an indexer
            print("Transaction not found in pending pool, searching confirmed transactions...")
            
            # Get current round
            status = algod_client.status()
            current_round = status['last-round']
            
            # Search recent blocks (last 100 rounds)
            for round_num in range(max(1, current_round - 100), current_round + 1):
                try:
                    block = algod_client.block_info(round_num)
                    if 'txns' in block:
                        for txn in block['txns']:
                            if txn.get('txn', {}).get('txn') == transaction_id:
                                txn_info = txn
                                break
                    if txn_info:
                        break
                except:
                    continue
        
        if not txn_info:
            raise ValueError(f"Transaction {transaction_id} not found")
        
        # Extract asset ID from transaction
        asset_id = None
        if 'asset-index' in txn_info:
            asset_id = txn_info['asset-index']
        elif 'txn' in txn_info and 'caid' in txn_info['txn']:
            asset_id = txn_info['txn']['caid']
        
        if not asset_id:
            raise ValueError("No asset ID found in transaction")
        
        # Get asset information
        asset_info = algod_client.asset_info(asset_id)

        
        print(f"✅ Asset retrieved successfully!")
        print(f"   Asset ID: {asset_id}")
        print(f"   Transaction ID: {transaction_id}")
        print(f"   Asset Name: {asset_info['params'].get('name', 'N/A')}")
        print(f"   Unit Name: {asset_info['params'].get('unit-name', 'N/A')}")
        print(f"   Total Supply: {asset_info['params'].get('total', 0)}")
        print(f"   Decimals: {asset_info['params'].get('decimals', 0)}")
        print(f"   Creator: {asset_info['params'].get('creator', 'N/A')}")
        print(f"   Manager: {asset_info['params'].get('manager', 'N/A')}")
        print(f"   Reserve: {asset_info['params'].get('reserve', 'N/A')}")
        print(f"   Freeze: {asset_info['params'].get('freeze', 'N/A')}")
        print(f"   Clawback: {asset_info['params'].get('clawback', 'N/A')}")
        print(f"   URL: {asset_info['params'].get('url', 'N/A')}")
        print(f"   metadata-hash: {asset_info['params'].get('metadata-hash', 'N/A')}")

        
        
        return asset_info['params'].get('metadata-hash')
        
    except Exception as e:
        print(f"❌ Error retrieving asset: {e}")
        raise


def main():
    """Main function to retrieve asset from transaction ID"""
    print("🔍 Retrieving Asset from Transaction ID")
    print("=" * 50)

    client = get_localnet_client()
    
    # Get transaction ID from command line argument or prompt
    if len(sys.argv) > 1:
        transaction_id = sys.argv[1]
    else:
        transaction_id = input("Enter transaction ID: ").strip()
    
    if not transaction_id:
        print("❌ Transaction ID is required")
        sys.exit(1)
    
    try:
        result = get_hash_from_transaction(client, transaction_id)
        
        print("\n🎉 Asset Retrieval Complete!")
        print(result)
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure LocalNet is running on localhost:4001")
        print("   2. Verify the transaction ID is correct")
        print("   3. Ensure the transaction was an asset creation transaction")
        sys.exit(1)


if __name__ == "__main__":
    main()