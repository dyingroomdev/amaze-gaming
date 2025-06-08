import discord
from discord.ext import commands
import random
import aiohttp

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.eight_ball_answers = [
            "It is certain.", "Without a doubt.", "You may rely on it.",
            "Ask again later.", "Better not tell you now.",
            "Don't count on it.", "My reply is no.", "Very doubtful."
        ]
        self.wyr_questions = [
            "Would you rather be invisible or be able to fly?",
            "Would you rather live without music or without TV?",
            "Would you rather explore space or the ocean?",
            # Add more questions here
        ]
        self.truths = [
            "What is your biggest fear?",
            "Have you ever lied to your best friend?",
            "What is your secret talent?",
            # Add more truths here
        ]
        self.dares = [
            "Do 10 push-ups right now.",
            "Sing a song in the voice channel.",
            "Post a funny meme in the chat.",
            # Add more dares here
        ]

    async def fetch_json(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return None

    @commands.command(name="meme")
    async def meme(self, ctx):
        """Sends a random meme from Reddit."""
        url = "https://meme-api.com/gimme"
        data = await self.fetch_json(url)
        if data and 'url' in data:
            embed = discord.Embed(title=data.get("title", "Meme"), color=discord.Color.blue())
            embed.set_image(url=data["url"])
            embed.set_footer(text=f"From r/{data.get('subreddit', 'memes')}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Could not fetch meme right now, try again later.")

    @commands.command(name="dog")
    async def dog(self, ctx):
        """Sends a random dog picture."""
        url = "https://dog.ceo/api/breeds/image/random"
        data = await self.fetch_json(url)
        if data and data.get("status") == "success":
            embed = discord.Embed(title="Random Dog 🐶", color=discord.Color.orange())
            embed.set_image(url=data["message"])
            await ctx.send(embed=embed)
        else:
            await ctx.send("Could not fetch dog image right now.")

    @commands.command(name="cat")
    async def cat(self, ctx):
        """Sends a random cat picture."""
        url = "https://api.thecatapi.com/v1/images/search"
        data = await self.fetch_json(url)
        if data and len(data) > 0 and "url" in data[0]:
            embed = discord.Embed(title="Random Cat 🐱", color=discord.Color.purple())
            embed.set_image(url=data[0]["url"])
            await ctx.send(embed=embed)
        else:
            await ctx.send("Could not fetch cat image right now.")

    @commands.command(name="trivia")
    async def trivia(self, ctx):
        """Sends a random trivia question."""
        url = "https://opentdb.com/api.php?amount=1&type=multiple"
        data = await self.fetch_json(url)
        if data and data.get("results"):
            q = data["results"][0]
            question = discord.utils.escape_markdown(q["question"])
            correct = q["correct_answer"]
            options = q["incorrect_answers"] + [correct]
            random.shuffle(options)
            embed = discord.Embed(title="Trivia Time!", description=question, color=discord.Color.green())
            for idx, opt in enumerate(options, start=1):
                embed.add_field(name=f"Option {idx}", value=opt, inline=False)
            embed.set_footer(text="Type the option number as your answer!")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't get a trivia question right now.")

    @commands.command(name="8ball")
    async def eightball(self, ctx, *, question: str):
        """Magic 8-Ball answers your yes/no question."""
        answer = random.choice(self.eight_ball_answers)
        embed = discord.Embed(title="🎱 Magic 8-Ball", description=answer, color=discord.Color.teal())
        embed.set_footer(text=f"Question: {question}")
        await ctx.send(embed=embed)

    @commands.command(name="coinflip")
    async def coinflip(self, ctx):
        """Flips a coin."""
        result = random.choice(["Heads", "Tails"])
        await ctx.send(f"🪙 The coin landed on: **{result}**")

    @commands.command(name="wyr")
    async def wouldyourather(self, ctx):
        """Sends a Would You Rather question."""
        question = random.choice(self.wyr_questions)
        await ctx.send(f"🤔 Would You Rather: {question}")

    @commands.command(name="truth")
    async def truth(self, ctx):
        """Sends a Truth question."""
        question = random.choice(self.truths)
        await ctx.send(f"🗣️ Truth: {question}")

    @commands.command(name="dare")
    async def dare(self, ctx):
        """Sends a Dare challenge."""
        challenge = random.choice(self.dares)
        await ctx.send(f"🔥 Dare: {challenge}")

async def setup(bot):
    await bot.add_cog(Fun(bot))
