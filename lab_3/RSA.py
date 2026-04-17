from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)


def generate_rsa_keys():
    """Generate a pair of public and private keys."""
    keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key


def serialize_public_key(public_key, public_pem: str):
    """Save the key in the format .pem on the path"""
    try:
        with open(public_pem, "wb") as public_out:
            public_out.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )
    except Exception as e:
        print(e)
        exit(2)


def serialize_private_key(private_key, private_pem: str):
    """Save the key in the format .pem on the path"""
    try:
        with open(private_pem, "wb") as private_out:
            private_out.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
    except Exception as e:
        print(e)
        exit(2)


def deserialize_public_key(public_pem: str):
    """Read the key in the format .pem on the path. Return public RSA key"""
    try:
        with open(public_pem, "rb") as pem_in:
            public_bytes = pem_in.read()
        return load_pem_public_key(public_bytes)
    except Exception as e:
        print(e)
        exit(2)


def deserialize_private_key(private_pem: str):
    """Read the key in the format .pem on the path. Return private RSA key"""
    try:
        with open(private_pem, "rb") as pem_in:
            private_bytes = pem_in.read()
        return load_pem_private_key(
            private_bytes,
            password=None,
        )
    except Exception as e:
        print(e)
        exit(2)


def encrypt_data(text, public_key):
    """Encrypt data using an RSA public key"""
    c_text = public_key.encrypt(
        text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return c_text


def decrypt_data(text, private_key):
    """Decrypt data using an RSA private key. Return decoded data"""
    dc_text = private_key.decrypt(
        text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return dc_text
