from pathlib import Path
from autenticacao import criar_senha_mestre, verificar_senha_mestre
from criptografia import gerar_chave
from criptografia import descriptografar
from criptografia import salvar_senhas
import secrets
import json

def adicionar_senha():
    site = input("Digite o site: ")
    usuario = input("Digite o usuario/email: ")
    senha = input("Digite a senha: ")
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
    senha_mestre = verificar_senha_mestre()
else:
    senha_mestre = criar_senha_mestre()


if senha_mestre is None:
    print("\n❌ Não foi possível continuar.")
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

print("1 - Adicionar senha")
print("2 - Listar senhas")
print("3 - Sair")

opcao = input("\nDigite uma opção: ")

if opcao == "1":
    print("\nVocê escolheu adicionar uma senha")
    site, usuario, senha = adicionar_senha()

    informacoes.append({
        "site": site,
        "usuario": usuario,
        "senha": senha
    })

    salvar_senhas(informacoes, objetoFernet, arquivo_senhas)
elif opcao == "2":
    for senha in informacoes:
        print("\nSite:", senha['site'])
        print("Usuario: ", senha['usuario'])
        print("Senha: ", senha['senha'])
        print("-" * 20)
elif opcao == "3":
    print("\nSaindo do cofre...")