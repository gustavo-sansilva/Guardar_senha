from pathlib import Path
from autenticacao import criar_senha_mestre, verificar_senha_mestre
from criptografia import gerar_chave
from criptografia import descriptografar
from criptografia import salvar_senhas
import secrets
import json
import getpass

def adicionar_senha():
    site = input("Digite o site: ")
    usuario = input("Digite o usuario/email: ")
    senha = getpass.getpass("Digite a senha: ")
    confirmar_senha = getpass.getpass("Confirme a senha: ")

    if not site or not usuario or not senha:
        print("As informações não podem ficar vazias")
        return None

    if senha != confirmar_senha:
        print("As senhas não são iguais.")
        return None
    
    return site, usuario, senha

print("=" * 20)
print("  COFRE DE SENHAS  ")
print("=" * 20 )

print("\nInicializando sistema...")

pasta_dados = Path("D:/Guardar_Senhas/Dados")

if pasta_dados.exists() and pasta_dados.is_dir():
    print("\nPasta encontrada")
else:
    pasta_dados.mkdir(exist_ok=True, parents=True)
    print("\nPasta criada")

arquivo_salt = pasta_dados / "salt.bin"
arquivo_senhas = pasta_dados / "senhas.bin"
arquivo_senha_mestre = pasta_dados / "senha_mestre.bin"

if arquivo_senha_mestre.exists():
    with open(arquivo_senha_mestre, "rb") as arquivo:
        dados_mestre = arquivo.read()

    salt_mestre = dados_mestre[:32] # Pega os primeiros 32 bytes do arquivo.
    verificador_salvo = dados_mestre[32:] # Pega do byte 32 até o final.
    
    senha_mestre = verificar_senha_mestre(salt_mestre, verificador_salvo)
else:

    resultado = criar_senha_mestre()

    if resultado is None:
        print('\n❌ Não foi possível continuar.')
        exit()

    senha_mestre, salt_mestre, verificador = resultado
    with open (arquivo_senha_mestre, "wb") as arquivo:
        arquivo.write(salt_mestre)
        arquivo.write(verificador)

if senha_mestre is None:
    print("\n❌ Não foi possível continuar.")
    exit()
else:
    print("\n✅ Autenticação concluída")

# Anotar como isso daqui funciona = Verificação se o arquivo do salt existe

if arquivo_salt.exists():
    with open(arquivo_salt, "rb") as arquivo:
        salt = arquivo.read()
else:
    salt = secrets.token_bytes(32)
    with open(arquivo_salt, "wb") as arquivo:
        arquivo.write(salt)

objetoFernet = gerar_chave(senha_mestre, salt)

# Anotar como isso daqui funciona = Verificação se o arquivo de senha existe

if arquivo_senhas.exists():
    with open (arquivo_senhas, "rb") as arquivo:
        dados = arquivo.read()
        
    dados_descripto = descriptografar(dados, objetoFernet)
    informacoes = json.loads(dados_descripto)
else:
    informacoes = []

#Bloco de Escolher informações das senhas

while True:

    print("1 - Adicionar senha")
    print("2 - Listar senhas")
    print("3 - Editar senha")
    print("4 - Excluir senha")
    print("5 - Pesquisar senha")
    print("6 - Sair")

    opcao = input("\nDigite uma opção: ")

# Opção 1

    if opcao == "1":
        print("\nVocê escolheu adicionar uma senha")
        resultado = adicionar_senha()

        if resultado is None:
            continue # Retorna para o inicio do Loop 

        site, usuario, senha = resultado

        informacoes.append({
            "site": site,
            "usuario": usuario,
            "senha": senha
        })

        salvar_senhas(informacoes, objetoFernet, arquivo_senhas)

# Opção 2

    elif opcao == "2":
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
                continue

            if escolha >= 1 and escolha <= len(informacoes):
                indice = escolha - 1
                entrada = informacoes[indice]

                print("Site: ", entrada["site"])
                print("Usuario: ", entrada["usuario"])

                confirmar = input("Deseja visualizar a senha? (s/n): ").islower()

                if confirmar == "s":
                    print("Senha: ", entrada["senha"])
                elif confirmar == "n":
                    print("Senha não exibida")
                else:
                    print("Digite apenas S ou N.")

            else:
                print("Número inválido")

# Opção 3

    elif opcao == "3":
        print("\nVocê escolheu editar uma senha")

        if not informacoes:
            print("\nNenhuma senha cadastrada.")
        else:
            for numero, senha in enumerate(informacoes, start=1):
                print(f"\n{numero} - Site:", senha["site"])
                print("Usuario:", senha["usuario"])
                print("-" * 20)

            try:
                escolha = int(input("\nDigite o número da senha que deseja editar: "))
            except ValueError:
                print("Digite apenas um número.")
                continue

            if escolha >= 1 and escolha <= len(informacoes):
                indice = escolha - 1
                entrada = informacoes[indice]

                print("\nSite: ", entrada["site"])
                print("Usuario atual: ", entrada["usuario"])

                novo_usuario = input("Digite o novo usuario/email: ")
                nova_senha = getpass.getpass("Digite a nova senha: ")
                confirmar_senha = getpass.getpass("Confirme a nova senha: ")

                if nova_senha != confirmar_senha:
                    print("As senhas não são iguais.")
                    continue
                else:
                    entrada["usuario"] = novo_usuario
                    entrada["senha"] = nova_senha
                    print("\nSenha alterada com sucesso!")
                    salvar_senhas(informacoes, objetoFernet, arquivo_senhas)
            else:
                print("\nNúmero inválido.")

#Opção 4

    elif opcao == "4":
        print("\nVocê escolheu excluir uma senha")

        if not informacoes:
            print("\nNenhuma senha cadastrada")
        else:
            for numero, senha in enumerate(informacoes, start=1):
                print(f"\n{numero} - Site:", senha["site"])
                print("Usuario:", senha["usuario"])
                print("-" * 20)

            try:
                escolha = int(input("\nDigite o número da senha que deseja excluir: "))
            except ValueError:
                print("Digite apenas um número.")
                continue

            if escolha >= 1 and escolha <= len(informacoes):
                indice = escolha - 1
                entrada = informacoes[indice]

                print("\nSite:", entrada["site"])
                print("Usuario:", entrada["usuario"])

                confirmar = input("\nTem certeza que deseja excluir esta senha? (s/n): ").lower()

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

# Opção 5

    elif opcao == "5":
        print("\nVocê escolheu pesquisar uma senha")

        if not informacoes:
            print("\nNenhuma senha cadastrada")
        else:
            for numero, senha in enumerate(informacoes, start=1):
                print(f"\n{numero} - Site:", senha["site"])
                print("Usuario:", senha["usuario"])
                print("-" * 20)

            site_pesquisa = input("\nDigite o nome do site que deseja pesquisar: ").lower()

            encontrou = False

            for senha in informacoes:
                if senha["site"].lower() == site_pesquisa:
                    encontrou = True
                    print("\nResultados encontrados: ")
                    print("\nSite:", senha["site"])
                    print("Usuario:", senha["usuario"])

            if not encontrou:
                print("\nNenhum site encontrado.")

# Opção 6

    elif opcao == "6":
        print("\nSaindo do cofre...")
        break
    else:
        print("\nValor invalido\n")