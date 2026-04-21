import os

from RSA import (
    encrypt_data,
    generate_rsa_keys,
    serialize_public_key,
    serialize_private_key,
)


def key_gen(
    lenght: int,
    public_key_pem_path: str,
    private_key_pem_path: str,
    symmetric_key_path: str,
):
    """
    Generate RSA pair of keys and symmetric key.
    :param lenght: Count bits of symmetric key
    :param public_key_pem_path: Path for save public key
    :param private_key_pem_path: Path for save private key
    :param symmetric_key_path: Path for save symmetric key
    """
    private_key, public_key = generate_rsa_keys()
    serialize_public_key(public_key, public_key_pem_path)
    serialize_private_key(private_key, private_key_pem_path)
    key = os.urandom(lenght // 8)
    serialize_symmetric_key(encrypt_data(key, public_key), symmetric_key_path)


def serialize_symmetric_key(key, symmetric_key_path: str):
    """
    Save the symmetric key to file
    :param key: source symmetric key
    :param symmetric_key_path: Path for save symmetric key
    """
    try:
        with open(symmetric_key_path, "wb") as key_file:
            key_file.write(key)
    except Exception as e:
        print(e)
        exit(2)


def deserialize_symmetric_key(symmetric_key_path: str):
    """
    Read symmetric key.
    :param symmetric_key_path: Path for read symmetric key
    :return: symmetric key
    """
    try:
        with open(symmetric_key_path, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print(f"Error: File {symmetric_key_path} not found!")
        exit(1)
    except Exception as e:
        print(e)
        exit(2)
