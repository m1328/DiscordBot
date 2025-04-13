import cohere
from src.config import COHERE_API_KEY

co = cohere.Client(COHERE_API_KEY)

async def get_movie_recommendation(prompt):
    response = co.generate(
        model="command-light",
        prompt=(
            f"You are a helpful movie recommendation bot.\n"
            f"Based on the following description from a user:\n"
            f"\"{prompt}\"\n"
            f"Recommend one existing, real movie title only – and explain briefly why it fits."
            f"\nStart your answer with the movie title in quotes."
        ),
        max_tokens=100,
        temperature=0.7
    )
    return response.generations[0].text.strip()


