""""
Helper functions responsible for reading the data from the datasets
"""
import csv
from typing import Dict

TORONTO = ('datasets/toronto_actual.csv', 'datasets/toronto_predicted.csv', (800, 1000), 'Toronto')
QUEBEC = ('datasets/quebec_actual.csv', 'datasets/quebec_predicted.csv', (950, 1000), 'Quebec')
HALIFAX = ('datasets/halifax_actual.csv', 'datasets/halifax_predicted.csv', (1315, 1060), 'Halifax')
WINNIPEG = ('datasets/winnipeg_actual.csv', 'datasets/winnipeg_predicted.csv',
            (658, 852), 'Winnipeg')

CITY_SET = {TORONTO, QUEBEC, HALIFAX, WINNIPEG}
MAP = 'canada_map2.jpg'
CITY_TEMPS = {}


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


def read_predicted_data(predicted_temps_filepath: str,
                        actual_temps_dict: dict) -> Dict[int, Dict[str, float]]:
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


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['read_actual_data', 'read_predicted_data'],
        'extra-imports': ['python_ta.contracts', 'csv'],
        'max-line-length': 100,
        'max-args': 7,
        'max-locals': 25,
        'disable': ['R1705', 'C0200'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
