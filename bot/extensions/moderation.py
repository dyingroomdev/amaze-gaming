import discord
from discord.ext import commands
from bot.utils import database
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Initialize DB when bot starts
        bot.loop.create_task(database.init_db())

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 Banned {member.mention} | Reason: {reason}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 Kicked {member.mention} | Reason: {reason}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
        await member.add_roles(muted_role)
        await ctx.send(f"🔇 Muted {member.mention}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"🔊 Unmuted {member.mention}")
        else:
            await ctx.send(f"{member.mention} is not muted.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            if ban_entry.user.id == user.id:
                await ctx.guild.unban(user)
                await ctx.send(f"✅ Unbanned {user.mention}")
                return
        await ctx.send(f"{user.mention} is not banned.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if amount <= 0:
            await ctx.send("⚠️ Please specify a positive number of messages to delete.")
            return
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Deleted {len(deleted) - 1} messages.", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await database.add_warning(member.id, ctx.author.id, reason)
        await ctx.send(f"⚠️ Warned {member.mention} | Reason: {reason}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, member: discord.Member):
        warnings = await database.get_warnings(member.id)
        if not warnings:
            await ctx.send(f"{member.mention} has no warnings.")
            return

        message = f"⚠️ Warnings for {member.mention}:\n"
        for i, (mod_id, reason, timestamp) in enumerate(warnings, start=1):
            moderator = ctx.guild.get_member(mod_id)
            mod_name = moderator.name if moderator else "Unknown"
            message += f"{i}. By {mod_name} on {timestamp}: {reason}\n"

        await ctx.send(message)

    @ban.error
    @kick.error
    @warn.error
    @purge.error
    @mute.error
    @unmute.error
    @unban.error
    @warnings.error
    async def mod_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 You don't have permission to use that command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❗ Missing argument(s). Please check your command usage.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❗ Invalid argument(s). Please check your input.")
        else:
            await ctx.send("⚠️ Something went wrong.")
            raise error


async def setup(bot):
    await bot.add_cog(Moderation(bot))
