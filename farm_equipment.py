"""
farm_equipment defines a number of classes for objects to be used in the
"""
import json
import numpy as n
import pandas as p

class Equipment():
    """
    Equipemt is the super class from which all farm equipment types inherit.
    """

    def __init__(self):
        """
        Constructor defines the minimum interface for the simulation to run.
        """
        self.state = None
        self.location = None
        self.properties = {
            "grain_in"       : None, #tn/min, rate of grain uptake (i.e. harvest)
            "grain_out"      : None, #tn/min, rate of grain offload (i.e. augur)
            "grain_tank"     : None, #tn, current grain mass in tank
            "grain_tank_max" : None, #tn, maximum grain tank capacity
            "fuel_in"        : None, #l/min, rate of fuel uptake
            "fuel_out"       : None, #l/min, rate of fuel delivery (not burn)
            "fuel_burn"      : None, #l/min, fuel burnt for operation
            "fuel_tank"      : None, #l, current fuel volume in tank
            "fuel_tank_max"  : None, #l, maximum fuel tank capacity
            "transit_spd"    : None, #km/min, transit speed between objects.
        }
        self.library = {}
        self.table = {}

    def state_iterator():
        """
        Performs actions based on current state for "this" time step. Updates
        state for the "next" time step.
        """
        raise NotImplementedError

    def transfer_resource():
        """
        Transfer a resource, such as grain or fuel, from one object to another.
        """
        raise NotImplementedError

    def log_data(time_step):
        """
        Collect data at each time step, save internally to self.table .
        """
        raise NotImplementedError

    def import_library(library_file):
        """
        Collect data for equipment from an external JSON library, and store it
        for reference in self.library.
        """
        data_in = open(library_file,'r')
        self.library.update(json.load(data_in))

class Harvester(Equipment):
    """
    """

    def __init__(self, make = "claas"):
        """
        """
        super().__init__()
        for k in library[make].keys():
            self.properties[k] = library[make][k]



class Chaser(Equipment):
    """
    """

    def __init__(self):
        """
        """

class Silo(Equipment):
    """
    Silos are sinks for incoming grain. They are recieve and hold grain only;
    other equipment delivers or retrieves grain from these sinks.
    """

    def __init__(self, max_capacity, starting_content = 0):
        """
        Constructor calls the super and sets appropriate properties.
        """
        super().__init__()
        self.properties["grain_tank"] = starting_content
        self.properties["grain_tank_max"] = max_capacity
        self.state = [] #Silos are stateless and passive.

    def import_library():
        """
        Silos are simple grain sinks. They have only a capacity property and
        no libraries.
        """
        raise NotImplementedError

class Fueler(Equipment):
    """
    """

    def __init__(self):
        """
        """
