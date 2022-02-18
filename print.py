######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     02/16/2022
# Project:  Distribution system coordination
######################################################################################################################

import csv
from csv import writer


def distribution_solution_writer(model, header):

    column_names = ['Objective_Function_Value']
    data = [model.model.getObjective().getValue()]
    for v in model.model.getVars():
        if header == 0:
            column_names.append(v.varName)
        data.append(v.x)

    # file path and name
    file = model.name + ".csv"

    if header == 0:
        # writing to csv file
        with open(file, 'w', newline='') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            # writing the fields
            csvwriter.writerow(column_names)

    # writing to existing csv file
    with open(file, 'a', newline='') as f_object:
        # creating a csv writer object
        writer_object = writer(f_object)

        writer_object.writerow(data)