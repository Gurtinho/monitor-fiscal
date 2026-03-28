import discord
import dotenv
import os
from bot import ModBot

def main():
    # Carregamento de env
    dotenv.load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = os.getenv('SERVER_ID')
    ENVIRONMENT = os.getenv('ENVIRONMENT')

    bot = ModBot()

    # Carrega os módulos
    async def load_extensions():
        commands: int = 0
        events: int = 0

        if os.path.exists('commands'):
            for command in os.listdir('commands'):
                if command.endswith('.py'): # Carrega somente arquivos python
                    commands += 1
                    await bot.load_extension(f'commands.{command[:-3]}') # Pegando arquivo sem a extensão

        if os.path.exists('events'):
            for event in os.listdir('events'):
                if event.endswith('.py'): # Carrega somente arquivos python
                    events += 1
                    await bot.load_extension(f'events.{event[:-3]}') # Pegando arquivo sem a extensão
            
        return commands, events

    # Evento principal
    @bot.event
    async def on_ready():
        commands, events = await load_extensions()

        if GUILD_ID and ENVIRONMENT == "dev":
            guild = discord.Object(id=GUILD_ID)
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
        else:
            await bot.tree.sync()
        
        CHANNEL_ID = os.getenv('CHANNEL_ID')
        if CHANNEL_ID:
            channel = bot.get_channel(int(CHANNEL_ID)) # Busca o canal pelo ID
            if channel:
                await channel.send(f"🚀 **Estou pronto pra te ajudar!**\n📦 Comandos: {commands}\n🔔 Eventos: {events}")


    bot.run(TOKEN)

if __name__ == "__main__":
    main()