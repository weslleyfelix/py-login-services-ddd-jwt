# **Login API com JWT e Flask**

## Índice


- [Visão Geral](#visão-geral)
- [Estrutura de Diretórios](#estrutura-de-diretórios)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
  - [Pré-requisitos](#pré-requisitos)
  - [Passos para Instalação](#passos-para-instalação)
- [Rotas da API](#rotas-da-api)
  - [/auth/login (POST)](#1-authlogin-post)
  - [/auth/protected (GET)](#2-authprotected-get)
  - [CRUD Usuários](#crud-usuários)
    - [GET /usuarios](#get-usuarios)
    - [POST /usuarios](#post-usuarios)
    - [PUT /usuarios/{id}](#put-usuariosid)
    - [DELETE /usuarios/{id}](#delete-usuariosid)
  - [CRUD Perfis](#crud-perfis)
    - [GET /perfis](#get-perfis)
    - [POST /perfis](#post-perfis)
    - [PUT /perfis/{id}](#put-perfisid)
    - [DELETE /perfis/{id}](#delete-perfisid)
  - [CRUD Permissões](#crud-permissões)
    - [GET /permissoes](#get-permissoes)
    - [POST /permissoes](#post-permissoes)
    - [PUT /permissoes/{id}](#put-permissoesid)
    - [DELETE /permissoes/{id}](#delete-permissoesid)
- [Códigos de Resposta](#códigos-de-resposta)

  
## **Visão Geral**

Esta API fornece autenticação de usuário via JWT (JSON Web Token), utilizando o framework Flask. A autenticação é realizada com base em um arquivo JSON que contém os usuários e senhas.


  
### **Estrutura de Diretórios**

 ```bash
├── application/             
│   ├── __init__.py          # Inicialização da aplicação Flask e configuração dos Blueprints.
│   ├── routes/              # Pasta contendo os arquivos de rotas.
│   │   ├── __init__.py      # Inicialização das rotas.
│   │   ├── auth_routes.py   # Rotas relacionadas à autenticação.
│   │   ├── user_routes.py   # Rotas relacionadas a usuários.
│   │   ├── profile_routes.py # Rotas relacionadas a perfis.
│   │   └── permission_routes.py # Rotas relacionadas a permissões.
├── config/                  
│   └── config.py            # Configurações globais da aplicação usando variáveis de ambiente.
├── domain/                  
│   └── authentication.py    # Lógica de autenticação e geração de tokens JWT.
├── infrastructure/          
│   ├── base_repository.py   # Interface para os repositórios.
│   ├── permission_repository.py # Lógica de acesso a dados de permissões.
│   ├── profile_repository.py    # Lógica de acesso a dados de perfis.
│   └── user_repository.py       # Lógica de acesso a dados de usuários.
├── data/                    
│   └── perfis.json          # Dados de perfis.
│   └── permissoes.json      # Dados de permissões.
│   └── usuarios.json        # Dados de usuários.
├── run.py                   # Script que inicia a aplicação Flask.
├── requirements.txt         # Dependências do projeto.
└── README.md                # Documentação do projeto.
 ```


### **Tecnologias Utilizadas**

- **Python 3.9+**
- **Flask**
- **JWT (PyJWT)**

---
## **Instalação**

### **Pré-requisitos**
- Python 3.9+
- Virtualenv (opcional, mas recomendado)

### **Passos para Instalação**
1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-repositorio/login-service.git
    ```

2. Navegue até o diretório do projeto:
    ```bash
    cd py-eugenia-rhtalent-login
    ```

3. (Opcional) Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Windows, use: venv\Scripts\activate
    ```

4. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

5. Execute o servidor:
    ```bash
    python run.py
    ```

---
## **Rotas da API**

### **1. /auth/login (POST)**

- **Descrição**: Realiza o login do usuário e retorna um token JWT se as credenciais forem válidas.
- **Endpoint**: `/auth/login`
- **Método**: `POST`
- **Corpo da Requisição**:
  ```json
  {
    "usuario": "string",
    "senha": "string"
  }
  ```

  - **Resposta de Sucesso**:
  ```json
  {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

   - **Códigos de Resposta**:
  ```bash
  200: Sucesso (Token gerado)
  401: Falha de autenticação
  ```

  ### **2. /auth/protected (GET)**

- **Descrição**: Rota protegida que requer um token JWT válido.
- **Endpoint**: `/auth/protected`
- **Método**: `GET`
- **Cabeçalhos**: x-access-token: (Token JWT gerado na rota de login)
  ```bash
    curl -X GET http://127.0.0.1:5000/auth/protected -H "x-access-token: SEU_TOKEN_JWT"
  ```
- **Resposta de Sucesso**: x-access-token: (Token JWT gerado na rota de login)
  ```json
  {
      "email": "email@empresa.com.br",
      "nome": "usuario",
      "perfis": [
          "perfil_01"
      ],
      "regras": [
          "perfil_01_regra_1",
          "perfil_01_regra_2",
          "perfil_01_regra_3"
      ]
  }
  ```
    - **Códigos de Resposta**:
  ```bash
  200: Sucesso (Token gerado)
  403: Falha de autenticação
  ```

### **CRUD Usuários**

#### **GET /usuarios**

- **Descrição:** Retorna a lista de todos os usuários.
- **Endpoint:** `/usuarios`
- **Método:** `GET`
- **Headers:**
  - `x-access-token: seu_token_jwt_aqui`
- **Resposta:**
  ```json
  [
    {
      "id": 1,
      "usuario": "nome.sobrenome",
      "nome": "nome sobrenome",
      "email": "nome.sobrenome@empresa.com.br",
      "perfilId": 1
    },
  ]
  ```

#### ** POST /usuarios**
- **Descrição:** Cria um novo usuário.
- **Endpoint:** `/usuarios`
- **Método:** `POST`
- **Headers:**
  - `x-access-token: seu_token_jwt_aqui`
- **Body:**
  ```json
  {
    "usuario": "nome.sobrenome",
    "nome": "nome sobrenome",
    "email": "nome.sobrenome@empresa.com.br",
    "senha": "senha",
    "perfilId": 2
  }
  ```
- **Resposta:**
  ```json
  {
    "message": "User created successfully!"
  }
  ```

  PUT /usuarios/{id}
Descrição: Atualiza as informações de um usuário existente.
Endpoint: /usuarios/{id}
Método: PUT
Headers:
x-access-token: seu_token_jwt_aqui
Body:
json
Copiar código
{
  "nome": "Usuario Atualizado",
  "email": "usuario.atualizado@empresa.com.br"
}
Resposta:
json
Copiar código
{
  "message": "User updated successfully!"
}
DELETE /usuarios/{id}
Descrição: Deleta um usuário existente.
Endpoint: /usuarios/{id}
Método: DELETE
Headers:
x-access-token: seu_token_jwt_aqui
Resposta:
json
Copiar código
{
  "message": "User deleted successfully!"
}
perl
Copiar código

### Parte 4: Rotas da API - CRUD Perfis e Permissões

```markdown
### **CRUD Perfis**

#### **GET /perfis**

- **Descrição:** Retorna a lista de todos os perfis.
- **Endpoint:** `/perfis`
- **Método:** `GET`
- **Headers:**
  - `x-access-token: seu_token_jwt_aqui`
- **Resposta:**
  ```json
  [
    {
      "id": 1,
      "perfil": "gerencial",
      "descricao": "Perfil destinado aos gestores da ferramenta"
    },
    ...
  ]
  
POST /perfis
Descrição: Cria um novo perfil.
Endpoint: /perfis
Método: POST
Headers:
x-access-token: seu_token_jwt_aqui
Body:
json

{
  "perfil": "novo_perfil",
  "descricao": "Descrição do novo perfil"
}
Resposta:
json

{
  "message": "Profile created successfully!"
}
PUT /perfis/{id}
Descrição: Atualiza as informações de um perfil existente.
Endpoint: /perfis/{id}
Método: PUT
Headers:
x-access-token: seu_token_jwt_aqui
Body:
json

{
  "perfil": "perfil_atualizado",
  "descricao": "Descrição atualizada"
}
Resposta:
json

{
  "message": "Profile updated successfully!"
}
DELETE /perfis/{id}
Descrição: Deleta um perfil existente.
Endpoint: /perfis/{id}
Método: DELETE
Headers:
x-access-token: seu_token_jwt_aqui
Resposta:
json

{
  "message": "Profile deleted successfully!"
}
CRUD Permissões
GET /permissoes
Descrição: Retorna a lista de todas as permissões.
Endpoint: /permissoes
Método: GET
Headers:
x-access-token: seu_token_jwt_aqui
Resposta:
json

[
  {
    "id": 1,
    "permissaoPaiId": 1,
    "permissao": "gerencial_admin",
    "descricao": "Acesso irrestrito a todas as funcionalidades",
    "perfilId": 1
  },
  ...
]
POST /permissoes
Descrição: Cria uma nova permissão.
Endpoint: /permissoes
Método: POST
Headers:
x-access-token: seu_token_jwt_aqui
Body:
json

{
  "permissaoPaiId": 2,
  "permissao": "nova_permissao",
  "descricao": "Descrição da nova permissão",
  "perfilId": 2
}
Resposta:
json

{
  "message": "Permission created successfully!"
}
PUT /permissoes/{id}
Descrição: Atualiza as informações de uma permissão existente.
Endpoint: /permissoes/{id}
Método: PUT
Headers:
x-access-token: seu_token_jwt_aqui
Body:
json
{
  "permissao": "permissao_atualizada",
  "descricao": "Descrição atualizada"
}
Resposta:
json

{
  "message": "Permission updated successfully!"
}
DELETE /permissoes/{id}
Descrição: Deleta uma permissão existente.
Endpoint: /permissoes/{id}
Método: DELETE
Headers:
x-access-token: seu_token_jwt_aqui
Resposta:
json

{
  "message": "Permission deleted successfully!"
}

Códigos de Resposta
Aqui estão os códigos de resposta comuns usados na API:

200: Sucesso
201: Criado com sucesso
400: Requisição inválida
401: Não autorizado (Credenciais inválidas)
403: Proibido (Permissões insuficientes)
404: Não encontrado
500: Erro interno do servidor
