# Monitor Fiscal AI

Bot de ChatOps que monitora as Notas Técnicas (NTs) dos portais da SEFAZ, analisa o impacto com IA e avisa o time no Discord.

## Funcionalidades

- **Monitoramento de NTs:** scraping de portais nacionais e estaduais (NFe, CTe, NFCe, MDFe). As URLs ficam no banco e são semeadas a partir de `config/links.py` no boot.
- **Saúde das URLs:** após falhas consecutivas a URL é desativada sozinha e reativada quando voltar a responder.
- **Incidentes SEFAZ:** checagem de disponibilidade por UF, com histórico e abertura/resolução automática de incidentes.
- **Análise com IA (Gemini):** lê os PDFs das NTs e extrai as mudanças críticas.
- **Impacto no código:** baixa arquivos do GitHub (ex: NFePHP) para a IA cruzar com a NT.
- **Discord:** comandos `/status` e `/documentos`.
- **API:** `GET /status` informa se o bot está online.

## Stack

Python 3.12 · FastAPI/Uvicorn · discord.py · PostgreSQL (SQLAlchemy async + asyncpg) · Gemini API · BeautifulSoup4/aiohttp · APScheduler

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env-example .env   # preencha as chaves
python main.py
```

Variáveis principais do `.env`: `DATABASE_URL`, `GEMINI_TOKEN`, `GITHUB_TOKEN`, `REPOSITORIO`, `CHANNEL_ID`, `ENVIRONMENT` e o token do Discord.

Com Docker: `docker compose up` (ou `docker-compose.dev.yml` em desenvolvimento).

## Banco de dados

Modelos em `services/models.py`. As tabelas são criadas no boot (`repository.init_db()`), sem migrations: o `create_all` só cria o que ainda não existe.

Se mudar uma coluna de tabela existente, o banco não é alterado. Em dev, rode `docker compose down -v` e suba de novo; em produção, faça um `ALTER TABLE` manual.

## Estrutura

```
main.py            entrada (API + bot + jobs)
app.py             rotas FastAPI
config/            banco e links dos portais
platforms/discord/ bot, comandos e eventos
services/          monitor, incidentes, status, repository, models
utils/             scrapper, IA, GitHub, jobs, download
```

## Escopo atual

Bot único, não multi-tenant: monitora todas as UFs e notifica um canal fixo (`CHANNEL_ID`). Atender vários clientes exigiria reintroduzir um model de assinatura/tenant. O roadmap está em [todo.md](todo.md).
