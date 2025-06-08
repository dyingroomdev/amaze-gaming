import discord
from discord.ext import commands

class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_role_id = None  # will store role ID to assign automatically

    @commands.command(name="setautorole")
    @commands.has_permissions(administrator=True)
    async def set_autorole(self, ctx, role: discord.Role):
        """Set the role to assign automatically to new members."""
        self.auto_role_id = role.id
        await ctx.send(f"Auto role set to {role.name}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.auto_role_id:
            return
        role = member.guild.get_role(self.auto_role_id)
        if role:
            try:
                await member.add_roles(role, reason="Auto role on join")
                print(f"Assigned {role.name} to {member.name}")
            except Exception as e:
                print(f"Failed to assign auto role: {e}")

async def setup(bot):
    await bot.add_cog(AutoRole(bot))
