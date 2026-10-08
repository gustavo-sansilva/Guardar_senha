from pathlib import Path
from autenticacao import inicializar_senha_mestre, alterar_senha_mestre, salvar_senha_mestre
from criptografia import gerar_chave, inicializar_salt, salvar_senhas
from cofre import adicionar_senha, listar_senhas, editar_senha, excluir_senha, pesquisar_senha, carregar_senhas

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

senha_mestre = inicializar_senha_mestre(arquivo_senha_mestre)

if senha_mestre is None:
    print('\n❌ Não foi possível continuar.')
    exit()
else:
    print("\n✅ Autenticação concluída")

salt = inicializar_salt(arquivo_salt)

objetoFernet = gerar_chave(senha_mestre, salt)
informacoes = carregar_senhas(arquivo_senhas, objetoFernet)

#Bloco de Escolher informações das senhas

while True:

    print("1 - Adicionar senha")
    print("2 - Listar senhas")
    print("3 - Editar senha")
    print("4 - Excluir senha")
    print("5 - Pesquisar senha")
    print("6 - Alterar senha mestre")
    print("7 - Sair")

    opcao = input("\nDigite uma opção: ")

# Opção 1

    if opcao == "1":
        print("\nVocê escolheu adicionar uma senha")
        adicionar_senha(informacoes, objetoFernet, arquivo_senhas)

# Opção 2

    elif opcao == "2":
        print("\nVocê escolheu listar as senhas")
        listar_senhas(informacoes)

# Opção 3

    elif opcao == "3":
        print("\nVocê escolheu editar uma senha")
        editar_senha(informacoes, objetoFernet, arquivo_senhas)

#Opção 4

    elif opcao == "4":
        print("\nVocê escolheu excluir uma senha")
        excluir_senha(informacoes, objetoFernet, arquivo_senhas)
        
# Opção 5

    elif opcao == "5":
        print("\nVocê escolheu pesquisar uma senha")
        pesquisar_senha(informacoes)

# Opção 6

    elif opcao == "6":
        print("\nVocê escolheu alterar a senha mestre")

        resultado = alterar_senha_mestre(arquivo_senha_mestre)

        if resultado is not None:
            nova_senha, salt_novo, verificador_novo = resultado
            objetoFernet = gerar_chave(nova_senha, salt)

            try:
                salvar_senhas(informacoes, objetoFernet, arquivo_senhas)
            except:
                print("\nErro ao salvar o cofre.")
            else:
                salvar_senha_mestre(arquivo_senha_mestre, salt_novo, verificador_novo)
                senha_mestre = nova_senha

# Opção 7

    elif opcao == "7":
        print("\nSaindo do cofre...")
        break
    else:
        print("\nValor invalido\n")