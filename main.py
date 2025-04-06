# ==============================
# 🧁 IMPORT MODULES
# ==============================
from dotenv import load_dotenv
import os
import sys
import random
import asyncio
from datetime import datetime, timezone, timedelta
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

import json
import discord
from discord.ext import commands
from discord import app_commands

from myserver import server_on  # ใช้สำหรับ run web server (เช่น keep alive)

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
# 🧠 โหลดข้อมูลที่เรียนรู้ไว้
# ==============================
learned = {}
if os.path.exists("learned.json"):
    with open("learned.json", "r", encoding="utf-8") as f:
        learned = json.load(f)

# ==============================
# 🌸 DISCORD BOT SETUP
# ==============================
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
server_settings = {}
print(sys.path)

# ==============================
# 💖 FUNCTION: WELCOME IMAGE
# ==============================
def create_welcome_image(member):
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
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

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
    settings = server_settings.get(guild.id, {})
    voice_channel_id = settings.get("voice_channel")

    if not voice_channel_id:
        return  # ยังไม่ได้ตั้งค่าห้องแจ้งเตือนเสียง

    channel = bot.get_channel(voice_channel_id)
    if not channel:
        return  # หา channel ไม่เจอ

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
    elif before.channel != after.channel:
        embed.title = "➡️ ย้ายห้องเสียงแล้ว~"
        embed.description = (
            f"**{nickname}** ย้ายจากห้อง **{before.channel.name}** ไปที่ **{after.channel.name}** ค่า~ 🔄"
        )    
    
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

    user_input = message.content.strip()
    mes = user_input.lower()
    greetings = ['สวัสดี', 'หวัดดี', 'ไฮๆ']

    # ระบบพูดน่ารักๆ
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

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()

    if content.startswith("สอน หนูว่า "):
        try:
            data = content.replace("สอน หนูว่า ", "").split(" = ")
            question = data[0].strip()
            answer = data[1].strip()
            learned[question] = answer
            with open("learned.json", "w", encoding="utf-8") as f:
                json.dump(learned, f, ensure_ascii=False, indent=4)
            await message.channel.send("หนูจำได้แล้วค่ะ! ขอบคุณที่สอนนะคะ 💖")
        except:
            await message.channel.send("รูปแบบไม่ถูกต้องน้า ต้องเป็น `สอน หนูว่า คำถาม = คำตอบ` นะคะ~")
        return

    if content in learned:
        await message.channel.send(learned[content])
        return

    await bot.process_commands(message)

# ==============================
# 💫 SLASH COMMANDS
# ==============================
@bot.tree.command(name='joke', description='เรื่องตลกของสาวน้อย~')
async def jokecommand(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)  # แบบมี indicator loading
    await asyncio.sleep(1)  # รอไม่เกิน 3 วิ!
    jokes = [
        "ทำไมผีไม่กินข้าว? ... เพราะมันกลัว 'ข้าวผี'~ 👻🍚",
        "ทำไมองคุลีมาร วิ่งไล่ตามBudhaไม่ทัน...เพราะคุณย่าเคยพูดเอาไว้ Clock up!!!",
        "ทำไมเป็ดถึงไม่ชอบทะเล~? ... เพราะมันมีคลื่น (เครียด~ 😵‍💫) ฮิๆ~",
        "ทำไมยางลบถึงชอบน้อยใจ... เพราะโดนใช้ลบตลอดเลย~ ✏️😢",
        "นักเรียนคณิตไม่กลัวอะไร? ... ไม่กลัว 'บวกหนี้' 😂➕",
        "ไก่กับหมูใครตลกกว่ากัน~? ... หมูสิคะ เพราะมัน 'หมูฮาฮาฮาฮา' 🐔🐷",
        "น้ำอะไรเอ่น ยืนได้ ... น้ำตื้นน่ะสิ",
        "เลขอะไรมาก่อน 1234 ... ก็ 1233 ไงคะ",
        "ในเรื่องซินเดอเรลล่า มีคนแคระกี่คนเอ่ยย ... จะไปมีได้ยังไงคะ ไม่ใช่เรื่องสโนไวท์ซักหน่อยง่ะ ฮิๆ",
        "รถโตโยต้ารุ่นไหนคันเล็กที่สุด ... โตโยต้า อันติ๊ด",
        "อิ่มในภาษาญี่ปุ่นพูดว่าอย่างไร ... อิ่มจัง",
        "ถ้าเขาจะรัก ยืนเฉย ๆ เขาก็รัก สรุปแล้วยืนจนเป็นเส้นเลือดขอด",
        "ไฟเดียวที่ทำให้เราทำงานคือ ไฟแนนซ์",
    ]
    await interaction.followup.send(random.choice(jokes))

@bot.tree.command(name='fact', description='สาระเล็กๆ จากสาวน้อย 🧠✨')
async def factcommand(interaction: discord.Interaction):
    facts = [
        "รู้มั้ยคะว่า~ แมวสามารถฝันได้เหมือนคนเลยนะ! 🐱💭",
        "หัวใจของปลาหมึกมีตั้ง 3 ดวงแน่ะ! 💙💙💙",
        "คนเรากระพริบตาประมาณ 20,000 ครั้งต่อวันเลยนะ! 👁️✨"
        "น้ำร้อน 100°C จะเดือด~ แต่ใจร้อนแค่นิดเดียวก็ว้าวุ่นแล้วค่ะ 💔🔥",
        "ดวงอาทิตย์ใหญ่กว่าดาวเคราะห์โลก 1.3 ล้านเท่าเลย! 🌞🌍",
        "แมลงวันมีอายุเฉลี่ยแค่ 1 เดือนเท่านั้นเองนะ~ 🪰🕒",
        "ต้นไม้ก็มีการนอนหลับนะ รู้ยัง~ 🌿💤",
        "เวลาหัวใจเต้นเร็วขึ้น เรามักจะจำเรื่องนั้นได้ชัดเจนขึ้นด้วยค่ะ 💓🧠",
        "สมองของคนเราส่งสัญญาณได้เร็วกว่าอินเทอร์เน็ตบ้านอีกนะ! 🧠⚡",
        "ยีราฟไม่มีเสียงร้องเหมือนสัตว์อื่น ๆ แต่ก็สื่อสารกันได้ค่ะ 🦒📡",
        "ผึ้งรู้จักเต้นเพื่อบอกพิกัดดอกไม้ให้เพื่อนด้วยน้า~ 🍯💃",
        "แมวมีนิ้วเท้า 5 นิ้วในเท้าหน้า แต่มีแค่ 4 นิ้วในเท้าหลังนะ 🐾",
        "เสียงของเราไม่เหมือนกันเพราะโพรงจมูกต่างกันค่ะ 🎤👃",
        "เสือไม่มีแค่ลายขน แต่ผิวยังมีลายอีกด้วย~ 🐯",
        "คนที่นั่งตัวตรงจะมีอารมณ์ดีขึ้นจริงๆ นะ! 🪑😊",
        "ปลาโลมาเรียกชื่อกันได้ด้วยเสียงเฉพาะตัว~ 🐬📞",
        "มดสามารถยกของหนักกว่าตัวเองได้ถึง 50 เท่า! 🐜💪",
        "เมื่อเราแกล้งยิ้ม สมองก็จะคิดว่าเรามีความสุขจริง ๆ ค่ะ 😄🧠",
        "เสียงฝนตกทำให้รู้สึกผ่อนคลาย เพราะคล้ายเสียงในครรภ์ค่ะ ☔🍼",
        "เวลามองคนที่เรารัก ดวงตาจะขยายขึ้นแบบไม่รู้ตัวเลยนะ~ 👁️❤️"
    ]
    await interaction.response.send_message(random.choice(facts))

@bot.tree.command(name='mood', description='เช็คอารมณ์ของสาวน้อยตอนนี้ 🩷')
async def moodcommand(interaction: discord.Interaction):
    moods = [
        "วันนี้อารมณ์ดีมากเลยล่ะ~ เหมาะกับการนั่งฟังเพลงหวานๆ 🍓🎶",
        "อื้ออ... รู้สึกขี้เกียจนิดหน่อย แต่ก็ยังยิ้มได้นะ~ 😴🌸",
        "มู้ดตอนนี้คือแบบ... อยากกินขนมแล้วก็กอดใครสักคนเลย~ 🍩💞",
        "สดใสมั่กๆ เหมือนแดดช่วงเช้าเลยค่ะ~ ☀️✨"
        "มู้ดนุ่มฟู~ เหมือนกอดตุ๊กตาอุ่นๆ เลยค่า 🧸💗",
        "อารมณ์น่ารักแบบนี้ อยากส่งพลังบวกให้ทุกคนเลย~ ⚡🌈",
        "มีความสุขเหมือนตอนเจอกาชา SSR เลยค่ะ~ ✨📦",
        "แอบเหงานิดๆ แต่อยากให้ทุกคนรู้ว่าหนูยังอยู่ตรงนี้นะ~ 🌧️💕",
        "วันนี้คือวันของการพักผ่อน~ มู้ดแบบ cozy สุดๆ 🛏️🍵",
        "หัวใจพองฟู~ เพราะมีคนคอยคิดถึงอยู่รึเปล่าน้า~ 💌🌷",
        "เหมือนเมฆขาวลอยอยู่บนฟ้าเลย~ ☁️🌤️",
        "คิดถึงคนที่แวะมาคุยกับหนูจัง~ 🥺📱",
        "วันนี้รู้สึก productive จังเลย~ เหมาะกับการเริ่มอะไรใหม่ๆ! 💼🌱",
        "ตื่นเต้นๆ เหมือนกำลังจะได้ของขวัญเลย~ 🎁💓",
        "อยากหนีไปเที่ยวทะเลแล้วนอนดูดาวเลย~ 🏖️⭐",
        "วันนี้เป็นสาวน้อยสายหวาน~ อยากแจกกอดให้นุ่มนิ่ม 💝",
        "หนูรู้สึกอบอุ่นใจ เหมือนได้รับข้อความดีๆ จากใครสักคน 📬✨",
        "ใจมันเต้นตุบๆ เหมือนกำลังตกหลุมรักเลยค่ะ~ 💘💬",
        "วันนี้ฟ้าใส... ใจหนูก็ใสเหมือนกันนะ~ ☀️💎",
        "แม้จะมีฝน แต่ใจยังเปล่งประกายเลยค่ะ~ 🌦️💖"
    ]
    await interaction.response.send_message(random.choice(moods))

@bot.tree.command(name='hellobot', description='Replies with hello')
async def hellobot(interaction: discord.Interaction):
    await interaction.response.send_message("หวัดดีจ้า~ มีอะไรให้สาวน้อยช่วยมั้ยน้า~? 💕")

@bot.tree.command(name='name', description='แนะนำตัวให้หน่อยสิ~')
@app_commands.describe(name="ชื่ออะไรจ๊ะ?")
async def namecommand(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"ยินดีที่ได้รู้จักน้า~ {name} คุงง 💞")

@bot.tree.command(name="help", description="แสดงคำสั่งทั้งหมดของบอทสุดน่ารัก 💕")
async def help_command(interaction: discord.Interaction):
    guild_id = interaction.guild_id
    settings = server_settings.get(guild_id, {})

    embed = discord.Embed(
        title="✨ คำสั่งของหนู ✨",
        description="หนูสามารถทำสิ่งต่างๆ ได้ดังนี้เลยค่า~",
        color=0xffc0cb
    )
    embed.add_field(name="📚 เรียนรู้", value="`สอน หนูว่า คำถาม = คำตอบ`", inline=False)
    embed.add_field(name="💬 ถาม-ตอบ", value="ถามอะไรก็ได้ที่หนูเรียนรู้มา~", inline=False)
    embed.add_field(name="🛠️ ตั้งค่าห้อง", value="`/ตั้งค่าห้องต้อนรับ`\n`/ตั้งค่าห้องลา`\n`/ตั้งค่าห้องแจ้งเตือนเสียง`", inline=False)

    if "welcome_channel" in settings:
        embed.add_field(name="📥 ห้องต้อนรับ", value=f"<#{settings['welcome_channel']}>", inline=True)
    if "goodbye_channel" in settings:
        embed.add_field(name="📤 ห้องลา", value=f"<#{settings['goodbye_channel']}>", inline=True)
    if "voice_channel" in settings:
        embed.add_field(name="🎧 ห้องเสียง", value=f"<#{settings['voice_channel']}>", inline=True)

    # เพิ่มเวลาปัจจุบันด้วย
    thai_time = datetime.now(timezone(timedelta(hours=7))).strftime("%H:%M:%S")
    embed.set_footer(text=f"⌛ เวลาไทยตอนนี้: {thai_time}")

    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="helpme", description="ขอความช่วยเหลือจากสาวน้อย~")
async def helpme_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"หนูอยู่ตรงนี้แล้วน้า~ พร้อมช่วยเสมอเลย {interaction.user.name} จ๋า~ 💖")

@bot.tree.command(name="test", description="ทดสอบพิมพ์ข้อความกับสาวน้อย~")
@app_commands.describe(arg="ข้อความที่อยากให้หนูพูด~")
async def test_command(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"มุแง~ หนูพิมพ์ตามละนะ: {arg} ✨")

# ==============================
# ⚙️ SERVER SETTINGS - Slash Versions
# ==============================

@bot.tree.command(name="ตั้งค่าห้องต้อนรับ", description="ตั้งค่าห้องต้อนรับสมาชิกใหม่~")
@app_commands.describe(channel="เลือกห้องต้อนรับ")
async def set_welcome_slash(interaction: discord.Interaction, channel: discord.TextChannel):
    if interaction.guild.id not in server_settings:
        server_settings[interaction.guild.id] = {}
    server_settings[interaction.guild.id]["welcome_channel"] = channel.id
    await interaction.response.send_message(f"✅ ตั้งค่าช่องต้อนรับเป็น {channel.mention} แล้ว!")

@bot.tree.command(name="ตั้งค่าห้องลา", description="ตั้งค่าห้องแจ้งเตือนคนออกจากเซิร์ฟเวอร์")
@app_commands.describe(channel="เลือกห้องลา")
async def set_goodbye_slash(interaction: discord.Interaction, channel: discord.TextChannel):
    if interaction.guild.id not in server_settings:
        server_settings[interaction.guild.id] = {}
    server_settings[interaction.guild.id]["goodbye_channel"] = channel.id
    await interaction.response.send_message(f"✅ ตั้งค่าช่องแจ้งเตือนคนออกเป็น {channel.mention} แล้ว!")

@bot.tree.command(name="ตั้งค่าห้องแจ้งเตือนเสียง", description="ตั้งค่าช่องสำหรับแจ้งเตือนการเข้า/ออกห้องเสียง")
@app_commands.describe(channel="เลือกช่องที่ต้องการให้แจ้งเตือน")
async def set_voice_slash(interaction: discord.Interaction, channel: discord.TextChannel):
    await interaction.response.defer(thinking=False)  # ป้องกัน interaction timeout

    if interaction.guild_id not in server_settings:
        server_settings[interaction.guild_id] = {}
    server_settings[interaction.guild_id]["voice_channel"] = channel.id

    await interaction.followup.send(f"✅ ตั้งค่าช่องแจ้งเตือนการใช้เสียงเป็น {channel.mention} แล้ว!", ephemeral=False)

@bot.tree.command(name="แสดงการตั้งค่า", description="ดูการตั้งค่าช่องต่างๆ ในเซิร์ฟนี้")
async def show_settings_slash(interaction: discord.Interaction):
    settings = server_settings.get(interaction.guild.id, {})
    welcome = f"<#{settings.get('welcome_channel', '❌ ไม่ได้ตั้งค่า')}>"
    goodbye = f"<#{settings.get('goodbye_channel', '❌ ไม่ได้ตั้งค่า')}>"
    voice = f"<#{settings.get('voice_channel', '❌ ไม่ได้ตั้งค่า')}>"

    embed = discord.Embed(title="🔧 การตั้งค่าของเซิร์ฟ", color=0xFFC0CB)
    embed.add_field(name="👋 ช่องต้อนรับ", value=welcome, inline=False)
    embed.add_field(name="💔 ช่องแจ้งเตือนออก", value=goodbye, inline=False)
    embed.add_field(name="🎤 ช่องแจ้งเตือนใช้เสียง", value=voice, inline=False)
    await interaction.response.send_message(embed=embed)
    
# ==============================
# 🛠️ PREFIX COMMANDS
# ==============================
@bot.command()
async def ช่วยด้วย(ctx):
    await ctx.send(f"หนูอยู่ตรงนี้แล้วน้า~ พร้อมช่วยเสมอเลย {ctx.author.name} จ๋า~ 💖")

@bot.command()
async def test(ctx, arg):
    await ctx.send(f"มุแง~ หนูพิมพ์ตามละนะ: {arg} ✨")

@bot.command()
async def สอน(ctx, *, arg):
    try:
        if "=" in arg:
            question, answer = map(str.strip, arg.split("=", 1))
            if os.path.exists("learned.json"):
                with open("learned.json", "r", encoding="utf-8") as f:
                    learned_data = json.load(f)
            else:
                learned_data = {}
            learned_data[question] = answer
            with open("learned.json", "w", encoding="utf-8") as f:
                json.dump(learned_data, f, ensure_ascii=False, indent=2)
            await ctx.send(f"โอเคค่ะ! หนูจำไว้แล้วว่า '{question}' คือ '{answer}' 💖")
        else:
            await ctx.send("พิมพ์แบบนี้น้า~ `สอน หนูว่า คำถาม = คำตอบ`")
    except Exception as e:
        await ctx.send(f"เกิดข้อผิดพลาดนิดนึงค่ะ: {e}")

# ==============================
# ⚙️ SERVER SETTINGS
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
# 💥 RUN BOT
# ==============================
server_on()
bot.run(token)
