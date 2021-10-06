from solcx import compile_standard,install_solc
import json

from web3 import Web3
from os import getenv
from dotenv import load_dotenv


load_dotenv()

with open("./SimpleStorage.sol", 'r') as file:
    simple_storage_file = file.read()

#Compile Our Solidity
print("Installing...")
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
 
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },

    },
    solc_version="0.6.0",
)

with open("compiled_code.json","w") as file:
    json.dump(compiled_sol, file)

# Get Bytecode for implementing the contract in python

bytecode = compiled_sol["contracts"][ "SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# Get ABI
abi = compiled_sol["contracts"][ "SimpleStorage.sol"]["SimpleStorage"]["abi"]

#print(abi)

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = getenv("PRIVATE_KEY")
#print(private_key)
# Create the contract in python

SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)

# Get the latest transaction

nonce = w3.eth.getTransactionCount(my_address)
#print(nonce)


#1. Build a transaction
#2. Sign a transaction
#3. Send a transaction

transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId":chain_id, "from" : my_address, 'nonce': nonce}
)

#print(transaction)
signed_txn = w3.eth.account.sign_transaction(transaction,private_key = private_key)
#print(signed_txn)
print("Deploying Contract")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed")
# Working with the contract
# Contract Address
# Contract ABI

simple_storage = w3.eth.contract(address = tx_receipt.contractAddress, abi = abi)

# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change

print(simple_storage.functions.retrieve().call())
print("Updating Contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key = private_key
)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!!")
print(simple_storage.functions.retrieve().call())

