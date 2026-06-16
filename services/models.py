from datetime import datetime
from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class Documento(Base):
    __tablename__ = "documentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(10))        # NFe, CTe, MDFe, NFCe
    texto: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text, unique=True)
    descoberto_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    notificacoes: Mapped[list["Notificacao"]] = relationship(back_populates="documento")


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_id: Mapped[str | None] = mapped_column(String(50), unique=True)
    telegram_id: Mapped[str | None] = mapped_column(String(50), unique=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    plano: Mapped[str] = mapped_column(String(20), default="free")   # free | pro | enterprise
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    assinaturas: Mapped[list["Assinatura"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    notificacoes: Mapped[list["Notificacao"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")


class Assinatura(Base):
    """O que cada usuário quer monitorar (tipo de doc + estado opcional)."""
    __tablename__ = "assinaturas"
    __table_args__ = (
        UniqueConstraint("usuario_id", "tipo", "estado", name="uq_assinatura"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    tipo: Mapped[str] = mapped_column(String(10))         # NFe, CTe, MDFe, NFCe
    estado: Mapped[str | None] = mapped_column(String(2)) # SP, RJ... None = todos

    usuario: Mapped["Usuario"] = relationship(back_populates="assinaturas")


class Notificacao(Base):
    """Registro de cada alerta enviado para evitar duplicatas."""
    __tablename__ = "notificacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    documento_id: Mapped[int] = mapped_column(ForeignKey("documentos.id"))
    canal: Mapped[str] = mapped_column(String(20))        # discord | telegram | email
    enviado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    usuario: Mapped["Usuario"] = relationship(back_populates="notificacoes")
    documento: Mapped["Documento"] = relationship(back_populates="notificacoes")
