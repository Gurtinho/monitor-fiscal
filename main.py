import threading
from urllib.parse import urljoin
import requests
import json
import dotenv
from datetime import datetime, time, timezone
from pathlib import Path
import sys
import asyncio
dotenv.load_dotenv()

from bs4 import BeautifulSoup
from fastapi import FastAPI

# importa depois do load dotenv
import links

sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI(title="Monitor API")


# ============================================================
# Startup do fastapi
# ============================================================
@app.on_event("startup")
async def startup_event():
  asyncio.create_task(worker_loop())


# ============================================================
# Rotas
# ============================================================

# Verifica o status
@app.get("/")
def home():
  return {"status": "ok", "mensagem": "Monitor API rodando"}

# Chama novamente pra confirmação de envio
@app.get("/verificar")
def forcar_verificacao():
  verificar_atualizacoes()
  return {"status": "executado"}


# ============================================================
# Worker - Função assíncrona de busca
# ============================================================
async def worker_loop():
  while True:
    agora = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S")
    print(f"[WORKER] Verificação automática {agora}")

    try:
      verificar_atualizacoes()
    except Exception as e:
      print(f"[WORKER] Erro: {e}")

    await asyncio.sleep(60 * 60 * 12)  # 12 horas

# ============================================================
# Cache - Valida se já foi buscado as informações
# ============================================================
CAMINHO_CACHE = Path("cache") / links.ARQUIVO_CACHE

def carregar_cache():
  if CAMINHO_CACHE.exists():
    with open(CAMINHO_CACHE, "r", encoding="utf-8") as f:
      return json.load(f)
  return {}

def salvar_cache(dados):
  Path('./cache').mkdir(exist_ok=True) # cria o arquivo caso não exista
  with open('./cache/' + links.ARQUIVO_CACHE, "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=2, ensure_ascii=False)


# ============================================================
# Busca as notas
# ============================================================
def buscar_nfe(url):
    if url == None: 
      return

    resp = requests.get(url, timeout=20) # busca a página com timeout de 20 segundos
    soup = BeautifulSoup(resp.text, "html.parser") # converte a árvore de análise sintática
    links = []

    for a in soup.find_all("a", href=True):
      href = a["href"]
      texto = a.get_text(strip=True)
      if "Nota Técnica" in texto or "NT" in texto:
        links.append({
          "texto": texto,
          "url": href if href.startswith("http") else f"https://www.nfe.fazenda.gov.br/portal/{href}"
        })
    return links

def buscar_cte(url):
  if url == None: 
    return

  resp = requests.get(url, timeout=20) # busca a página com timeout de 20 segundos
  soup = BeautifulSoup(resp.text, "html.parser") # converte a árvore de análise sintática
  links = []

  for a in soup.find_all("a", href=True):
    href = a["href"]
    texto = a.get_text(strip=True)
    if "Nota Técnica" in texto or "NT" in texto:
      links.append({
        "texto": texto,
        "url": href if href.startswith("http") else f"https://www.cte.fazenda.gov.br/portal/{href}"
      })
  return links
  
def buscar_nfce(url):
  print("nfce")
  
def buscar_mdfe(url):
  print("mdfe")
  
  
# ============================================================
# Escolhe qual função
# ============================================================
def buscar_notas(nome, url):
  if nome == "NFe":
    return buscar_nfe(url)
  elif nome == "CTe":
    return buscar_cte(url)
  elif nome == "NFCe":
    return buscar_nfce(url)
  elif nome == "MDFe":
    return buscar_mdfe(url)
  

# ============================================================
# Envio de mensagem
# ============================================================
def enviar_discord(nome, novos_links):
  if not novos_links:
    return

  cor = 0x007BFF
  titulo = f"🚨 Novas Notas Técnicas em {nome}"
  descricao = "\n".join([ f"🔗 [{x['texto']}]({x['url']})\n\n" for x in novos_links ])

  payload = {
    "embeds": [
      {
        "title": titulo,
        "description": descricao,
        "color": cor,
        "footer": {"text": "Monitor • Receita Federal"},
        "timestamp": datetime.now(timezone.utc).isoformat()
      }
    ]
  }

  try:
    if links.WEBHOOK_URL == None:
      return

    resp = requests.post(links.WEBHOOK_URL, json=payload)
    if resp.status_code in (200, 204):
      print("✅ Embed enviado ao Discord!")
    else:
      print(f"⚠️ Erro {resp.status_code}: {resp.text}")
  except Exception as e:
    print(f"❌ Falha ao enviar embed: {e}")
    

def enviar_email(nome, novos_links):
  if not novos_links:
    return


# ============================================================
# Verificação
# ============================================================
def verificar_atualizacoes():
  cache = carregar_cache()
  novos = []

  # Atualizações fiscais
  if links.URLS_FISCAIS == None:
    return

  for nome, url in links.URLS_FISCAIS.items():
    
    encontrados = buscar_notas(nome, url)
    
    if not encontrados:
      print(f"Nenhuma nota técnica encontrada em {nome}.")
      continue

    antigos = cache.get(nome, [])
    urls_antigas = {x["url"] for x in antigos}
    novos_links = [x for x in encontrados if x["url"] not in urls_antigas]

    if novos_links:
      print(f"🚨 {len(novos_links)} novas NTs em {nome}")
      novos.extend(novos_links)
      cache[nome] = antigos + novos_links
      salvar_cache(cache)
      enviar_discord(nome, novos_links)
      
    # Buscar serviços em manutenção
    # ...

  
# ============================================================
# Função main principal
# ============================================================
if __name__ == "__main__":
  verificar_atualizacoes()