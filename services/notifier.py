_handlers: dict = {}

def registrar(plataforma: str, handler):
    _handlers[plataforma] = handler

async def notificar_todos(novos: dict):
    """novos = {tipo: [lista de documentos]}"""
    for tipo, documentos in novos.items():
        for handler in _handlers.values():
            await handler(tipo, documentos)
