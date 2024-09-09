import asyncio
import json
import math
import random

from datetime import datetime # to be replaced with time
from hashlib import sha256
from time import time

import structlog
logger = structlog.get_logger("blockchain")

'''
# let's see if the still works >>>
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
        self.target = "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

        # Create the genesis block
        logger.info("Creating genesis block")
        self.chain.append(self.new_block())
    
    def new_block(self):
        block = self.create_block(
            height = len(self.chain),
            transactions = self.pending_transactions,
            previous_hash = self.last_block["hash"] if self.last_block else None,
            nonce = format(random.getrandbits(64), "x"),
            target = self.target,
            timestamp = time(),
        )

        # reset the list of pending transactions
        self.pending_transactions = []

        return block
    
    @staticmethod
    def create_block(
        self, height, transactions, previous_hash, nonce, target, timestamp=None
    ):
        block = {
            "height": height,
            "transactions": transactions,
            "previous_hash": previous_hash,
            "nonce": nonce,
            "target": target,
            "timestamp": timestamp or time(),
        }

        # get the hash of this new block and add it to the block
        block["hash"] = self.hash(block)
        return block

    @staticmethod
    def hash(block):
        # we ensure that the dictionary is sorted or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        # gets the latest block of the chain (if there are blocks)
        return self.chain[-1] if self.chain else None
    
    def valid_block(self, block):
        # check if a block's hash is less than the target
        return block["hash"] < self.target
    
    def add_block(self, block):
        # TODO: add proper validation logic here
        self.chain.append(block)
    
    # adding a primitive unsigned transaction for illustration's sake
    def new_transaction(self, sender, recipient, amount):
        # adds a new transaction to a list of pending transactions
        self.pending_transactions.append({
            "recipient": recipient,
            "sender": sender,
            "amount": amount,
        })

