import discord
from discord.ext import commands

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_role_name = "AG"  # role to auto assign on join
        self.self_role_message_id = None  # store your reaction role message ID here
        self.emoji_to_role = {
            "🎮": "gamer",
            "🎨": "artist",
            "💻": "coder",
        }

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        role = discord.utils.get(guild.roles, name=self.default_role_name)
        if role:
            try:
                await member.add_roles(role)
                print(f"Assigned auto role '{role.name}' to {member.display_name}")
            except Exception as e:
                print(f"Failed to assign role: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Ignore if reaction is not in guild
        if payload.guild_id is None:
            return

        # Only handle reaction if it matches the stored message ID
        if self.self_role_message_id is None or payload.message_id != self.self_role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        role_name = self.emoji_to_role.get(str(payload.emoji))
        if not role_name:
            return

        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            return

        member = guild.get_member(payload.user_id)
        if member is None or member.bot:
            return

        try:
            await member.add_roles(role)
            print(f"Added role '{role.name}' to {member.display_name} for reaction {payload.emoji}")
        except Exception as e:
            print(f"Failed to add role: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # Handle reaction removal to remove role
        if payload.guild_id is None:
            return

        if self.self_role_message_id is None or payload.message_id != self.self_role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        role_name = self.emoji_to_role.get(str(payload.emoji))
        if not role_name:
            return

        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            return

        member = guild.get_member(payload.user_id)
        if member is None or member.bot:
            return

        try:
            await member.remove_roles(role)
            print(f"Removed role '{role.name}' from {member.display_name} after removing reaction {payload.emoji}")
        except Exception as e:
            print(f"Failed to remove role: {e}")

    @commands.command(name="initselfrole")
    @commands.has_permissions(administrator=True)
    async def init_self_role(self, ctx):
        """
        Sends the self-role message with reaction emojis to assign roles.
        Admin only command.
        """
        embed = discord.Embed(
            title="Self Roles",
            description="React to get a role!\n\n"
                        "🎮 - gamer\n"
                        "🎨 - artist\n"
                        "💻 - coder",
            color=0x52991f
        )
        message = await ctx.send(embed=embed)
        self.self_role_message_id = message.id

        # Add reactions to the message
        for emoji in self.emoji_to_role.keys():
            await message.add_reaction(emoji)

        await ctx.send("Self role message initialized. Users can now react to assign roles.")

async def setup(bot):
    await bot.add_cog(RoleManager(bot))
