import discord
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 1380248329568653476  # replace with your log channel ID

    def get_log_channel(self, guild):
        return guild.get_channel(self.log_channel_id)

    # Message Delete
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild is None or message.author.bot:
            return
        channel = self.get_log_channel(message.guild)
        if channel:
            embed = discord.Embed(
                title="Message Deleted",
                description=f"**Author:** {message.author.mention} ({message.author.id})\n"
                            f"**Channel:** {message.channel.mention}\n"
                            f"**Content:** {message.content or '[No Content]'}",
                color=discord.Color.red(),
                timestamp=message.created_at
            )
            embed.set_footer(text=f"Author ID: {message.author.id} • Message ID: {message.id}")
            await channel.send(embed=embed)

    # Message Edit
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild is None or before.author.bot:
            return
        if before.content == after.content:
            return  # no content change
        channel = self.get_log_channel(before.guild)
        if channel:
            embed = discord.Embed(
                title="Message Edited",
                description=f"**Author:** {before.author.mention} ({before.author.id})\n"
                            f"**Channel:** {before.channel.mention}\n"
                            f"**Before:** {before.content or '[No Content]'}\n"
                            f"**After:** {after.content or '[No Content]'}",
                color=discord.Color.orange(),
                timestamp=after.edited_at or discord.utils.utcnow()
            )
            embed.set_footer(text=f"Author ID: {before.author.id} • Message ID: {before.id}")
            await channel.send(embed=embed)

    # Member Join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.get_log_channel(member.guild)
        if channel:
            embed = discord.Embed(
                title="Member Joined",
                description=f"{member.mention} ({member.id}) joined the server.",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await channel.send(embed=embed)

    # Member Leave
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.get_log_channel(member.guild)
        if channel:
            embed = discord.Embed(
                title="Member Left",
                description=f"{member.name}#{member.discriminator} ({member.id}) left the server.",
                color=discord.Color.dark_red(),
                timestamp=discord.utils.utcnow()
            )
            await channel.send(embed=embed)

    # Role Create
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        channel = self.get_log_channel(role.guild)
        if channel:
            embed = discord.Embed(
                title="Role Created",
                description=f"Role **{role.name}** ({role.id}) was created.",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )
            await channel.send(embed=embed)

    # Role Delete
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        channel = self.get_log_channel(role.guild)
        if channel:
            embed = discord.Embed(
                title="Role Deleted",
                description=f"Role **{role.name}** ({role.id}) was deleted.",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            )
            await channel.send(embed=embed)

    # Role Update
    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        channel = self.get_log_channel(before.guild)
        if channel:
            changes = []
            if before.name != after.name:
                changes.append(f"**Name:** {before.name} → {after.name}")
            if before.permissions != after.permissions:
                changes.append(f"**Permissions:** Updated")
            if changes:
                embed = discord.Embed(
                    title="Role Updated",
                    description=f"Role **{before.name}** ({before.id}) was updated.\n" + "\n".join(changes),
                    color=discord.Color.orange(),
                    timestamp=discord.utils.utcnow()
                )
                await channel.send(embed=embed)

    # Channel Create
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        log_channel = self.get_log_channel(channel.guild)
        if log_channel:
            embed = discord.Embed(
                title="Channel Created",
                description=f"Channel **{channel.name}** ({channel.id}) was created. Type: {str(channel.type)}",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )
            await log_channel.send(embed=embed)

    # Channel Delete
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_channel = self.get_log_channel(channel.guild)
        if log_channel:
            embed = discord.Embed(
                title="Channel Deleted",
                description=f"Channel **{channel.name}** ({channel.id}) was deleted. Type: {str(channel.type)}",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            )
            await log_channel.send(embed=embed)

    # Channel Update
    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        log_channel = self.get_log_channel(before.guild)
        if log_channel:
            changes = []
            if before.name != after.name:
                changes.append(f"**Name:** {before.name} → {after.name}")
            if getattr(before, "topic", None) != getattr(after, "topic", None):
                changes.append(f"**Topic:** {before.topic} → {after.topic}")
            if changes:
                embed = discord.Embed(
                    title="Channel Updated",
                    description=f"Channel **{before.name}** ({before.id}) was updated.\n" + "\n".join(changes),
                    color=discord.Color.orange(),
                    timestamp=discord.utils.utcnow()
                )
                await log_channel.send(embed=embed)

    # Mod action logging: To be called from your moderation commands
    async def log_mod_action(self, guild, action, user, moderator, reason=None):
        channel = self.get_log_channel(guild)
        if channel:
            embed = discord.Embed(
                title="Moderation Action",
                description=f"**Action:** {action}\n"
                            f"**User:** {user.mention} ({user.id})\n"
                            f"**Moderator:** {moderator.mention} ({moderator.id})\n"
                            f"**Reason:** {reason or 'No reason provided'}",
                color=discord.Color.dark_blue(),
                timestamp=discord.utils.utcnow()
            )
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logging(bot))
