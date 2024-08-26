from hashlib import sha256

# example image from pixabay https://pixabay.com/de/photos/banknoten-dollar-us-dollar-geld-941246/
file = open("../../../assets/image/pixabay-bank-notes-941246_1280.jpg", "rb")
hash = sha256(file.read()).hexdigest()
file.close()

print(f"The hash of the file is: {hash}") 
# 8478c0fceabdaa83da3b19ea727807577c77f170a597140d12c5a8ca939de770