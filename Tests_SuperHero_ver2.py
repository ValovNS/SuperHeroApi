import json
import requests
from itertools import product

def normalize_gender(input_gender):
    """Приведение ввода пола к стандартным значениям."""
    male_aliases = {"муж", "мужской", "мужчина", "м", "m", "male"}
    female_aliases = {"жен", "женский", "женщина", "ж", "f", "female"}
    none_aliases = {"no", "нет пола", "-", "н", "n", "none"}
    any_aliases = {"any", "любой", "все", "без разницы"}

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

def find_tallest_hero(data, gender, has_occupation):
    """Находит самого высокого героя по заданным параметрам."""
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

    return tallest_hero_name, tallest_height

def validate_combination(gender, has_occupation):
    """Валидация данных комбинации пола и профессии."""
    valid_genders = {"Male", "Female", "None", "Any"}
    if gender not in valid_genders:
        return False, "Некорректный пол"
    if not isinstance(has_occupation, bool):
        return False, "Некорректное значение наличия профессии"
    if gender not in valid_genders and not isinstance(has_occupation, bool):
        return False, "Некорректный пол и Некорректное значение наличия профессии"
    return True, ""

def test_all_combinations(data):
    """Тестирует все комбинации пола и наличия/отсутствия работы."""
    genders = ["Male", "Female", "None", "Any", "123", "!"]
    occupations = [True, False, "yes", "#"]
    combinations = product(genders, occupations)

    results = []
    for gender, has_occupation in combinations:
        is_valid, error_message = validate_combination(gender, has_occupation)
        if not is_valid:
            results.append({
                "Gender": gender,
                "Has Occupation": has_occupation,
                "Error": error_message
            })
        else:
            hero_name, hero_height = find_tallest_hero(data, gender, has_occupation)
            results.append({
                "Gender": gender,
                "Has Occupation": has_occupation,
                "Tallest Hero": hero_name or "Not Found",
                "Height (cm)": hero_height if hero_height > 0 else "N/A"
            })

    return results

def main():
    url = "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json"
    try:
        # Загружаем данные из API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return

    # Запуск попарного тестирования
    results = test_all_combinations(data)

    # Вывод результатов
    for result in results:
        if "Error" in result:
            print(f"Ошибка: Пол = {result['Gender']}, Наличие работы = {result['Has Occupation']} => {result['Error']}")
        else:
            print(f"Пол: {result['Gender']}, Наличие работы: {result['Has Occupation']}, "
                  f"Самый высокий герой: {result['Tallest Hero']}, Рост: {result['Height (cm)']} см")

if __name__ == "__main__":
    main()
