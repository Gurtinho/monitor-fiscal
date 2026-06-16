import aiohttp
import utils.log as log

async def fetch_html(url: str) -> str | None:
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=30, ssl=False) as resp:
                if resp.status == 200:
                    return await resp.text()
                log.logging.warning(f"Status {resp.status} ao buscar {url}")
                return None
    except Exception as e:
        log.logging.error(f"Erro ao buscar HTML de {url}: {e}")
        return None
