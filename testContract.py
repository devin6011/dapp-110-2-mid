from web3 import Web3, EthereumTesterProvider
from solcx import compile_source

with open('chatroom.sol', 'r') as f:
    contract_source = f.read()

compiled_sol = compile_source(contract_source, output_values=['abi', 'bin'])

contract_id, contract_interface = compiled_sol.popitem()

bytecode = contract_interface['bin']
abi = contract_interface['abi']

w3 = Web3(EthereumTesterProvider())
print(w3.isConnected())

w3.eth.default_account = w3.eth.accounts[0]

contract = w3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = contract.constructor().transact()

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print(contract.functions.getMessageCount().call())

tx_hash = contract.functions.sendMessage('applejack', 'funk').transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(contract.functions.getMessageCount().call())
print(contract.functions.messages(0).call())


tx_hash = contract.functions.sendMessage('deadmice', 'haha').transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
tx_hash = contract.functions.sendMessage('monkeyking', 'lgtm').transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(contract.functions.getMessageCount().call())
print(contract.functions.messages(0).call())
print(contract.functions.messages(1).call())
print(contract.functions.messages(2).call())


eventListener = contract.events.NewMessage.createFilter(fromBlock='latest')

while True:
    nickname = input()
    contents = input()
    tx_hash = contract.functions.sendMessage(nickname, contents).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("Message sent")

    for event in eventListener.get_new_entries():
        print(event['args'][''])
