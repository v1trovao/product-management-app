### Descrever o contexto da aplicações e os requisitos e casos de uso


Nome do Sistema: Product Management App

versão 0.1

### 1 - Contexto dos testes

Este documento descreve requisitos para testar, tipos de teste definidos em cada iteração, recursos e possíveis cronogramas. As seções permitem acompanhar a evolução atual dos testes 


### 2 - Funcionalidades a serem analisadas do sistema

Produtos 

- Gerenciar produtos (Cadastro, Edição, Remoção, Listagem)
    - model/Product
    - controller/Product
    - __init__.py/save_products()
    - __init__.py/update_products()
    - __init__.py/delete_products()
    - __init__.py/get_products(limit=None)
    - __init__.py/get_product(product_id)
    - admin/Views.py/ProductView

Usuários
- Gerenciar usuários (Cadastro, Edição, Remoção, Listagem)
    - model/User
    - controller/User
    - __init__.py/create_profile()
    - __init__.py/edit_total_profile()
    - __init__.py/get_user_profile()
    - __init__.py/load_user(user_id)
    - admin/Views.py/UserView

- Login e Logout
    - __init__.py/
    - __init__.py/login
    - __init__.py/login_api()
    - __init__.py/logout_send()
    - __init__.py/load_user()
- Recuperação de Senha
    - __init__.py/recovery_password()
    - __init__.py/send_recovery_password()
    - __init__.py/new_password(recovery_code)
    - __init__.py/send_new_password()

Categorias 

- Gerenciar Categorias (Cadastro, Edição, Remoção, Listagem)
    - admin/Views.py/CategoryView

Funções

- Gerenciar Funções (Cadastro, Edição, Remoção, Listagem)
    - admin/Views.py/RoleView

Painel Administrativo
- admin/Admin.py/start_views
- admin/Views.py/HomeView

### 3 - Requisitos

Identificador do requisito   |   Nome do requisito | Detalhes | 
-----------------------------|---------------------|----------|
RF01 | O sistema deve permitir o cadastro de produtos | O produto é cadastrado com nome de usuário, categoria, nome, quantidade, imagem, preço, data de criação, última atualização, status
RF02 | O sistema deve permitir a edição do produto | O usuário pode editar produto em: Categoria, Nome, Descrição, Quantidade, Imagem, Preço, Status
RF03 | O sistema deve permitir a remoção de produto | Cada produto deve ter uma opção de remover dos registros
RF04 | O sistema deve permitir a visualização do produto | O sistema mantém uma visão de tabela mostrando todos os registros de produtos
RF05 | O sistema deve permitir o gerenciamento de categorias | O sistema permite cadastrar, editar, remover e visualizar os campos: nome e descrição
RF06 | O sistema deve permitir cadastro de usuários | O usuário é cadastro com: Função, Nome, E-mail, Senha, Data de Criação, Ativo no Sistema
RF07 | O sistema deve permitir o cadastro de funções dos usuários | Uma função pode ser criada com nome e o nível de acesso no sistema
RF08 | O sistema deve mostrar um painel administrativo | O painel deve mostrar: Mensagem de boas vindas, Qtd de usuários, Qtd de categoria, Qtd de produtos, Ultimas movimentações de produtos
RF09 | O sistema deve permitir o acesso dos usuários por login | Os usuários fazem login por E-mail e Senha
RF10 | O sistema deve permitir que usuários façam logout | Os usuários podem fazer logout por um botão na página
RF11 | O sistema deve permitir que usuário altere a sua senha | Os usuários conseguem recuperar senha via e-mail na página de login, com link de acesso único com a nova senha

### 4 - Objetivos
- Validar as funções essenciais do sistema
- Identificar falhas funcionais e controle de acesso
- Verificar comportamentos e limites
- Verificar rastreabilidade de requisitos e testes
- Tipos de teste: Funcional e Unitários

#### 4.1. Itens a testar

Item | Comportamento
-----|----
Painel administrativo | Exibir qtd de usuários, produtos e categorias, estado vazio 
CRUD de usuários | Criar, consultar, editar e excluir dados de forma consistente
CRUD de produtos | Criar, consultar, editar e excluir dados de forma consistente
Recuperação de senha | Permitir alteração de senha por e-mail
Controle de Acesso | Redicionar usuários nas operações protegidas por nível
Autenticação | Permitir login e logout dos usuários
Sessão | Manter usuário enquanto sessão ser válida


### 5 - Ambiente de teste
Executado local conforme README

- Entrada
    - Pelo menos um usuário válido para autenticação
    - Funções de Admin, Gerente, Lojista e Cliente cadastrados
    - Navegador e console de erros disponível

- Saída
    - Casos classificados como Passou, Falhou e Não executado
    - Defeitos registrados com evidências dos testes realizados, esperado e obtido

Testes unitários executados no pytest seguindo o padrão AAA

### 6 - Técnicas de testes utilizadas
- Partição de equivalência
- Análise de valor limite
- Tabela de decisão


### Formato dos casos de teste

<table>
    <tr>
        <th> ID </th>
        <th colspan="6"> CT01 </th>
    </tr>
    <tr>
        <th> Cenário </th>
        <th colspan="6"> Descrição </th>
    </tr>
    <tr>
        <th> Requisito </th>
        <th colspan="4"> 
            Requisito associado
        <th>
    </tr>
    <tr>
        <th>Critério aplicado</th>
        <th colspan="2"> () P.E </th>
        <th colspan="2"> () V.L </th>
        <th colspan="2"> () T.D </th>
    </tr>
    <tr>
        <th> Pré-condição </th>
        <th colspan="6">
            Condições para executar
        </th>
    </tr>
    <tr>
        <th> Passos </th>
        <th colspan="6"> 1. Descrição passo-a-passo</th>
    </tr>
    <tr>
        <th> Resultados esperados
        </th>
        <th colspan="6"> Descrição da saída
        </th>
    </tr>
    <tr>
        <th> Status </th>
        <th colspan="6"> Executado?
    </tr>
</table>