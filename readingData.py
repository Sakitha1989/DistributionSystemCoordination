######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     02/08/2022
# Project:  Distribution system coordination
######################################################################################################################

# Creating all the attributes of the power system.

import csv
import os


class Generator(object):
    def __init__(self, attribute_list):
        self.id = int(attribute_list['genId'])
        self.bus = int(attribute_list['genBus'])
        self.cost = float(attribute_list['genCost'])
        self.active_max = float(attribute_list['genMaxReal'])
        self.active_min = float(attribute_list['genMinReal'])
        self.reactive_max = float(attribute_list['genMaxImagin'])
        self.reactive_min = float(attribute_list['genMinImagin'])


class Load(object):
    def __init__(self, attribute_list):
        self.id = int(attribute_list['loadId'])
        self.bus = int(attribute_list['loadBus'])
        self.active_max = float(attribute_list['loadMaxReal'])
        self.reactive_max = float(attribute_list['loadMaxImagin'])


class Bus(object):
    def __init__(self, attribute_list):
        self.id = int(attribute_list['busId'])
        self.min_voltage = float(attribute_list['busVmin'])
        self.max_voltage = float(attribute_list['busVmax'])
        self.susceptance = float(attribute_list['busSusceptance'])
        self.conductance = float(attribute_list['busConductance'])


class Line(object):
    def __init__(self, attribute_list):
        self.id = attribute_list['lineId']
        self.source = int(attribute_list['lineSource'])
        self.destination = int(attribute_list['lineDestination'])
        self.max_flow = float(attribute_list['lineMaxFlow'])
        self.susceptance = float(attribute_list['lineSusceptance'])
        self.conductance = float(attribute_list['lineConductance'])
        self.type = attribute_list['lineType']


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
        file_list = ["genData", "loadData", "busData", "lineData"]

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
                    elif file_name == "loadData":
                        for row in data:
                            self.loads.append(Load(row))
                            self.numLoads += 1
                    elif file_name == "busData":
                        for row in data:
                            self.buses.append(Bus(row))
                            self.numBuses += 1
                    elif file_name == "lineData":
                        for row in data:
                            if row['lineType'] == 'd':
                                self.distribution_lines.append(Line(row))
                                self.numDistributionLines += 1
                            elif row['lineType'] == 't':
                                self.transmission_lines.append(Line(row))
                                self.numTransmissionLines += 1


class TransmissionSystem(object):
    def __init__(self, system_name):
        self.name = system_name
        self.numBuses = 0
        self.bus_constant = 10
        self.buses = []

    def create_transmission_system(self, input_dir):

        if not os.path.exists(input_dir + "transmissionData.csv"):
            print(f"{self.name} does not exists!")
        else:
            with open(input_dir + "transmissionData.csv", 'r') as file:
                data = csv.DictReader(file)
                for row in data:
                    self.buses.append(Bus(row))
                    self.numBuses += 1
