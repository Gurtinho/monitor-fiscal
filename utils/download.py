import discord
import requests
import os
import io
import uuid
import zipfile
import aiohttp
import aiofiles
import asyncio

import urllib3

import utils.log as log

# Desativa o aviso chato de "Insecure Request" no console quando usar verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Usando apenas funções assincronas HEHEHE

async def realizar_download(url):
    # Headers mais robustos para enganar firewalls de órgãos públicos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,application/pdf,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/"
    }
    
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=30, verify_ssl=False) as resp:
                if resp.status == 200:
                    return await resp.read()
                else:
                    print(f"❌ Falha no Download: Status {resp.status} para a URL: {url}")
                    return None
            
    except aiohttp.ClientError as e:
        print(f"🚨 Erro de Conexão: {e}")
    
    return None

async def zipar(documentos, choice):
    zip_buffer = io.BytesIO()
    
    # Pegamos apenas os primeiros 5 para não estourar limite
    docs_para_baixar = documentos[:5]
    
    # Dispara todos os downloads ao mesmo tempo!
    tasks = [realizar_download(d['url']) for d in docs_para_baixar]
    conteudos = await asyncio.gather(*tasks) # Reuni todos os downloads

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for idx, content in enumerate(conteudos):
            if content:
                i = docs_para_baixar[idx]
                nome_pdf = f"{i['texto'][:50]}.pdf".replace("/", "-")
                zip_file.writestr(nome_pdf, content)
    
    zip_buffer.seek(0)
    return discord.File(fp=zip_buffer, filename=f"Documentos_{choice}.zip")

async def salvar_arquivo_local(url, pasta_destino=".temp"):
    """Faz o download e salva em disco com um nome único."""
    # Garante que a pasta de destino existe
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Gera um nome único para evitar que um download sobrescreva o outro
    nome_unico = f"{uuid.uuid4()}.pdf"
    caminho_completo = os.path.join(pasta_destino, nome_unico)

    try:
        content = await realizar_download(url)
        if not content or isinstance(content, str): 
            return None
        
        async with aiofiles.open(caminho_completo, "wb") as f:
            await f.write(content)
            
        return caminho_completo
    except Exception as e:
        log.logging.error(f"Erro ao salvar arquivo local: {e}")
        return None
    
    return None

async def deletar_arquivo_local(caminho):
    """Remove o arquivo do disco se ele existir."""
    try:
        if caminho and os.path.exists(caminho):
            os.remove(caminho)
            return True
    except Exception as e:
        print(f"Erro ao deletar arquivo: {e}")
    return False