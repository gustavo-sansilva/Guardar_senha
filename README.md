# Cofre de Senhas

Um cofre de senhas desenvolvido em Python para armazenar e gerenciar credenciais de forma local e criptografada.

O projeto foi desenvolvido com foco em aprendizado de Python, organização de código em módulos e conceitos básicos de segurança da informação.

## Funcionalidades

-  Criação e autenticação com senha mestre
-  Alteração da senha mestre
-  Adição de novas credenciais
-  Listagem das credenciais armazenadas
-  Edição de credenciais
-  Exclusão de credenciais
-  Pesquisa de credenciais por site
-  Criptografia dos dados armazenados
-  Armazenamento local dos dados

## Tecnologias utilizadas

- Python
- `cryptography`
- `hashlib`
- `secrets`
- `getpass`
- `json`
- `pathlib`

## Segurança

A senha mestre não é armazenada diretamente.

O projeto utiliza:

- **PBKDF2-HMAC com SHA-256** para derivação de verificadores e chaves;
- **Salt** para evitar que a mesma senha gere sempre o mesmo resultado;
- **Fernet** para criptografia dos dados do cofre;
- Arquivos binários para armazenamento dos dados criptografados.

O arquivo que contém as senhas armazenadas é mantido criptografado.

> Este projeto foi desenvolvido principalmente para fins de aprendizado e uso pessoal. Ele não deve ser considerado uma solução de segurança profissional ou um substituto para gerenciadores de senhas auditados.

## Estrutura do projeto

```text
Cofre-de-Senhas/
│
├── main.py
├── autenticacao.py
├── criptografia.py
├── cofre.py
├── LICENSE
├── README.md
└── .gitignore
