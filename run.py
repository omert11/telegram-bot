import uvicorn
from bot.api.app import app

if __name__ == "__main__":
    uvicorn.run("bot.api.app:app", host="0.0.0.0", port=8000, reload=True)
