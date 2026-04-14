import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from key_gen import deserialize_symmetric_key
from RSA import deserialize_private_key, decrypt_data
from text_processor import save_text, read_text, read_chipher


def encrypt(text_file: str, symmetric_path: str, private_pem: str, encrypt_file: str):
    print("Начинаю шифрование...")
    text = read_text(text_file)
    iv = os.urandom(16)
    key = decrypt_data(
        deserialize_symmetric_key(symmetric_path), deserialize_private_key(private_pem)
    )
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()  # 128 бит = 16 байт (размер блока)
    padded_data = padder.update(text) + padder.finalize()

    c_text = encryptor.update(padded_data) + encryptor.finalize()

    print("Сохраняем в файл...")
    save_text(iv + c_text, encrypt_file)


def decrypt(text_file: str, symmetric_path: str, private_pem: str, decrypt_path: str):
    print("Начинаю расшифровку...")
    iv, c_text = read_chipher(text_file)
    key = decrypt_data(
        deserialize_symmetric_key(symmetric_path), deserialize_private_key(private_pem)
    )
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(c_text) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    dc_text = unpadder.update(dc_text) + unpadder.finalize()

    print("Сохраняем в файл...")
    save_text(dc_text, decrypt_path)
