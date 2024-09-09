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
>>> bc.new_block()
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
        
        logger.info(f"New block created: {block}")

        # reset the list of pending transactions
        self.pending_transactions = []

        return block
    
    # for now it's not really clear how a new block gets appended to the chain
    # we're adding a helper here
    # TODO: figuring out where this is supposed to happen
    def add_a_new_block_to_the_chain(self):
        self.chain.append(self.new_block())

    @staticmethod
    def create_block(
        height, transactions, previous_hash, nonce, target, timestamp=None
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
        # block["hash"] = self.hash(block)
        block_string = json.dumps(block, sort_keys=True).encode()
        block["hash"] = sha256(block_string).hexdigest()
        return block
    
    # TODO: is it sufficient the the following method gets replaced with code in create_block?
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
    
    # the following function isn't described in any way in the book
    # so we've to find out what it does with trial and error
    def recalculate_target(self, block_index):
        """
        returns the number we need to get below to mine a block
        """
        # check if we need to recalculate the target
        if block_index % 10 == 0:
            # expected time span of 10 blocks
            expected_timespan = 10 * 10

            # calculate the actual time span
            actual_timespan = self.chain[-1]["timestamp"]
            expected_timespan = self.chain[-10]["timestamp"]

            # figure out what the offset is
            ratio = actual_timespan / expected_timespan

            # now let's adjust the to not be too extreme
            ratio = max(0.25, ratio)
            ratio = min(4.00, ratio)

            # calculate the new target by multiplying the current one by the ratio
            new_target = int(self.target, 16) * ratio

            self.target = format(math.floor(new_target), "x").zfill(64)
            logger.info(f"Calculated new mining target: {self.target}")

        return self.target
    
    async def get_blocks_after_timestamp(self, timestamp):
        for index, block in enumerate(self.chain):
            if timestamp < block["timestamp"]:
                return self.chain[index:]
    
    async def mine_new_block(self):
        self.recalculate_target(self.last_block["index"] + 1)
        while True:
            new_block = self.new_block()
            if self.valid_block(new_block):
                break

            await asyncio.sleep(0)
        
        self.chain.append(new_block)
        logger.info("Found a new block: " + new_block)
    
    # adding a primitive unsigned transaction for illustration's sake
    def new_transaction(self, sender, recipient, amount):
        # TODO: moving this method to its own class in transactions.py
        # adds a new transaction to a list of pending transactions
        self.pending_transactions.append({
            "recipient": recipient,
            "sender": sender,
            "amount": amount,
        })

