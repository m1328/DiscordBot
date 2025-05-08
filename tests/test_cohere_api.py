import pytest
from unittest.mock import MagicMock
from src import cohere_api


@pytest.mark.asyncio
async def test_get_movie_recommendation_with_mock(monkeypatch):
    mock_response = MagicMock()
    mock_response.generations = [MagicMock(text='"Inception" – a great sci-fi movie.')]

    mock_client = MagicMock()
    mock_client.generate.return_value = mock_response

    monkeypatch.setattr(cohere_api, "get_cohere_client", lambda: mock_client)

    result = await cohere_api.get_movie_recommendation("sci-fi with a twist")
    assert "Inception" in result
