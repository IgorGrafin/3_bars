import json
import sys
from math import sqrt, pow
import os
import requests
from geopy.distance import vincenty


def load_data(file_path):
    with open(file_path, "r", encoding="UTF-8") as file:
        json_data = json.load(file)
        return json_data


def get_data_from_api(api_key):
    url = "https://apidata.mos.ru/v1/features/1796?api_key=" + api_key
    request = requests.get(url)
    if request.status_code == 200:
        return request.json()
    else:
        return None


def get_biggest_bar(data):
    place_with_max_seat_count = data['features'][0]
    for place in data['features']:
        if place["properties"]["Attributes"]["SeatsCount"] > \
                place_with_max_seat_count["properties"]["Attributes"]["SeatsCount"]:
            place_with_max_seat_count = place

    return [place_with_max_seat_count["properties"]["Attributes"]["Name"],
            place_with_max_seat_count["properties"]["Attributes"]["SeatsCount"]]


def get_smallest_bar(data):
    place_with_min_seat_count = data['features'][0]
    for place in data['features']:
        if place["properties"]["Attributes"]["SeatsCount"] < \
                place_with_min_seat_count["properties"]["Attributes"]["SeatsCount"]:
            place_with_min_seat_count = place

    return [place_with_min_seat_count["properties"]["Attributes"]["Name"],
            place_with_min_seat_count["properties"]["Attributes"]["SeatsCount"]]


def get_closest_bar(data, my_coord):
    # get_distance = lambda x, y: sqrt(pow((x[0] - y[0]), 2) + pow((x[1] - y[1]), 2))
    get_distance = lambda x, y: vincenty(x, reversed(y)).meters
    closest_place = data["features"][0]

    closest_distance = get_distance(my_coord, closest_place["geometry"]["coordinates"])
    for place in data['features']:
        current_distance = get_distance(my_coord, place["geometry"]["coordinates"])
        if current_distance < closest_distance:
            closest_place = place
            closest_distance = current_distance

    return closest_place["properties"]["Attributes"]["Name"],\
           closest_place["properties"]["Attributes"]["Address"], closest_distance


if __name__ == "__main__":
    if os.getenv("API-mos-key"):
        json_data = get_data_from_api(os.environ["API-mos-key"])
        print("Загрузка онлайн")
        if json_data is None:
            print("неверный API key")
    else:
        try:
            json_data = load_data(sys.argv[1])
            print("Загрузка из файла")
        except FileNotFoundError:
            print("Файл %s не найден!" % sys.argv[1])
            sys.exit(0)
        except json.decoder.JSONDecodeError:
            print("Некорректный JSON!")
            sys.exit(0)
        except IndexError:
            print("Введите путь до файла с данными в качестве аргумента. Пример: 'python pprint_json.py in.json' ")
            sys.exit(0)

    if json_data:
        print("Чтобы определить ближайший к вам бар, введите ваши координаты")
        coordinates = (input("Введите координаты через запятую: ")).replace(" ", "")
        biggest_bar = get_biggest_bar(json_data)
        smallest_bar = get_smallest_bar(json_data)
        closest_bar = get_closest_bar(json_data, coordinates)

        print("Самый большой бар под названием {0} имеет сидячих мест {1}".format(biggest_bar[0],biggest_bar[1]))
        print("Самый маленький бар под названием {0} имеет сидячих мест {1}".format(smallest_bar[0],smallest_bar[1]))
        print("Ближайший к вам бар находится на расстоянии {0} метров под названием {1} находится по адресу {2}".format(
            int(closest_bar[2]), closest_bar[0], closest_bar[1]))
