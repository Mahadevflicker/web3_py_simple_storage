from solcx import compile_standard,install_solc
import json

from web3 import Web3

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

print(abi)

# for connecting to ganache
w3 - Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 5777
my_address = "0xAB22918645E050d44A21D9C45BDC4161efc23BfC"
private_key = "0x789bf2596b72d2e4cdb1695f39069f89ae9971031864d7ec62781088008fc7cd"

# Create the contract in python

SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)