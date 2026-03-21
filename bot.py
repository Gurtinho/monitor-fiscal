import discord
from discord.ext import commands
from components.view_welcome import ViewWelcome

# Bot modificado pra aceitar o uso de botões e recursos mesmo depois de reiniciado
# Usando POO pra acessar os dados da classe pai Bot
class ModBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents = discord.Intents.all())

    async def setup_hook(self) -> None:
        self.add_view(ViewWelcome())