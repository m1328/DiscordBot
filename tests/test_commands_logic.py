import pytest
import discord
from discord.ext.commands import Bot
from unittest.mock import AsyncMock, MagicMock
from src import commands


@pytest.mark.asyncio
async def test_topmovies_command(monkeypatch):
    intents = discord.Intents.default()
    bot = Bot(command_prefix="!", intents=intents)
    commands.setup(bot)

    ctx = MagicMock()
    ctx.send = AsyncMock()

    monkeypatch.setattr("src.vote_database.init_db", AsyncMock())
    monkeypatch.setattr(
        "src.vote_database.get_top_movies", AsyncMock(return_value=[("Inception", 3)])
    )

    await bot.get_command("topmovies")(ctx)
    ctx.send.assert_called_once()
    assert "Inception" in ctx.send.call_args[0][0]
