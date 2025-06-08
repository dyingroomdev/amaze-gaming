import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.utcnow()

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Check bot latency."""
        latency = round(self.bot.latency * 1000)  # ms
        await ctx.send(f"Pong! Latency: {latency}ms")

    @commands.command(name="userinfo")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        roles = [role.name for role in member.roles if role.name != "@everyone"]
        embed = discord.Embed(title=f"User Info - {member}", color=member.color)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Display Name", value=member.display_name)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S") if member.joined_at else "Unknown")
        embed.add_field(name=f"Roles ({len(roles)})", value=", ".join(roles) if roles else "No Roles")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        roles = [role.name for role in guild.roles if role.name != "@everyone"]
        embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.blurple())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Owner", value=str(guild.owner))
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name=f"Roles ({len(roles)})", value=", ".join(roles) if roles else "No Roles")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="avatar")
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member}'s Avatar")
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="roles")
    async def roles(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        roles = [role.name for role in member.roles if role.name != "@everyone"]
        if not roles:
            await ctx.send(f"{member} has no roles.")
        else:
            await ctx.send(f"Roles for {member}: {', '.join(roles)}")

    @commands.command(name="uptime")
    async def uptime(self, ctx):
        """Show how long the bot has been running."""
        delta = datetime.utcnow() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"Bot uptime: {hours}h {minutes}m {seconds}s")

    @commands.command(name="botinfo")
    async def botinfo(self, ctx):
        """Show info about the bot."""
        latency = round(self.bot.latency * 1000)
        commands_count = len(self.bot.commands)
        embed = discord.Embed(title="Amaze Gaming Bot Info", color=discord.Color.green())
        embed.add_field(name="Library", value="discord.py")
        embed.add_field(name="Latency", value=f"{latency}ms")
        embed.add_field(name="Commands", value=commands_count)
        embed.add_field(name="Python Version", value=f"{discord.__version__}")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="remindme")
    async def remindme(self, ctx, time: str, *, reminder: str):
        """
        Set a reminder.
        Usage example: !remindme 10m Take a break
        Supported suffixes: s, m, h
        """
        unit = time[-1]
        if unit not in ('s', 'm', 'h'):
            await ctx.send("Invalid time format! Use s, m, or h (seconds, minutes, hours).")
            return
        
        try:
            amount = int(time[:-1])
        except ValueError:
            await ctx.send("Invalid time amount!")
            return

        seconds = amount
        if unit == 'm':
            seconds *= 60
        elif unit == 'h':
            seconds *= 3600

        await ctx.send(f"Okay {ctx.author.mention}, I will remind you in {time}.")
        await asyncio.sleep(seconds)
        await ctx.send(f"{ctx.author.mention}, here is your reminder: {reminder}")

    @commands.command(name="poll")
    async def poll(self, ctx, *, question: str):
        """Create a simple yes/no poll."""
        embed = discord.Embed(title="Poll", description=question, color=discord.Color.blue())
        embed.set_footer(text=f"Poll created by {ctx.author}", icon_url=ctx.author.avatar.url)
        message = await ctx.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    @commands.command(name="timer")
    async def timer(self, ctx, seconds: int):
        """Start a countdown timer in seconds."""
        if seconds <= 0:
            await ctx.send("Please provide a positive number of seconds.")
            return
        await ctx.send(f"Timer started for {seconds} seconds.")
        await asyncio.sleep(seconds)
        await ctx.send(f"{ctx.author.mention}, your timer for {seconds} seconds has ended!")

async def setup(bot):
    await bot.add_cog(Utility(bot))
