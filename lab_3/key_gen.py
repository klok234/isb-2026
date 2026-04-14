import os

from RSA import (
    encrypt_data,
    generate_rsa_keys,
    serialize_public_key,
    serialize_private_key,
)


def key_gen(lenght: int, public_pem: str, private_pem: str, symmetric_path: str):
    private_key, public_key = generate_rsa_keys()
    serialize_public_key(public_key, public_pem)
    serialize_private_key(private_key, private_pem)
    key = os.urandom(lenght)  # это байты
    serialize_symmetric_key(encrypt_data(key, public_key), symmetric_path)


def serialize_symmetric_key(key, symmetric_path: str):
    with open(symmetric_path, "wb") as key_file:
        key_file.write(key)
