import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"


def _load_or_create_key():

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()

    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as f:
        f.write(key)

    return key


_key = _load_or_create_key()
_fernet = Fernet(_key)


def encrypt_password(plain_text):

    if plain_text is None:
        plain_text = ""

    return _fernet.encrypt(plain_text.encode("utf-8")).decode("utf-8")


def decrypt_password(encrypted_text):

    if not encrypted_text:
        return ""

    try:
        return _fernet.decrypt(encrypted_text.encode("utf-8")).decode("utf-8")
    except Exception:
        # Se falhar (ex: password antiga nao encriptada), devolve como esta
        return encrypted_text