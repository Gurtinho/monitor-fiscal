import os
from bs4 import BeautifulSoup
import requests
import json
import re

from config import links

# ============================================================
# Verificação
# ============================================================
# Busca de forma automática com event
async def verificar_atualizacoes():
    novos = []

    # Atualizações fiscais
    if links.URLS_NOTAS_TECNICAS == None:
        return

    for nome, url in links.URLS_NOTAS_TECNICAS.items():
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
def buscar_nfe():
    # tenta acessar a página de informes na home
    headers = {"User-Agent": "Mozilla/5.0"}
    base_url = "https://www.nfe.fazenda.gov.br/portal/"

    link_home = f"{base_url}principal.aspx"
    res_home = requests.get(link_home, headers=headers)
    soup_home = BeautifulSoup(res_home.text, "html.parser")
    
    codigos_informes = set()
    count = 0
    for item in soup_home.find_all("a"):
        if count == 5:
            break
        texto = item.get_text(strip=True)
        match = re.search(r"\d{4}\.\d{3}", texto)
        if match:
            codigos_informes.add(match.group(0))
            count += 1

    # tenta acessar a página de notas técnicas
    link_lista = f"{base_url}listaConteudo.aspx?tipoConteudo=04BIflQt1aY="
    res_lista = requests.get(link_lista, headers=headers)
    soup_lista = BeautifulSoup(res_lista.text, "html.parser")

    nts = {
        "url_portal": base_url,
        "documentos": []
    }
    count = 0

    divNormal = soup_lista.find("div", class_="indentacaoNormal")
    for p in divNormal.find_all("p"):
        a = p.find("a", href=True)
        if a:
            p = a.find("span", class_="tituloConteudo")
            href = a["href"].strip()

            match = re.search(r"\d{4}\.\d{3}", p.get_text(strip=True))
            if match:
                codigo = match.group(0)
                if codigo in codigos_informes:
                    url = f"{base_url}{href}" if a else None
                    nts['documentos'].append({
                        "texto": p.get_text(strip=True),
                        "url": url
                    })

    return nts

def buscar_cte():
    return "Ainda não foi implementado, aguarde um pouco mais...☕"

def buscar_nfce():
    return "Ainda não foi implementado, aguarde um pouco mais...☕"
    
def buscar_mdfe():
    return "Ainda não foi implementado, aguarde um pouco mais...☕"

def buscar_nfse():
    return "Ainda não foi implementado, aguarde um pouco mais...☕"


# ============================================================
# Escolhe qual função
# ============================================================
def buscar_notas(nome):
    if nome == "NFe":
        return buscar_nfe()
    elif nome == "CTe":
        return buscar_cte()
    elif nome == "NFCe":
        return buscar_nfce()
    elif nome == "MDFe":
        return buscar_mdfe()
    elif nome == "NFSe":
        return buscar_nfse()