# Class to hold all the parameters associated with the filament winder
from typing import List, Dict

class Winder:
    def __init__(self, mandrelDiameter: float, verboseOutput: bool = False):
        self.verboseOutput = verboseOutput
        self.gcode: List[str] = []
        self.feedRateMMpM = 0
        self.totalTimeS = 0
        self.totalTowLengthMM = 0
        self.lastPosition = {
            "CARRIAGE": 0,
            "MANDREL": 0,
            "DELIVERY_HEAD": 0
        }
        self.mandrelDiameter = mandrelDiameter
   
      