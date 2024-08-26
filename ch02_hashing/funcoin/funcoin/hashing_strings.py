import hashlib

# hash function expects bytes as input
# encode() turns strings to bytes
input_bytes = b"backpack"

output = hashlib.sha256(input_bytes)

# hexdigest() converts bytes to hex (easier to read)
print(output.hexdigest()) # 5f00368a6ad231c3c439c4f6bc33c27014b4d35a904ff1656d74f9528636f496

# now with minor change
input_bytes_2 = b"Backpack"

output_2 = hashlib.sha256(input_bytes_2)

# hexdigest() converts bytes to hex (easier to read)
print(output_2.hexdigest()) # 5118f76d9067edc593d6946b88693cefa6604c7e613111193db118166d4af589