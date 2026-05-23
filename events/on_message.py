import discord
from discord.ext import commands

import random

class OnMessage(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
      
        if 'kkk' in message.content.lower():
            if random.randint(1, 3) == 1:
                await message.add_reaction('🤣')

        # Validar o diário dos devs e suporte
      
async def setup(bot: commands.Bot):
    await bot.add_cog(OnMessage(bot))