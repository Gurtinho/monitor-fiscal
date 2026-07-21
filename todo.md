# Monitor Fiscal — Roadmap

> SaaS de monitoramento fiscal automatizado com múltiplas plataformas de notificação.
> Marca com ✅ o que está feito, 🔲 o que ainda falta.

---

## 1. Infraestrutura e Base

- [x] FastAPI + Uvicorn rodando em paralelo com o bot (`main.py`)
- [x] SQLAlchemy async com PostgreSQL (`config/database.py`)
- [x] Models: `Documento`, `Usuario`, `Assinatura`, `Notificacao` (`services/models.py`)
- [x] Repository layer com CRUD completo (`services/repository.py`)
- [x] Docker Compose com PostgreSQL e Redis (`docker-compose.yml`)
- [ ] Habilitar o serviço `bot` no `docker-compose.yml` (está comentado)
- [ ] Configurar Alembic para migrations — atualmente usa `create_all` direto no boot
- [ ] Implementar `utils/jobs.py` — arquivo criado mas vazio (destinado à fila de jobs)
- [ ] Integrar Redis com `utils/jobs.py` para filas de background (Redis já está no compose mas nada o usa)
- [ ] Implementar `utils/auto_clear.py` — arquivo existe só com um comentário; precisa limpar `.temp/` periodicamente
- [ ] Adicionar NFe ao `URLS_NOTAS_TECNICAS` em `config/links.py` (MDFe, CTe, NFCe estão; NFe está ausente)

---

## 2. Monitoramento e Scrapping

- [x] Scrapper de HTML assíncrono (`utils/scrapper.py`)
- [x] Extração de documentos via IA (Gemini) — `utils/ai_extractor.py`
- [x] Serviço de verificação de atualizações — `services/monitor.py`
- [x] Portais nacionais mapeados (MDFe, CTe, NFCe) — `config/links.py`
- [x] Portais estaduais por UF mapeados — `config/links.py`
- [x] Salvar documentos novos no banco e evitar duplicatas
- [ ] Monitorar portais estaduais (atualmente só os nacionais são verificados)
- [ ] Monitoramento por UF por assinatura — verificar só os estados que o usuário assinou
- [ ] Tarefa agendada de monitoramento SEFAZ de disponibilidade (hoje só manual via `/status`)
- [ ] Auto-healing do scrapper: usar IA para adaptar extração quando o layout do portal mudar
- [ ] Cache dos resultados no Redis para evitar scrapping redundante entre verificações próximas

---

## 3. Plataforma Discord

- [x] Bot Discord com auto-carregamento de commands e events (`platforms/discord/bot.py`)
- [x] Comando `/status` — Jira, GitHub, SEFAZ com select interativo
- [x] Comando `/documentos` — lista NTs por tipo com download, análise IA e análise com fontes
- [x] Task agendada `verificar_nts` às 8h05 (horário SP)
- [x] Task agendada `bom_dia` às 8h00
- [x] Alerta automático de novos documentos no canal configurado (`CHANNEL_ID`)
- [x] Integração com `notifier.py` para despacho multi-plataforma
- [ ] Comando `/assinar [tipo] [estado?]` — usuário se inscreve para receber alertas
- [ ] Comando `/cancelar [tipo] [estado?]` — cancela assinatura
- [ ] Comando `/minhas-assinaturas` — lista as assinaturas ativas do usuário
- [ ] Despacho de notificações por usuário — hoje envia só para `CHANNEL_ID`; deve enviar DM por assinatura
- [ ] Comando `/meu-plano` — exibe plano atual e limites do usuário
- [ ] Comando `/ajuda` — lista os comandos disponíveis com descrições
- [ ] Comandos admin: gerenciar usuários, forçar verificação, ver logs
- [ ] Registro automático de usuário Discord na primeira interação com o bot

---

## 4. Plataforma Telegram

- [ ] Criar `platforms/telegram/` seguindo a mesma estrutura de `platforms/discord/`
- [ ] Bot Telegram com `/start` para registro de usuário
- [ ] Comando `/status` para Jira, GitHub, SEFAZ
- [ ] Comando `/documentos` com seleção por tipo
- [ ] Comandos `/assinar`, `/cancelar`, `/minhas-assinaturas`
- [ ] Handler para envio de alertas automáticos (`notifier.registrar("telegram", ...)`)
- [ ] Adicionar token Telegram ao `.env-example`

---

## 5. Plataforma Email

- [ ] Criar `platforms/email/` com handler de envio
- [ ] Template HTML de alerta de novo documento fiscal
- [ ] Template de resumo diário
- [ ] Handler registrado no `notifier.py` (`notifier.registrar("email", ...)`)
- [ ] Configuração de SMTP no `.env-example` (host, porta, usuário, senha)
- [ ] Opt-in/opt-out por e-mail via API

---

## 6. Análise com IA

- [x] Análise de PDFs via Gemini (`utils/ai_api.py`)
- [x] Extração de links de documentos do HTML via IA (`utils/ai_extractor.py`)
- [x] Integração com código-fonte do GitHub para análise de impacto
- [x] Download de arquivos PHP do repositório configurado (`utils/github_api.py`)
- [x] Divisão de resposta longa em chunks (`utils/chunks.py`)
- [x] Validação de PDF com páginas (`utils/pdf_validate.py`)
- [ ] Suporte a análise de arquivos `.txt` e `.xml` além de PDF
- [ ] Upload para Google Drive (`utils/upload_gdrive.py` existe mas não está integrado ao fluxo)
- [ ] Resumo diário automático das NTs encontradas nas últimas 24h enviado nos alertas

---

## 7. API REST (FastAPI)

- [x] `GET /healthcheck` — status básico do sistema
- [x] `GET /status` — status do bot
- [ ] `POST /webhook/discord` — receber webhooks externos e encaminhar para canal Discord
- [ ] `GET /api/documentos` — listar documentos com paginação e filtro por tipo
- [ ] `GET /api/usuarios` — listar usuários (rota admin autenticada)
- [ ] `POST /api/usuarios` — criar usuário via API (integração com landing page/SaaS)
- [ ] `POST /api/assinaturas` — criar assinatura via API
- [ ] `DELETE /api/assinaturas/{id}` — cancelar assinatura via API
- [ ] Autenticação na API (API key ou JWT para rotas protegidas)
- [ ] Rate limiting nas rotas públicas da API

---

## 8. Sistema de Planos (SaaS)

- [x] Campo `plano` no model `Usuario` (free | pro | enterprise)
- [x] Função `atualizar_plano` no repository
- [ ] Definir e documentar os limites de cada plano (ex: free = 1 tipo, pro = todos, enterprise = multi-UF)
- [ ] Enforcement dos limites de plano nas assinaturas
- [ ] Integração com gateway de pagamento (Stripe ou Pagar.me) para upgrades
- [ ] Webhook de confirmação de pagamento para atualizar plano automaticamente
- [ ] Comando Discord `/upgrade` com link de checkout gerado dinamicamente
- [ ] Período de trial automático para novos usuários

---

## 9. Status de Serviços

- [x] `services/status_github.py` — verifica status via API pública do GitHub
- [x] `services/status_jira.py` — verifica status via API pública da Atlassian
- [x] `services/status_sefaz.py` — scrapping de disponibilidade por UF (NFe, CTe, NFCe, MDFe)
- [ ] Tarefa agendada de monitoramento automático de disponibilidade SEFAZ (proativo, não só sob demanda)
- [ ] Alerta automático quando UF entrar em indisponibilidade (para assinantes daquele estado)
- [ ] Histórico de disponibilidade por UF salvo no banco

---

## 10. Testes

- [x] Testes do comando `dado` (`tests/platforms/discord/test_discord_commands.py`)
- [x] Testes de `chunks` (`tests/utils/test_chunks.py`)
- [x] Testes de `status_jira` (`tests/services/test_status_jira.py`)
- [ ] Testes de `monitor.py` (mock do scrapper e AI extractor)
- [ ] Testes de `repository.py` (banco em memória com SQLite async)
- [ ] Testes de `notifier.py` (verificar despacho para handlers registrados)
- [ ] Testes de `status_sefaz.py` (mock do HTML de disponibilidade)
- [ ] Testes de `status_github.py` (mock da API)
- [ ] Testes de `ai_extractor.py` (mock da chamada Gemini)
- [ ] CI/CD: rodar `pytest` automaticamente via GitHub Actions a cada push
- [ ] Cobertura de testes mínima configurada (ex: 70%)

---

## 11. Operações e Observabilidade

- [x] Logger centralizado (`utils/log.py`)
- [x] Variáveis de ambiente com `.env-example`
- [ ] Preencher `.env-example` com descrição de cada variável (está vazio, sem documentação)
- [ ] Structured logging (JSON) para integração com ferramentas de observabilidade
- [ ] Integração com Sentry para rastreamento de erros em produção
- [ ] Métricas básicas expostas em `/metrics` (Prometheus-compatible)
- [ ] Dashboard de monitoramento do próprio serviço (Grafana ou similar)
- [ ] Estratégia de backup do banco de dados
- [ ] Habilitar e testar bot no Docker (`docker-compose up` com serviço `bot`)
