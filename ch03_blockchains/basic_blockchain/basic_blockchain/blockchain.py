class blockchain(object):

    def __init__(self):
        self.chain = []
        self.pending_transactions = []

    def new_block(self):
        # generates a new block and adds it to the chain
        pass

    @staticmethod
    def hash(block):
        # hashes a block
        pass

    def last_block(self):
        # gets the latest block of the chain
        pass
    
    # adding a primitive unsigned transaction for illustration's sake
    def new_transaction(self, sender, recipient, amount):
        # adds a new transaction to a list of pending transactions
        self.pending_transactions.append({
            "recipient": recipient,
            "sender": sender,
            "amount": amount,
        })

