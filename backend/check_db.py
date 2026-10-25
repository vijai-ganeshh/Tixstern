
import asyncio
from sqlalchemy import text
from app.db.session import engine


async def main():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT current_database(), current_user"))
            database, user = result.one()
            print(f"Connected successfully! Database: {database}, User: {user}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
