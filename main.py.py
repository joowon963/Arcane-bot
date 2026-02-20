import discord
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="공지사항", description="공지사항을 보냅니다")
@app_commands.describe(
    제목="공지 제목을 입력하세요",
    내용="공지 내용을 입력하세요",
    채널="보낼 채널을 선택하세요"
)
async def 공지사항(interaction: discord.Interaction, 제목: str, 내용: str, 채널: discord.TextChannel):

    embed = discord.Embed(
        title=f"📢 {제목}",
        description=내용,
        color=0x5865F2
    )

    await 채널.send(embed=embed)
    await interaction.response.send_message("공지 전송 완료!", ephemeral=True)


@client.event
async def on_ready():
    await tree.sync()
    print(f"{client.user} 로그인 완료")


client.run(TOKEN)
