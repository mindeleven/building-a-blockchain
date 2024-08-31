# a trivial example of proof of work
# requirement: the hash of some integer x multiplied by another integer y must end in 0
# so hash(x * y) must result in a hash that ends with a zero

from hashlib import sha256

x = 5
y = 0 # we've to find out the actual value of y

while sha256(f'{x * y}'.encode()).hexdigest()[-1] != "0":
    # print(sha256(f'{x * y}'.encode()).hexdigest())
    y += 1

print(f'The solution is y = {y}')
print(sha256(f'{x * y}'.encode()).hexdigest())