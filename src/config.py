import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

print(f"TMDB_API_KEY = {TMDB_API_KEY}")
