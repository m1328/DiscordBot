# 🎬 Discord MovieBot

A Discord bot for personalized movie recommendations, streaming info, and community voting – built with Python, TMDb API, Cohere AI, and Docker.

## Features

- `!movie genre=Action year=2020 actor="Tom Hanks"` – Search for a movie based on filters.
- `!movieinfo "Inception"` – Get runtime and rating of a movie.
- `!vote genre=Comedy` – Let users vote on 3 random movies and save the winner.
- `!votes` – Show the latest voting results.
- `!topmovies` – View the top 3 most-voted movies.
- `!recommend I'm in the mood for a sci-fi with a twist` – Get movie recommendations using AI.
- `!m1328_help` – Show help and usage instructions.
## AI Integration
Uses [Cohere](https://cohere.com/) to generate intelligent recommendations based on prompts like:
- `!recommend something like Interstellar but more psychological`
---

## Technologies

- Python 3.12
- discord.py
- TMDb API
- Cohere AI
- SQLite (for votes)
- Docker
- Azure DevOps Pipelines (CI/CD)

---

## Docker

Build and run locally:

```bash
docker build -t moviebot .
docker run --env-file .env moviebot
```

---
## Environment Variables
Create a .env file with:
```token
DISCORD_TOKEN=your_token_here
TMDB_API_KEY=your_tmdb_key
COHERE_API_KEY=your_cohere_key
```

### Where to get the API keys:

- **DISCORD_TOKEN** → [Discord Developer Portal](https://discord.com/developers/applications) → Create application → Bot → Token  
- **TMDB_API_KEY** → [TMDb Developer Portal](https://developer.themoviedb.org/) → Create account → Request API key  
- **COHERE_API_KEY** → [Cohere Platform](https://cohere.com/) → Sign up → View API key under dashboard

---
## Testing
```testing
pytest tests/
black --check src/
```
---

## Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY src/requirements.txt .
RUN pip install -r requirements.txt

COPY src /app/src
COPY .env /app/.env

CMD ["python", "-m", "src.app"]
```
---
## Azure DevOps CI/CD
- Automated test and Docker build pipeline.
- YAML pipeline defined in `azure-pipelines.yaml`.
---
This project is for educational use
