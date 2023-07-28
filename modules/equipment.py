import requests

def parse_weapon(weapon_data):
    name = weapon_data.get("name", "Unknown Name")
    weapon_category = weapon_data.get("equipment_category", {}).get("name", "Unknown Category")
    damage_dice = weapon_data["damage"]["damage_dice"]
    cost_quantity = weapon_data["cost"]["quantity"]
    cost_unit = weapon_data["cost"]["unit"]
    return f"**Название:** {name}\n**Категория:** {weapon_category}\n**Кубик урона:** {damage_dice}\n**Стоимость:** {cost_quantity} {cost_unit}"

def parse_armor(armor_data):
    name = armor_data.get("name", "Unknown Name")
    armor_category = armor_data.get("equipment_category", {}).get("name", "Unknown Category")
    armor_class = armor_data.get("armor_class", "Unknown Armor Class")
    cost_quantity = armor_data["cost"]["quantity"]
    cost_unit = armor_data["cost"]["unit"]
    return f"**Название:** {name}\n**Категория:** {armor_category}\n**Класс брони:** {armor_class}\n**Стоимость:** {cost_quantity} {cost_unit}"

def parse_gear(gear_data):
    name = gear_data.get("name", "Unknown Name")
    gear_category = gear_data.get("equipment_category", {}).get("name", "Unknown Category")
    cost_quantity = gear_data["cost"]["quantity"]
    cost_unit = gear_data["cost"]["unit"]
    return f"**Название:** {name}\n**Категория:** {gear_category}\n**Стоимость:** {cost_quantity} {cost_unit}"

def parse_equipment_pack(pack_data):
    name = pack_data.get("name", "Unknown Name")
    gear_category = pack_data.get("equipment_category", {}).get("name", "Unknown Category")
    contents = pack_data.get("contents", [])
    contents_names = [item.get("name", "Unknown Item") for item in contents]
    contents_str = ", ".join(contents_names)
    cost_quantity = pack_data["cost"]["quantity"]
    cost_unit = pack_data["cost"]["unit"]
    return f"""**Название:** {name}\n**Категория:** {gear_category}\n**Содержимое:** {contents_str}\n**Стоимость:** {cost_quantity} {cost_unit}"""

def make_api_request(equipment):
    try:
        response = requests.get(f"https://www.dnd5eapi.co/api/equipment/{equipment}")
        response.raise_for_status()  # Проверка наличия ошибок в ответе

        data = response.json()

        # Если получен ответ с ошибкой "Not found", отправить сообщение
        if "error" in data and data["error"] == "Not found":
            return "Предмет не найден"
        # В противном случае, выполнить парсинг JSON и извлечение нужных данных
        if "Weapon" in data['equipment_category']['name']:
            return parse_weapon(data)
        elif "Armor" in data['equipment_category']['name']:
            return parse_armor(data)
        elif "Gear" in data['equipment_category']['name']:
            return parse_gear(data)
        elif "EquipmentPack" in data['equipment_category']['name']:
            return parse_equipment_pack(data)
        else:
            return "Неизвестный тип предмета или недостаточно данных для обработки."

    except requests.exceptions.RequestException as e:
        return f"Ошибка при выполнении запроса: {e}"
    except ValueError as e:
        return f"Ошибка при обработке ответа: {e}"
