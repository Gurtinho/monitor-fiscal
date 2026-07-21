import dotenv
dotenv.load_dotenv()

import os
import discord
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('SERVER_ID')
ENVIRONMENT = os.getenv('ENVIRONMENT')

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents=discord.Intents.all())


    # Carrega os comandos e eventos
    async def load_extensions(self):
        commands_count, events_count = 0, 0
        for folder in ('commands', 'events'):
            path = f'platforms/discord/{folder}'
            if os.path.exists(path):
                for f in os.listdir(path):
                    if f.endswith('.py') and not f.startswith('_'):
                        await self.load_extension(f'platforms.discord.{folder}.{f[:-3]}')
                        if folder == 'commands':
                            commands_count += 1
                        else:
                            events_count += 1
        return commands_count, events_count
    

    # Carrega a função acima automaticamente usando o discord.py
    async def setup_hook(self):
        commands_count, events_count = await self.load_extensions()
        print(f"Loaded {commands_count} commands and {events_count} events.")

        if GUILD_ID and ENVIRONMENT == "dev":
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()


    # Comando start do bot
    async def start(self):
        await super().start(TOKEN)


    # Inicia o evento de prontidão
    async def on_ready(self):
        print(f"🚀 {self.user} is online and ready!")