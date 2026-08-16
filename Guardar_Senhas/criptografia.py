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

kdf = PBKDF2HMAC(algoritmo, length, salt, iterations)

chave_derivada = kdf.derive(senha_mestre.encode())

chave_fernet = base64.urlsafe_b64encode(chave_derivada)

print(Fernet(chave_fernet))

mensagem = "receba"

mensagem_criptografada = 