import hashlib


def hashing(to_hash):
    h = hashlib.new("sha512")
    h.update(to_hash.encode())
    hashed = h.hexdigest()
    print(hashed)
    return hashed
