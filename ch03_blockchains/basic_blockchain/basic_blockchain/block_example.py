# blocks we're going to build are simple Python dictionaries
# example block
block_1066 = {
    'index': 1066,
    'timestamp': "2024-01-19T03:14:07.299999",
    # a block can contain any data: files, images, transactions, records etc.
    # example here: single transaction from bob to alice about $5
    'data': [
        {
            'sender': "bob",
            'recipient': "alice",
            'amount': "$5",
        }
    ],
    'hash': "83b2ac5b",
    # each block contains a hash of the previous block
    'previous_hash': "2cf24ba5f"
}