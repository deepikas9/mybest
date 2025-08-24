import binascii
import os
from base64 import b64encode, b64decode
from hashlib import sha256
from django.conf import settings
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def _get_key() -> bytes:
    """
    Generate a 32-byte encryption key derived from the Django SECRET_KEY.
    """
    return sha256(settings.SECRET_KEY.encode()).digest()

def encrypt_message(plaintext: str) -> str:
    """
    Encrypt a plaintext message using AES-256-CBC.
    Returns a base64-encoded string containing the IV + ciphertext.
    """
    key = _get_key()
    iv = os.urandom(16)  # 16-byte IV
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()

    return b64encode(iv + ct).decode('utf-8')

def decrypt_message(encrypted_message: str) -> str:
    """
    Decrypt a base64-encoded string produced by encrypt_message.
    Falls back to returning the original string if decoding or decryption fails.
    """
    key = _get_key()
    try:
        encrypted_bytes = b64decode(encrypted_message)
    except binascii.Error:
        # Not a valid base64 string — return as-is
        return encrypted_message

    if len(encrypted_bytes) < 16:
        # Too short to contain IV — return as-is
        return encrypted_message

    iv, ct = encrypted_bytes[:16], encrypted_bytes[16:]
    try:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded = decryptor.update(ct) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded) + unpadder.finalize()
        return plaintext.decode('utf-8')
    except Exception:
        # Decryption failed — return original encrypted string
        return encrypted_message
