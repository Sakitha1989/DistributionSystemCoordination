######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     02/17/2022
# Project:  Distribution system coordination
######################################################################################################################

def percentage_gap_calculator(list_1, list_2, val):

    gap_list = []
    try:
        gap_list = [abs((i - j)/i) for i, j in zip(list_2, list_1)]
    except ZeroDivisionError:
        print("float division by zero")

    return True if all(x < val for x in gap_list) else False
