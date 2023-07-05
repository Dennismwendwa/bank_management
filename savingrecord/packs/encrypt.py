import os
from django.conf import settings
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

base_dir = settings.BASE_DIR
private_key_path = os.path.join(base_dir, "private_key.pem")
public_key_path = os.path.join(base_dir, "public_key.pem")


# enctypting the account number

def encode_account_number(account_number):

    with open(public_key_path, "rb") as file:
        public_key = serialization.load_pem_public_key(
                file.read(),
                backend=default_backend()
                )

    ciphertext = public_key.encrypt(
            account_number.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label = None
                )
            )

    return ciphertext

#decrypting the account number
def decode_account_number(ciphertext):

    with open(private_key_path, "rb") as file:
        private_key = serialization.load_pem_private_key(
                file.read(),
                password = None,
                backend = default_backend()
                )

    plaintext = private_key.decrypt(
            #base64.b64decode(ciphertext),
			ciphertext,
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
                )
            )
    account_number_plain = plaintext.decode("utf-8")
    
    return account_number_plain
