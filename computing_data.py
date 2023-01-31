""""
Helper functions responsible for computing on the data
"""

from typing import List, Tuple, Any


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


def make_high_rcp_list(predicted_temps_dict: dict) -> List[float]:
    """Return a list of RCP 8.5 temperature values
    """
    high_rcp_list = []

    for year in list(predicted_temps_dict.keys()):
        high_rcp_list.append(predicted_temps_dict[year]['RCP 8.5'])

    return high_rcp_list


def calc_low_actual_pd(actual_temps_dict: dict,
                       final_low_rcp_list: list) -> List[float]:
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


def calc_median_actual_pd(actual_temps_dict: dict,
                          final_median_rcp_list: list) -> List[float]:
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


def calc_high_actual_pd(actual_temps_dict: dict,
                        final_high_rcp_list: list) -> List[float]:
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


def rcp_to_slice(rcp_type: str) -> Any:
    """
    Returns the index that corresponds to that RCP value
    """
    if rcp_type == 'RCP 2.6':
        return 1
    elif rcp_type == 'RCP 4.5':
        return 2
    elif rcp_type == 'RCP 8.5':
        return 3
    else:
        return None


def temp_to_rgb(temp: float) -> Tuple:
    """
    Returns the rgb value that corresponds to that temperature
    """
    if temp > 20:
        return (0, 0, 0)
    elif temp >= 17.3:
        return (255, 0, int(35.55 * (temp - 17.3)))
    elif temp >= 5.6:
        return (255, int(21.79 * (17.3 - temp)), 0)
    elif temp >= 2.9:
        return (int(85.19 * (temp - 2.9)), 255, 0)
    elif temp >= -0.30:
        return (0, 255, int(79.69 * (2.9 - temp)))
    else:
        return (250, 250, 250)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'allowed-io': [],
        'extra-imports': ['python_ta.contracts'],
        'max-line-length': 100,
        'max-args': 7,
        'max-locals': 25,
        'disable': ['R1705', 'C0200'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
