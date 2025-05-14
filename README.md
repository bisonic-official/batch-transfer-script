# Batch Token Transfer Script 💻


This repository contains the `BatchTokenTransfer` abi file of contract + a script to perform batch transfers of specified token.

### Python setup

1. Clone this repository
2. Install Python dependencies: `pip install -r requirements.txt` <br>
    (You can create a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/) if you don't want to install packages globally.)

### Generated holders list

The generated holders list will be provided by the dev team as a JSON file with the following name: `holders.json`.

In order to use this file to execute the batch transfer of the tokens, please add this file to the main folder (`/batch-transfer/holders.json`).

If you plan to place the file in a diferent directory, please add the corresponding path to the file in the `config.ini` file.

### Execute the batch transfer

To exectute the batch transfer of the token, follow these steps:

1. Fill the `config.ini` file by adding the missing fields. This will provide the access to the wallet, chain and contract to run the batch transfer. Here's a detailed view of whats needed:

    ```ini
    [event]
    event_id = XXXXXXXXXXXXXXXXXXXXXXXX     # The id of the event
    holders = holders.json                  # The path to holders.json
    transactions = transactions.txt         # The path to transactions.txt
    block_size = 100                        # The batch size of txns

    [wallet]    # Access to the wallet
    address = 0x0000000000000000000000000000000000000000
    secret_key = 0x0000000000000000000000000000000000000000000000000000000000000000

    [network]   # Access to the blockchain network
    api_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  # This key is provided by Moralis
    network = ronin                             # Chain: saigon or ronin

    [contract]  # Access to the contract
    address = 0x0000000000000000000000000000000000000000
    abi = abi/TokenBatchTransfer.json
    ```

2. Run `python run-batch-transfer.py -c config.ini`. This will generate the file `transactions.txt` (as specified in `config.ini`) containing the list of transactions executed in the batch transfer.

3. Provide the generated `transactions.txt` file to the dev team in order to update the status of transfers in the database.

> **NOTE:** By default it uses the path `"holders.json"` to read a holders list and perform the batch transfer, but if needed, you can specify another path by modifying this in the `config.ini` file.