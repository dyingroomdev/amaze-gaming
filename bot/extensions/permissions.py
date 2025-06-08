import discord
from discord.ext import commands

# Replace these with your actual channel IDs
WELCOME_CHANNEL_ID = 1245673265226190939
LEAVE_CHANNEL_ID = 1380224589145309194

class PermissionChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_permissions(self, channel_id: int, channel_name: str):
        channel = self.bot.get_channel(channel_id)
        if not channel:
            print(f"[ERROR] {channel_name} channel with ID {channel_id} not found.")
            return

        everyone_role = channel.guild.default_role
        perms_everyone = channel.permissions_for(everyone_role)
        perms_bot = channel.permissions_for(channel.guild.me)

        print(f"\n🔍 Checking permissions for #{channel_name}:")

        # Permissions for @everyone
        if perms_everyone.view_channel and perms_everyone.read_message_history:
            print(f"✅ @everyone can VIEW and READ messages in #{channel_name}")
        else:
            print(f"❌ @everyone lacks required permissions in #{channel_name}")

        # Permissions for bot
        if perms_bot.send_messages and perms_bot.embed_links:
            print(f"✅ Bot can SEND MESSAGES and EMBED LINKS in #{channel_name}")
        else:
            print(f"❌ Bot lacks permissions in #{channel_name}")

    @commands.command(name="checkperms")
    @commands.has_permissions(administrator=True)
    async def checkperms(self, ctx):
        """Manually run the permission check for welcome/leave channels."""
        await self.check_permissions(WELCOME_CHANNEL_ID, "welcome")
        await self.check_permissions(LEAVE_CHANNEL_ID, "leave")
        await ctx.send("✅ Permission check completed. Check console for detailed results.")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.check_permissions(WELCOME_CHANNEL_ID, "welcome")
        await self.check_permissions(LEAVE_CHANNEL_ID, "leave")

async def setup(bot):
    await bot.add_cog(PermissionChecker(bot))
