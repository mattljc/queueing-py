"""

"""

import Object
import numpy as np
import pandas as p

class Equipment(Object):
    """
    """

    def __init__(self):
        """
        """
        self.state = None
        self.location = None
        self.properties = {
            'grain_in'       : None,
            'grain_out'      : None,
            'grain_tank'     : None,
            'grain_tank_max' : None,
            'fuel_in'        : None,
            'fuel_out'       : None,
            'fuel_burn'      : None,
            'fuel_tank'      : None,
            'fuel_tank_max'  : None,
            'transit_spd'    : None,
        }
        self.table = []

    def state_iterator():
        raise NotImplementedError

    def log_data():
        raise NotImplementedError

class Harvester(Equipment):
    """
    """
    library = {
      'claas' : {
        'grain_in'       : 0.583, #tn/min
        'grain_out'      : 5.460, #tn/min
        'grain_tank'     : 0.000, #tn
        'grain_tank_max' : None, #tn
        'fuel_burn'      : 1.167, #l/min
        'fuel_tank'      : None, #l
        'fuel_tank_max'  : None, #l
      }
    }

    def __init__(self, make = 'claas'):
        """
        """
        #call super constructor
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
    """

    def __init__(self, capacity):
        """
        """
        #call super constructor
        'grain_tank'     : None,
        'grain_tank_max' : None,

class Fueler(Equipment):
    """
    """

    def __init__(self):
        """
        """
