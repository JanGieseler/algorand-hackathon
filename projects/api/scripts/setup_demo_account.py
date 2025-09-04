"""
LocalNet utility functions for development and testing.

This module provides helper functions for working with Algorand LocalNet,
including account creation, funding, and other development utilities.
"""

from pathlib import Path
from algosdk import account, transaction, mnemonic
from algosdk.v2client import algod
import os
from typing import Tuple

from dotenv import load_dotenv


def get_localnet_client() -> algod.AlgodClient:
    """Get Algorand LocalNet client"""
    return algod.AlgodClient("a" * 64, "http://localhost:4001")


def create_demo_account(output_dir: str = "data/keys") -> str:
    """
    Create or load a demo account for development/testing.
    ⚠️ In production, use proper key management!
    
    Args:
        output_dir: Path to store/load the private key
        
    Returns:
        Tuple of (address, private_key)
    """

    Path(output_dir).mkdir(exist_ok=True, parents=True)

    private_key, address = account.generate_account()

    key_file_path = Path(output_dir)/f"{address}.key"
    
    # Create new demo account
    
    with open(key_file_path, 'w') as f:
        f.write(private_key)
    
    print(f"🔑 Demo account created: {address}")
    print(f"💰 Use fund_account() to add ALGOs to this account")
    
    return address


def get_dispenser_account() -> Tuple[str, str]:
    """
    Get a funded dispenser account for LocalNet.
    Uses the first funded account found in the LocalNet.
    
    Returns:
        Tuple of (address, private_key)
    """
    import subprocess
    
    try:
        # Get list of accounts and find the first funded one
        result = subprocess.run([
            "docker", "exec", "algokit_sandbox_algod",
            "goal", "account", "list", "--datadir", "/algod/data"
        ], capture_output=True, text=True, check=True)
        
        # Parse the output to find a funded account
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if 'microAlgos' in line and not line.strip().endswith('0 microAlgos'):
                # Extract address (first column after [online/offline])
                parts = line.split('\t')
                if len(parts) >= 2:
                    dispenser_address = parts[1].strip()
                    
                    # Get the private key for this account
                    key_result = subprocess.run([
                        "docker", "exec", "algokit_sandbox_algod",
                        "goal", "account", "export", "-a", dispenser_address, "--datadir", "/algod/data"
                    ], capture_output=True, text=True, check=True)
                    
                    # Extract mnemonic from output
                    mnemonic_phrase = key_result.stdout.split('"')[1]
                    dispenser_private_key = mnemonic.to_private_key(mnemonic_phrase)
                    
                    return dispenser_address, dispenser_private_key
        
        raise Exception("No funded account found in LocalNet")
        
    except Exception as e:
        # Fallback: Use the known funded account from LocalNet
        dispenser_mnemonic = ("despair knock expire deer math cement chapter describe close viable wrap boost "
                             "holiday unfair soccer raw cup minor piece pilot staff prepare foam about strike")
        
        dispenser_private_key = mnemonic.to_private_key(dispenser_mnemonic)
        dispenser_address = account.address_from_private_key(dispenser_private_key)
        
        return dispenser_address, dispenser_private_key


def fund_account(target_address: str, amount_algos: float = 1.0) -> str:
    """
    Fund an account with ALGOs on LocalNet using the dispenser account.
    
    Args:
        target_address: Address of the account to fund
        amount_algos: Amount of ALGOs to send (default: 1.0)
        
    Returns:
        Transaction ID of the funding transaction
        
    Raises:
        Exception: If the funding fails
    """
    algod_client = get_localnet_client()
    dispenser_address, dispenser_private_key = get_dispenser_account()
    
    # Convert ALGOs to microALGOs (1 ALGO = 1,000,000 microALGOs)
    amount_microalgos = int(amount_algos * 1_000_000)
    
    # Create funding transaction
    params = algod_client.suggested_params()
    txn = transaction.PaymentTxn(
        sender=dispenser_address,
        sp=params,
        receiver=target_address,
        amt=amount_microalgos
    )
    
    # Sign and send
    signed_txn = txn.sign(dispenser_private_key)
    txid = algod_client.send_transaction(signed_txn)
    
    # Wait for confirmation
    transaction.wait_for_confirmation(algod_client, txid, 4)
    
    print(f"✅ Funded {target_address} with {amount_algos} ALGOs, txid: {txid}")
    return txid


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


def ensure_account_funded(address: str, min_balance_algos: float = 0.1) -> bool:
    """
    Ensure an account has at least the minimum balance, funding it if necessary.
    
    Args:
        address: Address of the account to check/fund
        min_balance_algos: Minimum balance in ALGOs (default: 0.1)
        
    Returns:
        True if account has sufficient balance (or was successfully funded)
    """
    try:
        current_balance_microalgos = get_account_balance(address)
        current_balance_algos = current_balance_microalgos / 1_000_000
        
        if current_balance_algos >= min_balance_algos:
            print(f"✅ Account {address} has sufficient balance: {current_balance_algos:.6f} ALGOs")
            return True
        
        # Fund the account
        funding_amount = max(1.0, min_balance_algos)  # Fund with at least 1 ALGO
        print(f"💰 Account {address} needs funding. Current: {current_balance_algos:.6f} ALGOs, funding with {funding_amount} ALGOs")
        fund_account(address, funding_amount)
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to ensure account funding: {e}")
        raise e
        return False


def setup_demo_account(output_dir: str = "data/keys") -> str:
    """
    Create or load a demo account and ensure it's funded.
    This is a convenience function that combines account creation and funding.
    
    Args:
        output_dir: Path to store/load the private key
        
    Returns:
        Tuple of (address, private_key)
    """
    address = create_demo_account(output_dir)
    ensure_account_funded(address)
    return address


if __name__ == "__main__":

    load_dotenv()

    # key_file_path = "../data/keys/{algo_account}.key"

    algo_account = os.getenv('ALGO_ACCOUNT', default='')

    if algo_account == '':
        algo_account = setup_demo_account()
        print(f'\nCreated new account {algo_account}.\nUpdate you env varibale with\nALGO_ACCOUNT={algo_account}\nto use it\n')

    ensure_account_funded(algo_account)