# Monitor Fiscal — Pendências

Só o que falta. O que já está pronto está no [readme.md](readme.md).

## 🔥 Agora

- [ ] `monitor.py`: descomentar `return novos`
- [ ] `jobs.py`: trocar `seconds=10` por `INTERVALO`
- [ ] `jobs.py`: reativar o alerta de novos documentos no Discord
- [ ] `jobs.py`: reativar `verificar_saude_urls` e `verificar_incidentes_sefaz`
- [ ] Tratar erros em `fetch_html` / `ai_extractor.extrair` para não derrubar o loop inteiro
- [ ] Commitar a refatoração em blocos

## 🧱 Base

- [ ] Limpar `requirements.txt` (`motor`, `pymongo`, `psycopg2-binary`, `bs4`, `dotenv`, `PyPDF2`, `jurigged` sobrando)
- [ ] Reintroduzir Alembic (migrations)
- [ ] Habilitar o serviço `bot` no `docker-compose.yml`
- [ ] Adicionar NFe em `URLS_NOTAS_TECNICAS` (`config/links.py`)
- [ ] Limpar `.temp/` periodicamente
- [ ] Preencher `.env-example` com a descrição de cada variável
- [ ] Ignorar `monitor_fiscal.log` no `.gitignore`

## 🧪 Testes

- [ ] Restaurar `tests/` (o `conftest.py` e o `pytest.ini` estão órfãos)
- [ ] `monitor.py` (mock de scrapper e extractor)
- [ ] `repository.py` (SQLite async)
- [ ] `status_sefaz.py`, `status_github.py`, `ai_extractor.py`
- [ ] CI com GitHub Actions rodando `pytest`

## 🔍 Monitoramento

- [ ] Monitorar portais estaduais (hoje só os nacionais)
- [ ] Auto-healing do scrapper com IA quando o layout mudar
- [ ] Análise de `.txt` e `.xml` além de PDF
- [ ] Resumo diário das NTs das últimas 24h

## 💬 Discord

- [ ] `/ajuda`
- [ ] Comandos admin (forçar verificação, ver logs)

## 🚀 Produto (SaaS)

Exige reintroduzir usuário/assinatura/tenant no banco.

- [ ] Models `Usuario` e `Assinatura`
- [ ] `/assinar`, `/cancelar`, `/minhas-assinaturas`
- [ ] Alertas por DM conforme assinatura (por UF/tipo)
- [ ] Planos (free/pro/enterprise), limites e trial
- [ ] Pagamento (Stripe/Pagar.me), webhook e `/upgrade`
- [ ] API REST: documentos, usuários, assinaturas, com auth e rate limit
- [ ] Novas plataformas: Telegram e e-mail (com um `notifier` para despacho)

## 📊 Observabilidade

- [ ] Logs estruturados (JSON)
- [ ] Sentry
- [ ] `/metrics` (Prometheus)
- [ ] Backup do banco
