import discord
import asyncio
import uvicorn
import dotenv
import os
from bot import ModBot
from fastapi import FastAPI

bot = ModBot()
app = FastAPI()

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('SERVER_ID')
ENVIRONMENT = os.getenv('ENVIRONMENT')

async def load_extensions():
    commands, events = 0, 0
    if os.path.exists('commands'):
        for command in os.listdir('commands'):
            if command.endswith('.py'):
                commands += 1
                await bot.load_extension(f'commands.{command[:-3]}')

    if os.path.exists('events'):
        for event in os.listdir('events'):
            if event.endswith('.py'):
                events += 1
                await bot.load_extension(f'events.{event[:-3]}')
    return commands, events

@bot.event
async def on_ready():
    if GUILD_ID and ENVIRONMENT == "dev":
        guild = discord.Object(id=int(GUILD_ID))
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
    else:
        await bot.tree.sync()
    
    print(f"🚀 {bot.user} is online and ready!")

# rotas da api
@app.get("/healthcheck")
async def healthcheck():
    return {"status": "online", "bot": str(bot.user)}

@app.get("/status")
async def status():
    return {"status": "online", "bot": str(bot.user), "commands": len(bot.commands), "events": len(bot.events)}

@app.get("/commands")
async def commands():
    return {"commands": [command.name for command in bot.commands]}

@app.get("/events")
async def events():
    return {"events": [event.name for event in bot.events]}

@app.get("/guilds")
async def guilds():
    return {"guilds": [guild.name for guild in bot.guilds]}

async def main():
    # Carregar tudo primeiro
    commands, events = await load_extensions()
    print(f"Loaded {commands} commands and {events} events.")

    # API do bot
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)

    # Startando tudo
    await asyncio.gather(
        server.serve(),
        bot.start(TOKEN) 
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Prevents messy errors when you press Ctrl+C
        pass