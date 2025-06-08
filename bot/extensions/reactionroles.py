import discord
from discord.ext import commands

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = None  # message ID to watch for reactions
        self.roles = {}  # emoji: role_id

    @commands.command(name="initselfrole")
    @commands.has_permissions(administrator=True)
    async def init_selfrole(self, ctx, channel: discord.TextChannel):
        """Send a self-role message with reaction roles in the specified channel."""
        # Define your emoji-role placeholders here
        # Replace these with actual role IDs from your server
        self.roles = {
            "🎮": None,  # gamer role ID goes here
            "🎨": None,  # artist role ID goes here
            "💻": None,  # coder role ID goes here
        }

        # Try to get roles by name for demo (replace with your actual role IDs)
        for emoji in self.roles:
            role_name = None
            if emoji == "🎮":
                role_name = "gamer"
            elif emoji == "🎨":
                role_name = "artist"
            elif emoji == "💻":
                role_name = "coder"
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                self.roles[emoji] = role.id

        description_lines = []
        for emoji, role_id in self.roles.items():
            role = ctx.guild.get_role(role_id)
            if role:
                description_lines.append(f"{emoji} = {role.name}")

        embed = discord.Embed(title="Self Role Menu", description="\n".join(description_lines), color=0x52991f)
        message = await channel.send(embed=embed)
        self.message_id = message.id

        for emoji in self.roles.keys():
            await message.add_reaction(emoji)

        await ctx.send(f"Self role message sent in {channel.mention}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Ignore if no self role message set
        if payload.message_id != self.message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        role_id = self.roles.get(str(payload.emoji))
        if not role_id:
            return

        role = guild.get_role(role_id)
        if not role:
            return

        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return

        try:
            await member.add_roles(role, reason="Reaction role added")
            print(f"Added {role.name} to {member.display_name}")
        except Exception as e:
            print(f"Error adding role: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # Remove role when reaction removed
        if payload.message_id != self.message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        role_id = self.roles.get(str(payload.emoji))
        if not role_id:
            return

        role = guild.get_role(role_id)
        if not role:
            return

        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return

        try:
            await member.remove_roles(role, reason="Reaction role removed")
            print(f"Removed {role.name} from {member.display_name}")
        except Exception as e:
            print(f"Error removing role: {e}")

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
