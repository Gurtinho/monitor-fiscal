import aiohttp
from aiolimiter import AsyncLimiter
import utils.log as log

BASE_URL = "https://status.atlassian.com/api/v2"

# 7 requisições a cada 60 segundos por usuário
limiter = AsyncLimiter(7, 60)

async def checar_jira() -> dict:
    async with limiter:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/summary.json") as resp:
                    resp.raise_for_status()
                    data = await resp.json()

            components_jira = [
                {"name": c["name"], "status": c["status"]}
                for c in data["components"]
                if "jira" in c["name"].lower()
            ]

            return {
                "erro": None,
                "indicator": data["status"]["indicator"],
                "description": data["status"]["description"],
                "components": components_jira,
                "incidents": [
                    {"name": i["name"], "status": i["status"]}
                    for i in data.get("incidents", [])
                ],
            }

        except Exception as e:
            log.logging.error(f"Erro crítico na função checar jira: {e}")
            return {
                "erro": str(e),
                "indicator": None,
                "description": None,
                "components": [],
                "incidents": [],
            }
