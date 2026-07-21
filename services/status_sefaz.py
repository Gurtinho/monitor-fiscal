from aiolimiter import AsyncLimiter
from bs4 import BeautifulSoup
import utils.log as log
from utils.scrapper import fetch_html

PORTAIS = {
    "NFe": "https://www.nfe.fazenda.gov.br/portal/disponibilidade.aspx",
    "CTe": "https://www.cte.fazenda.gov.br/portal/disponibilidade.aspx",
    "NFCe": "https://www.nfce.fazenda.gov.br/portal/disponibilidade.aspx",
    "MDFe": "https://mdfe-portal.sefaz.rs.gov.br/MdfeMDFe/",
}

limiter = AsyncLimiter(7, 60)


def _parse_disponibilidade(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")

    # O portal NFe/CTe/NFCe usa uma GridView com esse id padrão
    table = soup.find("table", {"id": lambda x: x and "gdvDisponibilidade" in x})
    if not table:
        table = soup.find("table", class_=lambda x: x and "Grid" in (x or ""))
    if not table:
        return []

    components = []
    rows = table.find_all("tr")

    for row in rows[1:]: # pula o cabeçalho
        cols = row.find_all("td")
        if not cols:
            continue

        uf = cols[0].get_text(strip=True)
        if not uf or len(uf) > 5:
            continue

        # Status determinado pelas imagens na linha (src ou alt)
        imgs = row.find_all("img")
        is_down = any(
            "indisponivel" in (img.get("src", "") + img.get("alt", "")).lower()
            or "vermelho" in (img.get("src", "") + img.get("alt", "")).lower()
            for img in imgs
        )

        components.append({
            "name": uf,
            "status": "unavailable" if is_down else "operational",
        })

    return components


def _calcular_indicator(components: list[dict]) -> tuple[str, str]:
    if not components:
        return "minor", "Não foi possível verificar os serviços"

    down = [c for c in components if c["status"] != "operational"]

    if not down:
        return "none", "Todos os serviços operacionais"
    if len(down) > len(components) / 2:
        return "critical", f"{len(down)} estados indisponíveis"
    return "minor", f"{len(down)} estado(s) com problemas"


async def checar_sefaz(tipo: str = "NFe") -> dict:
    """
    Raspa o portal de disponibilidade SEFAZ e retorna status por UF.
    """
    async with limiter:
        try:
            url = PORTAIS.get(tipo, PORTAIS["NFe"])
            html = await fetch_html(url)

            if not html:
                return {
                    "erro": "Não foi possível acessar o portal SEFAZ",
                    "tipo": tipo,
                    "indicator": None,
                    "description": None,
                    "components": [],
                }

            components = _parse_disponibilidade(html)
            indicator, description = _calcular_indicator(components)

            return {
                "erro": None,
                "tipo": tipo,
                "indicator": indicator,
                "description": description,
                "components": components,
            }

        except Exception as e:
            log.logging.error(f"Erro ao checar SEFAZ {tipo}: {e}")
            return {
                "erro": str(e),
                "tipo": tipo,
                "indicator": None,
                "description": None,
                "components": [],
            }
