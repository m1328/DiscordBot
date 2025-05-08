import aiosqlite

DB_PATH = "votes.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS votes (
                movie_id INTEGER PRIMARY KEY,
                title TEXT,
                votes INTEGER DEFAULT 0
            )
        """
        )
        await db.commit()


async def add_vote(movie_id, title):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO votes (movie_id, title, votes)
            VALUES (?, ?, 1)
            ON CONFLICT(movie_id) DO UPDATE SET votes = votes + 1
        """,
            (movie_id, title),
        )
        await db.commit()


async def get_top_movies(limit=3):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT title, votes FROM votes
            ORDER BY votes DESC
            LIMIT ?
        """,
            (limit,),
        )
        return await cursor.fetchall()
