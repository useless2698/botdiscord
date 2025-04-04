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
    mes = message.content

    if mes in ['สวัสดี', 'หวัดดี', 'ไฮๆ']:
        response = random.choice(["หวัดดี ว่าไงพวก", "หวัดดีมีไร"])
        await message.channel.send(response)

    elif mes == 'เป็นไงบ้าง':
        await message.channel.send(f"ก็สบายดี, {message.author.name}")

    await bot.process_commands(message)


@bot.command()
async def ช่วยด้วย(ctx):
    print(ctx.author)
    await ctx.send(f"พร้อมล้ะ {ctx.author.name}!")


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.tree.command(name='hellobot', description='Replies with hello')
async def Hellobot(interaction: discord.Interaction):
    await interaction.response.send_message("มีอะไร อยากให้ช่วยมั้ย")


@bot.tree.command(name='name')
@app_commands.describe(name="=ชื่ออะไรจ้ะ?")
async def namecommand(interaction, name : str):
    await interaction.response.send_message(f"ดีฮ้าฟฟ {name}")

from datetime import datetime, timezone, timedelta

@bot.tree.command(name='help', description='แสดงคำสั่งบอท')
async def helpcommand(interaction: discord.Interaction):
    thailand_time = datetime.now(timezone.utc) + timedelta(hours=7)
    formatted_time = thailand_time.strftime("%Y-%m-%d %H:%M:%S")

    embed = discord.Embed(title='คำสั่งของบอท', description='คำสั่งทั้งหมดที่บอทรองรับ', color=0xFFD800)
    embed.add_field(name='/hellobot', value='ใช้ทักทายบอท', inline=False)
    embed.add_field(name='/neme', value='คำสั่งนี้ช่วยตอบกลับชื่อผู้ใช้', inline=False)
    embed.add_field(name='/help', value='ก็รู้นิ่ว่าใช้ยังไง ไม่งั้นคงไม่เห็นข้อความนี้', inline=False)

    embed.set_author(name='Admin Toy', url='https://www.instagram.com/tt_t2e/',
                     icon_url='https://instagram.fbkk22-1.fna.fbcdn.net/v/t51.2885-19/485904903_708049581565224_2367582016975570743_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_ht=instagram.fbkk22-1.fna.fbcdn.net&_nc_cat=100&_nc_oc=Q6cZ2QFIgTkUhFHL3szQNEqFxOvTPk-HvaHRowS9WAIRLRMyLOi-K8B0IOLcpieTz3jBNk0&_nc_ohc=M5evvr1vrH0Q7kNvgFcafqH&_nc_gid=t98COJz3vaVLFPhcQxks7w&edm=AP4sbd4BAAAA&ccb=7-5&oh=00_AYFHQ22xBI959z2fEo0yo7vhvOgq9_kngfhiUSv6AhgcNA&oe=67F430DA&_nc_sid=7a9f4b')
    embed.set_thumbnail(
        url='https://instagram.fbkk22-1.fna.fbcdn.net/v/t51.2885-19/485904903_708049581565224_2367582016975570743_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_ht=instagram.fbkk22-1.fna.fbcdn.net&_nc_cat=100&_nc_oc=Q6cZ2QFIgTkUhFHL3szQNEqFxOvTPk-HvaHRowS9WAIRLRMyLOi-K8B0IOLcpieTz3jBNk0&_nc_ohc=M5evvr1vrH0Q7kNvgFcafqH&_nc_gid=t98COJz3vaVLFPhcQxks7w&edm=AP4sbd4BAAAA&ccb=7-5&oh=00_AYFHQ22xBI959z2fEo0yo7vhvOgq9_kngfhiUSv6AhgcNA&oe=67F430DA&_nc_sid=7a9f4b')
    embed.set_footer(icon_url='https://instagram.fbkk22-1.fna.fbcdn.net/v/t51.2885-19/485904903_708049581565224_2367582016975570743_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_ht=instagram.fbkk22-1.fna.fbcdn.net&_nc_cat=100&_nc_oc=Q6cZ2QFIgTkUhFHL3szQNEqFxOvTPk-HvaHRowS9WAIRLRMyLOi-K8B0IOLcpieTz3jBNk0&_nc_ohc=M5evvr1vrH0Q7kNvgFcafqH&_nc_gid=t98COJz3vaVLFPhcQxks7w&edm=AP4sbd4BAAAA&ccb=7-5&oh=00_AYFHQ22xBI959z2fEo0yo7vhvOgq9_kngfhiUSv6AhgcNA&oe=67F430DA&_nc_sid=7a9f4b', text = f"🕒 เวลา: {formatted_time} (TH)")

    await interaction.response.send_message(embed=embed)

server_on()

bot.run(os.getenv('TOKEN'))
