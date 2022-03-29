from web3 import Web3
from solcx import compile_source
import sys
import signal

contractAddress = 'your-contract-address'

with open('chatroom.sol', 'r') as f:
    contract_source = f.read()

compiled_sol = compile_source(contract_source, output_values=['abi'])

contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface['abi']

w3 = Web3(Web3.HTTPProvider('your-infura-url'))
print(w3.isConnected())

contract = w3.eth.contract(address=contractAddress, abi=abi)

messageCount = contract.functions.getMessageCount().call()
print('Current number of messages:', messageCount)
eventListener = contract.events.NewMessage.createFilter(fromBlock='latest')

for i in range(messageCount):
    addr, nickname, contents = contract.functions.messages(i).call()
    print(f'{nickname}\n| {contents}\n')

def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    for event in eventListener.get_new_entries():
        addr, nickname, contents = event['args']['']
        print(f'{nickname}\n| {contents}\n')
