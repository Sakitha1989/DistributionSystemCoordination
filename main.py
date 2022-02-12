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

from readingData import create_distribution_system, create_transmission_system, DistributionSystem
from model import *
from solution import update_distribution_system_solution, DistributionSystemSolution, TransmissionSolution, \
    update_transmission_system_solution

# default inputs if not provided
directory = "C:\\Users\\sakit\\Documents\\Academic\\Research\\CoordinationSystem\\CoordinationDisSys\\"
network_name = "Test"
system_name = "System1"
num_systems = 2
num_iterations = 2
input_dir = ""
output_dir = ""


def cmdinputs() -> None:
    global directory, network_name, system_name, num_systems, num_iterations, input_dir, output_dir

    if len(sys.argv) >= 2:
        if not os.path.exists(sys.argv[1]):
            print(f"{sys.argv[1]}, Directory does not exists!")
            sys.exit()
        else:
            directory = sys.argv[1]
            input_dir = directory + "inputData\\"
            if len(sys.argv) >= 3:
                if not os.path.exists(input_dir + sys.argv[2] + "\\"):
                    print(f"{sys.argv[2]} network does not exists!")
                    sys.exit()
                else:
                    network_name = sys.argv[2]
                    input_dir = input_dir + network_name + "\\"
                if len(sys.argv) >= 4:
                    system_name = sys.argv[3]
                    if len(sys.argv) >= 5:
                        if len(os.listdir(input_dir)) >= int(sys.argv[4]):
                            num_systems = int(sys.argv[4])
                        else:
                            print("Invalid number of systems! The program will run for the available number of systems.")
                            num_systems = len(os.listdir(input_dir))
                        if len(sys.argv) >= 6:
                            num_iterations = int(sys.argv[5])

    output_dir = directory + "outputData\\" + network_name + "\\"
    os.chdir(output_dir)

    # Create system folder in the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print("Directory: ", output_dir, " Created ")


# reading command line arguments
cmdinputs()

# transmission system attributes
transmission_system = create_transmission_system(input_dir, network_name)
transmission_system_solution = TransmissionSolution(transmission_system.numBuses)

# distribution systems attributes
distribution_system = [DistributionSystem] * num_systems
distribution_system_model = [DistributionSystemModel] * num_systems
distribution_system_solution = [DistributionSystemSolution] * num_systems

for iteration_count in range(num_iterations):

    for system_number in range(num_systems):

        if iteration_count == 0:
            if not os.path.exists(input_dir + system_name + f"{system_number+1}\\"):
                print(f"{system_name + str(system_number+1)} does not exists!")
                sys.exit()
            else:
                file_path = input_dir + system_name + f"{system_number+1}\\"
                distribution_system[system_number] = create_distribution_system(file_path, system_name + f"{system_number+1}")

                distribution_system_model[system_number] = create_distribution_system_model(distribution_system[system_number], transmission_system, transmission_system_solution)
                init_distribution_system_solution = DistributionSystemSolution()
                distribution_system_solution[system_number] = update_distribution_system_solution(init_distribution_system_solution, distribution_system_model[system_number], iteration_count)

        else:
            distribution_system_model[system_number] = update_distribution_system_model(distribution_system_model[system_number], distribution_system[system_number], transmission_system, transmission_system_solution)
            distribution_system_solution[system_number] = update_distribution_system_solution(distribution_system_solution[system_number], distribution_system_model[system_number], iteration_count)

        transmission_system_solution = update_transmission_system_solution(transmission_system_solution, distribution_system_solution[system_number], transmission_system, distribution_system[system_number])

        if num_systems == system_number:
            break
