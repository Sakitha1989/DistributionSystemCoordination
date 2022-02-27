######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     02/08/2022
# Project:  Distribution system coordination
######################################################################################################################

# Creating all the attributes of the power system.

import csv
import os

from print import print_distribution_system_details


class Generator(object):
    def __init__(self, attribute_list):
        self.id = int(attribute_list['bus'])
        self.bus = int(attribute_list['bus'])
        self.c3 = float(attribute_list['c(2)'])
        self.c2 = float(attribute_list['c(1)'])
        self.c1 = float(attribute_list['c(0)'])
        self.active_max = float(attribute_list['Pmax'])
        self.active_min = float(attribute_list['Pmin'])
        self.reactive_max = float(attribute_list['Qmax'])
        self.reactive_min = float(attribute_list['Qmin'])


class Load(object):
    def __init__(self, attribute_list):
        self.id = int(attribute_list['bus_i'])
        self.bus = int(attribute_list['bus_i'])
        self.active_max = float(attribute_list['Pd'])
        self.reactive_max = float(attribute_list['Qd'])


class Bus(object):
    def __init__(self, attribute_list):
        self.id = int(attribute_list['bus_i'])
        self.min_voltage = float(attribute_list['Vmin'])*float(attribute_list['baseKV'])
        self.max_voltage = float(attribute_list['Vmax'])*float(attribute_list['baseKV'])
        self.susceptance = float(attribute_list['Bs'])
        self.conductance = float(attribute_list['Gs'])


class TransmissionBus(Bus):
    def __init__(self, attribute_list):
        super(TransmissionBus, self).__init__(attribute_list)
        self.constant_payment = int(attribute_list['busConstantPay'])
        self.variable_payment = int(attribute_list['busVariablePay'])


class Line(object):
    def __init__(self, attribute_list):
        self.id = int(attribute_list['LineID'])
        self.source = int(attribute_list['fbus'])
        self.destination = int(attribute_list['tbus'])
        self.max_flow = 99999
        self.susceptance = 1/float(attribute_list['x'])
        self.conductance = 1/float(attribute_list['r'])


class DistributionLine(Line):
    def __init__(self, attribute_list):
        super().__init__(attribute_list)
        self.type = "Distribution"


class TransmissionLine(Line):
    def __init__(self, attribute_list):
        super().__init__(attribute_list)
        self.type = "Transmission"


class DistributionSystem(object):
    def __init__(self, system_name):
        self.name = system_name
        self.VOLL = 1000
        self.numGenerators = 0
        self.numLoads = 0
        self.numBuses = 0
        self.numDistributionLines = 0
        self.numTransmissionLines = 0

        self.generators = []
        self.loads = []
        self.buses = []
        self.distribution_lines = []
        self.transmission_lines = []

    def create_distribution_system(self, input_dir):

        # list of file names to read
        file_list = ["genData", "busData", "lineData"]

        for file_name in file_list:
            if not os.path.exists(input_dir + file_name + ".csv"):
                print(f"{file_name} does not exists!")
            else:
                with open(input_dir + file_name + ".csv", 'r') as file:
                    data = csv.DictReader(file)
                    if file_name == "genData":
                        for row in data:
                            self.generators.append(Generator(row))
                            self.numGenerators += 1
                    elif file_name == "busData":
                        for row in data:
                            self.buses.append(Bus(row))
                            self.loads.append(Load(row))
                            self.numBuses += 1
                            self.numLoads += 1
                    elif file_name == "lineData":
                        for row in data:
                            if row['lineType'] == 'd':
                                self.distribution_lines.append(Line(row))
                                self.numDistributionLines += 1
                            elif row['lineType'] == 't':
                                self.transmission_lines.append(Line(row))
                                self.numTransmissionLines += 1

        print_distribution_system_details(self)


class TransmissionSystem(object):
    def __init__(self, system_name):
        self.name = system_name
        self.numBuses = 0
        self.buses = []

    def create_transmission_system(self, input_dir):

        if not os.path.exists(input_dir + "transmissionData.csv"):
            print(f"{self.name} does not exists!")
        else:
            with open(input_dir + "transmissionData.csv", 'r') as file:
                data = csv.DictReader(file)
                for row in data:
                    self.buses.append(TransmissionBus(row))
                    self.numBuses += 1
