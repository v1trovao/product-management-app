
## Visão Geral

Aplicação web para gerenciamento de produtos, que oferece um painel administrativo, autenticação de usuários e controle de acesso.

O projeto foi desenvolvido com Flask, Jinja2 e SQLAlchemy, como parte do estudo em desenvolvimento de aplicações web no backend.

## Funcionalidades
- Interface completa com as operações CRUD para produtos e usuários do sistema, integrado a um banco de dados.
- Painel Administrativo com informações atualizadas sobre o sistema, e histórico de movimentações dos produtos
- Autenticação de usuários cadastrados no sistema, com níveis de acesso para cada tipo de usuário

## Tecnologias Usadas
- **Flask** - Framework para desenvolvimento da aplicação
- **SQLAlchemy** - ORM para modelagem e interação com o banco de dados
- **MySQL**: Banco de dados usado no desenvolvimento
- **Jinja2**: Engine usado no Flask para servir as páginas na interface do usuário
- **Bootstrap 5**: Framework CSS para construção de interfaces
- **JWT**: Uso do módulo PyJWT que faz a autenticação dos usuário através de tokens de acesso

## Como executar 

1. Clone o repositório do projeto

```
git clone https://github.com/v1trovao/product-management-app.git
```

2. Navegue até o diretório do projeto

```
cd product-management-app
```

3. Inicie um ambiente virtual

```
python -m venv .venv
```

4. Ative o ambiente virtual (de acordo com seu Sistema Operacional)
```
# Exemplo com Windows CMD
.venv\Scripts\activate
```

5. Instale as dependências
```
pip install -r "requirements.txt"
```

6. Preencha o arquivo .env com os dados necessários
```
# Configs do ambiente Flask - Debug Ativo
FLASK_ENV=development 
CSRF_ENABLED=True
SECRET=your-secret-key

# Conexão com banco MySQL
USER=your-username
PASSWORD=your-password
HOST=your-host
PORT=3306
DATABASE=product-management-app
DATABASE_URL=mysql+pymysql://${USER}:${PASSWORD}@${HOST}:${PORT}/${DATABASE}
```

7. Execute o comando para carregar o banco de dados
```
flask db upgrade
```

8. Execute a aplicação local
```
python run.py
```

## Estrutura do Projeto

```
/admin                # Views do Usuário e Admin
/app              
  controller/         # Lógica do app
  extensions/         # Inicialização de módulos do Flask
  model/              # Modelo de Dados
  static/             # Arquivos estáticos da página
  templates/          # Estrutura das páginas (Jinja2)
  config.py           # Ambiente de configuração do app
/migrations           # Scripts e histórico para conexão no DB
requirements.txt      # Dependências
run.py                # Script de execução do app
.env
.README.md
```