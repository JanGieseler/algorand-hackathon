from algosdk.v2client.algod import AlgodClient

def get_localnet_client() -> AlgodClient:
    """Get Algorand LocalNet client"""
    return AlgodClient("a" * 64, "http://localhost:4001")