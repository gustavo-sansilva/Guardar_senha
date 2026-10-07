from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import json
import secrets

# EXPLICAR NO NOTION -> PARAMETROS DO KDF

length = 32 # 32 bytes para a chave / Define o tamanho da chave derivada em bytes.
algoritmo = hashes.SHA256() # Define o SHA-256 como algoritmo de hash do PBKDF2.
iterations = 310_000 # Define quantas vezes o PBKDF2 repete o processo de derivação.

# EXPLICAR NO NOTION -> COMO FUNCIONA A FUNÇÃO GERAR_CHAVE

def gerar_chave(senha_mestre, salt): # explicar os parametros da função

    kdf = PBKDF2HMAC(algoritmo, length, salt, iterations) # Cria o mecanismo PBKDF2 com os parâmetros definidos.

    chave_derivada = kdf.derive(senha_mestre.encode()) # Converte a senha para bytes e gera uma chave derivada.

    chave_fernet = base64.urlsafe_b64encode(chave_derivada) # Converte a chave derivada para o formato aceito pelo Fernet.
    objetoFernet = Fernet(chave_fernet) # Cria o objeto responsável por criptografar e descriptografar.
    return objetoFernet # Devolve o objeto Fernet para quem chamou a função.


# EXPLICAR NO NOTION -> COMO FUNCIONA A FUNÇÃO CRIPTOGRAFAR

def criptografar(mensagem, objetoFernet):

    mensagem_bytes = mensagem.encode()
    mensagem_criptografada = objetoFernet.encrypt(mensagem_bytes)
    return mensagem_criptografada

# EXPLICAR NO NOTION -> COMO FUNCIONA A FUNÇÃO CRIPTOGRAFAR

def descriptografar(resultado, objetoFernet):

    mensagem_descriptografada = objetoFernet.decrypt(resultado)
    mensagem_texto = mensagem_descriptografada.decode()
    return mensagem_texto

# EXPLICAR NO NOTION -> COMO FUNCIONA A FUNÇÃO SALVAR SENHAS

def salvar_senhas(informacoes, objetoFernet, arquivo_senhas):
    informacoes_json = json.dumps(informacoes)
    dados_criptografados = criptografar(informacoes_json, objetoFernet)

    with open(arquivo_senhas, "wb") as arquivo:
        arquivo.write(dados_criptografados)

    print("Senha salva com sucesso")

# CARREGAR SALT

def carregar_salt(arquivo_salt):

    with open(arquivo_salt, "rb") as arquivo:
        salt = arquivo.read()

    return salt

def salvar_salt(arquivo_salt, salt):

    with open(arquivo_salt, "wb") as arquivo:
        arquivo.write(salt)

def inicializar_salt(arquivo_salt):

    if arquivo_salt.exists():
        salt = carregar_salt(arquivo_salt)

    else:
        salt = secrets.token_bytes(32)
        salvar_salt(arquivo_salt, salt)
    return salt