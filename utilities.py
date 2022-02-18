######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     02/17/2022
# Project:  Distribution system coordination
######################################################################################################################

def percentage_gap_calculator(list_1, list_2, val):

    gap_list = [abs((i - j)/i) for i, j in zip(list_1, list_2)]

    return True if all(x < val for x in gap_list) else False


def compare_solutions(solution1, solution2):

    if not solution1.name == solution2.name:
        print('Cannot compare solutions!')
        return False

    tolerance = 0.05
    if percentage_gap_calculator([solution1.objective_value], [solution2.objective_value], tolerance):
        if percentage_gap_calculator(solution1.active_generation, solution2.active_generation, tolerance) and \
                percentage_gap_calculator(solution1.active_load, solution2.active_load, tolerance) and \
                percentage_gap_calculator(solution1.active_line_transmission, solution2.active_line_transmission, tolerance):
            return True
        else:
            return False

    else:
        return False
