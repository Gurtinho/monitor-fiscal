# 🚀 Monitor Fiscal AI
> Inteligência Artificial monitorando e analisando atualizações fiscais da SEFAZ em tempo real.

O **Monitor Fiscal AI** é um sistema robusto de ChatOps projetado para Software Houses e departamentos fiscais. Ele automatiza o monitoramento de Notas Técnicas (NTs) nos portais da SEFAZ, utiliza IA para analisar o impacto no código-fonte e notifica o time de desenvolvimento instantaneamente via Discord.

## ✨ Principais Funcionalidades
- **Monitoramento Automatizado:** Scrapping inteligente de portais nacionais (NFe, CTe, MDFe, etc).
- **Análise Semântica (IA):** Integração com Gemini API para interpretar PDFs de Notas Técnicas e extrair mudanças críticas.
- **ChatOps (Discord):** Bot integrado para notificações em tempo real e comandos de consulta rápida.
- **Integração com GitHub:** Download automático de arquivos fontes (ex: NFePHP) para análise de impacto via IA.
- **API FastAPI:** Endpoints robustos para integração com outros sistemas e recebimento de webhooks.
- **Auto-healing Scrapper:** (Em desenvolvimento) Uso de LLM para adaptar o scrapping a mudanças de layout da SEFAZ.

## 🛠️ Tech Stack
- **Linguagem:** Python 3.10+
- **Framework Web:** FastAPI & Uvicorn
- **Discord SDK:** Discord.py
- **IA:** Google Gemini API (modelos Pro e Flash)
- **Scrapping:** BeautifulSoup4 & Requests
- **Task Scheduling:** Discord.ext.tasks com suporte a Timezone (pytz)

## ⚙️ Configuração Inicial
1. **Clone o repositório** e entre na pasta do projeto.
2. **Crie um ambiente virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure o `.env`:** Utilize o `.env-example` como base para configurar suas chaves do Discord, GitHub e Gemini.
5. **Execute a aplicação:**
   ```bash
   python main.py
   ```

## 📈 Visão de Negócio
Este projeto foi concebido com uma arquitetura escalável (SaaS), permitindo monitoramento multi-UF e multi-tenant. É a solução ideal para empresas que buscam reduzir o risco de paradas no faturamento por falta de conformidade fiscal.

---
Desenvolvido com foco em automação e excelência técnica.