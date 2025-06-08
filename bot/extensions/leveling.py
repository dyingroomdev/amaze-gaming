import discord
from discord.ext import commands
import sqlite3
import io
import os
import time
from PIL import Image, ImageDraw, ImageFont, ImageOps

DB_PATH = os.path.expanduser("~") + "/amaze-gaming-bot/bot/data/leveling.db"
FONT_PATH_BOLD = "/home/dyingroom/amaze-gaming-bot/bot/assets/fonts/Roboto-Bold.ttf"
FONT_PATH_REGULAR = "/home/dyingroom/amaze-gaming-bot/bot/assets/fonts/Roboto-Regular.ttf"
SERVER_LOGO_PATH = "/home/dyingroom/amaze-gaming-bot/bot/assets/images/server_logo.png"

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS leveling (
                guild_id INTEGER,
                user_id INTEGER,
                xp INTEGER,
                level INTEGER,
                PRIMARY KEY(guild_id, user_id)
            )"""
        )
        self.conn.commit()

        self.cooldowns = {}  # user_id -> last xp timestamp

    def draw_rank_card(self, user, level, xp, xp_for_next_level):
        width, height = 900, 300
        card = Image.new("RGBA", (width, height), "#1a330b")  # Dark green background
        draw = ImageDraw.Draw(card)

        # Gradient overlay for subtle depth
        for i in range(height):
            gradient_color = (26, 51, 11, int(255 * (i / height) * 0.3))
            draw.line([(0, i), (width, i)], fill=gradient_color)

        # Server logo top-left
        try:
            server_logo = Image.open(SERVER_LOGO_PATH).convert("RGBA")
            server_logo.thumbnail((100, 100))
            card.paste(server_logo, (25, 25), server_logo)
        except Exception as e:
            print(f"Error loading server logo: {e}")

        # User avatar circular crop on left center
        avatar_asset = user.display_avatar.with_size(128).with_static_format('png')
        avatar_bytes = avatar_asset.read()
        avatar_image = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
        avatar_image = avatar_image.resize((150, 150))
        mask = Image.new("L", (150, 150), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 150, 150), fill=255)
        avatar_image = ImageOps.fit(avatar_image, (150, 150))
        card.paste(avatar_image, (50, 75), mask)

        # Fonts
        font_large = ImageFont.truetype(FONT_PATH_BOLD, 40)
        font_medium = ImageFont.truetype(FONT_PATH_BOLD, 30)
        font_small = ImageFont.truetype(FONT_PATH_REGULAR, 24)

        # Username#discriminator
        username_text = f"{user.name}#{user.discriminator}"
        draw.text((220, 40), username_text, font=font_large, fill="white")

        # Level text
        level_text = f"Level: {level}"
        draw.text((220, 90), level_text, font=font_medium, fill="#52991f")

        # XP text
        xp_text = f"XP: {xp} / {xp_for_next_level}"
        draw.text((220, 130), xp_text, font=font_medium, fill="white")

        # Progress bar background
        bar_x, bar_y = 220, 180
        bar_width, bar_height = 600, 40
        draw.rounded_rectangle(
            [bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
            radius=20,
            fill="#2a4a06"
        )

        # Progress bar foreground
        progress_width = int((xp / xp_for_next_level) * bar_width)
        if progress_width > 0:
            draw.rounded_rectangle(
                [bar_x, bar_y, bar_x + progress_width, bar_y + bar_height],
                radius=20,
                fill="#52991f"
            )

        # Return bytes
        with io.BytesIO() as image_binary:
            card.save(image_binary, "PNG")
            image_binary.seek(0)
            return image_binary.read()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        user_id = message.author.id
        guild_id = message.guild.id
        now = time.time()
        last_time = self.cooldowns.get(user_id, 0)
        if now - last_time < 60:  # 60 second cooldown
            return
        self.cooldowns[user_id] = now

        xp_gain = 20
        self.cursor.execute("SELECT xp, level FROM leveling WHERE guild_id=? AND user_id=?", (guild_id, user_id))
        row = self.cursor.fetchone()

        if row is None:
            xp, level = xp_gain, 0
            self.cursor.execute("INSERT INTO leveling (guild_id, user_id, xp, level) VALUES (?, ?, ?, ?)", (guild_id, user_id, xp, level))
        else:
            xp, level = row
            xp += xp_gain
            xp_for_next_level = (level + 1) * 1000
            if xp >= xp_for_next_level:
                level += 1
                xp -= xp_for_next_level
                channel = message.channel
                await channel.send(f"🎉 Congrats {message.author.mention}, you leveled up to **Level {level}**!")

            self.cursor.execute("UPDATE leveling SET xp=?, level=? WHERE guild_id=? AND user_id=?", (xp, level, guild_id, user_id))

        self.conn.commit()

    @commands.command()
    async def rank(self, ctx):
        guild_id = ctx.guild.id
        user_id = ctx.author.id
        self.cursor.execute("SELECT level, xp FROM leveling WHERE guild_id=? AND user_id=?", (guild_id, user_id))
        result = self.cursor.fetchone()
        if not result:
            await ctx.send(f"{ctx.author.mention}, you have no XP yet.")
            return

        level, xp = result
        xp_for_next_level = (level + 1) * 1000

        card_bytes = self.draw_rank_card(ctx.author, level, xp, xp_for_next_level)

        file = discord.File(io.BytesIO(card_bytes), filename="rank.png")
        embed = discord.Embed(title=f"{ctx.author.name}'s Rank", color=0x52991f)
        embed.set_image(url="attachment://rank.png")
        await ctx.send(file=file, embed=embed)

    @commands.command()
    async def top(self, ctx):
        guild_id = ctx.guild.id
        self.cursor.execute("SELECT user_id, level, xp FROM leveling WHERE guild_id=? ORDER BY level DESC, xp DESC LIMIT 10", (guild_id,))
        rows = self.cursor.fetchall()

        if not rows:
            await ctx.send("No leveling data found.")
            return

        embed = discord.Embed(title=f"Top 10 Levels - {ctx.guild.name}", color=0x52991f)
        description = ""
        for i, (user_id, level, xp) in enumerate(rows, start=1):
            member = ctx.guild.get_member(user_id)
            name = member.name if member else f"User ID {user_id}"
            description += f"**{i}. {name}** - Level {level} ({xp} XP)\n"
        embed.description = description

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leveling(bot))
