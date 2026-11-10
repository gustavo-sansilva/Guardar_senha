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

def carregar_senha_mestre(arquivo_senha_mestre):
    with open(arquivo_senha_mestre, "rb") as arquivo:
        dados_mestre = arquivo.read()

    salt_mestre = dados_mestre[:32] # Pega os primeiros 32 bytes do arquivo.
    verificador_salvo = dados_mestre[32:] # Pega do byte 32 até o final.
    
    return salt_mestre, verificador_salvo

def salvar_senha_mestre(arquivo_senha_mestre, salt_mestre, verificador):

    with open(arquivo_senha_mestre, "wb") as arquivo:
        arquivo.write(salt_mestre)
        arquivo.write(verificador)

def inicializar_senha_mestre(arquivo_senha_mestre):

    if arquivo_senha_mestre.exists():
        salt_mestre, verificador_salvo = carregar_senha_mestre(arquivo_senha_mestre)
        senha_mestre = verificar_senha_mestre(salt_mestre, verificador_salvo)

    else:
        resultado = criar_senha_mestre()

        if resultado is None:
            return None

        senha_mestre, salt_mestre, verificador = resultado
        salvar_senha_mestre(arquivo_senha_mestre, salt_mestre, verificador)

    return senha_mestre

def alterar_senha_mestre(arquivo_senha_mestre):
    salt_mestre, verificador_salvo = carregar_senha_mestre(arquivo_senha_mestre)

    senha_atual = verificar_senha_mestre(salt_mestre, verificador_salvo)

    if senha_atual is None:
        print("\nSenha mestre incorreta.")
        return

    nova_senha = getpass.getpass("Digite a nova senha mestre: ")
    confirmar_nova_senha = getpass.getpass("Confirme a nova senha mestre: ")

    if nova_senha != confirmar_nova_senha:
        print("\nAs novas senhas não são iguais.")
        return

    salt_novo = secrets.token_bytes(32)
    verificador_novo = gerar_verificador(nova_senha, salt_novo)

    return nova_senha, salt_novo, verificador_novo