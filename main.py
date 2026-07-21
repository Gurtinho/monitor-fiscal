import dotenv
dotenv.load_dotenv()  # deve rodar antes de qualquer import que leia os.getenv()

import discord
import asyncio
import uvicorn
import os

from fastapi import FastAPI
from platforms.discord.bot import DiscordBot
from services import repository
from utils.jobs import scheduler, configurar_jobs
from app import app

# Inicia os bots
bot = DiscordBot()

async def main():
    # Inicia o banco de dados
    await repository.init_db()

    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    
    # jobs
    configurar_jobs()
    scheduler.start()

    # Inicia o servidor e demais tarefas
    await asyncio.gather(
        server.serve(),
        bot.start(),
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
