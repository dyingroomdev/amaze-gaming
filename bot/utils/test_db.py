import aiosqlite
import asyncio
import os

DB_PATH = "bot/data/amaze_gaming.db"

async def test():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY)")
        await db.commit()
        print("DB connection success")

asyncio.run(test())
