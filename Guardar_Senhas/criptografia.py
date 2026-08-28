from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import secrets

# EXPLICAR NO NOTION -> PARAMETROS DO KDF

length = 32 # 32 bytes para a chave / Define o tamanho da chave derivada em bytes.
salt = secrets.token_bytes(32) # 32 bytes aleatórios usados como salt.
algoritmo = hashes.SHA256() # Define o SHA-256 como algoritmo de hash do PBKDF2.
iterations = 310_000 # Define quantas vezes o PBKDF2 repete o processo de derivação.

senha_mestre = "MinhaSenhaMestre123" # Senha mestre usada para gerar a chave de criptografia.

# EXPLICAR NO NOTION -> COMO FUNCIONA A FUNÇÃO GERAR_CHAVE

def gerar_chave(senha_mestre, salt): # explicar os parametros da função

    kdf = PBKDF2HMAC(algoritmo, length, salt, iterations) # Cria o mecanismo PBKDF2 com os parâmetros definidos.

    chave_derivada = kdf.derive(senha_mestre.encode()) # Converte a senha para bytes e gera uma chave derivada.

    chave_fernet = base64.urlsafe_b64encode(chave_derivada) # Converte a chave derivada para o formato aceito pelo Fernet.
    objetoFernet = Fernet(chave_fernet) # Cria o objeto responsável por criptografar e descriptografar.
    return objetoFernet # Devolve o objeto Fernet para quem chamou a função.

objetoFernet = gerar_chave(senha_mestre, salt)

# EXPLICAR NO NOTION -> COMO FUNCIONA A FUNÇÃO CRIPTOGRAFAR

def criptografar(mensagem, objetoFernet):

    mensagem_bytes = mensagem.encode()
    mensagem_criptografada = objetoFernet.encrypt(mensagem_bytes)
    return mensagem_criptografada

mensagem = "receba"

resultado = criptografar(mensagem, objetoFernet)

# EXPLICAR NO NOTION -> COMO FUNCIONA A FUNÇÃO CRIPTOGRAFAR

def descriptografar(resultado, objetoFernet):

    mensagem_descriptografada = objetoFernet.decrypt(resultado)
    mensagem_texto = mensagem_descriptografada.decode()
    return mensagem_texto

mensagem_original = descriptografar(resultado, objetoFernet)
print(mensagem_original)