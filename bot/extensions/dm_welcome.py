import discord
from discord.ext import commands

class DMWelcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            embed = discord.Embed(
                title="👋 Welcome to Amaze Gaming!",
                description=(
                    f"Hey {member.name}, we're thrilled to have you join **{member.guild.name}**! 🎉\n\n"
                    "Please read the rules and grab your roles.\n"
                    "If you need help, moderators are here for you!"
                ),
                color=0x4CAF50  # Green color
            )

            embed.set_image(url="https://cdn.discordapp.com/attachments/1103724767749619762/1376573173801156688/amzcraft.gif?ex=68960eac&is=6894bd2c&hm=513260a8e0c98d1527a4e1e702991e68ccc547eb957a499cdf1c2c395bb15d17")

            if member.guild.icon:
                embed.set_thumbnail(url=member.guild.icon.url)

            # AmzCraft Server Info Field with emojis
            embed.add_field(
                name="🛡️ AmzCraft Server Info",
                value=(
                    "💻 **Java IP:**\n"
                    "`play.amzcraft.xyz`\n\n"
                    "📱 **Bedrock IP:**\n"
                    "`amzcraft.xyz:25568`\n\n"
                    "🆕 **Version:**\n"
                    "`1.21+`"
                ),
                inline=False
            )

            embed.add_field(
                name="🎮 Server Info Commands",
                value=(
                    "`!ip` — Shows the Minecraft Server IP and version\n"
                    "`!vote` — Get the list of voting websites to earn rewards\n"
                    "`!map` — View the live Dynmap\n"
                    "`!status` — Check if the server is online and who's playing\n\n"
                    f"Use these commands in this channel:\n"
                    f"https://discord.com/channels/1118248694236590131/1388478801662709780"
                ),
                inline=False
            )

            embed.add_field(
                name="📜 Server Rules",
                value=(
                    "Please make sure to read the rules here:\n"
                    "https://discord.com/channels/1118248694236590131/1351255942406078474"
                ),
                inline=False
            )

            embed.set_footer(text="Enjoy your stay in the community! 🏰")

            await member.send(embed=embed)
        except discord.Forbidden:
            print(f"❌ Couldn't send DM to {member.name} (DMs might be closed).")

async def setup(bot):
    await bot.add_cog(DMWelcome(bot))
