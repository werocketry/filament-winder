from enum import Enum
from typing import Dict, List, Optional, Union, TypedDict

# General Parameters

class MandrelParameters:
    def __init__(self, diameter: float, wind_length: float):
        self.diameter = diameter
        self.wind_length = wind_length


class TowParameters:
    def __init__(self, width: float, thickness: float):
        self.width = width
        self.thickness = thickness


# Layer-specific Parameters

class LayerType(Enum):
    HOOP = "hoop"
    HELICAL = "helical"
    SKIP = "skip"


class HoopLayer:
    def __init__(self, terminal: bool):
        self.wind_type = LayerType.HOOP
        self.terminal = terminal


class HelicalLayer:
    def __init__(
        self,
        wind_angle: float,
        pattern_number: int,
        skip_index: int,
        lock_degrees: float,
        lead_in_mm: float,
        lead_out_degrees: float,
        skip_initial_near_lock: Optional[bool] = None,
    ):
        self.wind_type = LayerType.HELICAL
        self.wind_angle = wind_angle
        self.pattern_number = pattern_number
        self.skip_index = skip_index
        self.lock_degrees = lock_degrees
        self.lead_in_mm = lead_in_mm
        self.lead_out_degrees = lead_out_degrees
        self.skip_initial_near_lock = skip_initial_near_lock


class SkipLayer:
    def __init__(self, mandrel_rotation: float):
        self.wind_type = LayerType.SKIP
        self.mandrel_rotation = mandrel_rotation


LayerParameters = Union[HoopLayer, HelicalLayer, SkipLayer]


class LayerParametersGeneric:
    def __init__(
        self,
        parameters: LayerParameters,
        mandrel_parameters: MandrelParameters,
        tow_parameters: TowParameters,
    ):
        self.parameters = parameters
        self.mandrel_parameters = mandrel_parameters
        self.tow_parameters = tow_parameters


# Whole Wind Definition

class WindParameters:
    def __init__(
        self,
        layers: List[LayerParameters],
        mandrel_parameters: MandrelParameters,
        tow_parameters: TowParameters,
        default_feed_rate: float,
    ):
        self.layers = layers
        self.mandrel_parameters = mandrel_parameters
        self.tow_parameters = tow_parameters
        self.default_feed_rate = default_feed_rate


# Helper Types

class CoordinateAxes(Enum):
    CARRIAGE = "carriage"
    MANDREL = "mandrel"
    DELIVERY_HEAD = "deliveryHead"


class CoordinateAxesValues(TypedDict):
    carriage: float
    mandrel: float
    delivery_head: float


AxisLookup: Dict[CoordinateAxes, str] = {
    CoordinateAxes.CARRIAGE: "X",
    CoordinateAxes.MANDREL: "Y",
    CoordinateAxes.DELIVERY_HEAD: "Z",
}
