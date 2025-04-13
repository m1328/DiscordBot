# 🎬 Discord MovieBot (Python + Docker)

This is a Discord bot that:
- Recommends movies based on genre, year, actor, or director (`!movie`)
- Fetches movie info like runtime and rating (`!movieinfo`)
- Suggests a movie using AI (`!recommend`)
- Allows users to vote on movies (`!vote`)
- Tracks top-voted movies (`!topmovies`)

---

## 🐳 Run with Docker

### 📁 Project Structure

```
DiscordBot/
├── src/
│   ├── app.py
│   ├── commands.py
│   ├── cohere_api.py
│   ├── tmdb_api.py
│   ├── vote_database.py
│   └── config.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env          ← your secrets (NOT pushed to repo!)
├── README.md
```

---

## 🔐 .env example

Stwórz plik `.env` w katalogu głównym:

```
DISCORD_TOKEN=your_token_here
TMDB_API_KEY=your_tmdb_api_key
COHERE_API_KEY=your_cohere_api_key
```

---

## 🔧 Build the image

```bash
docker build -t moviebot .
```

---

## ▶️ Run the bot

```bash
docker run --env-file .env moviebot
```

---

## 🐳 Dockerfile (używany do budowy)

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

## 📂 .dockerignore

```dockerignore
.venv/
__pycache__/
.env
*.pyc
votes.db
.git/
```

---

## 📦 Useful Docker Commands

```bash
docker ps -a              # List containers
docker images             # List images
docker rm <container>     # Remove a container
docker rmi <image>        # Remove an image
docker builder prune -af  # Clean up cache
```

---

## 🧪 Test Locally Without Docker

```bash
python -m src.app
```

---

## ✅ Ready!

Bot is now containerized, portable, and ready for local or cloud deployment 🚀
