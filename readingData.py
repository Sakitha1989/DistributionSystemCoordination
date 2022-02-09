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
        self.id = attribute_list['genId']
        self.bus = attribute_list['genBus']
        self.cost = attribute_list['genCost']
        self.active_max = attribute_list['genMaxReal']
        self.active_min = attribute_list['genMinReal']
        self.reactive_max = attribute_list['genMaxImagin']
        self.reactive_min = attribute_list['genMinImagin']


class Load(object):
    def __init__(self, attribute_list):
        self.id = attribute_list['loadId']
        self.bus = attribute_list['loadBus']
        self.active_max = attribute_list['loadMaxReal']
        self.reactive_max = attribute_list['loadMaxImagin']


class Bus(object):
    def __init__(self, attribute_list):
        self.id = attribute_list['busId']
        self.susceptance = attribute_list['busSusceptance']
        self.conductance = attribute_list['busConductance']


class Line(object):
    def __init__(self, attribute_list):
        self.id = attribute_list['lineId']
        self.source = attribute_list['lineSource']
        self.destination = attribute_list['lineDestination']
        self.max_flow = attribute_list['lineMaxFlow']
        self.susceptance = attribute_list['lineSusceptance']
        self.conductance = attribute_list['lineConductance']


class DistributionSystem(object):
    def __init__(self, system_name):
        self.name = system_name
        self.numGenerators = 0
        self.numLoads = 0
        self.numBuses = 0
        self.numLines = 0

        self.generators = []
        self.loads = []
        self.buses = []
        self.lines = []


def create_distribution_system(input_dir):

    distribution_system = DistributionSystem('Distribution_system_1')

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
                        distribution_system.generators.append(Generator(row))
                        distribution_system.numGenerators += 1
                elif file_name == "loadData":
                    for row in data:
                        distribution_system.loads.append(Load(row))
                        distribution_system.numLoads += 1
                elif file_name == "busData":
                    for row in data:
                        distribution_system.buses.append(Bus(row))
                        distribution_system.numBuses += 1
                if file_name == "lineData":
                    for row in data:
                        distribution_system.lines.append(Line(row))
                        distribution_system.numLines += 1

    return distribution_system
