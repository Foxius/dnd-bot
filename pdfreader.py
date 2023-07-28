import json
import requests
# def extract_spell_names(spell_data):
#     return [spell["content"][0]["text"] for spell in spell_data]
def convert_json_to_dnd_character(json_data):
    character = []

    character.append(("**Имя**", json_data["name"]["value"]))
    character.append(("**Класс и Уровень**", json_data["info"]["charClass"]["value"]))
    character.append(("**Уровень**", json_data["info"]["level"]["value"]))
    character.append(("**Предыстория**", json_data["info"]["background"]["value"]))
    character.append(("**Имя Игрока**", json_data["info"]["playerName"]["value"]))
    character.append(("**Раса**", json_data["info"]["race"]["value"]))
    character.append(("**Мировоззрение**", json_data["info"]["alignment"]["value"]))
    character.append(("**Опыт**", json_data["info"]["experience"]["value"]))

    # Дополнительная информация
    character.append(("**Возраст**", json_data["subInfo"]["age"]["value"]))
    character.append(("**Рост**", json_data["subInfo"]["height"]["value"]))
    character.append(("**Вес**", json_data["subInfo"]["weight"]["value"]))
    character.append(("**Глаза**", json_data["subInfo"]["eyes"]["value"]))
    character.append(("**Кожа**", json_data["subInfo"]["skin"]["value"]))
    character.append(("**Волосы**", json_data["subInfo"]["hair"]["value"]))

    # Способности и Навыки
    # character.append(("**Очки Заклинаний (Уровень 1)**", json_data["spells"]["slots-1"]["value"]))
    character.append(("**Бонус Мастерства**", json_data["proficiency"]))

    # Характеристики и Спасброски
    character.append(("**Сила**", json_data["stats"]["str"]["score"]))
    character.append(("**Ловкость**", json_data["stats"]["dex"]["score"]))
    character.append(("**Телосложение**", json_data["stats"]["con"]["score"]))
    character.append(("**Интеллект**", json_data["stats"]["int"]["score"]))
    character.append(("**Мудрость**", json_data["stats"]["wis"]["score"]))
    character.append(("**Харизма**", json_data["stats"]["cha"]["score"]))

    character.append(("**Спасбросок Силы**", json_data["saves"]["str"]["isProf"]))
    character.append(("**Спасбросок Ловкости**", json_data["saves"]["dex"]["isProf"]))
    character.append(("**Спасбросок Телосложения**", json_data["saves"]["con"]["isProf"]))
    character.append(("**Спасбросок Интеллекта**", json_data["saves"]["int"]["isProf"]))
    character.append(("**Спасбросок Мудрости**", json_data["saves"]["wis"]["isProf"]))
    character.append(("**Спасбросок Харизмы**", json_data["saves"]["cha"]["isProf"]))

    # Навыки
    for skill, info in json_data["skills"].items():
        character.append((skill.capitalize(), info.get("**isProf**", False)))

    # Здоровье
    character.append(("**Очки Здоровья (d6)**", json_data["vitality"]["hp-dice-current"]["value"]))
    character.append(("**Класс Доспеха**", json_data["vitality"]["ac"]["value"]))
    character.append(("**Скорость**", json_data["vitality"]["speed"]["value"]))
    character.append(("**Инициатива**", json_data["vitality"]["initiative"]["value"]))
    character.append(("**Кость Жизни**", json_data["vitality"]["hit-die"]["value"]))

    # Список Оружия (Пустой в данном JSON)
    character.append(("**Список Оружия**", json_data["weaponsList"]))

    # Снаряжение
    equipment_list = json_data["text"]["equipment"]["value"]["data"]["content"]
    equipment = [item["content"][0]["text"] for item in equipment_list if item["type"] == "paragraph"]
    character.append(("**Снаряжение**", equipment))

    # Предыстория, Черты Личности, Идеалы, Привязанности и Недостатки
    character.append(("**Предыстория**", json_data["text"]["background"]["value"]["data"]["content"][0]["content"][0]["text"]))
    character.append(("**Черты Личности**", json_data["text"]["personality"]["value"]["data"]["content"][0]["content"][0]["text"]))
    character.append(("**Идеалы**", json_data["text"]["ideals"]["value"]["data"]["content"][0]["content"][0]["text"]))
    character.append(("**Привязанности**", json_data["text"]["bonds"]["value"]["data"]["content"][0]["content"][0]["text"]))
    character.append(("**Недостатки**", json_data["text"]["flaws"]["value"]["data"]["content"][0]["content"][0]["text"]))

    # if "spells-level-0" in json_data:
    #     spells_level_0 = extract_spell_names(json_data["spells-level-0"]["value"]["data"]["content"])
    #     character.append(("**Заклинания - Уровень 0**", spells_level_0))

    # # Заклинания - Уровень 1
    # if "spells-level-1" in json_data:
    #     spells_level_1 = extract_spell_names(json_data["spells-level-1"]["value"]["data"]["content"])
    #     character.append(("**Заклинания - Уровень 1**", spells_level_1))

    # Монеты
    character.append(("**Золотые Монеты**", json_data["coins"]["gp"]["value"]))
    character.append(("**Серебряные Монеты**", json_data["coins"]["sp"]["value"]))
    character.append(("**Медные Монеты**", json_data["coins"]["cp"]["value"]))
    character.append(("**Платиновые Монеты**", json_data["coins"]["pp"]["value"]))
    character.append(("**Электрум Монеты**", json_data["coins"]["ep"]["value"]))

    return character

# Load the JSON data from a file or wherever it is stored
response = requests.get("https://pastebin.com/raw/rUhR5ur0")
json_data = response.text
# json_data = '''
# {"jsonType":"character","template":"default","name":{"value":"Гаррет Рейнхард"},"hiddenName":"Бурный Угол_597557694","info":{"charClass":{"name":"charClass","label":"класс и уровень","value":"Маг"},"level":{"name":"level","label":"уровень","value":1},"background":{"name":"background","label":"предыстория","value":"Благородный"},"playerName":{"name":"playerName","label":"имя игрока","value":""},"race":{"name":"race","label":"раса","value":"Человек"},"alignment":{"name":"alignment","label":"мировоззрение","value":"Нейтральный-Добрый"},"experience":{"name":"experience","label":"опыт","value":""}},"subInfo":{"age":{"name":"age","label":"возраст","value":"20"},"height":{"name":"height","label":"рост","value":"180"},"weight":{"name":"weight","label":"вес","value":""},"eyes":{"name":"eyes","label":"глаза","value":""},"skin":{"name":"skin","label":"кожа","value":""},"hair":{"name":"hair","label":"волосы","value":""}},"spellsInfo":{"base":{"name":"base","label":"Базовая характеристика заклинаний","value":""},"save":{"name":"save","label":"Сложность спасброска","value":""},"mod":{"name":"mod","label":"Бонус атаки заклинанием","value":""}},"spells":{"slots-1":{"value":2}},"proficiency":2,"stats":{"str":{"name":"str","label":"Сила","score":11,"modifier":-5,"check":-5},"dex":{"name":"dex","label":"Ловкость","score":14,"modifier":1,"check":1},"con":{"name":"con","label":"Телосложение","score":15,"modifier":-5,"check":-5},"int":{"name":"int","label":"Интеллект","score":16,"modifier":-5,"check":-5},"wis":{"name":"wis","label":"Мудрость","score":9,"modifier":null,"check":-5},"cha":{"name":"cha","label":"Харизма","score":13,"modifier":-5,"check":-5}},"saves":{"str":{"name":"str","isProf":false},"dex":{"name":"dex","isProf":false},"con":{"name":"con","isProf":false},"int":{"name":"int","isProf":true},"wis":{"name":"wis","isProf":true},"cha":{"name":"cha","isProf":false}},"skills":{"acrobatics":{"baseStat":"dex","name":"acrobatics","label":"Акробатика"},"investigation":{"baseStat":"int","name":"investigation","label":"Анализ"},"athletics":{"baseStat":"str","name":"athletics","label":"Атлетика"},"perception":{"baseStat":"wis","name":"perception","label":"Восприятие"},"survival":{"baseStat":"wis","name":"survival","label":"Выживание"},"performance":{"baseStat":"cha","name":"performance","label":"Выступление"},"intimidation":{"baseStat":"cha","name":"intimidation","label":"Запугивание"},"history":{"baseStat":"int","name":"history","label":"История","isProf":1},"sleight of hand":{"baseStat":"dex","name":"sleight of hand","label":"Ловкость рук"},"arcana":{"baseStat":"int","name":"arcana","label":"Магия"},"medicine":{"baseStat":"wis","name":"medicine","label":"Медицина"},"deception":{"baseStat":"cha","name":"deception","label":"Обман"},"nature":{"baseStat":"int","name":"nature","label":"Природа"},"insight":{"baseStat":"wis","name":"insight","label":"Проницательность"},"religion":{"baseStat":"int","name":"religion","label":"Религия"},"stealth":{"baseStat":"dex","name":"stealth","label":"Скрытность"},"persuasion":{"baseStat":"cha","name":"persuasion","label":"Убеждение","isProf":1},"animal handling":{"baseStat":"wis","name":"animal handling","label":"Уход за животными"}},"vitality":{"hp-dice-current":{"value":1},"hp-dice-multi":{},"ac":{"value":12},"speed":{"value":30},"initiative":{"value":2},"hit-die":{"value":"d6"}},"weaponsList":[],"weapons":{},"text":{"attacks":{"value":{"data":{"type":"doc","content":[{"type":"resource","attrs":{"id":"resource-1690099758835","textName":"attacks"}},{"type":"paragraph"}]}},"isHidden":false},"equipment":{"value":{"data":{"type":"doc","content":[{"type":"resource","attrs":{"id":"resource-1690096367426","textName":"equipment"}},{"type":"paragraph","content":[{"type":"text","text":"Парадная Одежда "}]},{"type":"paragraph","content":[{"type":"text","text":"Перстень-печатка "}]},{"type":"paragraph","content":[{"type":"text","text":"Свиток с родословной "}]},{"type":"paragraph","content":[{"type":"text","text":"Магическая фокусировка (посох) "}]},{"type":"paragraph","content":[{"type":"text","text":"Набор путешественника "}]},{"type":"paragraph","content":[{"type":"text","text":"Книга Заклинаний"}]}]}}},"prof":{"value":{"data":{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Языки: Эльфийский, общий"}]},{"type":"paragraph","content":[{"type":"text","text":"Оружие: Кинжалы, дротики, пращи, боевые посохи, лёгкие арбалеты"}]}]}}},"background":{"value":{"data":{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Предыстория Гаррета Рейнхардта началась в благородной семье, проживающей в прекрасном городе Элмор. Семья Рейнхардтов была известна своими великими воинскими традициями и преуспевающими торговыми делами."}]}]}}},"personality":{"value":{"data":{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Несмотря на благородное рождение, я не ставлю себя выше народа. У всех нас течёт одинаковая кровь."}]}]}}},"ideals":{"value":{"data":{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Независимость. Я должен доказать, что справлюсь и без заботы своей семьи."}]}]}}},"bonds":{"value":{"data":{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Я пойду на любой риск, лишь бы заслужить признание семьи."}]}]}}},"flaws":{"value":{"data":{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Я часто навлекаю позор на свою семью словами и действиями."}]}]}}},"spells-level-0":{"value":{"data":{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Защита от оружия [Blade ward]"}]},{"type":"paragraph","content":[{"type":"text","text":"Огненный снаряд [Fire bolt]"}]},{"type":"paragraph","content":[{"type":"text","text":"Погребальный звон [Toll the dead]"}]}]}}},"spells-level-1":{"value":{"data":{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Доспехи мага [Mage armor]"}]},{"type":"paragraph","content":[{"type":"text","text":"Цветной шарик [Chromatic orb]"}]},{"type":"paragraph","content":[{"type":"text","text":"Усыпление [Sleep] "}]},{"type":"paragraph","content":[{"type":"text","text":"Волшебная стрела [Magic missile] "}]},{"type":"paragraph","content":[{"type":"text","text":"Жуткий смех Таши [Tasha's hideous laughter]"}]}]}}}},"coins":{"gp":{"value":25},"total":{"value":0},"sp":{"value":0},"cp":{"value":0},"pp":{"value":0},"ep":{"value":0}},"resources":{"resource-1690096367426":{"id":"resource-1690096367426","name":"","current":0,"max":1,"location":"equipment"},"resource-1690099758835":{"id":"resource-1690099758835","name":"Б. Посох  +2","current":1,"max":6,"location":"attacks","isShortRest":false,"icon":""},"resource-1690100506520":{"id":"resource-1690100506520","name":"","current":0,"max":1,"location":"prof"}},"bonusesSkills":{},"bonusesStats":{},"conditions":[],"avatar":{"jpeg":"https://lss-s3-files.s3.eu-north-1.amazonaws.com/avatar/64b8e59d49365d9d4be3ea9c.jpeg?mod=1690100559730","webp":"https://lss-s3-files.s3.eu-north-1.amazonaws.com/avatar/64b8e59d49365d9d4be3ea9c.webp?mod=1690100559714"},"inspiration":false}
# '''
# Parse the JSON data
character_data = json.loads(json_data)

# Convert JSON to DND character list
dnd_character = convert_json_to_dnd_character(character_data)

# Print the DND character list
for item in dnd_character:
    print(f"{item[0]}: {item[1]}")
