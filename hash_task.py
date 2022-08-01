s = "Python Bootcamp"

def hash_func(text):
    """Function start hashing some inputs"""
    hash_text = hash(text)
    return print(hash_text)

hash_func(s)