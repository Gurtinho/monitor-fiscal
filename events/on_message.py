import discord
from discord.ext import commands
from discord import app_commands

import random

class OnMessage(commands.Cog):

    RESPOSTAS_PALAVRAO = [
        "Opa! Olha o nível do chat, vamos manter a classe. 🧐",
        "Linguagem inadequada detectada. Encontrei sujeira no chat! ⛏️",
        "Vixi, o clima pesou. Que tal a gente voltar a falar de trabalho?",
        "Falar essas coisas não ajuda na produtividade. ⚠️",
        "Minha IA foi treinada com bons modos, tente o mesmo! 🤖",
        "Cuidado com as palavras, tem gente trabalhando aqui. (ou quase isso) 👹",
        "Xingar não vai fazer o sistema andar mais rápido, infelizmente. 📉"
    ]

    PALAVRAS_INADEQUADAS = [
        "pica",
        "pika",
        "piroca",
        "piroka",
        "puta",
        "caralho",
        "foda-se",
        "merda",
        "porra",
        "cacete",
        "viado",
        "bosta",
        "cu",
        "cuzão",
        "buceta",
        "pau",
        "xoxota"
    ]

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
    
        # por enquanto não é viável
        # for palavra in self.PALAVRAS_INADEQUADAS:
        #     if palavra in message.content.lower():
        #         if random.randint(1, 3) == 1:
        #             await message.channel.send(f'{message.author.mention}, {random.choice(self.RESPOSTAS_PALAVRAO)}')
        #         break
      
        if 'kkk' in message.content.lower():
            if random.randint(1, 3) == 1:
                await message.add_reaction('🤣')

        # validar o diário dev todos os dias e salvar no gist
      
async def setup(bot: commands.Bot):
    await bot.add_cog(OnMessage(bot))