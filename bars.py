import json
import sys
import os
import requests
from geopy.distance import vincenty


def load_data_from_file(file_path):
    with open(file_path, "r") as file:
        json_data = json.load(file)
        return json_data


def load_data_from_api(api_key):
    url = "https://apidata.mos.ru/v1/features/1796?"
    request = requests.get(url, params={"api_key": api_key})
    if request.ok:
        return request.json()


def get_biggest_bar(json_data):
    max_bar = max(json_data["features"],
                  key=lambda bar: bar["properties"]["Attributes"]["SeatsCount"])
    return max_bar["properties"]["Attributes"]["Name"], \
           max_bar["properties"]["Attributes"]["SeatsCount"]


def get_smallest_bar(json_data):
    min_bar = min(json_data["features"],
                  key=lambda bar: bar["properties"]["Attributes"]["SeatsCount"])
    return min_bar["properties"]["Attributes"]["Name"], \
           min_bar["properties"]["Attributes"]["SeatsCount"]


def get_closest_bar(json_data, my_coord):
    closest_bar = min(json_data["features"],
                      key=lambda bar:
                      vincenty(my_coord, reversed(bar["geometry"]["coordinates"])).meters)

    return [vincenty(my_coord, reversed(closest_bar["geometry"]["coordinates"])).meters,
            closest_bar["properties"]["Attributes"]["Name"],
            closest_bar["properties"]["Attributes"]["Address"]]


def get_data():
    if os.getenv("API-mos-key"):
        print("Загрузка онлайн")
        json_data = load_data_from_api(os.environ["API-mos-key"])
        if json_data is None:
            print("неверный API key")
        return json_data

    try:
        print("Загрузка из файла")
        json_data = load_data_from_file(sys.argv[1])
        return json_data
    except FileNotFoundError:
        print("Файл %s не найден!" % sys.argv[1])
    except json.decoder.JSONDecodeError:
        print("Некорректный JSON!")
    except IndexError:
        print("Введите путь до файла с данными в качестве аргумента."
              "Пример: 'python pprint_json.py in.json' ")


if __name__ == "__main__":
    json_data = get_data()
    if json_data:
        print("Чтобы определить ближайший к вам бар, введите ваши координаты")
        coordinates = (input("Введите координаты через запятую: ")).replace(" ", "")
        biggest_bar = get_biggest_bar(json_data)
        smallest_bar = get_smallest_bar(json_data)
        closest_bar = get_closest_bar(json_data, coordinates)

        print("Самый большой бар под названием {0} имеет сидячих мест {1}"
              .format(biggest_bar[0], biggest_bar[1]))
        print("Самый маленький бар под названием {0} имеет сидячих мест {1}"
              .format(smallest_bar[0], smallest_bar[1]))
        print("Ближайший к вам бар находится на расстоянии {0} метров"
              " под названием {1} находится по адресу {2}".format(int(closest_bar[0]),
                                                                  closest_bar[1], closest_bar[2]))
