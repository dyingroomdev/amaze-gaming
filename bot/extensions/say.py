from discord.ext import commands
import discord

class SayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say")
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, channel: discord.TextChannel, *, message: str):
        try:
            await channel.send(message)
            await ctx.message.add_reaction("✅")  # React to confirm success
        except Exception as e:
            await ctx.send(f"❌ Could not send message: {e}")

async def setup(bot):
    await bot.add_cog(SayCommand(bot))
