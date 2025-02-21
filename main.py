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


def main():
    plants_data = get_plants_data()
    name_width = max(len(plant[0]) for plant in plants_data) + 2
    qty_width = 15  # Możesz dostosować

    for plant in plants_data:
        print(
            colored(" Name: ", "red").ljust(10) + colored(plant[0].ljust(name_width), "white") +
            colored(" Creation day quantity: ", "yellow").ljust(25) + colored(str(plant[1]).rjust(qty_width), "white") +
            colored(" Current day quantity: ", "green").ljust(25) + colored(str(plant[2]).rjust(qty_width), "white")
        )

if __name__ == "__main__":
    main()