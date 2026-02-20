import discord
from discord import app_commands
import os
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")

# -------- Render용 웹서버 --------
app = Flask('')

@app.route('/')
def home():
    return "Bot Alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -------- 디스코드 봇 --------
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="공지사항", description="공지 보내기")
@app_commands.describe(
    제목="공지 제목",
    내용="공지 내용",
    채널="보낼 채널"
)
async def gongji(interaction: discord.Interaction, 제목: str, 내용: str, 채널: discord.TextChannel):

    # ⭐ 3초 제한 방지
    await interaction.response.defer(ephemeral=True)

    try:
        # ⭐ 권한 확인
        perms = 채널.permissions_for(interaction.guild.me)
        if not perms.send_messages:
            await interaction.followup.send("❌ 그 채널에 메시지 보낼 권한이 없어요.")
            return

        embed = discord.Embed(
            title=f"📢 {제목}",
            description=내용,
            color=0x5865F2
        )

        await 채널.send(embed=embed)
        await interaction.followup.send("✅ 공지 전송 완료!")

    except Exception as e:
        await interaction.followup.send(f"❌ 오류 발생: {e}")

@client.event
async def on_ready():
    await tree.sync()
    print(f"{client.user} 로그인 완료")

keep_alive()
client.run(TOKEN)
