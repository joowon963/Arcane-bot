import discord
from discord import app_commands
import os
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")

# ---- 웹서버 추가 (Render용) ----
app = Flask('')

@app.route('/')
def home():
    return "Bot Alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ---- 디스코드 봇 ----
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="공지사항", description="공지 보내기")
async def gongji(interaction: discord.Interaction, 제목: str, 내용: str, 채널: discord.TextChannel):
    embed = discord.Embed(title=f"📢 {제목}", description=내용)
    await 채널.send(embed=embed)
    await interaction.response.send_message("공지 완료!", ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print("로그인 완료")

keep_alive()
client.run(TOKEN)
