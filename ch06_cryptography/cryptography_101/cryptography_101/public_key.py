# public key cryptography

from nacl.public import PrivateKey, Box
import random

# song titles of beatles songs
message = [
    "I Am the Walrus",
    "Why Don't We Do It in the Road",
    "Helter Skelter",
    "We all Live in a Yellow Submarine"
]

# generate secret keys for alice and bob
alices_private_key = PrivateKey.generate()
bobs_private_key = PrivateKey.generate()

# public keys are generated from the private keys
alices_public_key = alices_private_key.public_key
bobs_public_key = bobs_private_key.public_key

# bob will send alice a message
# -> he makes a box with his private key and alices public key
bobs_box = Box(bobs_private_key, alices_public_key)

# we encrypt bob's secret message (bytes)
encrypted = bobs_box.encrypt(bytes(message[random.randint(0, len(message)-1)], 'utf-8'))

# alice creates a second box with her private key 
# and bob's public key so she can decrypt the message
alices_box = Box(alices_private_key, bobs_public_key)

# now alice can decrypt the message
plaintext = alices_box.decrypt(encrypted)
print(plaintext.decode('utf-8'))
