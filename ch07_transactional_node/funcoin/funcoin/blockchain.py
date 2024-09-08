import json

from datetime import datetime
from hashlib import sha256

'''
# testing the blockchain on the terminal with python:
$ poetry shell
$ python3 -i blockchain.py
>>> bc = Blockchain()
>>> bc.chain
# add a new block by copying the hash from the terminal output
>>> bc.new_block(previous_hash="XXX")
'''

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        # Create the genesis block
        print("Creating genesis block")
        self.new_block()
    
    def new_block(self, previous_hash=None):
        # generates a new block and adds it to the chain
        block = {
            'index': len(self.chain),
            'timestamp': datetime.now().isoformat(), #.utcnow().isoformat(),
            'transactions': self.pending_transactions,
            'previous_hash': previous_hash,
        }
        # get the hash of this new block, and add it to the block
        block_hash = self.hash(block)
        block["hash"] = block_hash

        # reset the list of pending transactions
        self.pending_transactions = []
        # add the block to the chain
        self.chain.append(block)

        print(f"Created block {block['index']}")
        return block

    @staticmethod
    def hash(block):
        # we ensure that the dictionary is sorted or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    def last_block(self):
        # gets the latest block of the chain (if there are blocks)
        return self.chain[-1] if self.chain else None
    
    # adding a primitive unsigned transaction for illustration's sake
    def new_transaction(self, sender, recipient, amount):
        # adds a new transaction to a list of pending transactions
        self.pending_transactions.append({
            "recipient": recipient,
            "sender": sender,
            "amount": amount,
        })

