import requests

class Highest_SuperHero():
    base_url= "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api"

#       Класс содержит функции для нахождения наибольшего роста персонажа путем осуществления последовательных запросов по каждому id
#       и нахождения наибольшего параметра height с учетом заданных пользователем условий
#       В связи с необходимостью отправки большого количества запросов, код требует времени на обработку и выдачу ответа

    def __init__(self):
        # Инициализация переменных с помощью функции
        self.gender = self.get_gender_from_input()
        self.work_status = self.get_work_from_input()

    def get_gender_from_input(self):        # Функция запрашивает ввод пола персонажа и проверяет релевантность запроса
        while True:
            str_gender_input = input("Введите пол персонажа: ")

            gender = str_gender_input.lower()
            if gender in ("male", "муж", "мужской", "мужчина", "м", "m"):
                i_gender = "Male"
                return i_gender
            elif gender in ("female", "жен", "женский", "женщина", "f", "ж",):
                i_gender = "Female"
                return i_gender
            elif gender in ("no", "нет пола", "-", "н","n"):
                i_gender = "-"
                return i_gender
            else:
                print("Введите пол персонажа буквами")

    def get_work_from_input(self):      # Функция запрашивает ввод статуса работы персонажа и проверяет релевантность запроса
        while True:
            str_work_input = input("Есть ли у персонажа работа? ")
            work_input = str_work_input.lower()
            if work_input in ("y", "yes", "t", "true", "on", "1", "да", "д"):
                return True
            elif work_input in ("n", "no", "f", "false", "off", "0", "нет", "н"):
                return False
            else:
                print (f"Уточните есть ли у персонажа работа (Да/Нет, True/False)")

    def initialization_input_work_status(self, occupation):     # Функция уточняет статус работы для дальнейшего использования
        w_status = None
        if not self.work_status:
            w_status = "-"
        else:
            if occupation != "-":
                w_status = occupation
        return w_status

    def all_id(self): #  Функция получает количество id в базе
        all_characters = self.base_url + "/all.json"
        response = requests.get(all_characters)
        data = response.json()
        max_id = max(item["id"] for item in data if "id" in item)
        return max_id


    def looking_for_superhero(self):        # Функция проходит по всем карточкам супергероев с запрошенными данными и определяет наибольший рост
        print ("Ожидайте ответа. Необходимо время чтобы проанализировать всех супергероев.")
        max_height = 0  # Для хранения максимального значения роста
        max_height_character = None  # Для хранения данных персонажа с максимальным ростом
        max_id = self.all_id() + 1
        max_name = None
        for i in range(1,max_id):
            character = self.base_url + f"/id/{i}.json"
            response = requests.get(character)
            if response.status_code == 200:
                data = response.json()
                name = data.get("name")
                gender = data.get("appearance", {}).get("gender")
                occupation = data.get("work", {}).get("occupation")
                height = data.get("appearance", {}).get("height", ["0", "0 cm"])[1]
                work_status = self.initialization_input_work_status(occupation)
                if gender == self.gender and occupation == work_status:
                # Преобразование высоты в числовое значение (см)
                    if "meters" in height:
                        height_cm = float(height.split()[0]) * 100  # Метры -> см
                    elif "cm" in height:
                        height_cm = float(height.split()[0])
                        if height_cm > max_height:
                            max_name = name
                            max_height = height_cm
                            max_height_character = data

    #   Выводим результаты
        if max_height_character:
            print(f"Самый высокий персонаж - {max_name} ростом - {max_height} см:")
            print(f"Соответствующий JSON-ответ: {max_height_character}")
        else:
            print("Не найдено персонажей, удовлетворяющих условиям.")


start = Highest_SuperHero()
start.looking_for_superhero()
