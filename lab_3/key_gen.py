import os

from RSA import (
    encrypt_data,
    generate_rsa_keys,
    serialize_public_key,
    serialize_private_key,
)


def key_gen(lenght: int, public_pem: str, private_pem: str, symmetric_path: str):
    """Generate RSA pair of keys and symmetric key and saving it to files"""
    private_key, public_key = generate_rsa_keys()
    serialize_public_key(public_key, public_pem)
    serialize_private_key(private_key, private_pem)
    key = os.urandom(lenght // 8)
    serialize_symmetric_key(encrypt_data(key, public_key), symmetric_path)


def serialize_symmetric_key(key, symmetric_path: str):
    """Save the symmetric key on the path"""
    try:
        with open(symmetric_path, "wb") as key_file:
            key_file.write(key)
        print(f"Key is saved to {symmetric_path}")
    except Exception as e:
        print(e)
        exit(2)


def deserialize_symmetric_key(symmetric_path: str):
    """Read the key on the path. Return symmetric key"""
    try:
        with open(symmetric_path, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print(f"Error: File {symmetric_path} not found!")
        exit(1)
    except Exception as e:
        print(e)
        exit(2)
