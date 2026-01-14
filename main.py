from urllib.parse import urljoin
import requests
import json
import os
import dotenv
from datetime import datetime, timezone
from pathlib import Path
import sys

from bs4 import BeautifulSoup
# from fastapi import FastAPI

sys.stdout.reconfigure(encoding='utf-8')
dotenv.load_dotenv()

# app = FastAPI(title="Monitor API")

# ============================================================
# Constantes
# ============================================================
INTERVALO = 3600 * 12  # 12 horas

ARQUIVO_CACHE = "documentos_fiscais.json"

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

URLS_FISCAIS = {
  # "NFe": os.getenv("NFE_URL"),
  "CTe": os.getenv("CTE_URL"),
  # "NFCe": os.getenv("NFCE_URL"),
  # "MDFe": os.getenv("MDFE_URL"),
  # "Sped": os.getenv("SPED_URL")
}

URL_JIRA = os.getenv("JIRA_URL")


# ============================================================
# Rotas
# ============================================================
# @app.get("/")
# def home():
#   return {"status": "ok", "mensagem": "Monitor API rodando"}

# @app.get("/verificar")
# def forcar_verificacao():
#   verificar_atualizacoes()
#   return {"status": "executado"}


# ============================================================
# Worker paralelo pra rodar sozinho
# ============================================================
# def worker_loop():
#     while True:
#       hoje = datetime.today()
#       hoje = hoje.replace(tzinfo=timezone.utc)
#       hoje = hoje.strftime('%d/%m/%Y %H:%M:%S')
#       print(f"Execução automática do monitor em andamento {hoje}...")
#       verificar_atualizacoes()
#       time.sleep(3600 * 12)  # a cada 12 horas

# threading.Thread(target=worker_loop, daemon=True).start()


# ============================================================
# Cache - Valida se já foi buscado as informações
# ============================================================
def carregar_cache():
  if os.path.exists(ARQUIVO_CACHE):
    with open('./cache/' + ARQUIVO_CACHE, "r", encoding="utf-8") as f:
      return json.load(f)
  return {}

def salvar_cache(dados):
  Path('./cache').mkdir(exist_ok=True) # cria o arquivo caso não exista
  with open('./cache/' + ARQUIVO_CACHE, "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=2, ensure_ascii=False)


# ============================================================
# Busca as notas
# ============================================================
def buscar_nfe(url):
    resp = requests.get(url) # busca a página
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
  
def buscar_mdfe(url):
  print("mdfe")
  
def buscar_cte(url):
    resp = requests.get(url) # busca a página
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
  print("nfe")
  
def buscar_sped(url):
  print("sped")
  
def buscar_notas(url):
  if "NFe" in URLS_FISCAIS:
    return buscar_nfe(url)
  elif "CTe" in URLS_FISCAIS:
    return buscar_cte(url)
  elif "NFCe" in URLS_FISCAIS:
    return buscar_nfce(url)
  elif "MDFe" in URLS_FISCAIS:
    return buscar_mdfe(url)
  elif "Sped" in URLS_FISCAIS:
    return buscar_sped(url)
  
  
# ============================================================
# Busca outras atualizações
# ============================================================
def buscar_status_jira():
  print("status jira")
  

# ============================================================
# Envio para Discord
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
    resp = requests.post(WEBHOOK_URL, json=payload)
    if resp.status_code in (200, 204):
      print("✅ Embed enviado ao Discord!")
    else:
      print(f"⚠️ Erro {resp.status_code}: {resp.text}")
  except Exception as e:
    print(f"❌ Falha ao enviar embed: {e}")

        
# ============================================================
# Verificação
# ============================================================
def verificar_atualizacoes():
  cache = carregar_cache()
  novos = []

  # Atualizações fiscais
  for nome, url in URLS_FISCAIS.items():
    print(f"🔍 Verificando {nome}...")
    encontrados = buscar_notas(url)
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
    else:
      print(f"Nenhuma nova nota técnica encontrada em {nome}.")


# ============================================================
# Tray
# ============================================================
def loop_monitoramento():
  verificar_atualizacoes()
  
  
# ============================================================
# Função main principal
# ============================================================
if __name__ == "__main__":
  loop_monitoramento()