import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from key_gen import deserialize_symmetric_key
from RSA import deserialize_private_key, decrypt_data
from text_processor import save_text, read_text, read_chipher


def encrypt(
    text_file_path: str,
    symmetric_key_path: str,
    private_key_pem_path: str,
    encrypted_file_path: str,
):
    """
    Encrypt data with symmetric encryption using RSA key encryption
    :param text_file_path: Path to source file
    :param symmetric_key_path: Path to serialized encrypted symmetric key
    :param private_key_pem_path: Path to serialized private RSA key
    :param encrypted_file_path: Path for save encrypted data
    """
    text = read_text(text_file_path)
    iv = os.urandom(16)
    key = decrypt_data(
        deserialize_symmetric_key(symmetric_key_path),
        deserialize_private_key(private_key_pem_path),
    )
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(text) + padder.finalize()

    c_text = encryptor.update(padded_data) + encryptor.finalize()

    save_text(iv + c_text, encrypted_file_path)


def decrypt(
    text_file_path: str,
    symmetric_key_path: str,
    private_key_pem_path: str,
    decrypted_file_path: str,
):
    """
    Decrypt data with symmetric encryption using RSA key encryption
    :param text_file_path: Path to encrypted file
    :param symmetric_key_path: Path to serialized encrypted symmetric key
    :param private_key_pem_path: Path to serialized private RSA key
    :param decrypted_file_path: Path for save decrypted data
    """
    iv, c_text = read_chipher(text_file_path)
    key = decrypt_data(
        deserialize_symmetric_key(symmetric_key_path),
        deserialize_private_key(private_key_pem_path),
    )
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(c_text) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    dc_text = unpadder.update(dc_text) + unpadder.finalize()

    save_text(dc_text, decrypted_file_path)
