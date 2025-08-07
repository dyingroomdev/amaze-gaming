import discord
from discord.ext import commands
from urllib.parse import urlparse
import aiohttp
import re

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Server Info
        self.java_ip = "play.amzcraft.xyz"
        self.bedrock_ip = "amzcraft.xyz:25568"
        self.server_version = "1.21+"

        # Vote Sites from your config, with names and URLs cleaned
        self.vote_sites = [
            {"name": "TopG", "url": "https://topg.org/minecraft-servers/server-671146"},
            {"name": "Minecraft-Server.net", "url": "https://minecraft-server.net/details/AmzCraft/"},
            {"name": "Minecraft-MP.com", "url": "https://minecraft-mp.com/server/341570/vote"},
            {"name": "Best-Minecraft-Servers", "url": "https://best-minecraft-servers.co/server-amzcraft.27860/vote"},
            {"name": "MinecraftBuzz", "url": "https://minecraft.buzz/vote/13832"},
            {"name": "TopMinecraftServers", "url": "https://topminecraftservers.org/server/40251"},
        ]

    @commands.command(name="ip")
    async def ip(self, ctx):
        """Send the Minecraft server IPs and version."""
        embed = discord.Embed(
            title="🎮 AmzCraft Server Info",
            color=discord.Color.green()
        )
        embed.add_field(name="🖥️ Java IP", value=self.java_ip, inline=False)
        embed.add_field(name="📱 Bedrock IP", value=self.bedrock_ip, inline=False)
        embed.add_field(name="🌐 Version", value=self.server_version, inline=False)
        embed.set_footer(text="Join us and have fun!")
        await ctx.send(embed=embed)

    @commands.command(name="vote")
    async def vote(self, ctx):
        """Send voting links with site names."""
        embed = discord.Embed(
            title="🗳️ Vote for AmzCraft",
            description="Support the server by voting daily on these sites:",
            color=discord.Color.gold()
        )
        for site in self.vote_sites:
            # Clean URL text for display: remove any color codes or formatting if needed
            clean_name = re.sub(r'&.', '', site["name"])  # just in case
            embed.add_field(name=clean_name, value=f"[Click here]({site['url']})", inline=False)
        embed.set_footer(text="Thanks for your support!")
        await ctx.send(embed=embed)

    @commands.command(name="status")
    async def status(self, ctx):
        """Check the Minecraft Java & Bedrock server status."""
        java_host = self.java_ip.split(':')[0]
        bedrock_host = self.bedrock_ip.split(':')[0]
        bedrock_port = self.bedrock_ip.split(':')[1] if ':' in self.bedrock_ip else None

        java_url = f"https://api.mcsrvstat.us/3/{java_host}"
        bedrock_url = f"https://api.mcsrvstat.us/bedrock/3/{bedrock_host}"
        if bedrock_port:
            bedrock_url += f":{bedrock_port}"

        async with aiohttp.ClientSession() as session:
            # Java server check
            async with session.get(java_url) as resp_java:
                if resp_java.status != 200:
                    return await ctx.send("⚠️ Failed to fetch Java server status.")
                data_java = await resp_java.json()

            # Bedrock server check
            async with session.get(bedrock_url) as resp_bedrock:
                if resp_bedrock.status != 200:
                    return await ctx.send("⚠️ Failed to fetch Bedrock server status.")
                data_bedrock = await resp_bedrock.json()

        embed = discord.Embed(title="📡 AmzCraft Server Status", color=discord.Color.blurple())

        # Java status
        if data_java.get("online"):
            players = data_java.get("players", {})
            embed.add_field(
                name="🖥️ Java Edition",
                value=(
                    f"🟢 Online\n"
                    f"Players: {players.get('online', '?')}/{players.get('max', '?')}\n"
                    f"Version: {data_java.get('version', 'Unknown')}"
                ),
                inline=False
            )
        else:
            embed.add_field(name="🖥️ Java Edition", value="🔴 Offline", inline=False)

        # Bedrock status
        if data_bedrock.get("online"):
            players = data_bedrock.get("players", {})
            embed.add_field(
                name="📱 Bedrock Edition",
                value=(
                    f"🟢 Online\n"
                    f"Players: {players.get('online', '?')}/{players.get('max', '?')}\n"
                    f"Version: {data_bedrock.get('version', 'Unknown')}"
                ),
                inline=False
            )
        else:
            embed.add_field(name="📱 Bedrock Edition", value="🔴 Offline", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Minecraft(bot))
