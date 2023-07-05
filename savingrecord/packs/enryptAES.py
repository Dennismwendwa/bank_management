import os
from django.conf import settings
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes

KEY_FILE_PATH = "/home/dennis/projects/saving_record/savingrecord/aes_key.bin"
AES_KEY_PATH = 'aes_key.bin'
AES_KEY_SIZE = 32 # 256-bit key

base_dir = settings.BASE_DIR
key_path = os.path.join(base_dir, "aes_key.bin")

def generate_aes_key():
    #Generate a new AES key

    key_path = "aes_key.bin"

    try:
        with open(key_path, "rb") as key_file:
            key = key_file.write()
    except FileNotFoundError:
        generate_and_save_key()
        with open(key_path, "rb") as key_file:
            key = key_file.read()

    return key

def get_aes_key():

    if not os.path.exists(KEY_FILE_PATH):
        generate_and_save_key()


    #load the AES key from file
    with open(key_path, "rb") as key_file:
        return key_file.read()

def encrypt(plaintext):
    # Generate new initialization vector (IV)
    iv = os.urandom(16)

    key_size = 32  # 256-bit key
    key = os.urandom(key_size)

    #Create the AES cipher with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    padder = padding.PKCS7(128).padder()

    padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

    #Encryp the padded
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    return iv + ciphertext


def decrypt_eas(ciphertext):
    # Extract the IV from the ciphertext
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]

    #get the AES key
    key_size = 32  # 256-bit key
    key = os.urandom(key_size)

    iv_bytes = iv.encode('utf-8')
    ciphertext_bytes = ciphertext.encode('utf-8')

    #creating the AES cipher with CBC mode
    cipher =Cipher(algorithms.AES(key), modes.CBC(iv_bytes), backend = default_backend())

    # Decrpht the cipher
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext_bytes) + decryptor.finalize()

    # removing padding from the plaintext
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(plaintext) + unpadder.finalize()

    plaintext_final = plaintext.decode()

    return plaintext_final


def generate_and_save_key():
    salt = b'salt_'
    password = b'password'
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=AES_KEY_SIZE,
            salt=salt,
            iterations=100000,
            backend=default_backend()
            )
    key = kdf.derive(password)

    with open(AES_KEY_PATH, "wb") as key_file:
        key_file.write(key)


