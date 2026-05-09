# ✂ Shorty

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-19-blue)
![Coverage](https://img.shields.io/badge/Coverage-99%25-brightgreen)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

Encurtador de URLs fullstack com autenticação JWT, painel de gerenciamento e redirecionamento automático.

---

# 🚀 Stack

## Backend

* Python 3.12
* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT Authentication (Bearer Token)
* Pytest
* Pydantic v2

## Frontend

* React 19
* TypeScript
* Tailwind CSS v4
* Vite

## Infra

* Docker
* Docker Compose

---

# ✨ Funcionalidades

## 🔐 Autenticação

* Cadastro e login de usuários
* JWT Authentication
* Access Token + Refresh Token
* Logout com revogação de token
* Validação e expiração automática de JWTs
* Rotas protegidas com autenticação

## 🔗 URLs

* Criação de URLs encurtadas
* Geração automática de short keys
* Redirecionamento automático
* Listagem de URLs do usuário
* Atualização de URLs
* Remoção de URLs
* Controle de URLs ativas/inativas
* Contador de cliques por URL
* Isolamento por usuário (ownership)

## ✅ Qualidade

* 34 testes automatizados com Pytest
* Cobertura de 99%
* Fixtures reutilizáveis
* Banco isolado para testes
* Arquitetura em camadas
* Validação tipada com Pydantic v2

---

# 🧱 Arquitetura

O backend segue arquitetura em camadas:

```txt
Router → Service → Repository
```

Separando:

* regras de negócio
* acesso ao banco
* autenticação
* validações
* serialização
* persistência

---

# 📦 Pré-requisitos

* Docker
* Docker Compose

---

# ▶️ Como rodar

## 🐳 Docker (recomendado)

Clone o projeto:

```bash
git clone https://github.com/LuizZorzenon/Shorty.git
cd Shorty
```

Crie o `.env`:

```bash
cp .env.example .env
```

Suba os containers:

```bash
docker compose up --build
```

Acesse:

* Frontend: http://localhost:5173
* Backend: http://localhost:8000
* Swagger: http://localhost:8000/docs

---

# 💻 Desenvolvimento local

## Backend

Crie o ambiente virtual:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o `.env`:

```env
DATABASE_URL=postgresql://admin:admin@localhost:5432/shorty
DATABASE_URL_TEST=postgresql://admin:admin@localhost:5432/shorty_test
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
```

Suba apenas o banco:

```bash
docker compose up db -d
```

Execute a API:

```bash
uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd front
npm install
npm run dev
```

Crie o `.env` em `front/`:

```env
VITE_API_URL=http://localhost:8000
```

---

# 🧪 Testes

Execute todos os testes:

```bash
pytest tests/
```

Cobertura atual: **99% (34 testes)**

Cenários cobertos:

* Autenticação e autorização
* Refresh token e logout
* Token expirado, inválido e sem campos obrigatórios
* Ownership e isolamento entre usuários
* CRUD completo de URLs
* Redirecionamento e URLs desabilitadas
* Click tracking

---

# 📁 Estrutura do projeto

```txt
Shorty/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── repository/
│   ├── schema/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── tests/
│   ├── fixtures/
│   │   ├── db_fixtures.py
│   │   ├── auth_fixtures.py
│   │   └── url_fixtures.py
│   ├── test_auth.py
│   ├── test_url.py
│   ├── test_health.py
│   ├── test_redirect.py
│   └── conftest.py
│
├── front/
│   └── src/
│
├── docker/
│   └── init.sql
│
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

# 📚 API

Swagger disponível em:

```txt
/docs
```

| Método | Rota               | Descrição                           | Auth |
| ------ | ------------------ | ----------------------------------- | ---- |
| GET    | `/health`          | Health check                        | —    |
| POST   | `/auth/register`   | Cadastro de usuário                 | —    |
| POST   | `/auth/login`      | Login                               | —    |
| POST   | `/auth/refresh`    | Renovação do access token           | —    |
| POST   | `/auth/logout`     | Logout e revogação do refresh token | ✓    |
| GET    | `/users/me`        | Usuário autenticado                 | ✓    |
| GET    | `/urls/`           | Lista URLs do usuário               | ✓    |
| POST   | `/urls/`           | Cria URL encurtada                  | ✓    |
| GET    | `/urls/{shortkey}` | Busca URL                           | ✓    |
| PATCH  | `/urls/{shortkey}` | Atualiza URL                        | ✓    |
| DELETE | `/urls/{shortkey}` | Remove URL                          | ✓    |
| GET    | `/{short_key}`     | Redirect para URL original          | —    |

---

# 🛣️ Roadmap

* [ ] Redis cache
* [ ] Kafka analytics
* [ ] QRCode generation
* [ ] Rate limiting
* [ ] CI/CD pipeline
* [ ] URL expiration
* [ ] Observability
* [ ] Background workers
