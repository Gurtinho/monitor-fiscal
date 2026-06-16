import dotenv
dotenv.load_dotenv()  # deve rodar antes de qualquer import que leia os.getenv()

import discord
import asyncio
import uvicorn
import os

from platforms.discord.bot import ModBot
from services import repository
from fastapi import FastAPI

bot = ModBot()
app = FastAPI()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('SERVER_ID')
ENVIRONMENT = os.getenv('ENVIRONMENT')

# Carrega as extensões (cogs) de comandos e eventos do Discord
async def load_extensions():
    commands_count, events_count = 0, 0
    for folder in ['commands', 'events']:
        path = f'platforms/discord/{folder}'
        if os.path.exists(path):
            for f in os.listdir(path):
                if f.endswith('.py') and not f.startswith('_'):
                    await bot.load_extension(f'platforms.discord.{folder}.{f[:-3]}')
                    if folder == 'commands':
                        commands_count += 1
                    else:
                        events_count += 1
    return commands_count, events_count

@bot.event
async def on_ready():
    if GUILD_ID and ENVIRONMENT == "dev":
        guild = discord.Object(id=int(GUILD_ID))
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
    else:
        await bot.tree.sync()
    print(f"🚀 {bot.user} is online and ready!")

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "online", "bot": str(bot.user)}

@app.get("/status")
async def status():
    return {"status": "online", "bot": str(bot.user)}

async def main():
    # Inicia o banco de dados
    await repository.init_db()

    commands_count, events_count = await load_extensions()
    print(f"Loaded {commands_count} commands and {events_count} events.")

    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)

    # Inicia o servidor e demais tarefas
    await asyncio.gather(
        server.serve(),
        bot.start(TOKEN)
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
