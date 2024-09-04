# example: using an agreed on shared password to encrypt a message
# our protagonists are once again bob and alice
# -> they have shared a secret passwort the use for encryption
# trivial example to illustrate the principle

from hashlib import sha256

shared_password = "p@55wOrD" # alice and bob have it

# alice is sending her message
message_alice = "Hello Bob, let's meet at the Kruger National Park on 2024-12-12 at 1pm"
alices_hash = sha256((shared_password + message_alice).encode()).hexdigest()

print(alices_hash) # the computed has of alice's message
# 3c7413e9cfcd5cb0ad76f0996a736400aec015a22d384135290b567323bc72da

# alice sends the message including the hash to Bob
# bob receives message_alice plus alices_hash
# bob creates a hash out of message_alice and shared_password to verify
bobs_hash = sha256((shared_password + message_alice).encode()).hexdigest()
print(bobs_hash) # the computed has of alice's message
# 3c7413e9cfcd5cb0ad76f0996a736400aec015a22d384135290b567323bc72da

# verifying...
if bobs_hash == alices_hash:
    print("YoOO! Message has not been tampered with!")
else:
    print("There's a fox in the henhouse")