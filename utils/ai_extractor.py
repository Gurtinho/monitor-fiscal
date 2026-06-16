import aiohttp
import os
import json
import re
from bs4 import BeautifulSoup
import utils.log as log

async def extrair(html: str, url_base: str) -> list:
    """
    Recebe o HTML bruto de um portal fiscal e retorna lista de documentos
    [{texto, url}] extraída pela IA. Resiliente a mudanças no layout do site.
    """
    api_key = os.getenv("GEMINI_TOKEN")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"

    links_texto = _extrair_links(html, url_base)

    prompt = f"""Analise os links extraídos de um portal fiscal brasileiro.
Identifique apenas links de notas técnicas ou documentos fiscais oficiais (NTs, manuais, leiautes).
Ignore menus, links de navegação e páginas genéricas.

Retorne SOMENTE um JSON válido, sem texto adicional nem markdown:
{{"documentos": [{{"texto": "NT 2025.001 v1.00", "url": "https://..."}}]}}

Se não encontrar documentos relevantes, retorne {{"documentos": []}}.
URLs relativas devem ser absolutas usando a base: {url_base}

Links encontrados:
{links_texto}"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 2000}
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=30) as resp:
                if resp.status != 200:
                    log.logging.error(f"Gemini retornou status {resp.status} no extractor")
                    return []
                data = await resp.json()
                texto = data['candidates'][0]['content']['parts'][0]['text']

                match = re.search(r'\{[\s\S]*\}', texto)
                if not match:
                    log.logging.warning("ai_extractor: resposta sem JSON válido")
                    return []

                resultado = json.loads(match.group(0))
                return resultado.get('documentos', [])

    except Exception as e:
        log.logging.error(f"Erro no ai_extractor: {e}")
        return []

def _extrair_links(html: str, url_base: str) -> str:
    """Extrai apenas os links do HTML para reduzir tokens enviados à IA."""
    soup = BeautifulSoup(html, 'html.parser')
    linhas = []

    for a in soup.find_all('a', href=True):
        texto = a.get_text(strip=True)
        href = a['href'].strip()

        if not texto or not href or href in ('#', 'javascript:void(0)'):
            continue

        if not href.startswith('http'):
            href = url_base.rstrip('/') + '/' + href.lstrip('/')

        linhas.append(f"{texto} => {href}")

    return "\n".join(linhas[:500])
