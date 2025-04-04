import os
import discord
from discord.ext import commands
from discord import app_commands

import sys
print(sys.path)
from myserver import server_on


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot online!")
    synced = await bot.tree.sync()
    print(f"{len(synced)} command(s)")



@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1243402785161216141)
    text = f"welcome to the feild on Server, {member.mention}!"

    embed = discord.Embed(title='Welcome to the field!',
                          description=text,
                          color=0x66FFE1)


    await channel.send(text)
    await channel.send(Embed = embed)
    await member.send(text)


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1243402785161216141)
    text = f"{member.name}has left the Feild!"

    emmbed = discord.embed(title='left the feild!',
                           description=text,
                           color=0xFF0032)

    await channel.send(text)
    await channel.send(embed=emmbed)
    await member.send(text)

import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta

@bot.event
async def on_voice_state_update(member, before, after):
    channel_id = 1259688382863245393
    channel = bot.get_channel(channel_id)

    if not channel:
        print("❌ ไม่พบแชแนล! ตรวจสอบว่า Channel ID ถูกต้อง")
        return

    thailand_time = datetime.now(timezone.utc) + timedelta(hours=7)
    formatted_time = thailand_time.strftime("%Y-%m-%d %H:%M:%S")

    if before.channel is None and after.channel is not None:
        embed = discord.Embed(
            title="🎙️ เข้าห้องเสียง",
            description=f"**{member.name}** เข้าห้องเสียง **{after.channel.name}**",
            color=0x66FFE1)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"🕒 เวลา: {formatted_time} (TH)")
        await channel.send(embed=embed)

    elif before.channel is not None and after.channel is None:
        embed = discord.Embed(
            title="🎤 ออกจากห้องเสียง",
            description=f"**{member.name}** ออกจากห้องเสียง **{before.channel.name}**",
            color=0xFF0032)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"🕒 เวลา: {formatted_time} (TH)")
        await channel.send(embed=embed)

    elif before.channel != after.channel:
        embed = discord.Embed(
            title="🔄 ย้ายห้องเสียง",
            description=f"**{member.name}** ย้ายจากห้องเสียง **{before.channel.name}** ไปยังห้องเสียง **{after.channel.name}**",
            color=0xFFD800)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"🕒 เวลา: {formatted_time} (TH)")
        await channel.send(embed=embed)


import random

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

    # 🧸 จิปาถะน่ารัก
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

import random

@bot.tree.command(name='joke', description='เรื่องตลกของสาวน้อย~')
async def jokecommand(interaction: discord.Interaction):
    jokes = [
        "ทำไมผีไม่กินข้าว? ... เพราะมันกลัว 'ข้าวผี'~ 👻🍚",
        "รู้มั้ยว่าน้องแมวชอบเครื่องดื่มอะไร~? ... มิ๊ลค์ทีสิ~ เมี๊ยวว~ 🐱🧋",
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


@bot.command()
async def ช่วยด้วย(ctx):
    print(ctx.author)
    await ctx.send(f"หนูอยู่ตรงนี้แล้วน้า~ พร้อมช่วยเสมอเลย {ctx.author.name} จ๋า~ 💖")

@bot.command()
async def test(ctx, arg):
    await ctx.send(f"มุแง~ หนูพิมพ์ตามละนะ: {arg} ✨")

@bot.tree.command(name='hellobot', description='Replies with hello')
async def Hellobot(interaction: discord.Interaction):
    await interaction.response.send_message("หวัดดีจ้า~ มีอะไรให้สาวน้อยช่วยมั้ยน้า~? 💕")

@bot.tree.command(name='name')
@app_commands.describe(name="ชื่ออะไรจ๊ะ?")
async def namecommand(interaction, name: str):
    await interaction.response.send_message(f"ยินดีที่ได้รู้จักน้า~ {name} คุงง 💞")

from datetime import datetime, timezone, timedelta

@bot.tree.command(name='help', description='แสดงคำสั่งบอท')
async def helpcommand(interaction: discord.Interaction):
    thailand_time = datetime.now(timezone.utc) + timedelta(hours=7)
    formatted_time = thailand_time.strftime("%Y-%m-%d %H:%M:%S")

    embed = discord.Embed(
        title='คำสั่งของหนูเอง~ 💫',
        description='นี่คือคำสั่งทั้งหมดที่สาวน้อยคนนี้ทำได้นะคะ ✨',
        color=0xFFD1DC
    )
    embed.add_field(name='/hellobot 💬', value='ทักทายกับหนูได้น้า~', inline=False)
    embed.add_field(name='/name 💖', value='หนูจะทักทายชื่อที่พี่บอกมา~', inline=False)
    embed.add_field(name='/help 🌸', value='เอ๋? ใช้ไม่เป็นเหรอ~ งั้นอ่านตรงนี้เลยน้า~', inline=False)
    embed.set_footer(text=f"เวลาในประเทศไทยตอนนี้: {formatted_time} ⏰")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='name')
@app_commands.describe(name="=ชื่ออะไรจ้ะ?")
async def namecommand(interaction, name : str):
    await interaction.response.send_message(f"ดีฮ้าฟฟ {name}")

from datetime import datetime, timezone, timedelta

@bot.tree.command(name='help', description='แสดงคำสั่งบอท')
async def helpcommand(interaction: discord.Interaction):
    thailand_time = datetime.now(timezone.utc) + timedelta(hours=7)
    formatted_time = thailand_time.strftime("%Y-%m-%d %H:%M:%S")

    embed = discord.Embed(
        title='✨ คำสั่งของสาวน้อยบอท ✨',
        description='ฮัลโหล~ นี่คือคำสั่งทั้งหมดที่หนูทำได้น้า~ ลองเล่นดูได้นะพี่คะ! 💖',
        color=0xFFC0CB
    )

    embed.add_field(
        name='🌟 คำสั่งพื้นฐาน',
        value=(
            "`!ช่วยด้วย` — เรียกสาวน้อยให้มาช่วยทันทีเลยจ้า~\n"
            "`!test <ข้อความ>` — พิมพ์อะไรมาหนูก็จะพูดตามเลย~\n"
            "`/hellobot` — ทักทายหนูได้เลยนะ~ หนูไม่กัดน้า 🍭\n"
            "`/name <ชื่อ>` — หนูจะทักชื่อที่พี่พิมพ์มาอย่างน่ารักเลยล่ะ 💬"
        ),
        inline=False
    )

    embed.add_field(
        name='🎈 คำสั่งถามเล่นๆ จิปาถะ',
        value=(
            "`/joke` — ฟังมุกตลกกุ๊กกิ๊กจากหนู~ ฮ่าๆ\n"
            "`/fact` — สาวน้อยมาพร้อมสาระวันละนิด~ 🧠\n"
            "`/mood` — รู้มั้ยตอนนี้หนูรู้สึกยังไง~ มาดูกัน 💓"
        ),
        inline=False
    )

    embed.add_field(
        name='🎀 สไตล์ของสาวน้อยบอท 🎀',
        value=(
            "บอทตัวนี้จะพูดแบบนุ่มฟู~ ติดหวาน ๆ น่ารัก ๆ นะคะ~ 🍓\n"
            "ทุกคำสั่งจะตอบกลับด้วยอารมณ์ของสาวน้อยวัยใส ขี้เล่นนิด ๆ 💫\n"
            "เหมาะกับคนที่อยากได้เพื่อนคุยในแบบเมี๊ยว~ งุงิ~ 💕"
        ),
        inline=False
    )

    embed.set_footer(text=f"⌛ เวลาไทยตอนนี้: {formatted_time}")
    await interaction.response.send_message(embed=embed)
    
server_on()

bot.run(os.getenv('TOKEN'))
