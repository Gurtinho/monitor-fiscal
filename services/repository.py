from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from config.database import AsyncSessionLocal, engine, Base
from services.models import Documento, Usuario, Assinatura, Notificacao
from config import links


# ─── Setup ────────────────────────────────────────────────────────────────────

async def init_db():
    import services.models  # garante que os models estão registrados no Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ─── Documentos ───────────────────────────────────────────────────────────────

async def salvar_documento(tipo: str, texto: str, url: str) -> bool:
    """Retorna True se é novo, False se já existia (url duplicada)."""
    async with AsyncSessionLocal() as session:
        try:
            session.add(Documento(tipo=tipo, texto=texto, url=url))
            await session.commit()
            return True
        except IntegrityError:
            await session.rollback()
            return False

async def buscar_documentos(tipo: str = None) -> list[Documento]:
    async with AsyncSessionLocal() as session:
        stmt = select(Documento).order_by(Documento.descoberto_em.desc())
        if tipo:
            stmt = stmt.where(Documento.tipo == tipo)
        result = await session.scalars(stmt)
        return result.all()

async def buscar_documentos_formatados(tipo: str) -> dict:
    """Formato esperado pelos commands do Discord."""
    url_portal = links.URLS_NOTAS_TECNICAS.get(tipo, "https://www.nfe.fazenda.gov.br")
    documentos = await buscar_documentos(tipo)
    return {
        "url_portal": url_portal,
        "documentos": [{"texto": d.texto, "url": d.url} for d in documentos]
    }


# ─── Usuários ─────────────────────────────────────────────────────────────────

async def criar_usuario(
    discord_id: str = None,
    telegram_id: str = None,
    email: str = None,
) -> Usuario:
    async with AsyncSessionLocal() as session:
        usuario = Usuario(discord_id=discord_id, telegram_id=telegram_id, email=email)
        session.add(usuario)
        await session.commit()
        await session.refresh(usuario)
        return usuario

async def buscar_usuario_por_discord(discord_id: str) -> Usuario | None:
    async with AsyncSessionLocal() as session:
        stmt = select(Usuario).where(Usuario.discord_id == discord_id)
        return await session.scalar(stmt)

async def buscar_usuario_por_telegram(telegram_id: str) -> Usuario | None:
    async with AsyncSessionLocal() as session:
        stmt = select(Usuario).where(Usuario.telegram_id == telegram_id)
        return await session.scalar(stmt)

async def buscar_usuarios_por_tipo(tipo: str) -> list[Usuario]:
    """Retorna todos os usuários ativos que assinaram um tipo de documento."""
    async with AsyncSessionLocal() as session:
        stmt = (
            select(Usuario)
            .join(Assinatura)
            .where(Assinatura.tipo == tipo, Usuario.ativo == True)
            .distinct()
        )
        result = await session.scalars(stmt)
        return result.all()

async def atualizar_plano(usuario_id: int, plano: str) -> None:
    async with AsyncSessionLocal() as session:
        usuario = await session.get(Usuario, usuario_id)
        if usuario:
            usuario.plano = plano
            await session.commit()


# ─── Assinaturas ──────────────────────────────────────────────────────────────

async def criar_assinatura(usuario_id: int, tipo: str, estado: str = None) -> Assinatura | None:
    """Retorna None se a assinatura já existe."""
    async with AsyncSessionLocal() as session:
        try:
            assinatura = Assinatura(usuario_id=usuario_id, tipo=tipo, estado=estado)
            session.add(assinatura)
            await session.commit()
            await session.refresh(assinatura)
            return assinatura
        except IntegrityError:
            await session.rollback()
            return None

async def buscar_assinaturas(usuario_id: int) -> list[Assinatura]:
    async with AsyncSessionLocal() as session:
        stmt = select(Assinatura).where(Assinatura.usuario_id == usuario_id)
        result = await session.scalars(stmt)
        return result.all()

async def remover_assinatura(usuario_id: int, tipo: str, estado: str = None) -> bool:
    async with AsyncSessionLocal() as session:
        stmt = select(Assinatura).where(
            Assinatura.usuario_id == usuario_id,
            Assinatura.tipo == tipo,
            Assinatura.estado == estado,
        )
        assinatura = await session.scalar(stmt)
        if assinatura:
            await session.delete(assinatura)
            await session.commit()
            return True
        return False


# ─── Notificações ─────────────────────────────────────────────────────────────

async def registrar_notificacao(usuario_id: int, documento_id: int, canal: str) -> Notificacao:
    async with AsyncSessionLocal() as session:
        notificacao = Notificacao(usuario_id=usuario_id, documento_id=documento_id, canal=canal)
        session.add(notificacao)
        await session.commit()
        await session.refresh(notificacao)
        return notificacao

async def ja_notificado(usuario_id: int, documento_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        stmt = select(Notificacao).where(
            Notificacao.usuario_id == usuario_id,
            Notificacao.documento_id == documento_id,
        )
        return await session.scalar(stmt) is not None
