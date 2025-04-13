FROM python:3.12-slim

WORKDIR /app

# najpierw requirements – dla lepszego cache'owania
COPY src/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# skopiuj cały folder src (czyli cały kod aplikacji)
COPY src/ ./src

# dodaj użytkownika
RUN addgroup --system bot && adduser --system --ingroup bot botuser
RUN chown -R botuser:bot /app
USER botuser

# uruchom bota
CMD ["python", "-m", "src.app"]
