import pytest
import discord
from discord.ext.commands import Bot
from unittest.mock import AsyncMock, MagicMock
from src import commands

@pytest.mark.asyncio
async def test_movie_command_integration(monkeypatch):
    intents = discord.Intents.default()
    bot = Bot(command_prefix="!", intents=intents)
    commands.setup(bot)

    ctx = MagicMock()
    ctx.send = AsyncMock()

    monkeypatch.setattr("src.tmdb_api.search_movies", lambda **kwargs: [{"id": 1, "title": "Test Movie"}])
    monkeypatch.setattr("src.tmdb_api.get_movie_details", lambda movie_id: {
        "release_date": "2022-01-01",
        "genres": [{"name": "Drama"}]
    })
    monkeypatch.setattr("src.tmdb_api.get_movie_director", lambda movie_id: "Director X")

    await bot.get_command("movie")(ctx, query="genre=Drama")

    ctx.send.assert_called()
