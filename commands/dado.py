import discord
from discord.ext import commands
from discord import app_commands

import random

from utils import scrapper

class Dado(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()
    
    async def rolar_dado(self):
        valor = random.randint(1, 20)
        if valor == 1:
            return f"Você tirou 1! Que azar! 🎲"
        elif valor == 20:
            return f"Você tirou 20! Que sorte! 🎲"
        else:
            return f"Você tirou {valor}! 🎲"

    @commands.command(name='dado', description='Rola um dado D20')
    async def documentos_prefix(self, ctx: commands.Context):
        value = await self.rolar_dado()
        await ctx.reply(value)
    
    @app_commands.command(name='dado', description='Rola um dado D20')
    async def documentos_slash(self, interaction: discord.Interaction):
        value = await self.rolar_dado()
        await interaction.response.send_message(value)

async def setup(bot):
    await bot.add_cog(Dado(bot))