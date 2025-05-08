import pytest
import discord
from unittest.mock import AsyncMock, MagicMock
from discord.ext.commands import Bot
from src import commands

intents = discord.Intents.default()


@pytest.mark.asyncio
async def test_movie_command_with_genre(monkeypatch):
    bot = Bot(command_prefix="!", intents=intents)
    commands.setup(bot)

    mock_ctx = MagicMock()
    mock_ctx.send = AsyncMock()

    fake_movie = {"id": 1, "title": "Action Movie"}
    fake_details = {"genres": [{"name": "Action"}], "release_date": "2020-01-01"}

    monkeypatch.setattr("src.tmdb_api.search_movies", lambda **kwargs: [fake_movie])
    monkeypatch.setattr("src.tmdb_api.get_movie_details", lambda movie_id: fake_details)
    monkeypatch.setattr(
        "src.tmdb_api.get_movie_director", lambda movie_id: "Director X"
    )

    command = bot.get_command("movie")
    await command.callback(mock_ctx, query="genre=Action")

    mock_ctx.send.assert_called_once()
    assert "Action Movie" in mock_ctx.send.call_args[0][0]


@pytest.mark.asyncio
async def test_movieinfo_with_real_input(monkeypatch):
    bot = Bot(command_prefix="!", intents=intents)
    commands.setup(bot)

    mock_ctx = MagicMock()
    mock_ctx.send = AsyncMock()

    monkeypatch.setattr(
        "src.tmdb_api.search_movie_by_title",
        lambda title: {"id": 42, "title": "Inception"},
    )
    monkeypatch.setattr(
        "src.tmdb_api.get_movie_details",
        lambda movie_id: {"runtime": 148, "vote_average": 9.0, "vote_count": 10000},
    )
    monkeypatch.setattr("src.tmdb_api.get_movie_watch_providers", lambda movie_id: {})

    command = bot.get_command("movieinfo")
    await command.callback(mock_ctx, title="Inception")

    mock_ctx.send.assert_called_once()
    assert "Inception" in mock_ctx.send.call_args[0][0]


@pytest.mark.asyncio
async def test_vote_too_few_movies(monkeypatch):
    bot = Bot(command_prefix="!", intents=intents)
    commands.setup(bot)

    mock_ctx = MagicMock()
    mock_ctx.send = AsyncMock()
    mock_ctx.bot = bot

    monkeypatch.setattr("src.vote_database.init_db", AsyncMock())
    monkeypatch.setattr(
        "src.tmdb_api.search_movies",
        lambda **kwargs: [{"id": 1, "title": "Solo Movie"}],
    )

    command = bot.get_command("vote")
    await command.callback(mock_ctx, query="genre=Drama")

    mock_ctx.send.assert_called_once()
    assert "Not enough movies" in mock_ctx.send.call_args[0][0]
