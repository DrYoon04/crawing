#imports
import random

import discord
from discord import app_commands
from discord.ext import commands

from module import chatgpt as gpt
from module import food

file_path = '/Users/dryoon04/Documents/GitHub/university-project/discord_chatbot/discord_api_token.txt'

# 파일 열기 (읽기 모드로 열기)
with open(file_path, 'r', encoding='utf-8') as file:
    # 파일 내용 읽어오기
    file_content = file.read()


#paramètres
intents = discord.Intents.all()
client = discord.Client(intents = intents)
activity = discord.Activity(type = discord.ActivityType.streaming, name="name", url = "twitch_url")
tree = app_commands.CommandTree(client)
bot = commands.Bot(intents=intents, command_prefix="!")
blue = discord.Color.from_rgb(0, 0, 200)
red = discord.Color.from_rgb(200, 0, 0)
green = discord.Color.from_rgb(0, 200, 0)
discord_blue = discord.Color.from_rgb(84, 102, 244)

guild=discord.Object(id=951082793037873212)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=951082793037873212))
    print('Ready!')

@tree.command(name='핑',description='핑!',guild=guild)
async def first_command(interaction):
    await interaction.response.send_message('퐁')

@tree.command(name='기숙사',description='기숙사 메뉴을 알 수 있습니다(푸름, 오름1, 오름3)',guild=guild)
async def menu(interaction: discord.Integration,동이름 : str):
    embed  = discord.Embed(title = '😝오늘의 식단😝', description = food.get_menu_data(동이름),colour=0x3498DB)
    await interaction.response.send_message(embed = embed)

@tree.command(name='학생회관',description='학식 메뉴을 알 수 있습니다(분식당, 교직원식당, 학생식당)',guild=guild)
async def menu(interaction: discord.Integration,학식 : str):
    embed  = discord.Embed(title = '😝오늘의 식단😝', description = food.school_food(학식),colour=0x3498DB)
    await interaction.response.send_message(embed = embed)

@tree.command(name='주사위',description='주사위가 조금... 이상한거 같습니다..!',guild=guild)
async def rsp(interaction: discord.Integration,넣을숫자 :int):
    pick = random.randint(1,넣을숫자)
    embed = discord.Embed(title='결과!',description=pick,colour=0x3498DB)
    await interaction.response.send_message(embed = embed)

@tree.command(name='메롱',description='😝',guild=guild)
async def wow(interaction : discord.Integration):
    embed = discord.Embed(title='😝',description='😝',colour=0x3498DB)
    await interaction.response.send_message(embed = embed)


@tree.command(name='chat', description='만능 명령어를 경험해보세요',guild=guild)
async def chat(interaction: discord.Integration,질문사항 : str):
    embed = discord.Embed(title = "GPT", description =gpt.chat(질문사항) ,colour=0x3498DB)

    await interaction.response.send_message(embed = embed)

    
client.run(file_content)