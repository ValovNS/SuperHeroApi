import json
import requests

#       Более оптимизированный вариант кода, который также запрашивает у пользователя условия и производит поиск персонажа
#       Но уже в рамках одного json запроса со всеми персонажами, что оптимизирует скорость выдачи ответа

def normalize_gender(input_gender):
    """Приведение ввода пола к стандартным значениям."""
    male_aliases = {"муж", "мужской", "мужчина", "м", "m", "male"}
    female_aliases = {"жен", "женский", "женщина", "ж", "f", "female"}
    none_aliases = {"no", "нет пола", "-", "н", "n", "none"}
    any_aliases = {"any", "любой", "все", "без разницы", "неважно"}

    input_gender = input_gender.strip().lower()
    if input_gender in male_aliases:
        return "Male"
    elif input_gender in female_aliases:
        return "Female"
    elif input_gender in none_aliases:
        return "None"
    elif input_gender in any_aliases:
        return "Any"
    return None  # Неверный ввод


def normalize_yes_no(input_value):
    """Приведение ввода наличия профессии к логическим значениям."""
    yes_aliases = {"y", "yes", "t", "true", "on", "1", "да", "д"}
    no_aliases = {"n", "no", "f", "false", "off", "0", "нет", "н"}

    input_value = input_value.strip().lower()
    if input_value in yes_aliases:
        return True
    elif input_value in no_aliases:
        return False
    return None  # Неверный ввод


def convert_height_to_cm(height_str):
    """Конвертирует строку роста в сантиметры."""
    if " cm" in height_str:
        return int(height_str.replace(" cm", "").strip())
    elif " m" in height_str:
        try:
            return int(float(height_str.replace(" m", "").strip()) * 100)
        except ValueError:
            return 0
    return 0  # Если формат неизвестен


def find_tallest_hero_from_api(url):
    try:
        # Загружаем данные из API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return

    # Получаем корректный пол от пользователя
    while True:
        gender_input = input("Введите пол персонажа: ")
        gender = normalize_gender(gender_input)
        if gender is not None:
            break
        print("Некорректный ввод пола. Попробуйте снова. Варианты: муж, жен, нет пола, любой.")

    # Получаем корректное значение для профессии
    while True:
        has_occupation_input = input("Есть ли у персонажа работа?: ")
        has_occupation = normalize_yes_no(has_occupation_input)
        if has_occupation is not None:
            break
        print("Уточните есть ли у персонажа работа (Да/Нет, True/False)")

    tallest_height = 0
    tallest_hero_name = None

    for hero in data:
        hero_gender = hero.get('appearance', {}).get('gender', "-")
        hero_occupation = hero.get('work', {}).get('occupation', "-")
        height = hero.get('appearance', {}).get('height', [None, "0 cm"])[1]
        hero_name = hero.get('name', "Unknown")

        # Проверяем пол (включая любое значение) и наличие/отсутствие профессии
        is_occupation_present = hero_occupation != "-"
        if (
                (gender == "Any") or
                (gender == "None" and hero_gender == "-") or
                (gender != "Any" and gender != "None" and hero_gender == gender)
        ) and (is_occupation_present == has_occupation):
            try:
                height_cm = convert_height_to_cm(height)
                if height_cm > tallest_height:
                    tallest_height = height_cm
                    tallest_hero_name = hero_name
            except ValueError:
                continue

    if tallest_hero_name:
        print(f"Самый высокий персонаж - {tallest_hero_name}, ростом - {tallest_height} см")
    else:
        print("Не найдено персонажей, удовлетворяющих условиям.")

# URL API
api_url = "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json"
find_tallest_hero_from_api(api_url)

