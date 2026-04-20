# ✂ Shorty

Encurtador de URLs fullstack com autenticação JWT, painel de gerenciamento e redirecionamento automático.

## Stack

**Backend** — Python 3.12, FastAPI, SQLAlchemy, PostgreSQL, JWT (access + refresh token)  
**Frontend** — React 19, TypeScript, Tailwind CSS v4, Vite  
**Infra** — Docker, Docker Compose

---

## Funcionalidades

- Cadastro e login de usuários
- Criação de URLs encurtadas com chave aleatória
- Redirecionamento automático via short key
- Listagem, edição e remoção de URLs
- Controle de URLs ativas/inativas
- Contador de cliques por URL
- Autenticação com access token + refresh token
- Logout com revogação de token

---

## Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose instalados

---

## Como rodar

### Com Docker (recomendado)

1. Clone o repositório:
```bash
git clone https://github.com/LuizZorzenon/Shorty.git
cd Shorty
```

2. Crie o arquivo `.env` na raiz do projeto:
```bash
cp .env.example .env
```

3. Suba os serviços:
```bash
docker compose up --build
```

Acesse:
- Frontend: http://localhost:5173
- Backend (docs): http://localhost:8000/docs

---

### Sem Docker (desenvolvimento local)

**Backend:**
```bash
cd Shorty
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Crie o `.env` na raiz:
```env
DATABASE_URL=postgresql://admin:admin@localhost:5432/shorty
SECRET_KEY=sua_chave_secreta_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30
```

Suba o banco com Docker:
```bash
docker compose up db -d
```

Inicie o servidor:
```bash
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd front
npm install
```

Crie o `.env` em `front/`:
```env
VITE_API_URL=http://localhost:8000
```

Inicie o servidor de desenvolvimento:
```bash
npm run dev
```

---

## Variáveis de ambiente

### Backend (`.env` na raiz)

| Variável | Descrição | Exemplo |
|---|---|---|
| `DATABASE_URL` | String de conexão com o PostgreSQL | `postgresql://admin:admin@db:5432/shorty` |
| `SECRET_KEY` | Chave secreta para assinar os JWTs | `uma_chave_longa_e_aleatoria` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do access token | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Tempo de expiração do refresh token | `30` |

### Frontend (`.env` em `front/`)

| Variável | Descrição | Exemplo |
|---|---|---|
| `VITE_API_URL` | URL base da API | `http://localhost:8000` |

---

## Estrutura do projeto

```
Shorty/
├── app/
│   ├── api/           # Routers (auth, urls, redirect)
│   ├── core/          # Configurações, banco, segurança, deps
│   ├── models/        # Modelos SQLAlchemy
│   ├── repository/    # Acesso ao banco de dados
│   ├── schema/        # Schemas Pydantic (request/response)
│   ├── services/      # Regras de negócio
│   ├── utils/         # Utilitários (geração de short key)
│   └── main.py
├── front/
│   └── src/
│       ├── components/ # Navbar, UrlForm, UrlTable, etc.
│       ├── pages/      # Dashboard, Login, Register
│       ├── services/   # Camada de comunicação com a API
│       └── types/      # Tipos TypeScript compartilhados
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## API

A documentação interativa completa está disponível em `/docs` (Swagger) após subir o backend.

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `POST` | `/auth/register` | Cadastro de usuário | — |
| `POST` | `/auth/login` | Login, retorna tokens | — |
| `POST` | `/auth/refresh` | Renova o access token | — |
| `POST` | `/auth/logout` | Revoga o refresh token | — |
| `GET` | `/urls/` | Lista URLs do usuário | ✓ |
| `POST` | `/urls/` | Cria nova URL encurtada | ✓ |
| `GET` | `/urls/{shortkey}` | Busca URL por short key | ✓ |
| `PATCH` | `/urls/{shortkey}` | Atualiza URL | ✓ |
| `DELETE` | `/urls/{shortkey}` | Remove URL | ✓ |
| `GET` | `/{short_key}` | Redireciona para a URL original | — |