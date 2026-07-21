import aiohttp
from aiolimiter import AsyncLimiter
import utils.log as log

BASE_URL = "https://www.githubstatus.com/api/v2"

# Define o limite: 7 requisições a cada 60 segundos por usuário
limiter = AsyncLimiter(7, 60)

async def checar_github() -> dict:
    async with limiter:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/summary.json") as resp:
                    resp.raise_for_status()
                    data = await resp.json()

            return {
                "erro": None,
                "indicator": data["status"]["indicator"],
                "description": data["status"]["description"],
                "components": [
                    {"name": c["name"], "status": c["status"]}
                    for c in data["components"]
                ],
                "incidents": [
                    {"name": i["name"], "status": i["status"]}
                    for i in data.get("incidents", [])
                ],
            }

        except Exception as e:
            log.logging.error(f"Erro crítico na função checar github: {e}")
            return {
                "erro": str(e),
                "indicator": None,
                "description": None,
                "components": [],
                "incidents": [],
            }
