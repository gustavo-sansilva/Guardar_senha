from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import secrets

length = 32 # 32 bytes para a chave
salt = secrets.token_bytes(32) # 32 bytes aleatórios
algoritmo = hashes.SHA256()
iterations = 310_000

senha_mestre = "MinhaSenhaMestre123"

def gerar_chave(senha_mestre, salt):

    kdf = PBKDF2HMAC(algoritmo, length, salt, iterations)

    chave_derivada = kdf.derive(senha_mestre.encode())

    chave_fernet = base64.urlsafe_b64encode(chave_derivada)
    objetoFernet = Fernet(chave_fernet)
    return objetoFernet

objetoFernet = gerar_chave(senha_mestre, salt)

def criptografar(mensagem, objetoFernet):
    mensagem_bytes = mensagem.encode()
    mensagem_criptografada = objetoFernet.encrypt(mensagem_bytes)
    return mensagem_criptografada