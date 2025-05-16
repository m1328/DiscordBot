from src import tmdb_api
import random
import shlex
import asyncio
from src import vote_database
from src import cohere_api


def setup(bot):
    @bot.command()
    async def movie(ctx, *, query=None):
        """Pick a movie based on filters: !movie genre=Action year=2012 actor="Tom Hanks\" """
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
            director=filters.get("director"),
        )

        if not movies:
            await ctx.send("No movies found.")
            return

        movie = random.choice(movies)
        movie_id = movie["id"]
        details = tmdb_api.get_movie_details(movie_id)

        title = movie["title"]
        year = details.get("release_date", "????")[:4]
        genres = ", ".join([g["name"] for g in details.get("genres", [])]) or "Unknown"
        director = tmdb_api.get_movie_director(movie_id) or "Unknown"

        await ctx.send(
            f"**{title}**\n"
            f"Year: {year}\n"
            f"🎞Genre: {genres}\n"
            f"Director: {director}\n"
            f"https://www.themoviedb.org/movie/{movie_id}"
        )

    @bot.command(name="m1328_help")
    async def help_command(ctx):
        """Shows available commands and usage"""
        message = (
            "🎬 **MovieBot – Commands**\n\n"
            "**!movie** – Pick a random movie based on filters:\n"
            "`!movie genre=Comedy`\n"
            "`!movie year=2012`\n"
            '`!movie actor="Tom Hanks"`\n'
            '`!movie director="Christopher Nolan"`\n'
            '`!movie genre=Drama year=2000 actor="Tom Cruise"`\n'
            "**Available filters:** `genre`, `year`, `actor`, `director`\n"
            'If a value contains spaces, use quotes – e.g. `actor="Brad Pitt"`\n\n'
            '**!movieinfo "Movie Title"** – Show movie runtime and rating\n'
            '`!movieinfo "Inception"`\n'
            '`!movieinfo "The Godfather"`\n\n'
            "**!vote [filters]** – Vote for 1 of 3 random movies (1 minute)\n"
            "`!vote genre=Action year=2020`\n"
            "**!votes** – Show results of the most recent vote\n"
            "**!topmovies** – Show top 3 voted movies of all time\n\n"
            "**!recommend your description** – Get an AI-generated movie suggestion\n"
            "`!recommend I'm in the mood for a sci-fi with a twist`\n"
            "`!recommend I want a sad movie about family`\n\n"
            "**!m1328_help** – Show this help message\n"
        )
        await ctx.send(message)

    @bot.command()
    async def movieinfo(ctx, *, title):
        """Get info about a movie by title: !movieinfo "The Godfather" """
        movie = tmdb_api.search_movie_by_title(title)
        if not movie:
            await ctx.send("Movie not found.")
            return

        movie_id = movie["id"]
        details = tmdb_api.get_movie_details(movie_id)
        providers = tmdb_api.get_movie_watch_providers(movie_id)

        runtime = details.get("runtime", "Unknown")
        vote = details.get("vote_average", "?")
        vote_count = details.get("vote_count", "?")

        await ctx.send(
            f"**{movie['title']}**\n"
            f"Runtime: {runtime} min\n"
            f"Rating: {vote} ({vote_count} votes)\n"
            f"https://www.themoviedb.org/movie/{movie_id}"
        )

    @bot.command()
    async def vote(ctx, *, query=None):
        await vote_database.init_db()

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
            director=filters.get("director"),
        )

        if not movies or len(movies) < 3:
            await ctx.send("Not enough movies found for voting.")
            return

        choices = random.sample(movies, 3)
        emojis = ["🇦", "🇧", "🇨"]
        description = ""
        for i, movie in enumerate(choices):
            year = movie.get("release_date", "")[:4] or "Unknown"
            description += f"{emojis[i]} **{movie['title']}** ({year})\n"

        message = await ctx.send(
            f"**Vote for a movie!** (you have 1 minute)\n\n{description}"
        )
        for emoji in emojis:
            await message.add_reaction(emoji)

        await asyncio.sleep(60)  # 1 minute to vote

        message = await ctx.channel.fetch_message(message.id)
        user_votes = {}
        vote_counts = {}

        for i, emoji in enumerate(emojis):
            reaction = next(
                (r for r in message.reactions if str(r.emoji) == emoji), None
            )
            if not reaction:
                continue
            async for user in reaction.users():
                if user.bot:
                    continue
                if user.id in user_votes:
                    continue
                user_votes[user.id] = i
                vote_counts[i] = vote_counts.get(i, 0) + 1

        if not vote_counts:
            await ctx.send("No votes were cast.")
            return

        winner_index = max(vote_counts, key=vote_counts.get)
        winning_movie = choices[winner_index]
        await vote_database.add_vote(winning_movie["id"], winning_movie["title"])

        # Save last vote results
        ctx.bot.last_vote_results = {
            "message": message,
            "choices": choices,
            "vote_counts": vote_counts,
        }

        await ctx.send(
            f"The winner is **{winning_movie['title']}** with {vote_counts[winner_index]} votes!"
        )

    @bot.command()
    async def topmovies(ctx):
        await vote_database.init_db()
        top = await vote_database.get_top_movies()
        if not top:
            await ctx.send("No votes recorded yet.")
            return

        msg = "**Top Voted Movies:**\n"
        for i, (title, votes) in enumerate(top, 1):
            msg += f"{i}. {title} – {votes} votes\n"
        await ctx.send(msg)

    @bot.command()
    async def votes(ctx):
        results = getattr(ctx.bot, "last_vote_results", None)
        if not results:
            await ctx.send("No recent voting results available.")
            return

        msg = "**Last Voting Results:**\n"
        for i, movie in enumerate(results["choices"]):
            title = movie["title"]
            count = results["vote_counts"].get(i, 0)
            msg += f"{['🇦','🇧','🇨'][i]} {title} – {count} votes\n"
        await ctx.send(msg)

    @bot.command()
    async def recommend(ctx, *, prompt):
        """Get a movie recommendation based on your mood or preferences (via Cohere AI)"""
        await ctx.send("Thinking...")

        try:
            suggestion = await cohere_api.get_movie_recommendation(prompt)
            await ctx.send(f"🎬 **AI Suggests:**\n{suggestion}")
        except Exception as e:
            await ctx.send("Something went wrong while contacting Cohere.")
            print("Cohere error:", e)
