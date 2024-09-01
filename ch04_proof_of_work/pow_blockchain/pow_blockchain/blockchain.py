import json
import random

from datetime import datetime
from hashlib import sha256

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        # Create the genesis block
        print("Creating genesis block")
        self.chain.append(self.new_block())
    
    def new_block(self, previous_hash=None):

        if self.last_block():
            previous_hash = self.last_block()["hash"]

        # generates a new block and adds it to the chain
        block = {
            'index': len(self.chain),
            'timestamp': datetime.now().isoformat(), #.utcnow().isoformat(),
            'transactions': self.pending_transactions,
            'previous_hash': previous_hash,
            # 'previous_hash': self.last_block["hash"] if self.last_block else None,
            # 'nonce': None,
            'nonce': format(random.getrandbits(64), "x"),
        }
        # get the hash of this new block, and add it to the block
        block_hash = self.hash(block)
        block["hash"] = block_hash

        # reset the list of pending transactions
        self.pending_transactions = []
        # add the block to the chain
        # self.chain.append(block) # not validated, don't add here, add in proof_of_work()

        # print(f"Created block {block['index']}")
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

    def proof_of_work(self):
        while True:
            # creating a new block with a random nonce
            new_block = self.new_block()
            # hash the block to see if it's valid
            if self.valid_block(new_block):
                break # break if valid otherwise repeat step

        self.chain.append(new_block)
        print("Found a new block: ", new_block)
    
    # method for validating hashes
    # previously referred to as valid_hash() in the book
    def valid_block(block):
        return block["hash"].startswith("0000")
        

