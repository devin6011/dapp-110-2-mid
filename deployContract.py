from web3 import Web3
from solcx import compile_source

with open('chatroom.sol', 'r') as f:
    contract_source = f.read()

compiled_sol = compile_source(contract_source, output_values=['abi', 'bin'])

contract_id, contract_interface = compiled_sol.popitem()
bytecode = contract_interface['bin']
abi = contract_interface['abi']


w3 = Web3(Web3.HTTPProvider('your-infura-url'))
print(w3.isConnected())

with open('./privateKey', 'r') as f:
    privateKey = f.read().strip()

contract = w3.eth.contract(abi=abi, bytecode=bytecode)

acct = w3.eth.account.privateKeyToAccount(privateKey)
print(acct.address)

tx = contract.constructor().buildTransaction({
    'from': acct.address,
    'nonce': w3.eth.getTransactionCount(acct.address),
    'maxFeePerGas': w3.toWei(250, 'gwei'),
    'maxPriorityFeePerGas': w3.toWei(120, 'gwei'),})

signed_tx = acct.signTransaction(tx)

tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print('Tx hash:', tx_hash.hex())
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

address = tx_receipt['contractAddress']

print('Contract Address: ', address)
