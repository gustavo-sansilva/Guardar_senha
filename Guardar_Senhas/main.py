from pathlib import Path
from autenticacao import criar_senha_mestre

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

if arquivo_salt.exists():
    print("Arquivo existe")
else:
    print("Arquivo inexistente")

    