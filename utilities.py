######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     02/17/2022
# Project:  Distribution system coordination
######################################################################################################################

def percentage_gap_calculator(list_1, list_2, val):

    gap_list = [0 if i == 0 else abs((j - i)/i) for i, j in zip(list_2, list_1)]

    return True if all(x < val for x in gap_list) else False
