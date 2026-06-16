import utils.log as log
from utils import scrapper, ai_extractor
from services import repository

async def verificar_atualizacoes(urls: dict) -> dict:
    """
    Busca HTML de cada portal, extrai documentos via IA e salva os novos.
    Retorna {tipo: [novos_documentos]} apenas para tipos com novidades.
    """
    novos = {}

    for tipo, url in urls.items():
        html = await scrapper.fetch_html(url)
        if not html:
            log.logging.warning(f"Sem resposta ao buscar {tipo} ({url})")
            continue

        documentos = await ai_extractor.extrair(html, url)
        novos_docs = []

        for doc in documentos:
            is_new = await repository.salvar_documento(tipo, doc['texto'], doc['url'])
            if is_new:
                novos_docs.append(doc)

        if novos_docs:
            novos[tipo] = novos_docs
            log.logging.info(f"🚨 {len(novos_docs)} novo(s) em {tipo}")

    return novos
