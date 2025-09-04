
from .dev_tools import get_localnet_client
from .models import BalanceResponse
from .storage import storage
import os
from dotenv import load_dotenv


def get_account_balance(address: str) -> int:
    """
    Get the balance of an account in microALGOs.
    
    Args:
        address: Address of the account
        
    Returns:
        Balance in microALGOs
    """
    algod_client = get_localnet_client()
    account_info = algod_client.account_info(address)
    return account_info["amount"]