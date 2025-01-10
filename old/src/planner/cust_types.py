from typing import Union, List, Dict, TypedDict, Optional
from enum import Enum


class IMandrelParameters:
    def __init__(self, diameter: float, windLength: float):
        self.diameter = diameter
        self.windLength = windLength


class ITowParameters:
    def __init__(self, width: float, thickness: float):
        self.width = width
        self.thickness = thickness


class ELayerType(Enum):
    HOOP = 'hoop'
    HELICAL = 'helical'
    SKIP = 'skip'


class THoopLayer:
    def __init__(self, terminal: bool):
        self.windType = ELayerType.HOOP
        self.terminal = terminal


class THelicalLayer:
    def __init__(
        self,
        windAngle: float,
        patternNumber: int,
        skipIndex: int,
        lockDegrees: float,
        leadInMM: float,
        leadOutDegrees: float,
        skipInitialNearLock: Optional[bool] = None
    ):
        self.windType = ELayerType.HELICAL
        self.windAngle = windAngle
        self.patternNumber = patternNumber
        self.skipIndex = skipIndex
        self.lockDegrees = lockDegrees
        self.leadInMM = leadInMM
        self.leadOutDegrees = leadOutDegrees
        self.skipInitialNearLock = skipInitialNearLock


class TSkipLayer:
    def __init__(self, mandrelRotation: float):
        self.windType = ELayerType.SKIP
        self.mandrelRotation = mandrelRotation


TLayerParameters = Union[THoopLayer, THelicalLayer, TSkipLayer]


class ILayerParameters:
    def __init__(
        self,
        parameters: TLayerParameters,
        mandrelParameters: IMandrelParameters,
        towParameters: ITowParameters
    ):
        self.parameters = parameters
        self.mandrelParameters = mandrelParameters
        self.towParameters = towParameters


class IWindParameters:
    def __init__(
        self,
        layers: List[TLayerParameters],
        mandrelParameters: IMandrelParameters,
        towParameters: ITowParameters,
        defaultFeedRate: float
    ):
        self.layers = layers
        self.mandrelParameters = mandrelParameters
        self.towParameters = towParameters
        self.defaultFeedRate = defaultFeedRate


class ECoordinateAxes(Enum):
    CARRIAGE = 'carriage'
    MANDREL = 'mandrel'
    DELIVERY_HEAD = 'deliveryHead'


class TCoordinateAxes(TypedDict):
    carriage: float
    mandrel: float
    deliveryHead: float


class AtLeastOne:
    """
    Simulates the TypeScript utility type `AtLeastOne`.
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


TCoordinate = AtLeastOne


AxisLookup: Dict[ECoordinateAxes, str] = {
    ECoordinateAxes.CARRIAGE: 'X',
    ECoordinateAxes.MANDREL: 'Y',
    ECoordinateAxes.DELIVERY_HEAD: 'Z'
}
