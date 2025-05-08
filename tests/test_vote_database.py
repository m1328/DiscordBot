import pytest
from src import vote_database

@pytest.mark.asyncio
async def test_add_and_get_top_movies(tmp_path):
    vote_database.DB_PATH = str(tmp_path / "votes.db")
    await vote_database.init_db()
    await vote_database.add_vote(1, "Test Movie")
    top = await vote_database.get_top_movies()
    assert top == [("Test Movie", 1)]
