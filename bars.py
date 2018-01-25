import json
import sys
import os
import requests
from geopy.distance import vincenty
import re


def get_data_from_file(file_path):
    with open(file_path, "r") as file:
        json_data = json.load(file)
        return json_data


def fetch_data_from_api(api_key):
    url = "https://apidata.mos.ru/v1/features/1796?"
    request = requests.get(url, params={"api_key": api_key})
    if request.ok:
        return request.json()


def get_biggest_bar(json_data):
    max_bar = max(json_data, key=lambda bar: get_value(bar, "SeatsCount"))
    return max_bar


def get_smallest_bar(json_data):
    min_bar = min(json_data, key=lambda bar: get_value(bar, "SeatsCount"))
    return min_bar


def get_closest_bar(json_data, my_coord):
    closest_bar = min(
        json_data,
        key=lambda bar:
        vincenty(my_coord, reversed(get_value(bar, "coordinates"))).meters)
    return [vincenty(my_coord, reversed(get_value(closest_bar,
                                                  "coordinates"))).meters,
            closest_bar]


def get_data():
    if os.getenv("API-mos-key"):
        print("Загрузка онлайн")
        return fetch_data_from_api(os.environ["API-mos-key"])
    try:
        print("Загрузка из файла")
        return get_data_from_file(sys.argv[1])
    except FileNotFoundError:
        print("Файл {} не найден!".format(sys.argv[1]))
    except json.decoder.JSONDecodeError:
        print("Некорректный JSON!")
    except IndexError:
        print("Введите путь до файла с данными в качестве аргумента."
              "Пример: 'python pprint_json.py in.json' ")


def get_value(bar, property):
    if property == "Name":
        return bar["properties"]["Attributes"]["Name"]
    if property == "Address":
        return bar["properties"]["Attributes"]["Address"]
    if property == "coordinates":
        return bar["geometry"]["coordinates"]
    if property == "SeatsCount":
        return bar["properties"]["Attributes"]["SeatsCount"]


def print_bar(bar):
    print("""Название: {0}\nАдрес: {1}\nКол-во мест: {2}
    """.format(get_value(bar, "Name"),
               get_value(bar, "Address"),
               get_value(bar, "SeatsCount")))


if __name__ == "__main__":
    json_data = get_data()
    if not json_data:
        sys.exit(0)
    print("Самый большой бар: ")
    print_bar(get_biggest_bar(json_data["features"]))
    smallest_bar = get_smallest_bar(json_data["features"])

    print("Самый маленький бар: ")
    print_bar(smallest_bar)

    print("Чтобы определить ближайший к вам бар, введите ваши координаты")
    coordinates = input("Введите координаты через запятую: ")
    if not re.fullmatch(" *\d+.?\d*,+ *\d+.?\d* *", coordinates):
        print("Некорректные координаты. Пример: 55.691484, 37.568782")
        sys.exit(0)

    distance, closest_bar = get_closest_bar(json_data["features"],
                                            coordinates)
    print("\nБлижайший к вам бар находится на расстоянии {0} метров"
          .format(int(distance)))
    print_bar(closest_bar)
