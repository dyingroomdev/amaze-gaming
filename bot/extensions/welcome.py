import os
import discord
from discord.ext import commands

WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", 0))
LEAVE_CHANNEL_ID = int(os.getenv("LEAVE_CHANNEL_ID", 0))
RULES_CHANNEL_ID = int(os.getenv("RULES_CHANNEL_ID", 0))
SELF_ROLE_CHANNEL_ID = int(os.getenv("SELF_ROLE_CHANNEL_ID", 0))

WELCOME_BANNER_URL = os.getenv("WELCOME_BANNER_URL", None)
LEAVE_BANNER_URL = os.getenv("LEAVE_BANNER_URL", None)

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_welcome_embed(self, member):
        embed = discord.Embed(
            title=f"Welcome to {member.guild.name}!",
            description=(
                f"Hey {member.mention}, welcome to the server!\n\n"
                f"Please read the {self.bot.get_channel(RULES_CHANNEL_ID).mention} and "
                f"visit {self.bot.get_channel(SELF_ROLE_CHANNEL_ID).mention} to assign yourself roles."
            ),
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        if WELCOME_BANNER_URL:
            embed.set_image(url=WELCOME_BANNER_URL)
        return embed

    def create_leave_embed(self, member):
        embed = discord.Embed(
            title=f"Goodbye from {member.guild.name}",
            description=f"{member} has left the server. We'll miss you!",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        if LEAVE_BANNER_URL:
            embed.set_image(url=LEAVE_BANNER_URL)
        return embed

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"[DEBUG] {member} joined.")
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            embed = self.create_welcome_embed(member)
            await channel.send(embed=embed)
        else:
            print("[WARN] Welcome channel not found or ID not set.")

        # Auto assign role example (optional)
        role = discord.utils.get(member.guild.roles, name="Member")
        if role:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"[DEBUG] {member} left.")
        channel = self.bot.get_channel(LEAVE_CHANNEL_ID)
        if channel:
            embed = self.create_leave_embed(member)
            await channel.send(embed=embed)
        else:
            print("[WARN] Leave channel not found or ID not set.")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
