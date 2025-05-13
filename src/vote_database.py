import asyncpg
import os

DB_CONFIG = {
    "user": os.getenv("POSTGRES_USER", "botuser"),
    "password": os.getenv("POSTGRES_PASSWORD", "botpass"),
    "database": os.getenv("POSTGRES_DB", "botdb"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
}


async def get_connection():
    return await asyncpg.connect(**DB_CONFIG)


async def init_db():
    conn = await get_connection()
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            movie_id INTEGER PRIMARY KEY,
            title TEXT,
            votes INTEGER DEFAULT 0
        )
    """)
    await conn.close()


async def add_vote(movie_id, title):
    conn = await get_connection()
    await conn.execute("""
        INSERT INTO votes (movie_id, title, votes)
        VALUES ($1, $2, 1)
        ON CONFLICT (movie_id) DO UPDATE SET votes = votes + 1
    """, movie_id, title)
    await conn.close()


async def get_top_movies(limit=3):
    conn = await get_connection()
    rows = await conn.fetch("""
        SELECT title, votes FROM votes
        ORDER BY votes DESC
        LIMIT $1
    """, limit)
    await conn.close()
    return rows
