######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     02/08/2022
# Project:  Distribution system coordination
######################################################################################################################

# Need two command line inputs;
#           1. Directory path
#           2. System name
#
# The script assumes that there are 'inputData' and 'outputData' folders exist inside the directory. Also, inside the
# 'inputData' folder there must be folder for the system containing all the data files.

import sys
import os

from readingData import read_files

import gurobipy as gb
from gurobipy import GRB, Model, quicksum
import pandas as pd
import numpy as np


directory = "C:\\Users\\sakit\\Documents\\Academic\\Research\\CoordinationSystem\\CoordinationDisSys\\"
system_name = "Test"
input_dir = ""
output_dir = ""


def cmdinputs() -> None:
    global directory, system_name, input_dir, output_dir

    if not(len(sys.argv) == 1):
        directory = sys.argv[1]
        system_name = sys.argv[2]

    input_dir = directory + "inputData\\" + system_name + "\\"
    output_dir = directory + "outputData\\" + system_name + "\\"

    # Create system folder in the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print("Directory: ", output_dir, " Created ")


cmdinputs()

file_list = ["genData", "loadData", "busData", "lineData"]
for file in file_list:
    read_files(input_dir, file)
print(input_dir)
print(system_name)
