import discord
from discord.ext import commands

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # You can customize these
        self.server_ip = "amzcraft.xyz:25565"
        self.server_version = "Java 1.20.4"
        self.vote_links = [
            "https://topminecraftservers.org/server/40251",
            "https://minecraft-server-list.com/server/512358",
            "https://topg.org/minecraft-servers/server-671146",
            # Add more vote links here if you want
        ]

    @commands.command(name="ip")
    async def ip(self, ctx):
        """Send the Minecraft server IP and version."""
        embed = discord.Embed(title="AmzCraft Minecraft Server Info", color=discord.Color.green())
        embed.add_field(name="IP Address", value=self.server_ip)
        embed.add_field(name="Version", value=self.server_version)
        embed.set_footer(text="Join us and have fun!")
        await ctx.send(embed=embed)

    @commands.command(name="vote")
    async def vote(self, ctx):
        """Send voting links and info."""
        embed = discord.Embed(title="Vote for AmzCraft", description="Support the server by voting on these sites!", color=discord.Color.gold())
        for url in self.vote_links:
            embed.add_field(name="Vote Link", value=f"[Click here]({url})", inline=False)
        embed.set_footer(text="Thanks for your support!")
        await ctx.send(embed=embed)

    @commands.command(name="baltop")
    async def baltop(self, ctx):
        """Show the in-game baltop leaderboard."""
        # Placeholder: you should replace this with actual data fetching
        # from your Minecraft server or database.
        # For now, let's send a static example list:

        example_baltop = [
            ("Player1", 15000),
            ("Player2", 12000),
            ("Player3", 9000),
            ("Player4", 8000),
            ("Player5", 7500),
        ]

        embed = discord.Embed(title="AmzCraft Balance Top Players", color=discord.Color.purple())
        for rank, (player, balance) in enumerate(example_baltop, start=1):
            embed.add_field(name=f"#{rank} {player}", value=f"${balance:,}", inline=False)
        embed.set_footer(text="Keep playing to climb the ranks!")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Minecraft(bot))
