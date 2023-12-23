from botomploy import app
from dotenv import load_dotenv
import asyncio

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(app.run())
