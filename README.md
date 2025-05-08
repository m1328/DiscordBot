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
## Project Structure
```text
.
├── src/
│ ├── app.py
│ ├── commands.py
│ ├── cohere_api.py
│ ├── tmdb_api.py
│ ├── vote_database.py
│ └── ...
├── tests/
│ ├── test_tmdb_api.py
│ ├──test_cohere_api.py
│ └──test_integration_commands.py
├── .env
├── requirements.txt
├── azure-pipelines.yml
├── Dockerfile
└── README.md
```
---
## Running Locally
1. Clone repo and set your `.env` file:
```token
DISCORD_TOKEN=your_token_here
TMDB_API_KEY=your_tmdb_key
COHERE_API_KEY=your_cohere_key
```
### Where to get the API keys:

- **DISCORD_TOKEN** → [Discord Developer Portal](https://discord.com/developers/applications) → Create application → Bot → Token  
- **TMDB_API_KEY** → [TMDb Developer Portal](https://developer.themoviedb.org/) → Create account → Request API key  
- **COHERE_API_KEY** → [Cohere Platform](https://cohere.com/) → Sign up → View API key under dashboard


2. Install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r src/requirements.txt
```
3. Run the bot:
```commandline
python src/app.py
```
4. Run tests:
- The project includes both unit and integration tests.
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
## Docker

Build and run locally:

```bash
docker build -t moviebot .
docker run --env-file .env moviebot
```
---
## Azure DevOps CI/CD
- Automated test and Docker build pipeline.
- YAML pipeline defined in `azure-pipelines.yaml`.
---
This project is for educational use
