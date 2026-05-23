import discord
from discord.ext import tasks, commands
import datetime
import pytz
import os
import utils.log as log

# Define o fuso horário fora da classe para ser usado nos decoradores
FUSO = pytz.timezone('America/Sao_Paulo')

HORARIO_BOM_DIA = datetime.time(hour=5, minute=51, tzinfo=FUSO) # 08:00

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.garimpar_dados.start() # Inicia a tarefa quando o Cog carrega

    def cog_unload(self):
        self.garimpar_dados.cancel() # Para a tarefa se o bot desligar

    # Configura para rodar todo dia às 09:00 no fuso do Brasil (BRT/BRST)
    @tasks.loop(time=HORARIO_BOM_DIA)
    # @tasks.loop(seconds=10.0)
    async def garimpar_dados(self):
        CANAL_ID = os.getenv("CHANNEL_ID")
        channel = self.bot.get_channel(CANAL_ID)

        if channel:
            await channel.send("☀️ Bom dia! Mandem o resumo de ontem e o que farão hoje!")
        else:
            log.logging.info("Canal não encontrado. Verifique o ID!")

    @garimpar_dados.before_loop
    async def before_garimpar(self):
        await self.bot.wait_until_ready() # Espera o bot logar antes de rodar

async def setup(bot):
    await bot.add_cog(Tasks(bot))