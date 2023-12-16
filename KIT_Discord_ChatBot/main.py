import os
import discord
import base64
from src.discordBot import DiscordClient, Sender
from src.server import keep_alive
import datetime

from module import food
from module import chatgpt as gpt
from module import elasticsearch_engine as ese
print("main.py 실행중")
file_path = "discord_api_key_base64.txt"

with open(file_path, 'r') as file:
    # 파일 내용 읽기
    encoded_content = file.read()

    # base64 디코딩
    decoded_content = base64.b64decode(encoded_content)
    decoded_string = decoded_content.decode('utf-8')



def run():
    client = DiscordClient()
    sender = Sender()

    @client.tree.command(name="chat", description="Have a chat with ChatGPT")
    async def chat(interaction: discord.Interaction, *, message: str):
        user_id = interaction.user.id
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        receive = gpt.chat(message)
        await sender.send_message(interaction, message, receive)



    
    @client.tree.command(name='기숙사',description='기숙사 메뉴을 알 수 있습니다(푸름, 오름1, 오름3, 분식당, 교직원식당, 학생식당)')
    async def menu(interaction: discord.Integration,이름 : str):
        embed = discord.Embed(title = '😝오늘의 식단😝', description = food.get_menu_data(이름), colour=0x3498DB)
        await interaction.response.send_message(embed = embed)


    @client.tree.command(name="ping", description="Ping!")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    @client.tree.command(name='메롱',description='😝')
    async def wow(interaction : discord.Integration):
        embed = discord.Embed(title='😝',description='😝',colour=0x3498DB)
        await interaction.response.send_message(embed = embed)

    client.run(decoded_string)


if __name__ == '__main__':
    keep_alive()
    run()
