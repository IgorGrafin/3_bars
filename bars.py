import json
import sys
from math import sqrt, pow


def load_data(file_path):
    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            json_data = json.load(file)
            return json_data
    except FileNotFoundError:
        print("File %s not found!" % file_path)
        return None
    except json.decoder.JSONDecodeError:
        print("JSON is not valid!")
        return None


def get_biggest_bar(data):
    place_with_max_seat_count = data['features'][0]

    for place in data['features']:
        if place["properties"]["Attributes"]["SeatsCount"] > place_with_max_seat_count["properties"]["Attributes"]["SeatsCount"]:
            place_with_max_seat_count = place

    print("Самый большой бар под названием {0} имеет сидячих мест {1}".format(
        place_with_max_seat_count["properties"]["Attributes"]["Name"],
        place_with_max_seat_count["properties"]["Attributes"]["SeatsCount"]))


def get_smallest_bar(data):
    # print(data['features'])
    # print(type(data['features']))
    # print(data['features'][0])
    # print(type(data['features'][0]))
    # # print(data['features'][0]["properties"]["Attributes"]["Name"])
    # print(data['features'][0]["properties"]["Attributes"]["SeatsCount"])
    place_with_min_seat_count = data['features'][0]

    for place in data['features']:
        if place["properties"]["Attributes"]["SeatsCount"] < place_with_min_seat_count["properties"]["Attributes"]["SeatsCount"]:
            place_with_min_seat_count = place

    print("Самый маленький бар под названием {0} имеет сидячих мест {1}".format(
        place_with_min_seat_count["properties"]["Attributes"]["Name"],
        place_with_min_seat_count["properties"]["Attributes"]["SeatsCount"]))


def get_closest_bar(data, longitude, latitude):
    closest_place = data["features"][0]
    # print(closest_place["geometry"]["coordinates"])
    closest_place_coordinates = closest_place["geometry"]["coordinates"]
    distance = sqrt(pow((longitude - closest_place_coordinates[0]), 2) +
                    pow((latitude - closest_place_coordinates[1]), 2))
# TODO: Разобраться с lambda
    for place in data['features']:
        if place["geometry"]["coordinates"] < distance:
            pass

    print(distance)


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) > 1:
        json_data = load_data(sys.argv[1])
        if json_data:
            get_biggest_bar(json_data)
            get_smallest_bar(json_data)
            get_closest_bar(json_data, 55.600054, 37.718310)

    else:
        print(len(sys.argv))