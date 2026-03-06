import os
import json
from web3 import Web3
from dotenv import load_dotenv
from eth_account import Account
from pathlib import Path

load_dotenv()

RPC_URL = os.getenv("RPC_URL", "http://127.0.0.1:8545")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

if not PRIVATE_KEY:
    raise RuntimeError("PRIVATE_KEY not set in env")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
acct = Account.from_key(PRIVATE_KEY)

# Load ABI compiled by Hardhat (we will place ABI file path here)
ABI_PATH = Path(__file__).parent.parent.parent / "blockchain" / "artifacts" / "contracts" / "CertificateRegistry.sol" / "CertificateRegistry.json"

if not ABI_PATH.exists():
    # fallback: require user to set CONTRACT_ABI_JSON path
    raise RuntimeError(f"ABI JSON not found at {ABI_PATH}. Deploy contract and produce artifact.")

with open(ABI_PATH, "r") as f:
    artifact = json.load(f)

abi = artifact["abi"]
contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)
contract = w3.eth.contract(address=contract_address, abi=abi)

def store_hash_onchain(cert_hash_hex: str) -> str:
    """
    cert_hash_hex: "0x..."
    returns tx hash
    """
    nonce = w3.eth.get_transaction_count(acct.address)
    tx = contract.functions.store(Web3.to_bytes(hexstr=cert_hash_hex)).build_transaction({
        "from": acct.address,
        "nonce": nonce,
        "gas": 200_000,
        "gasPrice": w3.eth.gas_price,
    })
    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return tx_hash.hex()

def get_record(cert_hash_hex: str):
    """
    return (issuer, timestamp) or (None, 0) if not present
    """
    try:
        r = contract.functions.get(Web3.to_bytes(hexstr=cert_hash_hex)).call()
        issuer, timestamp = r[0], r[1]
        if int(timestamp) == 0:
            return None
        return {"issuer": issuer, "timestamp": int(timestamp)}
    except Exception as e:
        raise
