from fastapi import FastAPI

app = FastAPI()

# Rotas
@app.get("/healthcheck")
async def healthcheck():
    return {"status": "online", "bot": str(bot.user)}

@app.get("/status")
async def status():
    return {"status": "online", "bot": str(bot.user)}