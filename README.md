![Python](https://img.shields.io/badge/Python-3.12.*-blue.svg)
![Django](https://img.shields.io/badge/Django-5.1.*-092E20.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-2.8.2-red.svg)

# NoPrep Manager

NoPrep Manager é um sistema de gestão de eventos construído com Django, destinado a gerenciar inscrições de pilotos em eventos. O projeto está configurado para rodar em um ambiente Dockerizado com PostgreSQL como banco de dados, e utiliza o Poetry para gerenciamento de dependências.

## Tecnologias Utilizadas

- **Python 3.12** como linguagem de programação
- **Django 5.1** como framework web
- **PostgreSQL** como banco de dados
- **Poetry** para gerenciamento de dependências
- **Docker** e **Docker Compose** para containerização
- **Pytest** para testes unitários
- **Black** e **Ruff** para linting e formatação

## Preparando o Ambiente

### Pré-requisitos

Certifique-se de ter os seguintes softwares instalados:

- **Docker**: Para rodar o banco de dados e serviços relacionados.
- **Docker Compose**: Para orquestrar os containers.
- **Python 3.12**: Para rodar o projeto Django.
- **Poetry**: Para gerenciamento de dependências.

### Passos para Configuração

## 1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/noprep-manager.git
cd noprep-manager
```
## 2. Prepare o Ambiente

### 2.1 Verificar a Versão do Python

Primeiro, verifique se você já tem o Python 3.12 instalado no seu sistema. Abra o terminal e execute o seguinte comando:

```bash
python3 --version
```
ou
```bash
python --version
```
Você deve ver algo como:

```bash
Python 3.12.x
```

Se a versão exibida não for a 3.12.x, você precisará instalar a versão correta do Python usando pyenv.

### 2.2 Verificar se o pyenv está Instalado
O pyenv é uma ferramenta para gerenciar várias versões do Python no seu sistema. Para verificar se o pyenv está instalado, execute:

```bash
pyenv --version
```
Você deve ver algo como:

```bash
pyenv 2.x.x
```

### 2.3 Instalar o Pyenv (Caso não esteja instalado)
Se o pyenv não estiver instalado, siga os passos abaixo para instalá-lo:

Instale as dependências necessárias:
#### No macOS:
```bash
brew install openssl readline sqlite3 xz zlib
```

#### No Ubuntu/Debian:
```bash
sudo apt-get update &&
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev \
python-openssl git
```
Instale o pyenv usando o curl:
```bash
curl https://pyenv.run | bash
```

Adicione as seguintes linhas ao seu arquivo de configuração do shell (~/.bashrc, ~/.zshrc, etc.):

```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
Então, reinicie o seu terminal ou execute:
```bash
source ~/.bashrc  # ou source ~/.zshrc para usuários do Zsh
```

### 2.4 Instale o Python 3.12
Agora, você pode instalar o Python 3.12 usando o pyenv:
```bash
pyenv install 3.12.4
```

### 2.5 Definir a Versão do Python 3.12
Defina a versão do Python 3.12 como local no seu sistema:
```bash
pyenv local 3.12.4
```
## 3. Iniciando o Projeto

Depois de preparar o ambiente, você pode iniciar o projeto com um único comando que cuidará de todas as etapas necessárias.

### 3.1 Inicializar o Projeto

Para configurar e iniciar o projeto, execute:

```bash
make init
```
Este comando fará o seguinte:

- Instalar o Poetry: Verifica se o Poetry está instalado no seu sistema. Se não estiver, ele será instalado automaticamente.
- Instalar Dependências: Instala todas as dependências listadas no pyproject.toml, incluindo quaisquer extras configurados.
- Configurar o Ambiente Virtual: Configura o ambiente virtual do Poetry dentro do diretório do projeto.
- Copiar o Arquivo .env: Copia o arquivo .env.example para .env, preparando o ambiente para o desenvolvimento.

#### Atenção: Após a execução deste comando, você precisará editar o arquivo .env para preencher as variáveis de ambiente necessárias para o seu ambiente de desenvolvimento.

Agora que o ambiente está configurado e o projeto foi inicializado, você pode prosseguir com os próximos passos, como aplicar migrações, criar um superusuário, e rodar o servidor de desenvolvimento.


### 4. Criando o Banco de Dados
Após configurar o ambiente, aplique as migrações do Django para iniciar o banco de dados:

```bash
make create-db
```

### 5. Rodando a aplicação
Para rodar a aplicação, execute:

```bash
make run
```
