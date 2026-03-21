import requests
import json
import os
from config import links
from pathlib import Path


def create_gist_from_file(file_path, description, public, token=None):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    # salva na var o conteudo do arquivo
    with open(file_path, 'r') as f:
        content = f.read()

    filename = os.path.basename(file_path)

    # cria um dict pra armazenar as informações em json
    data = {
        "description": description,
        "public": public,
        "files": {
        filename: {
            "content": content
        }
        }
    }

    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    # usa as autorizações pra criar um gist
    if token:
        headers["Authorization"] = f"token {token}"

    url = "https://api.github.com/gists"

    # valida se existe um gist com o nome correto
    gists_online = buscar_gist_por_nome("Gurtinho", "documentos_fiscais.json")
    gist_online_id = gists_online[0]["id"] if gists_online else None

    # valida se o gist ta preenchido localmente
    with open(os.path.join(links.CAMINHO_CACHE, "gist.json"), 'r', encoding="utf-8") as f:
        gist_local = json.load(f)
        
    # só edita se houver local e online
    if gist_local['gist_id'] and gist_online_id:
        url = f"https://api.github.com/gists/{gist_local['gist_id']}"

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        gist_data = response.json()
        
        # salva o id no json
        if not gist_local['gist_id']:
            with open(os.path.join(links.CAMINHO_CACHE, "gist.json"), 'w', encoding="utf-8") as f:
                json.dump({
                "gist_id": gist_data['id']
                }, f)
        
        print(f"Successfully created gist: {gist_data['html_url']}")
        return gist_data['html_url']

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def buscar_gist_por_nome(username, nome_arquivo):
    url = f"https://api.github.com/users/{username}/gists"
    # Se estiver usando autenticação, adicione 'headers=headers' na chamada get
    response = requests.get(url) 

    if response.status_code != 200:
        print(f"Erro ao buscar gists: {response.status_code}")
        return []

    gists = response.json()
    gists_encontrados = []

    for gist in gists:
        for filename in gist['files']:
            if filename == nome_arquivo:
                gists_encontrados.append({
                'id': gist['id'],
                'descricao': gist.get('description', ''),
                'url': gist['html_url'],
                'nome_arquivo': filename
                })
                break

    return gists_encontrados

def carregar_gist():
    if links.CAMINHO_CACHE and os.path.exists(os.path.join(links.CAMINHO_CACHE, "gist.json")):
        with open(os.path.join(links.CAMINHO_CACHE, "gist.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_gist(dados):
    Path(links.CAMINHO_CACHE).mkdir(exist_ok=True) # cria o arquivo caso não exista
    with open(os.path.join(links.CAMINHO_CACHE, "gist.json"), "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)