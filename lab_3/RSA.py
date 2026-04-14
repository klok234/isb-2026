from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)


def generate_rsa_keys():
    print("Начинаю генерацию...")
    keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key


def serialize_public_key(public_key, public_pem: str) -> None:
    with open(public_pem, "wb") as public_out:
        public_out.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )
    print(f"Публичный ключ сохранен в {public_pem}")


def serialize_private_key(private_key, private_pem: str) -> None:
    with open(private_pem, "wb") as private_out:
        private_out.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    print(f"Приватный ключ сохранен в {private_pem}")


def deserialize_public_key(public_pem: str):
    with open(public_pem, "rb") as pem_in:
        public_bytes = pem_in.read()
    return load_pem_public_key(public_bytes)


def deserialize_private_key(private_pem: str):
    with open(private_pem, "rb") as pem_in:
        private_bytes = pem_in.read()
    return load_pem_private_key(
        private_bytes,
        password=None,
    )


def encrypt_data(text, public_key):
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
    dc_text = private_key.decrypt(
        text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return dc_text
