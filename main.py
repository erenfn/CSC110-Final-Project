"""
Climate Change Project by
Eren Findik
Can Yildiz
Alamgir Khan
"""
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
from computing_data import calc_high_actual_pd, \
    calc_low_actual_pd, \
    calc_median_actual_pd, \
    make_high_rcp_list, make_low_rcp_list, \
    make_median_rcp_list, rcp_to_slice, temp_to_rgb
from reading_data import read_actual_data, read_predicted_data, CITY_SET, MAP, CITY_TEMPS


def plot_temp_data(actual_temps_dict: dict, final_low_rcp_list: list, final_median_rcp_list: list,
                   final_high_rcp_list: list) -> None:
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
        yaxis_title="Temperature (Celsius)",
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
    Draws both maps for predicted and actual temperature of the cities in Canada
    """

    map = Image.open(MAP)
    width, height = map.size

    new_map = Image.new('RGB', (width * 2, height + 80))

    # fills the cities for the actual map
    for city in CITY_SET:
        temp = CITY_TEMPS[city][0]
        ImageDraw.floodfill(map, city[2], temp_to_rgb(temp), thresh=50)

    map2 = Image.open(MAP)

    # fills the cities for the predicted map
    for city in CITY_SET:
        temp = CITY_TEMPS[city][rcp_to_slice(rcp_type)]
        ImageDraw.floodfill(map2, city[2], temp_to_rgb(temp), thresh=50)

    new_map.paste(map, (0, 80))
    new_map.paste(map2, (width, 80))

    # Writes the titles
    title_font = ImageFont.truetype("arial.ttf", 50)
    new_map_editable = ImageDraw.Draw(new_map)
    new_map_editable.text((width // 3, 10),
                          'Actual Temperatures(' + year + ')', font=title_font)
    new_map_editable.text((int(1.3 * width), 10),
                          'Predicted Temperatures(' + year + ')', font=title_font)

    new_map.show()


def run(city: tuple, year: int, city_name: str) -> None:
    """
    Runs the code for one city
    """
    actual_temps_dict = read_actual_data(city[0])
    predicted_temps_dict = read_predicted_data(city[1], actual_temps_dict)

    if city[3].lower() == city_name.lower():
        final_low_rcp_list = make_low_rcp_list(predicted_temps_dict)
        low_rcp_percentage_difference = \
            calc_low_actual_pd(actual_temps_dict, final_low_rcp_list)
        final_median_rcp_list = make_median_rcp_list(predicted_temps_dict)
        median_rcp_percentage_difference = \
            calc_median_actual_pd(actual_temps_dict,
                                  final_median_rcp_list)
        final_high_rcp_list = make_high_rcp_list(predicted_temps_dict)
        high_rcp_percentage_difference = \
            calc_high_actual_pd(actual_temps_dict,
                                final_high_rcp_list)
        plot_temp_data(actual_temps_dict, final_low_rcp_list,
                       final_median_rcp_list, final_high_rcp_list)
        draw_table(actual_temps_dict, final_low_rcp_list, final_median_rcp_list,
                   final_high_rcp_list,
                   low_rcp_percentage_difference, median_rcp_percentage_difference,
                   high_rcp_percentage_difference)

    temperatures = [actual_temps_dict[year], predicted_temps_dict[year]['RCP 2.6'],
                    predicted_temps_dict[year]['RCP 4.5'], predicted_temps_dict[year]['RCP 8.5']]
    CITY_TEMPS[city] = temperatures


# this is the main part of the program that calls every function
if __name__ == '__main__':

    year = input('Write the year for the map to display data from '
                 '(in range of 2003-2019 inclusive)')
    if not 2003 <= int(year) <= 2019:
        year = input('Try again. Write the number between 2003 and 2019 inclusive')
    city_name = input(
        'Type the name of the city you want to display its stats on graph'
        '(TORONTO, QUEBEC, HALIFAX, WINNIPEG)')
    if city_name.lower() not in ('toronto', 'halifax', 'quebec', 'winnipeg'):
        city_name = input(
            'Try again. Type Toronto or Quebec or Halifax or Winnipeg')
    rcp_type = input(
        'Write an RCP value for the map to display on the "predicted" side.'
        '(write RCP 2.6 or RCP 4.5 or RCP 8.5)')
    if rcp_type not in ('RCP 2.6', 'RCP 4.5', 'RCP 8.5'):
        rcp_type = input('Try again. Write RCP 2.6 or RCP 4.5 or RCP 8.5)')

    while True:
        for city in CITY_SET:
            run(city, int(year), city_name)

        draw_map(rcp_type)

        year = input('Write the year for the map to display data from '
                     '(in range of 2003-2019 inclusive). '
                     'Type 2 wrong answers to exit')
        if not 2003 <= int(year) <= 2019:
            year = input('Try again. Write the number between 2003 and 2019 inclusive. '
                         'Type a wrong aswer to exit')
        if not 2003 <= int(year) <= 2019:
            break

        city_name = input(
            'Type the name of the city you want to display its stats on graph'
            '(TORONTO, QUEBEC, HALIFAX, WINNIPEG) Type 2 wrong answers to exit.')
        if city_name.lower() not in ('toronto', 'halifax', 'quebec', 'winnipeg'):
            city_name = input(
                'Try again. Type Toronto or Quebec or Halifax or Winnipeg. '
                'Type a wrong answer to exit.')
        if city_name.lower() not in ('toronto', 'halifax', 'quebec', 'winnipeg'):
            break

        rcp_type = input(
            'Write an RCP value for the map to display on the "predicted" side.'
            '(write RCP 2.6 or RCP 4.5 or RCP 8.5) Type 2 wrong answers to exit')
        if rcp_type not in ('RCP 2.6', 'RCP 4.5', 'RCP 8.5'):
            rcp_type = input('Try again. Write RCP 2.6 or RCP 4.5 or RCP 8.5'
                             'Type a wrong answer to exit.')
        if rcp_type not in ('RCP 2.6', 'RCP 4.5', 'RCP 8.5'):
            break

    # import python_ta
    #
    # python_ta.check_all(config={
    #     'allowed-io': ['read_actual_data', 'read_predicted_data'],
    #     'extra-imports': ['python_ta.contracts', 'csv',
    #                       'plotly.graph_objects', 'plotly.subplots', 'PIL', 'computing_data',
    #                       'reading_data'],
    #     'max-line-length': 100,
    #     'max-args': 7,
    #     'max-locals': 25,
    #     'disable': ['R1705'],
    # })
    #
    # import python_ta.contracts
    #
    # python_ta.contracts.DEBUG_CONTRACTS = False
    # python_ta.contracts.check_all_contracts()
