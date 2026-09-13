import getpass
import hashlib
import secrets

def gerar_verificador(senha, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode(),
        salt,
        310_000
    )

def criar_senha_mestre():
    senha = getpass.getpass("Digite a senha mestre: ")
    confirmar_senha = getpass.getpass("Confirme a senha: ")

    if senha == confirmar_senha:
        salt = secrets.token_bytes(32)
        verificador = gerar_verificador(senha, salt)
        return senha, salt, verificador
    else:
        return None

def verificar_senha_mestre(salt, verificador_salvo):
    senha = getpass.getpass("Digite a senha mestre: ")
    verificador = gerar_verificador(senha, salt)

    if verificador == verificador_salvo:

        return senha