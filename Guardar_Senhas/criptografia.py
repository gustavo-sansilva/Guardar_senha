from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import secrets

chave = Fernet.generate_key()

objeto = Fernet(chave)

mensagem = "Minha senha teste"

mensagem_criptografada = objeto.encrypt(mensagem.encode()) # encode transforma o texto em bytes

mensagem_descriptografada = objeto.decrypt(mensagem_criptografada).decode() # transforma bytes em texto

salt = secrets.token_bytes(32)

algoritmo = hashes.SHA256

