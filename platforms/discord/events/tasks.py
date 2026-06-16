import discord
from discord.ext import tasks, commands
import datetime
import pytz
import os
import utils.log as log

from services import monitor, notifier
from config import links

FUSO = pytz.timezone('America/Sao_Paulo')
HORARIO_BOM_DIA = datetime.time(hour=8, minute=0, tzinfo=FUSO)
HORARIO_VERIFICACAO = datetime.time(hour=8, minute=5, tzinfo=FUSO)

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        notifier.registrar("discord", self._enviar_alerta)
        self.bom_dia.start()
        self.verificar_nts.start()

    def cog_unload(self):
        self.bom_dia.cancel()
        self.verificar_nts.cancel()

    async def _enviar_alerta(self, tipo: str, documentos: list):
        canal_id = os.getenv("CHANNEL_ID")
        if not canal_id:
            return
        channel = self.bot.get_channel(int(canal_id))
        if not channel:
            log.logging.warning("Canal não encontrado. Verifique o CHANNEL_ID!")
            return

        embed = discord.Embed(
            title=f"🚨 Novos documentos fiscais - {tipo}",
            description=f"{len(documentos)} novo(s) documento(s) encontrado(s)!",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        for doc in documentos:
            embed.add_field(name=doc['texto'], value=doc['url'].replace(" ", ""), inline=False)

        await channel.send(embed=embed)

    @tasks.loop(time=HORARIO_BOM_DIA)
    async def bom_dia(self):
        canal_id = os.getenv("CHANNEL_ID")
        if not canal_id:
            return
        channel = self.bot.get_channel(int(canal_id))
        if channel:
            await channel.send("☀️ Bom dia! Mandem o resumo de ontem e o que farão hoje!")

    @tasks.loop(time=HORARIO_VERIFICACAO)
    async def verificar_nts(self):
        log.logging.info("Iniciando verificação de notas técnicas...")
        novos = await monitor.verificar_atualizacoes(links.URLS_NOTAS_TECNICAS)
        if novos:
            await notifier.notificar_todos(novos)
        else:
            log.logging.info("Nenhuma novidade encontrada.")

    @bom_dia.before_loop
    async def before_bom_dia(self):
        await self.bot.wait_until_ready()

    @verificar_nts.before_loop
    async def before_verificar(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Tasks(bot))
