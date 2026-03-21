
import json
import os
from pathlib import Path

from config import links

# ============================================================
# Cache - Valida se já foi buscado as informações
# ============================================================

class Cache:
    def __init__(self, caminho_cache):
        self.caminho_cache = caminho_cache
        self.dados = self.carregar_cache()
    

    def carregar_cache(self):
        if links.CAMINHO_CACHE and os.path.exists(os.path.join(links.CAMINHO_CACHE, links.ARQUIVO_CACHE)):
            with open(os.path.join(links.CAMINHO_CACHE, links.ARQUIVO_CACHE), "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def salvar_cache(self, dados):
        Path(links.CAMINHO_CACHE).mkdir(exist_ok=True) # cria o arquivo caso não exista
        with open(os.path.join(links.CAMINHO_CACHE, links.ARQUIVO_CACHE), "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
