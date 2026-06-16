import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import discord

from platforms.discord.commands.dado import Dado


# Diz pro pytest-asyncio rodar todos os testes async desse arquivo no modo auto
pytestmark = pytest.mark.asyncio(loop_scope="session")


# ─── Fixtures ─────────────────────────────────────────────────────────────────
#
# Fixtures são funções que preparam objetos reutilizáveis entre testes.
# Em vez de criar um bot_falso em cada teste, declara uma vez aqui.

@pytest.fixture
def bot_falso():
    return MagicMock(spec=discord.ext.commands.Bot)

@pytest.fixture
def interaction_falsa():
    """Simula um discord.Interaction completo."""
    interaction = MagicMock(spec=discord.Interaction)
    interaction.response = MagicMock()
    interaction.response.send_message = AsyncMock()   # async → AsyncMock
    interaction.response.edit_message = AsyncMock()
    interaction.followup = MagicMock()
    interaction.followup.send = AsyncMock()
    return interaction

@pytest.fixture
def ctx_falso():
    """Simula um commands.Context (prefix command)."""
    ctx = MagicMock()
    ctx.reply = AsyncMock()
    ctx.send = AsyncMock()
    return ctx


# ─── Dado ─────────────────────────────────────────────────────────────────────

async def test_rolar_dado_retorna_string_com_emoji(bot_falso):
    cog = Dado(bot=bot_falso)
    resultado = await cog.rolar_dado()

    assert isinstance(resultado, str)
    assert "🎲" in resultado

async def test_rolar_dado_valor_entre_1_e_20(bot_falso):
    cog = Dado(bot=bot_falso)

    # Roda várias vezes pra garantir que nunca sai do range
    for _ in range(50):
        resultado = await cog.rolar_dado()
        # Extrai o número da string "Você tirou 15! 🎲"
        numeros = [int(s) for s in resultado.split() if s.isdigit()]
        if numeros:
            assert 1 <= numeros[0] <= 20

async def test_dado_slash_chama_send_message(bot_falso, interaction_falsa):
    cog = Dado(bot=bot_falso)

    # Os decorators @app_commands.command e @commands.command envolvem o método
    # num objeto Command — pra chamar a função real nos testes, usa .callback
    await cog.dado_slash.callback(cog, interaction_falsa)

    interaction_falsa.response.send_message.assert_called_once()

async def test_dado_slash_resposta_contem_emoji(bot_falso, interaction_falsa):
    cog = Dado(bot=bot_falso)
    await cog.dado_slash.callback(cog, interaction_falsa)

    mensagem_enviada = interaction_falsa.response.send_message.call_args[0][0]
    assert "🎲" in mensagem_enviada

async def test_dado_prefix_chama_reply(bot_falso, ctx_falso):
    cog = Dado(bot=bot_falso)
    await cog.dado_prefix.callback(cog, ctx_falso)

    ctx_falso.reply.assert_called_once()