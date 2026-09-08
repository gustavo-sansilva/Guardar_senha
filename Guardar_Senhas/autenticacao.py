import getpass

def criar_senha_mestre():
    senha = getpass.getpass("Digite a senha mestre: ")
    confirmar_senha = getpass.getpass("Confirme a senha: ")

    if senha == confirmar_senha:
        return senha
    else:
        return None

def verificar_senha_mestre():
    senha = getpass.getpass("Digite a senha mestre: ")
    return senha