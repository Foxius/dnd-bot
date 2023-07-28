import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.join(current_directory, 'modules')
sys.path.append(modules_path)
import discord
from discord.ext import commands
import tkinter as tk
from tkinter import Canvas, NW
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random
import os
import sqlite3
from mathdnd import *
from savejson import *
from equipment import make_api_request
import requests
from bs4 import BeautifulSoup as bs
from asyncio import sleep
import asyncio
connection = sqlite3.connect("dnd_characters.db")
cursor = connection.cursor()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
VALID_LIMITS = [4, 6, 8, 10, 12, 20, 100]
@bot.command()
async def roll(ctx, dice_string: str, gui: str = None):
    try:
        num_dice, limit = map(int, dice_string.lower().split('d'))
    except ValueError:
        await ctx.send("Пожалуйста, укажите кубики в формате XdY, например, 2d20 для двух кубиков с гранями 20.")
        return

    if num_dice < 1 or num_dice > 20 or limit not in VALID_LIMITS:
        await ctx.send("Пожалуйста, укажите значение от 1 до 20 для количества кубиков и один из следующих кубов: d4, d6, d8, d10, d12, d20, d100.")
        return

    results = []
    for _ in range(num_dice):
        random_digit = random.randint(1, limit)
        results.append(random_digit)

    result_str = f"**Результат броска**: `{', '.join(map(str, results))}`"
    
    if gui and gui.lower() == "gui":
        image_path = f"files/images/d{limit}.png"
        image = Image.open(image_path)

        embed = discord.Embed(title=f"Бросок кубиков", description=f"Результаты бросков: {', '.join(map(str, results))}", color=discord.Color.red())

        for idx, result in enumerate(results):
            temp_image_path = f"files/images/temp_d{limit}_{idx + 1}.png"
            image_with_digit = image.copy()
            draw = ImageDraw.Draw(image_with_digit)
            center_x = image.width // 2
            center_y = image.height // 2
            font = ImageFont.truetype("files/arial.ttf", 30)
            draw.text((center_x, center_y), str(result), fill="white", anchor="mm", font=font)
            image_with_digit.save(temp_image_path)

            with open(temp_image_path, "rb") as f:
                image_data = f.read()
                embed.set_image(url=f"attachment://dice_{idx + 1}.png")

            await ctx.send(embed=embed, file=discord.File(temp_image_path, filename=f"dice_{idx + 1}.png"))

            os.remove(temp_image_path)
    
    await ctx.send(result_str)
@bot.command()  
async def check(ctx, ch):
    # Убедимся, что входная характеристика находится в списке доступных характеристик
    valid_characteristics = [
        'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma',
        'save_strength', 'save_dexterity', 'save_constitution', 'save_intelligence',
        'save_wisdom', 'save_charisma', 'acrobatics', 'investigation', 'athletics',
        'perception', 'survival', 'performance', 'intimidation', 'history', 'sleight_of_hand',
        'arcana', 'medicine', 'deception', 'nature', 'insight', 'religion', 'stealth',
        'persuasion', 'animal_handling', 'hp_dice_current', 'armor_class', 'speed', 'initiative'
    ]
    
    ch = ch.lower()  # Приведем характеристику к нижнему регистру (для регистронезависимости)
    
    if ch not in valid_characteristics:
        await ctx.send(f"Некорректная характеристика. Доступные характеристики: {', '.join(valid_characteristics)}.")
        return
    
    # Получаем ID автора команды (пользователя)
    user_id = ctx.message.author.id
    
    cursor.execute("SELECT {} FROM characters WHERE id=?".format(ch), (user_id,))
    characteristic_value = cursor.fetchone()
    
    if not characteristic_value:
        await ctx.send("Персонаж не найден в базе данных.")
        return
    dice = random.randint(1,20)
    embed = discord.Embed(title=f"Проверка характеристики - {dice + int(get_modifier(int(characteristic_value[0])))}", description=f"Результат: ({dice}) + {get_modifier(int(characteristic_value[0]))}\n ", color=discord.Color.red())
    await ctx.send(embed=embed)
@bot.command()
async def profile(ctx):
    user_id = ctx.message.author.id
    cursor.execute("SELECT * FROM characters WHERE id=?", (user_id,))
    character_data = cursor.fetchone()
    
    if not character_data:
        await ctx.send("Персонаж не найден в базе данных.")
        return
    
    embed = discord.Embed(title="Ваш Профиль", color=discord.Color.red())
    embed.description = (
        f"**Имя**: {character_data[1]}\n"
        f"**Класс**: {character_data[2]}\n"
        f"**Уровень**: {character_data[3]}\n"
        f"**Предыстория**: {character_data[4]}\n"
        f"**Имя Игрока**: {character_data[5]}\n"
        f"**Раса**: {character_data[6]}\n"
        f"**Мировоззрение**: {character_data[7]}\n"
        f"**Опыт**: {character_data[8]}\n"
        f"**Возраст**: {character_data[9]}\n"
        f"**Рост**: {character_data[10]}\n"
        f"**Вес**: {character_data[11]}\n"
        f"**Глаза**: {character_data[12]}\n"
        f"**Кожа**: {character_data[13]}\n"
        f"**Волосы**: {character_data[14]}\n"
        f"**Сила**: {character_data[17]}\n"
        f"**Ловкость**: {character_data[18]}\n"
        f"**Телосложение**: {character_data[19]}\n"
        f"**Интеллект**: {character_data[20]}\n"
        f"**Мудрость**: {character_data[21]}\n"
        f"**Харизма**: {character_data[22]}\n"
        f"**Очки Здоровья (d6)**: {character_data[47]}\n"
        f"**Класс Доспеха**: {character_data[48]}\n"
        f"**Скорость**: {character_data[49]}\n"
        f"**Инициатива**: {character_data[50]}\n"
        f"**Кость Жизни**: {character_data[50]}\n"
        f"**Список Оружия**: {character_data[52]}\n"
        f"**Снаряжение**: {character_data[53]}\n"
        f"**Предыстория**: {character_data[54]}\n"
        f"**Черты Личности**: {character_data[55]}\n"
        f"**Идеалы**: {character_data[56]}\n"
        f"**Привязанности**: {character_data[57]}\n"
        f"**Недостатки**: {character_data[58]}\n"
        f"**Золотые Монеты**: {character_data[61]}\n"
        f"**Серебряные Монеты**: {character_data[62]}\n"
        f"**Медные Монеты**: {character_data[63]}\n"
        f"**Платиновые Монеты**: {character_data[64]}\n"
        f"**Электрум Монеты**: {character_data[65]}\n"
    )

    await ctx.send(embed=embed)
@bot.command()
async def help(ctx):
    await ctx.send(embed = discord.Embed(title="Помощь", description="""`!roll [дайс] [gui]` - позволяет кинуть кубик. Аргумент gui позволяет увидеть графическое падение кубика. Например - **!roll 2d20 gui**\n
        `!check [характеристика]` - Позволяет проверить характеристику. Например - **!check charisma**\n
        `!profile` - позволяет увидеть профиль игрока\n
        `!spell [Название заклинания]` - Позволяет увидеть карточку заклинания. Например - **!spell Огненный шар**\n
        `!equipment [название-предмета]` - Позволяет подробнее узнать о предмете. Например - **!equipment leather-armor**\n
        `!newprofile [ссылка на pastebin.com]`- Создает профиль игрока. Работает от платформы LongStory. Например: **!newprofile https://pastebin.com/rUhR5ur0**. \nP.S.Если не будут заполнены выжные поля - Профиль не будет создан.\n
        `!cost [Имя предмета]`- Позволяет узнать стоимость магических предметов (источник предметов https://dnd.su/). Например - **!cost Амулет инсомнии**
        """, color=discord.Color.red()))
@bot.command()
async def newprofile(ctx, *, link):
    process_json_and_save_to_database(ctx.message.author.id, link)
    await ctx.send("Профиль создан!")
    
@bot.command()
async def spell(ctx,*, spell_name):
    # Путь к папке "spells"
    spells_folder = "spells"

    # Ищем файл с именем, соответствующим названию заклинания (добавляем расширение .jpg)
    target_file = spell_name + ".jpg"

    # Рекурсивный обход всех файлов и подпапок в папке "spells"
    for root, _, files in os.walk(spells_folder):
        if target_file in files:
            # Если файл найден, отправляем его в чат
            file_path = os.path.join(root, target_file)
            with open(file_path, "rb") as f:
                picture = discord.File(f)
                await ctx.send(file=picture)
            return

    # Если файл не найден, отправляем сообщение об ошибке
    await ctx.send(f"Заклинания {spell_name}  не найдено. Проверьте правильности и повторите попытку!")    

@bot.command()
async def equipment(ctx, equipment):
    text = make_api_request(equipment)
    embed = discord.Embed(title="Снаряжение", description=text, color=discord.Color.red())
    await ctx.send(embed=embed)
@bot.command()
async def cost(ctx, *, item):    
    # print(1)
    link = "https://dnd.su/items/"
    response = requests.get(link)
    soup = bs(response.text, "html.parser")
    cell = soup.findAll('a', class_="list-item-wrapper")
    rar = ""
    link = ""
    for c in cell:
        title = c.findAll("div", class_="list-item-title")
        rarity = c.findAll('span', class_='list-icon__quality')
        for t, r in zip(title, rarity):
            if t.text.lower() == str(item).lower():
                link = f"https://dnd.su{c.get('href')}"
                rar = str(r['title']).lower()
                print(t.text," - ", r['title'])
                break
    link = "https://dnd.su/homebrew/items/"
    response = requests.get(link)
    soup = bs(response.text, "html.parser")
    cell = soup.findAll('a', class_="list-item-wrapper")
    rar = ""
    link = ""
    for c in cell:
        title = c.findAll("div", class_="list-item-title")
        rarity = c.findAll('span', class_='list-icon__quality')
        for t, r in zip(title, rarity):
            if t.text.lower() == str(item).lower():
                link = f"https://dnd.su{c.get('href')}"
                rar = str(r['title']).lower()
                print(t.text," - ", r['title']) 
                break           
    # print(rar)
    if str(rar).lower() == 'обычный':
        embed = discord.Embed(title="Обычный предмет", url = link, description = f"Стоимость: {random.randint(50,100)} зм", color=discord.Color.light_grey())
        await ctx.send(embed = embed)
    elif str(rar).lower() == 'необычный':
        embed = discord.Embed(title="Необычный предмет", url = link, description = f"Стоимость: {random.randint(101,500)} зм", color=discord.Color.green())
        await ctx.send(embed = embed)
    elif str(rar).lower() == 'редкое':
        embed = discord.Embed(title="Редкий предмет", url = link, description = f"Стоимость: {random.randint(501,5000)} зм", color=discord.Color.blue())
        await ctx.send(embed = embed)
    elif str(rar).lower() == 'очень редкий':
        embed = discord.Embed(title="Очень редкий предмет", url = link, description = f"Стоимость: {random.randint(5001,50000)} зм", color=discord.Color.purple())
        await ctx.send(embed = embed)
    elif str(rar).lower() == 'легендарный':
        embed = discord.Embed(title="Легендарный предмет", url = link, description = f"Стоимость: {random.randint(50001,300000)} зм", color=discord.Color.gold())
        await ctx.send(embed = embed)
    elif str(rar).lower() == 'артефакт':
        embed = discord.Embed(title="Артефакт", url = link, description = f"Стоимость уточняйте у DM", color=discord.Color.red())
        await ctx.send(embed = embed)                             
    else:
        await ctx.send("Предмет не найден")
@bot.event
async def on_ready():
  guilds = len(bot.guilds)
  info = "!"
  print("[{}] Бот готов к работе.".format(info)) #в командную строку идёт инфа о запуске
  while True:
    await bot.change_presence(status = discord.Status.online, activity = discord.Activity(name = f'Dungeons & Dragons', type = discord.ActivityType.playing)) #Идёт инфа о команде помощи (префикс изменить)
    await asyncio.sleep(15)
    await bot.change_presence(status = discord.Status.online, activity = discord.Activity(name = f'!help', type = discord.ActivityType.playing)) #Инфа о количестве серверов, на котором находится бот.
    await asyncio.sleep(15)
    members = 0
    for guild in bot.guilds:
      for member in guild.members:
        members += 1
    await bot.change_presence(status = discord.Status.online, activity = discord.Activity(name = f'за {members} участниками', type = discord.ActivityType.watching)) #Общее количество участников, за которыми следит бот (Находятся на серверах)
    await asyncio.sleep(15)
bot.run('')
