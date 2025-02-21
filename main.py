import requests
import os
from termcolor import colored

SERVER_URL = 'https://giant-panda.play.eco/'
GAME_DATA_LOCATION = "D:/SteamLibrary/steamapps/common/Eco/Eco_Data/"

# Returns number of days, server is running.
def get_server_days_running() -> int:
    response = requests.get(os.path.join(SERVER_URL, "info"))
    data = response.json()
    return int(data["DaysRunning"])


# Returns list formatted [[plant_name, creation_day_quantity, current_day_quantity],...].
def get_plants_data() -> list:
    PLANTS_DIR_SUFFIX = 'Server/Mods/__core__/AutoGen/Plant'

    server_days_running = get_server_days_running()

    plants_list = [plant.replace('.cs', '') for plant in
                   os.listdir(os.path.join(GAME_DATA_LOCATION, PLANTS_DIR_SUFFIX))]

    plants_data = []

    for plant in plants_list:
        response = requests.get(os.path.join(SERVER_URL,
                                  f"datasets/get?dataSet={plant}Species&dayStart=0&dayEnd={server_days_running}"))
        plants_data.append([plant, response.json()])

    plants_cleaned_up_data = []

    for plant in plants_data:
        cleaned_up_data = [plant[0], plant[1]['Values'][0], plant[1]['Values'][-1]]
        plants_cleaned_up_data.append(cleaned_up_data)

    return plants_cleaned_up_data

# Returns list formatted [[animal_name, creation_day_quantity, current_day_quantity],...].
def get_animals_data() -> list:
    ANIMALS_DIR_SUFFIX = 'Server/Mods/__core__/AutoGen/Animal'

    server_days_running = get_server_days_running()

    animals_list = [animal.replace('.cs', '') for animal in
                   os.listdir(os.path.join(GAME_DATA_LOCATION, ANIMALS_DIR_SUFFIX))]

    animals_data = []

    for animal in animals_list:
        response = requests.get(os.path.join(SERVER_URL,
                                  f"datasets/get?dataSet={animal}Species&dayStart=0&dayEnd={server_days_running}"))
        animals_data.append([animal, response.json()])

    animals_cleaned_up_data = []

    for animal in animals_data:
        cleaned_up_data = [animal[0], animal[1]['Values'][0], animal[1]['Values'][-1]]
        animals_cleaned_up_data.append(cleaned_up_data)

    return animals_cleaned_up_data

def plants_data_visualization():
    plants_data = get_plants_data()
    name_width = max(len(plant[0]) for plant in plants_data) + 2
    qty_width = 10

    for plant in plants_data:
        balance = round(plant[2]-plant[1],1)

        print(
            colored(" Name: ", "yellow").ljust(10) + colored(plant[0].ljust(name_width), "white") +
            colored(" Creation day quantity: ", "yellow").ljust(25) + colored(str(round(plant[1],1)).rjust(qty_width), "white") +
            colored(" Current day quantity: ", "yellow").ljust(25) + colored(str(round(plant[2],1)).rjust(qty_width), "white") +
            colored(" Balance: ", "green" if balance > 0 else "red").ljust(25) + colored(str(balance).rjust(qty_width), "green" if balance > 0 else "red")
        )

def animals_data_visualization():
    animals_data = get_animals_data()
    name_width = max(len(animal[0]) for animal in animals_data) + 2
    qty_width = 10

    for animal in animals_data:
        balance = round(animal[2]-animal[1],1)

        print(
            colored(" Name: ", "yellow").ljust(10) + colored(animal[0].ljust(name_width), "white") +
            colored(" Creation day quantity: ", "yellow").ljust(25) + colored(str(round(animal[1],1)).rjust(qty_width), "white") +
            colored(" Current day quantity: ", "yellow").ljust(25) + colored(str(round(animal[2],1)).rjust(qty_width), "white") +
            colored(" Balance: ", "green" if balance > 0 else "red").ljust(25) + colored(str(balance).rjust(qty_width), "green" if balance > 0 else "red")
        )

def main():
    animals_data_visualization()

if __name__ == "__main__":
    main()