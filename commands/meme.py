import os

import discord
from discord.ext import commands
from discord import app_commands

import requests

from utils import scrapper

class Meme(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()
    
    async def buscar_meme(self):
        url = "https://meme-api.com/gimme/MemesBR"
        response = requests.get(url).json()
        meme_url = response['url']
        return meme_url

    @commands.command(name='meme', description='Envia um meme aleatório')
    async def documentos_prefix(self, ctx: commands.Context):
        value = await self.buscar_meme()
        await ctx.reply(value)
    
    @app_commands.command(name='meme', description='Envia um meme aleatório')
    async def documentos_slash(self, interaction: discord.Interaction):
        value = await self.buscar_meme()
        await interaction.response.send_message(value)

async def setup(bot):
    await bot.add_cog(Meme(bot))