import rsa

# Generate a pair of new keys of 2048 bytes.
public_key,private_key = rsa.newkeys(2048)
# Export these key in their correspondent files. .PEM is the format that has been chosen. PEM is a method of encoding
# binary data as a string (also known as utf-8 armor). It contains a header and a footer line (specifying the type of
# data that is encoded and showing begin/end if the data is chained together) and the data in the middle is the base
# 64 data.
# PEM may also encode / protect other kinds of data that is related to certificates such as public / private keys,
# certificate requests, etc.
with open("public_key.pem","wb") as f:
    # Saves the public key in PKCS#1 DER or PEM format.
    f.write(public_key.save_pkcs1("PEM"))

with open("private_key.pem","wb") as f:
    f.write(private_key.save_pkcs1("PEM"))

signature = rsa.sign("message".encode(), private_key , "SHA-256")
with open ("signature","wb") as f:
    f.write(signature)