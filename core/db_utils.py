import asyncmy

from dotenv import load_dotenv
import os
from typing import Optional, Union, Any, Tuple, List, TypeAlias


SQLParams: TypeAlias = Optional[Tuple[Any, ...]]
SQLResult: TypeAlias = Union[None, Tuple, List[Tuple]]

load_dotenv()

async def get_db_connection() -> asyncmy.Connection:
    return await asyncmy.connect(
        host=os.getenv("host", "localhost"),
        port=os.getenv("port", 3306),
        user=os.getenv("user", "root"),
        password=os.getenv("password", ""),
        database=os.getenv("database", "")
    )
    

async def execute_update(query: str, params: SQLParams = None) -> None:
    db = await get_db_connection()
    try:
        async with db.cursor() as cursor:
            await cursor.execute(query, params or ())
            await db.commit()
    except Exception as e:
        print(f"Error executing update: {e}")
    finally:
        await db.ensure_closed()

async def fetch_one(query: str, params: SQLParams = None) -> SQLResult:
    db = await get_db_connection()
    try:
        async with db.cursor() as cursor:
            await cursor.execute(query, params or ())
            return await cursor.fetchone()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    finally:
        await db.ensure_closed()

async def fetch_all(query: str, params: SQLParams = None) -> SQLResult:
    db = await get_db_connection()
    try:
        async with db.cursor() as cursor:
            await cursor.execute(query, params or ())
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    finally:
        await db.ensure_closed()
