# public key cryptography is an example of asymetric cryptography
# it involves two or more key pairs, one of them being kept secret
# in this example: the popular RSA algorithm
# output of all algorithms: a correlated pair of keys A and B
# these keys can be used for encryting a message and send it through an unsecure channel
# key A remains secret and private
# key B is made public
# (1) public key B is used to encrypt a message that only can be decrypted 
#     with the correlated private key A
# (2) private key A can be used to sign a message and public key B can be
#     used to verify that the message got signed by the correlated private key

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
# so, the box gets signed with bob's private key and encrypted with alice's public key
bobs_box = Box(bobs_private_key, alices_public_key)

# we encrypt bob's secret message (bytes)
encrypted = bobs_box.encrypt(bytes(message[random.randint(0, len(message)-1)], 'utf-8'))

# alice creates a second box with her private key 
# and bob's public key so she can decrypt the message
# alice verifys that the message is from bob with his public key
# and decrypts it with her private key
alices_box = Box(alices_private_key, bobs_public_key)

# now alice can decrypt the message
plaintext = alices_box.decrypt(encrypted)
print(plaintext.decode('utf-8'))
