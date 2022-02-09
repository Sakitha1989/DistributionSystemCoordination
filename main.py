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

from readingData import create_distribution_system, DistributionSystem

import gurobipy as gb
from gurobipy import GRB, Model, quicksum
import pandas as pd
import numpy as np

# default inputs if not provided
directory = "C:\\Users\\sakit\\Documents\\Academic\\Research\\CoordinationSystem\\CoordinationDisSys\\"
network_name = "Test"
system_name = "System1"
num_systems = 2
input_dir = ""
output_dir = ""


def cmdinputs() -> None:
    global directory, network_name, system_name, num_systems, input_dir, output_dir

    if len(sys.argv) >= 2:
        if not os.path.exists(sys.argv[1]):
            print(f"{directory} Directory does not exists!")
            sys.exit()
        else:
            directory = sys.argv[1]
            input_dir = directory + "inputData\\"
            if len(sys.argv) >= 3:
                if not os.path.exists(input_dir + sys.argv[2] + "\\"):
                    print(f"{network_name} does not exists!")
                    sys.exit()
                else:
                    network_name = sys.argv[2]
                    input_dir = input_dir + network_name + "\\"
                if len(sys.argv) >= 4:
                    system_name = sys.argv[3]
                    if len(sys.argv) >= 5:
                        num_systems = int(sys.argv[4])

    output_dir = directory + "outputData\\" + network_name + "\\"

    # Create system folder in the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print("Directory: ", output_dir, " Created ")


cmdinputs()

i = 1
while len(os.listdir(input_dir)) >= i:

    distribution_systems = DistributionSystem(system_name + str(i))

    if not os.path.exists(input_dir + system_name + f"{i}\\"):
        print(f"{system_name + str(i)} does not exists!")
        sys.exit()
    else:
        file_path = input_dir + system_name + f"{i}\\"
        distribution_systems = create_distribution_system(file_path)
        if num_systems == i:
            sys.exit()
        i += 1
