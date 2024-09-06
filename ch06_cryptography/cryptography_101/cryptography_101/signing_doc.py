import nacl.encoding
import nacl.signing

# generate a new key pair for bob
bobs_private_key = nacl.signing.SigningKey.generate()
bobs_public_key = bobs_private_key.verify_key
print("BOB'S PUBLIC KEY:")
print(bobs_public_key)

# since it's bytes we need to serialize the key to a readable format 
# before publishing it
bobs_public_hex_key = bobs_public_key.encode(encoder=nacl.encoding.HexEncoder)
print("BOB'S PUBLIC HEX KEY:")
print(bobs_public_hex_key)

# now let's bob sign a message with it
signed_message = bobs_private_key.sign(b"Send $37 to Alice")
print("BOB'S SIGNED MESSAGE:")
print(signed_message)

# verification process
# the verification process uses the signer's public key to check the signature
# we alread have bobs_public_hex_key

# we generate the verify key
verify_key = nacl.signing.VerifyKey(bobs_public_hex_key, encoder=nacl.encoding.HexEncoder)
print("THE VERIFY KEY:")
print(verify_key)

# bobs signed message is stored in signed_message
# let's attempt to verify the message
verify_key.verify(signed_message) # any invalidation will result in an exception
print("PRINT VERIFY:")
print(verify_key.verify(signed_message)) # reurns the message that got signed