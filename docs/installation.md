# Installation

## 1. Clone the repository
```bash
git clone <your-repo-url>
cd DiscordBot
```

## 2. Create `.env` file
```env
DISCORD_TOKEN=your_token_here
TMDB_API_KEY=your_tmdb_key
COHERE_API_KEY=your_cohere_key
```

## 3. Set up a virtual environment
```bash
python -m venv venv
```

**On Windows:**
```bash
.\venv\Scripts\activate
```

**On Linux/Mac:**
```bash
source venv/bin/activate
```

## 4. Install dependencies
```bash
pip install -r src/requirements.txt
```

## 5. Run the bot
```bash
python src/app.py
```

## 6. Run tests
```bash
pytest tests/
black --check src/
```
