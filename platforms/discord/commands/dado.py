import discord
from discord.ext import commands
from discord import app_commands
import random

class Dado(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    async def rolar_dado(self):
        valor = random.randint(1, 20)
        if valor == 1:
            return "Você tirou 1! Que azar! 🎲"
        elif valor == 20:
            return "Você tirou 20! Que sorte! 🎲"
        return f"Você tirou {valor}! 🎲"

    @commands.command(name='dado', description='Rola um dado D20')
    async def dado_prefix(self, ctx: commands.Context):
        await ctx.reply(await self.rolar_dado())

    @app_commands.command(name='dado', description='Rola um dado D20')
    async def dado_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(await self.rolar_dado())

async def setup(bot):
    await bot.add_cog(Dado(bot))
