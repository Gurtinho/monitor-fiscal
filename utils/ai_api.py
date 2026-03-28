import os
import aiohttp
import aiofiles
import json
from aiolimiter import AsyncLimiter
import asyncio
import base64
import utils.log as log
from utils.pdf_validate import pdf_tem_paginas

# Define o limite: 7 requisições a cada 60 segundos
limiter = AsyncLimiter(7, 60)

async def analisar(prompt_texto, arquivos=None):
    async with limiter:
        try:
            api_key = os.getenv("GEMINI_TOKEN")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
            headers = {
                "Content-Type": "application/json"
            }

            if not prompt_texto:
                return "Por algum motivo fiquei sem o prompt 😥"


            if not arquivos:
                return "Por algum motivo fiquei sem os arquivos 😥"

            parts = [{"text": prompt_texto}]

            for arquivo in arquivos:
                if arquivo is None: continue
                
                if arquivo.endswith('.pdf'):
                    if pdf_tem_paginas(arquivo):
                        async with aiofiles.open(arquivo, "rb") as f:
                            conteudo = await f.read()
                            encoded_content = base64.b64encode(conteudo).decode('utf-8')
                            mime_type = "application/pdf" if arquivo.endswith('.pdf') else "text/plain"
                            
                            parts.append({
                                "inlineData": {
                                    "mimeType": mime_type,
                                    "data": encoded_content
                                }
                            })

            # Se depois do loop só sobrou o texto (nenhum arquivo válido)
            if len(parts) == 1 and arquivos:
                return "Os arquivos baixados parecem estar vazios ou corrompidos (bloqueio da SEFAZ?)"

            payload = {
                "contents": [{"parts": parts}],
                "generationConfig": {
                    "maxOutputTokens": 1800, # Um pouco mais de margem, já que temos o chunks
                    "temperature": 0.7
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload, timeout=60) as response:
                    res_json = await response.json()

                    log.logging.info(response)

                    if response.status == 200:
                        try:
                            return res_json['candidates'][0]['content']['parts'][0]['text']
                        except (KeyError, IndexError):
                            log.logging.error(f"Estrutura de resposta inesperada: {res_json}")
                            return "A IA retornou uma resposta vazia ou em formato inesperado."
                    else:
                        msg_erro = res_json.get('error', {}).get('message', 'Erro desconhecido')
                        return f"Erro na API ({response.status}): {msg_erro}"

        except Exception as e:
            log.logging.error(f"Erro crítico na função analisar: {e}")
            return f"Erro de IA: {e}"