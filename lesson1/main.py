
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os


def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key


def encrypt_file(file_path, password, output_path):
    salt = os.urandom(16)
    key = generate_key(password, salt)

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()



    with open(file_path, 'rb') as f:
        file_data = f.read()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(file_data) + padder.finalize()

        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(output_path, 'wb') as f:
        f.write(salt + iv + encrypted_data)


def decrypt_file(file_path, password, output_path):


    with open(file_path, 'rb') as f:
        salt = f.read(16)
        iv = f.read(16)
        encrypted_data = f.read()

    key = generate_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    with open(output_path, 'wb') as f:
        f.write(decrypted_data)

if __name__ == "__main__":
    action = input("Виберіть дію (encrypt/decrypt): ").strip().lower()
    file_path = input("Введіть шлях до файлу: ").strip()
    password = input("Введіть пароль: ").strip()
    output_path = input("Введіть шлях для збереження результату: ").strip()

    if action == "encrypt":
        encrypt_file(file_path, password, output_path)
        print(f"Файл зашифровано та збережено як {output_path}.")
    elif action == "decrypt":
        decrypt_file(file_path, password, output_path)
        print(f"Файл дешифровано та збережено як {output_path}.")
    else:
        print("Невірна дія. Використовуйте 'encrypt' або 'decrypt'.")
