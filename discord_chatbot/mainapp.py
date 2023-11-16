import discord
from discord import app_commands,Integration,Object
from discord.ext import commands
from discord.ui import Button, View
from discord import ButtonStyle
import module.food as food
import random

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
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

class SelectMenu(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label="test1",description="test1 설명"),
                discord.SelectOption(label="test2",description="test2 설명"),
                discord.SelectOption(label="test3",description="test3 설명"),]
        super().__init__(placeholder = "Select 메뉴 창 입니다.", options = options)

class Select(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SelectMenu())

@tree.command(name='chat', description='만능 명령어를 경험해보세요',guild=guild)
async def select(interaction: discord.Interaction):
    await interaction.response.send_message(content="여기는 1번content", view=Select())

    
client.run('OTYyOTE0MjEwMzIzNTI1NjYy.G1dBk_.WsNAszVjJCcG2wy3Ovlj36gWruOqiPuu5DxFHs')