import json
import sqlite3
import requests
def get_json_data_from_link(link):
    mainlink = link.replace("https://pastebin.com/", "https://pastebin.com/raw/")
    response = requests.get(mainlink)
    return response.text
def convert_json_to_dnd_character(json_data):
    character = []

    def get_value_safely(data, key, default=None):
        try:
            return data[key]
        except (KeyError, TypeError):
            return default


    character.append(("**Имя**", get_value_safely(json_data, "name")["value"]))
    character.append(("**Класс и Уровень**", get_value_safely(json_data, "info")["charClass"]["value"]))
    character.append(("**Уровень**", get_value_safely(json_data, "info")["level"]["value"]))
    character.append(("**Предыстория**", get_value_safely(json_data, "info")["background"]["value"]))
    character.append(("**Имя Игрока**", get_value_safely(json_data, "info")["playerName"]["value"]))
    character.append(("**Раса**", get_value_safely(json_data, "info")["race"]["value"]))
    character.append(("**Мировоззрение**", get_value_safely(json_data, "info")["alignment"]["value"]))
    character.append(("**Опыт**", get_value_safely(json_data, "info")["experience"]["value"]))

    # Дополнительная информация
    character.append(("**Возраст**", get_value_safely(json_data, "subInfo")["age"]["value"]))
    character.append(("**Рост**", get_value_safely(json_data, "subInfo")["height"]["value"]))
    character.append(("**Вес**", get_value_safely(json_data, "subInfo")["weight"]["value"]))
    character.append(("**Глаза**", get_value_safely(json_data, "subInfo")["eyes"]["value"]))
    character.append(("**Кожа**", get_value_safely(json_data, "subInfo")["skin"]["value"]))
    character.append(("**Волосы**", get_value_safely(json_data, "subInfo")["hair"]["value"]))

    # Способности и Навыки
    character.append(("**Очки Заклинаний (Уровень 1)**", "-"))
    character.append(("**Бонус Мастерства**", get_value_safely(json_data, "proficiency")))

    # Характеристики и Спасброски
    character.append(("**Сила**", get_value_safely(json_data, "stats")["str"]["score"]))
    character.append(("**Ловкость**", get_value_safely(json_data, "stats")["dex"]["score"]))
    character.append(("**Телосложение**", get_value_safely(json_data, "stats")["con"]["score"]))
    character.append(("**Интеллект**", get_value_safely(json_data, "stats")["int"]["score"]))
    character.append(("**Мудрость**", get_value_safely(json_data, "stats")["wis"]["score"]))
    character.append(("**Харизма**", get_value_safely(json_data, "stats")["cha"]["score"]))

    character.append(("**Спасбросок Силы**", get_value_safely(json_data, "saves")["str"]["isProf"]))
    character.append(("**Спасбросок Ловкости**", get_value_safely(json_data, "saves")["dex"]["isProf"]))
    character.append(("**Спасбросок Телосложения**", get_value_safely(json_data, "saves")["con"]["isProf"]))
    character.append(("**Спасбросок Интеллекта**", get_value_safely(json_data, "saves")["int"]["isProf"]))
    character.append(("**Спасбросок Мудрости**", get_value_safely(json_data, "saves")["wis"]["isProf"]))
    character.append(("**Спасбросок Харизмы**", get_value_safely(json_data, "saves")["cha"]["isProf"]))

    # Навыки
    for skill, info in json_data["skills"].items():
        character.append((skill.capitalize(), get_value_safely(info, "**isProf**", False)))

    # Здоровье
    character.append(("**Очки Здоровья (d6)**", get_value_safely(json_data, "vitality")["hp-dice-current"]["value"]))
    character.append(("**Класс Доспеха**", get_value_safely(json_data, "vitality")["ac"]["value"]))
    character.append(("**Скорость**", get_value_safely(json_data, "vitality")["speed"]["value"]))
    character.append(("**Инициатива**", get_value_safely(json_data, "vitality")["initiative"]["value"]))
    character.append(("**Кость Жизни**", get_value_safely(json_data, "vitality")["hit-die"]["value"]))

    # Список Оружия (Пустой в данном JSON)
    character.append(("**Список Оружия**", get_value_safely(json_data, "weaponsList")))

    # Снаряжение
    equipment_list = get_value_safely(json_data, "text")["equipment"]["value"]["data"]["content"]
    equipment = [item["content"][0]["text"] for item in equipment_list if item["type"] == "paragraph"]
    character.append(("**Снаряжение**", equipment))

    # Предыстория, Черты Личности, Идеалы, Привязанности и Недостатки
    character.append(("**Предыстория**", get_value_safely(json_data, "text")["background"]["value"]["data"]["content"][0]["content"][0]["text"]))
    character.append(("**Черты Личности**", get_value_safely(json_data, "text")["personality"]["value"]["data"]["content"][0]["content"][0]["text"]))
    character.append(("**Идеалы**", get_value_safely(json_data, "text")["ideals"]["value"]["data"]["content"][0]["content"][0]["text"]))
    character.append(("**Привязанности**", get_value_safely(json_data, "text")["bonds"]["value"]["data"]["content"][0]["content"][0]["text"]))
    character.append(("**Недостатки**", get_value_safely(json_data, "text")["flaws"]["value"]["data"]["content"][0]["content"][0]["text"]))
    character.append(("**spell_level_0**", 0))
    character.append(("**spell_level_0**", 1))
    # Монеты
    character.append(("**Золотые Монеты**", get_value_safely(json_data, "coins")["gp"]["value"]))
    character.append(("**Серебряные Монеты**", get_value_safely(json_data, "coins")["sp"]["value"]))
    character.append(("**Медные Монеты**", get_value_safely(json_data, "coins")["cp"]["value"]))
    character.append(("**Платиновые Монеты**", get_value_safely(json_data, "coins")["pp"]["value"]))
    character.append(("**Электрум Монеты**", get_value_safely(json_data, "coins")["ep"]["value"]))

    return character
def save_to_database(userid, character_data):
    conn = sqlite3.connect('dnd_characters.db')
    c = conn.cursor()

    # Create a table to store character data
    c.execute('''CREATE TABLE IF NOT EXISTS characters
                 (id TEXT PRIMARY KEY,name TEXT, char_class TEXT, level INTEGER, background TEXT, player_name TEXT,
                 race TEXT, alignment TEXT, experience INTEGER, age TEXT, height TEXT, weight TEXT,
                 eyes TEXT, skin TEXT, hair TEXT, spell_slots_1 INTEGER, proficiency INTEGER,
                 strength INTEGER, dexterity INTEGER, constitution INTEGER, intelligence INTEGER,
                 wisdom INTEGER, charisma INTEGER, save_strength INTEGER, save_dexterity INTEGER,
                 save_constitution INTEGER, save_intelligence INTEGER, save_wisdom INTEGER,
                 save_charisma INTEGER, acrobatics INTEGER, investigation INTEGER, athletics INTEGER,
                 perception INTEGER, survival INTEGER, performance INTEGER, intimidation INTEGER,
                 history INTEGER, sleight_of_hand INTEGER, arcana INTEGER, medicine INTEGER,
                 deception INTEGER, nature INTEGER, insight INTEGER, religion INTEGER, stealth INTEGER,
                 persuasion INTEGER, animal_handling INTEGER, hp_dice_current INTEGER, armor_class INTEGER,
                 speed INTEGER, initiative INTEGER, hit_die TEXT, weapons_list TEXT, equipment TEXT,
                 background_info TEXT, personality_traits TEXT, ideals TEXT, bonds TEXT, flaws TEXT,
                 spell_level_0 TEXT, spell_level_1 TEXT, gold_coins INTEGER, silver_coins INTEGER,
                 copper_coins INTEGER, platinum_coins INTEGER, electrum_coins INTEGER)''')

    # Insert character data into the table
    character_data.insert(0, userid)  # Insert userid as the first element in the list
    c.execute('''INSERT OR REPLACE INTO characters VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)''',
              character_data)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
def process_json_and_save_to_database(userid,link):
    # Get JSON data from the link
    json_data = get_json_data_from_link(link)
    jsjs = json.loads(json_data)
    # Convert JSON data to DND character list
    dnd_character = convert_json_to_dnd_character(jsjs)
    
    # Prepare character data as a tuple for saving into the database
    character_data_for_db = [str(item[1]) for item in dnd_character]
    # If any value is missing, replace it with None
    while len(character_data_for_db) < 65:
        character_data_for_db.append(None)
    
    # Save the DND character data to the SQLite3 database
    save_to_database(userid,character_data_for_db)