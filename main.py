# ==============================
# 🧁 IMPORT MODULES
# ==============================
from dotenv import load_dotenv
import os
import sys
import random
from datetime import datetime, timezone, timedelta
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

import discord
from discord.ext import commands
from discord import app_commands

from myserver import server_on  # ส่วนนี้น่าจะเปิด web server (เช่น keep alive)

# ==============================
# 🎀 LOAD .env AND TOKEN
# ==============================
dotenv_path = ".env"
load_dotenv(dotenv_path)

token = os.getenv("TOKEN")
if token:
    print("TOKEN จาก .env คือ:", token)
else:
    print("ไม่พบค่า TOKEN ในไฟล์ .env")

# ==============================
# 🌸 DISCORD BOT SETUP
# ==============================
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
server_settings = {}

print(sys.path)  # Debug path

# ==============================
# 💖 FUNCTION: WELCOME IMAGE
# ==============================
def create_welcome_image(member):
    """ สร้างรูปต้อนรับแบบน่ารัก 💕 """
    bg_path = "welcome_bg.jpg"
    font_path = "font.ttf"
    avatar_size = 150

    bg = Image.open(bg_path).convert("RGBA")
    draw = ImageDraw.Draw(bg)

    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).convert("RGBA")
    avatar = avatar.resize((avatar_size, avatar_size))

    mask = Image.new("L", (avatar_size, avatar_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
    bg.paste(avatar, (200, 50), mask)

    font = ImageFont.truetype(font_path, 40)
    draw.text((180, 220), f"Welcome {member.display_name}!", font=font, fill="white")

    img_path = f"welcome_{member.id}.png"
    bg.save(img_path)
    return img_path

# ==============================
# 🌟 BOT EVENTS
# ==============================
@bot.event
async def on_ready():
    print("Bot online!")
    synced = await bot.tree.sync()
    print(f"{len(synced)} command(s)")

@bot.event
async def on_member_join(member):
    guild_id = member.guild.id
    welcome_channel_id = server_settings.get(guild_id, {}).get("welcome_channel")

    if welcome_channel_id:
        channel = bot.get_channel(welcome_channel_id)
        image_path = create_welcome_image(member)
        file = discord.File(image_path, filename="welcome.png")
        await channel.send(
            f"🎉 {member.mention} joined the server! 🌟\nNow we have {member.guild.member_count} members!",
            file=file
        )

@bot.event
async def on_member_remove(member):
    guild_id = member.guild.id
    goodbye_channel_id = server_settings.get(guild_id, {}).get("goodbye_channel")

    if goodbye_channel_id:
        channel = bot.get_channel(goodbye_channel_id)
        await channel.send(
            f"💔 {member.display_name} has left the server...\nNow we have {member.guild.member_count} members left."
        )

@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    channel = discord.utils.get(guild.text_channels, name="voice-log")
    if not channel:
        return

    nickname = member.display_name
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    time_now = datetime.now().strftime("%H:%M:%S")

    embed = discord.Embed(color=0xFFB6C1)
    if before.channel is None and after.channel is not None:
        embed.title = "🎧 เข้าห้องเสียงแล้ว~"
        embed.description = f"**{nickname}** ได้เข้าร่วมห้อง **{after.channel.name}** นะคะ~ 🎀"
    elif before.channel is not None and after.channel is None:
        embed.title = "🚪 ออกจากห้องเสียงแล้ว~"
        embed.description = f"**{nickname}** ออกจากห้อง **{before.channel.name}** ไปแล้วน้า~ 😢"
    else:
        return

    embed.set_thumbnail(url=avatar_url)
    embed.add_field(name="⏰ เวลา", value=f"{time_now} น.", inline=True)
    embed.set_footer(text="ขอให้สนุกกับเสียงน้า~ 💕")
    await channel.send(embed=embed)

# ==============================
# 🎀 TEXT INTERACTION RESPONSES
# ==============================
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    mes = message.content.lower()
    greetings = ['สวัสดี', 'หวัดดี', 'ไฮๆ']

    if mes in greetings:
        responses = [
            f"หวัดดีค่าา~ วันนี้อากาศดีเนอะ {message.author.name} ☀️",
            f"เย้~ เจอกันอีกแล้วน้า {message.author.name}~ ✨",
            f"ไฮจ้า~ มีอะไรให้เราช่วยมั้ยน้า? 💖"
        ]
        await message.channel.send(random.choice(responses))

    elif mes in ['เป็นไงบ้าง', 'สบายดีมั้ย']:
        await message.channel.send(f"อุ๊งง~ เราสบายดีเลยล่ะ ขอบคุณที่ถามนะคะ {message.author.name} 💕")

    elif mes in ['หิวจัง', 'เบื่อจัง', 'ง่วง']:
        reactions = {
            'หิวจัง': "งือ~ งั้นไปหาอะไรกินด้วยกันมั้ย~ 🍙🍜",
            'เบื่อจัง': "เบื่อเหรอ~ งั้นเรามาเล่นเกมกันมั้ย~ 🎮",
            'ง่วง': "ง่วงก็พักเถอะน้า เดี๋ยวฝันดีแน่นอน~ 🌙💤"
        }
        await message.channel.send(reactions[mes])

    elif mes in ['รักนะ', 'คิดถึง']:
        await message.channel.send(f"แงง~ เขินเลยอ่ะ {message.author.name} เราก็รักน้าา 💗")

    elif 'ชอบกินอะไร' in mes:
        await message.channel.send("เราชอบของหวานล่ะ~ พวกพุดดิ้ง ช็อกโกแลต หรือเค้กสตรอเบอร์รี่ก็เลิฟสุดๆ 🍰🍓")

    elif 'สีโปรด' in mes or 'สีที่ชอบ' in mes:
        await message.channel.send("สีชมพูวว~ น่ารักสดใสเหมือนหัวใจของเราไงล่ะ~ 💖✨")

    elif 'เพลงโปรด' in mes:
        await message.channel.send("ชอบเพลงนุ่มๆ ฟังแล้วใจฟู~ อย่างเพลงอนิเมะก็ชอบนะ ♪(๑ᴖ◡ᴖ๑)♪")

    elif 'ชื่ออะไร' in mes:
        await message.channel.send("เรียกเราว่า ‘สาวน้อยบอทจัง’ ก็ได้น้า~ ยินดีที่ได้รู้จัก~! 🩷")

    elif 'อายุเท่าไหร่' in mes:
        await message.channel.send("จะบอกก็เขินจัง~ แต่เรายังสาวอยู่เลยล่ะ! (≧◡≦)")

    elif 'อยู่ไหน' in mes:
        await message.channel.send("เราอยู่ในคลาวด์ลอยๆ น่ารักๆ แบบเมฆชมพูน้า~ ☁️💗")

    await bot.process_commands(message)

# ==============================
# 💫 SLASH COMMANDS
# ==============================
@bot.tree.command(name='joke', description='เรื่องตลกของสาวน้อย~')
async def jokecommand(interaction: discord.Interaction):
    jokes = [
        "ทำไมผีไม่กินข้าว? ... เพราะมันกลัว 'ข้าวผี'~ 👻🍚",
        "ทำไมองคุลีมาร วิ่งไล่ตาม พระพุ?ะเจ้าไม่ทัน...เพราะคุณย่าเคยพูดเอาไว้ Clock up!!!",
        "ทำไมเป็ดถึงไม่ชอบทะเล~? ... เพราะมันมีคลื่น (เครียด~ 😵‍💫) ฮิๆ~"
    ]
    await interaction.response.send_message(random.choice(jokes))

@bot.tree.command(name='fact', description='สาระเล็กๆ จากสาวน้อย 🧠✨')
async def factcommand(interaction: discord.Interaction):
    facts = [
        "รู้มั้ยคะว่า~ แมวสามารถฝันได้เหมือนคนเลยนะ! 🐱💭",
        "หัวใจของปลาหมึกมีตั้ง 3 ดวงแน่ะ! 💙💙💙",
        "คนเรากระพริบตาประมาณ 20,000 ครั้งต่อวันเลยนะ! 👁️✨"
    ]
    await interaction.response.send_message(random.choice(facts))

@bot.tree.command(name='mood', description='เช็คอารมณ์ของสาวน้อยตอนนี้ 🩷')
async def moodcommand(interaction: discord.Interaction):
    moods = [
        "วันนี้อารมณ์ดีมากเลยล่ะ~ เหมาะกับการนั่งฟังเพลงหวานๆ 🍓🎶",
        "อื้ออ... รู้สึกขี้เกียจนิดหน่อย แต่ก็ยังยิ้มได้นะ~ 😴🌸",
        "มู้ดตอนนี้คือแบบ... อยากกินขนมแล้วก็กอดใครสักคนเลย~ 🍩💞",
        "สดใสมั่กๆ เหมือนแดดช่วงเช้าเลยค่ะ~ ☀️✨"
    ]
    await interaction.response.send_message(random.choice(moods))

@bot.tree.command(name='hellobot', description='Replies with hello')
async def hellobot(interaction: discord.Interaction):
    await interaction.response.send_message("หวัดดีจ้า~ มีอะไรให้สาวน้อยช่วยมั้ยน้า~? 💕")

@bot.tree.command(name='name', description='แนะนำตัวให้หน่อยสิ~')
@app_commands.describe(name="ชื่ออะไรจ๊ะ?")
async def namecommand(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"ยินดีที่ได้รู้จักน้า~ {name} คุงง 💞")

@bot.tree.command(name='help', description='แสดงคำสั่งบอท')
async def helpcommand(interaction: discord.Interaction):
    await interaction.response.defer()  # บอก Discord ว่ารอก่อนน้า

    thailand_time = datetime.now(timezone.utc) + timedelta(hours=7)
    formatted_time = thailand_time.strftime("%Y-%m-%d %H:%M:%S")

    embed = discord.Embed(
        title='✨ คำสั่งของสาวน้อยบอท ✨',
        description='ฮัลโหล~ นี่คือคำสั่งทั้งหมดที่หนูทำได้น้า~ ลองเล่นดูได้นะพี่คะ! 💖',
        color=0xFFC0CB
    )
    embed.add_field(name='🌟 คำสั่งพื้นฐาน', value="`!ช่วยด้วย`, `!test <ข้อความ>`, `/hellobot`, `/name <ชื่อ>`", inline=False)
    embed.add_field(name='🎈 คำสั่งถามเล่นๆ จิปาถะ', value="`/joke`, `/fact`, `/mood`", inline=False)
    embed.add_field(name='🎀 สไตล์ของสาวน้อยบอท 🎀',
                    value="บอทนี้จะพูดแบบน่ารัก นุ่มฟู เหมือนสาวน้อยวัยใสค่ะ~ ลองเล่นกับเราเยอะๆ น้า~ งุงิ~ 💕",
                    inline=False)
    embed.set_footer(text=f"⌛ เวลาไทยตอนนี้: {formatted_time}")

    await interaction.followup.send(embed=embed)  # ส่ง embed หลัง defer

# ==============================
# 🛠️ TEXT COMMANDS (PREFIX)
# ==============================
@bot.command()
async def ช่วยด้วย(ctx):
    await ctx.send(f"หนูอยู่ตรงนี้แล้วน้า~ พร้อมช่วยเสมอเลย {ctx.author.name} จ๋า~ 💖")

@bot.command()
async def test(ctx, arg):
    await ctx.send(f"มุแง~ หนูพิมพ์ตามละนะ: {arg} ✨")

# ==============================
# ⚙️ SERVER SETTINGS COMMANDS
# ==============================
@bot.command()
async def set_welcome_channel(ctx, channel: discord.TextChannel):
    if ctx.guild.id not in server_settings:
        server_settings[ctx.guild.id] = {}
    server_settings[ctx.guild.id]["welcome_channel"] = channel.id
    await ctx.send(f"✅ ตั้งค่าช่องต้อนรับเป็น {channel.mention} แล้ว!")

@bot.command()
async def set_goodbye_channel(ctx, channel: discord.TextChannel):
    if ctx.guild.id not in server_settings:
        server_settings[ctx.guild.id] = {}
    server_settings[ctx.guild.id]["goodbye_channel"] = channel.id
    await ctx.send(f"✅ ตั้งค่าช่องแจ้งเตือนคนออกเป็น {channel.mention} แล้ว!")

@bot.command()
async def set_voice_channel(ctx, channel: discord.TextChannel):
    if ctx.guild.id not in server_settings:
        server_settings[ctx.guild.id] = {}
    server_settings[ctx.guild.id]["voice_channel"] = channel.id
    await ctx.send(f"✅ ตั้งค่าช่องแจ้งเตือนการใช้เสียงเป็น {channel.mention} แล้ว!")

@bot.command()
async def show_settings(ctx):
    settings = server_settings.get(ctx.guild.id, {})
    welcome = f"<#{settings.get('welcome_channel', '❌ ไม่ได้ตั้งค่า')}>"
    goodbye = f"<#{settings.get('goodbye_channel', '❌ ไม่ได้ตั้งค่า')}>"
    voice = f"<#{settings.get('voice_channel', '❌ ไม่ได้ตั้งค่า')}>"

    embed = discord.Embed(title="🔧 การตั้งค่าของเซิร์ฟ", color=0xFFC0CB)
    embed.add_field(name="👋 ช่องต้อนรับ", value=welcome, inline=False)
    embed.add_field(name="💔 ช่องแจ้งเตือนออก", value=goodbye, inline=False)
    embed.add_field(name="🎤 ช่องแจ้งเตือนใช้เสียง", value=voice, inline=False)
    await ctx.send(embed=embed)

# ==============================
# 💥 RUN THE BOT
# ==============================
server_on()
bot.run(token)
