#Cryptography_pwm
#everything in this module is for encrypting and decripting, as well as hashing functions

import hashlib
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
  
    
    
def hasher(password, salt):
    bin_pw = password.encode()
    hasher = hashlib.pbkdf2_hmac('sha256', bin_pw, salt, 100000)
    
    hashed_pw = hasher.hex()
    #print(hashed_pw)
    return hashed_pw
    
def en_de_alg(password, salt):
    pw = password  # This is input in the form of a string
    pw_b = pw.encode()  # Convert to type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(pw_b))  # Can only use kdf once
    return key


def encrypter(password, salt, db_file):
    key = en_de_alg(password, salt)
    input_file = db_file
    output_file = db_file

    with open(input_file, 'rb') as f:
        data = f.read()  # Read the bytes of the input file

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)  # Write the encrypted bytes to the output file

    # delete input_file
    # os.remove(input_file)
    # return output_file    


def decrypter(password, salt, db_file):
    key = en_de_alg(password, salt)
    input_file = db_file 
    output_file = db_file

    with open(input_file, 'rb') as f:
        data = f.read()  # Read the bytes of the encrypted file

    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(data)

        with open(output_file, 'wb') as f:
            f.write(decrypted)  # Write the decrypted bytes to the output file

        # Note: You can delete input_file here if you want
        # os.remove(input_file)

    except InvalidToken as e:
        print("Invalid Key - Unsuccessfully decrypted")
        print(e)

    # return output_file








