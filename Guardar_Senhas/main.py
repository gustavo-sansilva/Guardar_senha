from pathlib import Path
from autenticacao import criar_senha_mestre
from criptografia import gerar_chave
from criptografia import criptografar
from criptografia import descriptografar
import secrets

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

senha_mestre = criar_senha_mestre()

if senha_mestre is None:
    print("\n❌ Não foi possível continuar.")
else:
    print("\n✅ Autenticação concluída")

arquivo_salt = pasta_dados / "salt.bin"
arquivo_senhas = pasta_dados / "senhas.bin"

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

site = "Google"
usuario = "Gustavo"
senha = "asdasdasda"
informacoes = site + "|" + usuario + "|" + senha
print("Informações: ", informacoes)

if arquivo_senhas.exists():
    with open (arquivo_senhas, "rb") as arquivo:
        dados = arquivo.read()
        
    print(dados)
    dados_descripto = descriptografar(dados, objetoFernet)
    print(dados_descripto)
else:
    with open(arquivo_senhas, "wb") as arquivo:
        teste_cripto = criptografar(informacoes, objetoFernet)
        arquivo.write(teste_cripto)


mensagem = "aaa"

resultado = criptografar(mensagem, objetoFernet)

mensagem_descriptografada = descriptografar(resultado, objetoFernet)

