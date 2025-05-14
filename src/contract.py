"""Contract utilities."""

import json

from web3 import Web3
from web3.middleware import geth_poa_middleware
from tqdm import tqdm


def connect_to_web3(network="saigon", api_key=None):
    """Connect to web3 and return the web3 object and connection status.

    Parameters
    ----------
    network : str, optional
        The network to connect to, by default "goerli-eth".
    api_key : str
        The API key for the Alchemy API.

    Returns
    -------
    w3 : Web3
        The web3 object.
    status : bool
        The connection status.
    """

    if api_key is None or api_key == "":
        raise ValueError("API key is required for Alchemy")

    if network in ["main-ron", "main-ronin", "ronin"]:
        url = "https://site1.moralis-nodes.com/ronin/" + api_key
    elif network in ["saigon-ron", "saigon-ronin", "saigon"]:
        url = "https://site1.moralis-nodes.com/ronin-testnet/" + api_key
    else:
        raise ValueError("Invalid network")

    # Create web3 object
    w3 = Web3(Web3.HTTPProvider(url))

    # Inyect middleware for PoA chains
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Get status
    status = w3.is_connected()

    return w3, status


def load_contract(w3, contract_address, abi_path):
    """Load the contract ABI from a JSON contract file.

    Parameters
    ----------
    w3 : Web3
        The web3 object.
    contract_address : str
        The contract address.
    abi_path : str
        The path to the ABI file.

    Returns
    -------
    contract : w3.eth.Contract
        The contract to be used.
    """

    # Import the contract abi from a file
    with open(abi_path, "rt", encoding="utf-8") as f:
        contract = json.load(f)
    abi = contract["abi"]

    # Connect to the contract in Arbitrum
    contract = w3.eth.contract(address=contract_address, abi=abi)

    return contract


def execute_batch_transfer_call(w3, contract, owner_address, private_key,
                                addresses, amounts):
    """Calls the function in contract.

    Parameters
    ----------
    w3 : Web3
        The web3 object.
    contract : w3.eth.Contract
        The contract to be used.
    owner_address : str
        The address of contract owner.
    private_key : str
        The private key of wallet.
    addresses : list
        The list of addresses.
    amounts : list
        The list of amounts per address.

    Returns
    -------
    txn_receipt : str
        The string with the transaction hex.
    """

    # Build nonce and estimate gas
    nonce = w3.eth.get_transaction_count(owner_address)
    gas_estimate = contract.functions.batchTransfer(
        addresses, amounts).estimate_gas({"from": owner_address})
    gas_limit = int(gas_estimate * 1.1)  # Add 10% buffer

    # Build transaction
    txn = contract.functions.batchTransfer(addresses,
                                           amounts).build_transaction({
                                               "nonce":
                                               nonce,
                                               "gas":
                                               gas_limit
                                           })

    # Sign the transaction
    txn_signed = w3.eth.account.sign_transaction(txn, private_key)

    # Send the transaction and wait for the transaction receipt
    txn_hash = w3.eth.send_raw_transaction(txn_signed.rawTransaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    txn_receipt = txn_receipt.transactionHash.hex()

    return txn_receipt


def batch_transfer(config, holders, amounts, block_size=100):
    """Function to batch transfer to holders.

    Parameters
    ----------
    config : dict
        The config dictionary.
    event_id : str
        The id of the event.
    addresses : list
        The list of addresses.
    amounts : list
        The list of amounts per address.
    """

    # Connect to web3
    w3, status = connect_to_web3(config["network"]["network"],
                                 config["network"]["api_key"])

    if status:
        # Load contract abi
        contract_addr = w3.to_checksum_address(config["contract"]["address"])
        contract = load_contract(w3, contract_addr, config["contract"]["abi"])

        # Load owner wallet
        owner_address = w3.to_checksum_address(config["wallet"]["address"])
        private_key = config["wallet"]["secret_key"]

        # Preprocess addresses to convert to checksum
        addresses = [w3.to_checksum_address(address) for address in holders]

        # Verify length of lists
        assert len(addresses) == len(amounts)

        # Iteration number
        iterations = len(addresses) // block_size
        transactions = []

        for iteration in tqdm(range(iterations + 1)):
            # Set block
            from_index = iteration * block_size
            to_index = min(from_index + block_size, len(addresses))
            addresses_block = addresses[from_index:to_index]
            amounts_block = amounts[from_index:to_index]

            txn_receipt = execute_batch_transfer_call(w3, contract,
                                                      owner_address,
                                                      private_key,
                                                      addresses_block,
                                                      amounts_block)

            transactions.append(txn_receipt)

        return transactions
