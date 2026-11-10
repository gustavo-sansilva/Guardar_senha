import getpass
import json
from criptografia import salvar_senhas
from criptografia import descriptografar

# CARREGA AS INFORMAÇÕES

def carregar_senhas(arquivo_senhas, objetoFernet):

    if arquivo_senhas.exists():
        with open(arquivo_senhas, "rb") as arquivo:
            dados = arquivo.read()

        dados_descripto = descriptografar(dados, objetoFernet)
        informacoes = json.loads(dados_descripto)

        return informacoes

    else:
        return []

# ADICIONAR

def adicionar_senha(informacoes, objetoFernet, arquivo_senhas):

    site = input("\nDigite o site: ")
    usuario = input("\nDigite o usuario/email: ")
    senha = getpass.getpass("Digite a senha: ")
    confirmar_senha = getpass.getpass("Confirme a senha: ")

    if not site or not usuario or not senha:
        print("\nAs informações não podem ficar vazias")
        return None

    if senha != confirmar_senha:
        print("\nAs senhas não são iguais.")
        return None

    informacoes.append({
        "site": site,
        "usuario": usuario,
        "senha": senha
    })

    salvar_senhas(informacoes, objetoFernet, arquivo_senhas)

# LISTAR

def listar_senhas(informacoes):
    if not informacoes:
        print('\nNenhuma Senha cadastrada.')
    else:
        for numero, senha in enumerate(informacoes, start=1):
            print(f"\n{numero} - Site:", senha['site'])
            print("Usuario: ", senha['usuario'])
            print("-" * 20)
        try:
            escolha = int(input("\nDigite o número da senha que deseja visualizar: "))
        except ValueError:
            print("Digite apenas um número.")
            return

        if escolha >= 1 and escolha <= len(informacoes):
            indice = escolha - 1
            entrada = informacoes[indice]

            print("\nSite: ", entrada["site"])
            print("Usuario: ", entrada["usuario"])

            confirmar = input("\nDeseja visualizar a senha? (s/n): ").lower()

            if confirmar == "s":
                print("\nSenha: ", entrada["senha"])
            elif confirmar == "n":
                print("\nSenha não exibida")
            else:
                print("\nDigite apenas S ou N.")

        else:
            print("\nNúmero inválido")

# EDITAR

def editar_senha(informacoes, objetoFernet, arquivo_senhas):

    if not informacoes:
        print("\nNenhuma senha cadastrada.")
        return

    for numero, senha in enumerate(informacoes, start=1):
        print(f"\n{numero} - Site:", senha["site"])
        print("Usuario:", senha["usuario"])
        print("-" * 20)

    try:
        escolha = int(input("\nDigite o número da senha que deseja editar: "))
    except ValueError:
        print("\nDigite apenas um número.")
        return

    if escolha >= 1 and escolha <= len(informacoes):
        indice = escolha - 1
        entrada = informacoes[indice]

        print("\nSite:", entrada["site"])
        print("Usuario atual:", entrada["usuario"])

        novo_usuario = input("\nDigite o novo usuario/email: ")
        nova_senha = getpass.getpass("Digite a nova senha: ")
        confirmar_senha = getpass.getpass("Confirme a nova senha: ")

        if nova_senha != confirmar_senha:
            print("\nAs senhas não são iguais.")
            return
        else:
            entrada["usuario"] = novo_usuario
            entrada["senha"] = nova_senha

            print("\nSenha alterada com sucesso!")
            salvar_senhas(informacoes, objetoFernet, arquivo_senhas)
    else:
        print("\nNúmero inválido.")

# EXCLUIR

def excluir_senha(informacoes, objetoFernet, arquivo_senhas):

    if not informacoes:
        print("\nNenhuma senha cadastrada")
        return

    for numero, senha in enumerate(informacoes, start=1):
        print(f"\n{numero} - Site:", senha["site"])
        print("Usuario:", senha["usuario"])
        print("-" * 20)

    try:
        escolha = int(input("\nDigite o número da senha que deseja excluir: "))
    except ValueError:
        print("\nDigite apenas um número.")
        return

    if escolha >= 1 and escolha <= len(informacoes):
        indice = escolha - 1
        entrada = informacoes[indice]

        print("\nSite:", entrada["site"])
        print("Usuario:", entrada["usuario"])

        confirmar = input(
            "\nTem certeza que deseja excluir esta senha? (s/n): ").lower()

        if confirmar == "s":
            del informacoes[indice]

            print("\nSenha excluída com sucesso!")

            salvar_senhas(informacoes, objetoFernet, arquivo_senhas)

        elif confirmar == "n":
            print("\nSenha não excluída.")

        else:
            print("\nDigite apenas S ou N.")

    else:
        print("\nNúmero inválido.")

# PESQUISAR

def pesquisar_senha(informacoes):

    if not informacoes:
        print("\nNenhuma senha cadastrada")
        return

    for numero, senha in enumerate(informacoes, start=1):
        print(f"\n{numero} - Site:", senha["site"])
        print("Usuario:", senha["usuario"])
        print("-" * 20)

    site_pesquisa = input(
        "\nDigite o nome do site que deseja pesquisar: ").lower()

    encontrou = False

    for senha in informacoes:
        if senha["site"].lower() == site_pesquisa:
            encontrou = True

            print("\nResultados encontrados:")
            print("\nSite:", senha["site"])
            print("Usuario:", senha["usuario"])

    if not encontrou:
        print("\nNenhum site encontrado.")