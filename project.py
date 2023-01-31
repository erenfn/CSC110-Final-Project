"""
Climate Change Project
"""

import csv
from typing import Dict, List, Tuple
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont


TORONTO = ('datasets/toronto_actual.csv', 'datasets/toronto_predicted.csv', (800, 1000), 'Toronto')
QUEBEC = ('datasets/quebec_actual.csv', 'datasets/quebec_predicted.csv', (950, 1000), 'Quebec')
HALIFAX = ('datasets/halifax_actual.csv', 'datasets/halifax_predicted.csv', (1315, 1060), 'Halifax')
WINNIPEG = ('datasets/winnipeg_actual.csv', 'datasets/winnipeg_predicted.csv', (658, 852), 'Winnipeg')

CITIES_SET = {TORONTO, QUEBEC, HALIFAX, WINNIPEG}
MAP = 'canada_map2.jpg'
CITY_TEMPS = {}

#this the reader part of our project (both functions read the data from the datasets)



def read_actual_data(actual_data_filepath: str) -> Dict[int, float]:
    """Return a dictionary mapping of year to temperature from the data in a CSV file.

    Preconditions:
        - filepath refers to a csv file in the format of
          datasets/toronto.actual_temps.csv
          (i.e., could be that file or a different file in the same format)
    """
    with open(actual_data_filepath) as file:
        reader = csv.reader(file)

        next(reader)

        monthly_temps = []
        years = []
        yearly_dict = {}
        index = 0
        sum_so_far = 0
        for row in reader:
            monthly_temps.append(float(row[4]))

            year = int(row[2])
            if year not in years:
                years.append(year)

    for year in years:
        for _ in range(0, 12):
            sum_so_far = sum_so_far + monthly_temps[index]
            index += 1
        mean_temp = sum_so_far / 12
        yearly_dict[year] = round(mean_temp, 2)
        sum_so_far = 0

    return yearly_dict


def read_predicted_data(predicted_temps_filepath: str, actual_temps_dict: dict) -> Dict[int, Dict[str, float]]:
    """Return a dictionary of year to a dictionary of varying RCPs
        and their respective predicted temperature from the data in a CSV file.

    Preconditions:
        - filepath refers to a csv file in the format of
          datasets/toronto.predicted_temps.csv
          (i.e., could be that file or a different file in the same format)
    """
    with open(predicted_temps_filepath) as file:
        reader = csv.reader(file)

        years = list(actual_temps_dict.keys())

        next(reader)

        for _ in range(0, years[0] - 2000):
            next(reader)

        temp_low_rcp_list = []
        temp_medium_rcp_list = []
        temp_high_rcp_list = []
        rcp_dict = {}
        index = 0

        for row in reader:
            temp_low_rcp_list.append(float(row[2]))
            temp_medium_rcp_list.append(float(row[5]))
            temp_high_rcp_list.append(float(row[8]))

    for year in years:
        rcp_dict[year] = {'RCP 2.6': temp_low_rcp_list[index],
                          'RCP 4.5': temp_medium_rcp_list[index],
                          'RCP 8.5': temp_high_rcp_list[index]}
        index += 1

    return rcp_dict
#

# these functions all compute on the data
def make_low_rcp_list(predicted_temps_dict: dict) -> List[float]:
    """Return a list of RCP 2.6 temperature values
    """
    low_rcp_list = []

    for year in list(predicted_temps_dict.keys()):
        low_rcp_list.append(predicted_temps_dict[year]['RCP 2.6'])

    return low_rcp_list


def make_median_rcp_list(predicted_temps_dict: dict) -> List[float]:
    """Return a list of RCP 4.5 temperature values
    """
    median_rcp_list = []

    for year in list(predicted_temps_dict.keys()):
        median_rcp_list.append(predicted_temps_dict[year]['RCP 4.5'])

    return median_rcp_list


def make_high_rcp_list(predicted_temps_dict) -> List[float]:
    """Return a list of RCP 8.5 temperature values
    """
    high_rcp_list = []

    for year in list(predicted_temps_dict.keys()):
        high_rcp_list.append(predicted_temps_dict[year]['RCP 8.5'])

    return high_rcp_list


def calculate_low_actual_percentage_difference(actual_temps_dict: dict, final_low_rcp_list: list) -> List[float]:
    """
    Return a list of percentage differences of low RCP values to actual temperature values
    """
    actual_temps_list = list(actual_temps_dict.values())
    low_rcp_pd = []
    for index in range(0, len(final_low_rcp_list)):
        difference = abs(final_low_rcp_list[index] - actual_temps_list[index])
        percentage_difference = round(((difference / actual_temps_list[index]) * 100), 1)
        low_rcp_pd.append(percentage_difference)

    return low_rcp_pd


def calculate_median_actual_percentage_difference(actual_temps_dict: dict, final_median_rcp_list: list) -> List[float]:
    """
    Return a list of percentage differences of median RCP values to actual temperature values
    """
    actual_temps_list = list(actual_temps_dict.values())
    median_rcp_pd = []
    for index in range(0, len(final_median_rcp_list)):
        difference = abs(final_median_rcp_list[index] - actual_temps_list[index])
        percentage_difference = round(((difference / actual_temps_list[index]) * 100), 1)
        median_rcp_pd.append(percentage_difference)

    return median_rcp_pd


def calculate_high_actual_percentage_difference(actual_temps_dict: dict, final_high_rcp_list: list) -> List[float]:
    """
    Return a list of percentage differences of high RCP values to actual temperature values
    """
    actual_temps_list = list(actual_temps_dict.values())
    high_rcp_pd = []
    for index in range(0, len(final_high_rcp_list)):
        difference = abs(final_high_rcp_list[index] - actual_temps_list[index])
        percentage_difference = round(((difference / actual_temps_list[index]) * 100), 1)
        high_rcp_pd.append(percentage_difference)

    return high_rcp_pd
#


# these functions visualise our program (plot graph and table)
def plot_temp_data(actual_temps_dict: dict, final_low_rcp_list: list, final_median_rcp_list: list, final_high_rcp_list: list) -> None:
    """Plot a line and scatter graph of real and predicted temperatures
        using plotly's line and scatter plots
    """
    x = list(actual_temps_dict.keys())
    actual_y = list(actual_temps_dict.values())
    low_predicted_y = final_low_rcp_list
    median_predicted_y = final_median_rcp_list
    high_predicted_y = final_high_rcp_list

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=low_predicted_y,
                             mode='lines+markers',
                             name='RCP 2.6 Predicted Temperature'))

    fig.add_trace(go.Scatter(x=x, y=median_predicted_y,
                             mode='lines+markers',
                             name='RCP 4.5 Predicted Temperature'))

    fig.add_trace(go.Scatter(x=x, y=high_predicted_y,
                             mode='lines+markers',
                             name='RCP 8.5 Predicted Temperature'))

    fig.add_trace(go.Scatter(x=x, y=actual_y,
                             mode='lines+markers',
                             name='Actual Temperature'))
    fig.update_layout(
        title="Actual vs Predicted Temperature of " + city[3],
        xaxis_title="Years",
        yaxis_title="Temperature (Celcius)",
        font=dict(
            family="Courier New, monospace",
            size=18)
    )

    fig.show()


def draw_table(actual_temps_dict: dict,
               final_low_rcp_list: list,
               final_median_rcp_list: list,
               final_high_rcp_list: list,
               low_rcp_percentage_difference: list,
               median_rcp_percentage_difference: list,
               high_rcp_percentage_difference: list) -> None:
    """
    Draw a table using a plotly's basic table
    """
    fig = go.Figure(data=[go.Table(header=dict(values=['Actual Temperature', 'RCP 2.6',
                                                       '% Difference of RCP 2.6 and Actual Temp',
                                                       'RCP 4.5',
                                                       '% Difference of RCP 4.5 and Actual Temp',
                                                       'RCP 8.5',
                                                       '% Difference of RCP 8.5 and Actual Temp'],
                                               line_color='darkslategray',
                                               fill_color='lightskyblue'),
                                   cells=dict(values=[list(actual_temps_dict.values()),
                                                      final_low_rcp_list,
                                                      low_rcp_percentage_difference,
                                                      final_median_rcp_list,
                                                      median_rcp_percentage_difference,
                                                      final_high_rcp_list,
                                                      high_rcp_percentage_difference]))])

    fig.update_layout(
        title="Actual vs Predicted Temperature of " + city[3]
    )

    fig.show()


def draw_map(rcp_type: str) -> None:
    """
    Draws the map
    """

    map = Image.open(MAP)
    width, height = map.size

    new_map = Image.new('RGB', (width * 2, height + 80))

    # fills the states for the actual map
    for city in CITIES_SET:
        temp = CITY_TEMPS[city][0]
        ImageDraw.floodfill(map, city[2], temp_to_rgb(temp), thresh=50)

    map2 = Image.open(MAP)

    # fills the states for the predicted map
    for city in CITIES_SET:
        temp = CITY_TEMPS[city][rcp_to_slice(rcp_type)]
        ImageDraw.floodfill(map2, city[2], temp_to_rgb(temp), thresh=50)

    new_map.paste(map, (0, 80))
    new_map.paste(map2, (width, 80))

    # Writes the titles
    title_font = ImageFont.truetype("arial.ttf", 50)
    new_map_editable = ImageDraw.Draw(new_map)
    new_map_editable.text((width // 3, 10), 'Actual Temperatures(' + year + ')', font=title_font)
    new_map_editable.text((int(1.3 * width), 10), 'Predicted Temperatures(' + year + ')', font=title_font)

    new_map.show()


def rcp_to_slice(rcp_type: str) -> int:
    """
    returns the index that corresponds to that RCP value
    """
    if rcp_type == 'RCP 2.6':
        return 1
    elif rcp_type == 'RCP 4.5':
        return 2
    elif rcp_type == 'RCP 8.5':
        return 3


def temp_to_rgb(temp: float) -> Tuple:
    """
    returns the rgb value that corresponds to that temperature
    """
    if temp > 20:
        return (0, 0, 0, 40)
    elif temp >= 17.3:
        return (255, 0, int(35.55 * (temp - 17.3)), 40)
    elif temp >= 5.6:
        return (255, int(21.79 * (17.3-temp)), 0, 40)
    elif temp >= 2.9:
        return (int(85.19 * (temp - 2.9)), 255, 0, 40)
    elif temp >= -0.30:
        return (0, 255, int(79.69 * (2.9 - temp)), 40)
    else:
        return (250, 250, 250, 40)


def run(city: tuple, year: int, city_name: str) -> None:
    """
    runs the code for one city
    """
    actual_temps_dict = read_actual_data(city[0])
    predicted_temps_dict = read_predicted_data(city[1], actual_temps_dict)


    if city[3].lower() == city_name.lower():
        final_low_rcp_list = make_low_rcp_list(predicted_temps_dict)
        low_rcp_percentage_difference = calculate_low_actual_percentage_difference(actual_temps_dict, final_low_rcp_list)
        final_median_rcp_list = make_median_rcp_list(predicted_temps_dict)
        median_rcp_percentage_difference = calculate_median_actual_percentage_difference(actual_temps_dict,
                                                                                         final_median_rcp_list)
        final_high_rcp_list = make_high_rcp_list(predicted_temps_dict)
        high_rcp_percentage_difference = calculate_high_actual_percentage_difference(actual_temps_dict, final_high_rcp_list)
        plot_temp_data(actual_temps_dict, final_low_rcp_list, final_median_rcp_list, final_high_rcp_list)
        draw_table(actual_temps_dict, final_low_rcp_list, final_median_rcp_list, final_high_rcp_list,
                   low_rcp_percentage_difference, median_rcp_percentage_difference, high_rcp_percentage_difference)

    temperatures = [actual_temps_dict[year], predicted_temps_dict[year]['RCP 2.6'],
                    predicted_temps_dict[year]['RCP 4.5'], predicted_temps_dict[year]['RCP 8.5']]
    CITY_TEMPS[city] = temperatures


# this is the main part of the program that calls every function
if __name__ == '__main__':

    year = input("Write the year you want to see in the map from 2003-2019")
    if not(2003 <= int(year) <= 2019):
        year = input("Try again. Write the year you want to see in the map from 2003-2019")
    city_name = input(
        "Type the name of the city you want to display its stats on graph (TORONTO, QUEBEC, HALIFAX, WINNIPEG)")
    if not (city_name.lower() == 'toronto' or city_name.lower() == 'quebec' or city_name.lower() == 'halifax' or
            city_name.lower() == 'winnnipeg'):
        city_name = input(
            "Try again. Type the name of the city you want to display its stats on graph (TORONTO, QUEBEC, HALIFAX, WINNIPEG)")
    rcp_type = input(' write an rcp value (RCP 2.6, RCP 4.5, RCP 8.5)')
    if not (rcp_type == 'RCP 2.6' or rcp_type == 'RCP 4.5' or rcp_type == 'RCP 8.5'):
        rcp_type = input('Try again. Write an rcp value (RCP 2.6, RCP 4.5, RCP 8.5)')

    while True:
        for city in CITIES_SET:
            run(city, int(year), city_name)

        draw_map(rcp_type)

        year = input("Write the year you want to see in the map from 2003-2019")
        if not (2003 <= int(year) <= 2019):
            year = input("Try again. Write the year you want to see in the map from 2003-2019")
        if not (2003 <= int(year) <= 2019):
            break

        city_name = input(
            "Type the name of the city you want to display its stats on graph (TORONTO, QUEBEC, HALIFAX, WINNIPEG)")
        if not(city_name.lower() == 'toronto' or city_name.lower() == 'quebec' or city_name.lower() == 'halifax' or
               city_name.lower() == 'winnnipeg'):
            city_name = input(
                "Try again. Type the name of the city you want to display its stats on graph (TORONTO, QUEBEC, HALIFAX, WINNIPEG)")
        if not (city_name.lower() == 'toronto' or city_name.lower() == 'quebec' or city_name.lower() == 'halifax' or
                city_name.lower() == 'winnnipeg'):
            break

        rcp_type = input(' write an rcp value (RCP 2.6, RCP 4.5, RCP 8.5)')
        if not(rcp_type == 'RCP 2.6' or rcp_type == 'RCP 4.5' or rcp_type == 'RCP 8.5'):
            rcp_type = input('Try again. Write an rcp value (RCP 2.6, RCP 4.5, RCP 8.5)')
        if not (rcp_type == 'RCP 2.6' or rcp_type == 'RCP 4.5' or rcp_type == 'RCP 8.5'):
            break
#     import python_ta
#
#     python_ta.check_all(config={
#         'allowed-io': ['read_csv_data'],
#         'extra-imports': ['python_ta.contracts', 'csv', 'datetime',
#                           'plotly.graph_objects', 'plotly.subplots'],
#         'max-line-length': 100,
#         'max-args': 6,
#         'max-locals': 25,
#         'disable': ['R1705'],
#     })
#
#     import python_ta.contracts
#
#     python_ta.contracts.DEBUG_CONTRACTS = False
#     python_ta.contracts.check_all_contracts()
# #
