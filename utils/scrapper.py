import os
from bs4 import BeautifulSoup
import requests
import json
from config import links

# ============================================================
# Verificação
# ============================================================
# Busca de forma automática com event
async def verificar_atualizacoes():
    novos = []

    # Atualizações fiscais
    if links.URLS_FISCAIS == None:
        return

    for nome, url in links.URLS_FISCAIS.items():
        encontrados = buscar_notas(nome, url)

        if not encontrados:
            print(f"Nenhuma nota técnica encontrada em {nome}.")
            continue

        urls_antigas = {x["url"] for x in encontrados}
        novos_links = [x for x in encontrados if x["url"] not in urls_antigas]

        if novos_links:
            print(f"🚨 {len(novos_links)} novas NTs em {nome}")
            novos.extend(novos_links)


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
    return "nfce"
    
def buscar_mdfe(url):
    return "mdfe"


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