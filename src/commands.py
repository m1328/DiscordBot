from src import tmdb_api
import random
import shlex

def setup(bot):
    @bot.command()
    async def movie(ctx, *, query=None):
        """Pick a movie based on filters: !movie genre=Action year=2012 actor="Tom Hanks\""""
        filters = {}
        if query:
            args = shlex.split(query)
            for pair in args:
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    filters[k.lower()] = v

        movies = tmdb_api.search_movies(
            genre=filters.get("genre"),
            year=filters.get("year"),
            actor=filters.get("actor"),
            director=filters.get("director")
        )

        if not movies:
            await ctx.send("❌ No movies found.")
            return

        movie = random.choice(movies)
        movie_id = movie["id"]
        details = tmdb_api.get_movie_details(movie_id)

        title = movie["title"]
        year = details.get("release_date", "????")[:4]
        genres = ", ".join([g["name"] for g in details.get("genres", [])]) or "Unknown"
        director = tmdb_api.get_movie_director(movie_id) or "Unknown"

        await ctx.send(
            f"🎬 **{title}**\n"
            f"📅 Year: {year}\n"
            f"🎞️ Genre: {genres}\n"
            f"🎬 Director: {director}\n"
            f"🔗 https://www.themoviedb.org/movie/{movie_id}"
        )

    @bot.command(name="m1328_help")
    async def help_command(ctx):
        """Shows available commands and usage"""
        message = (
            "🎬 **MovieBot – Commands**\n\n"
            "**!movie** – Pick a movie based on your filters:\n"
            "`!movie genre=Comedy`\n"
            "`!movie year=2012`\n"
            "`!movie actor=\"Tom Hanks\"`\n"
            "`!movie director=\"Christopher Nolan\"`\n"
            "`!movie genre=Drama year=2000 actor=\"Tom Cruise\"`\n\n"
            "**Available filters:** `genre`, `year`, `actor`, `director`\n"
            "If a value contains spaces, use quotes – e.g. `actor=\"Brad Pitt\"`\n\n"
            "**!m1328_help** – Show this help message.\n"
        )
        await ctx.send(message)
