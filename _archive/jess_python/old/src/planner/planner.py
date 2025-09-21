from typing import List, Dict
from .cust_types import (
    IWindParameters,
    IMandrelParameters,
    ITowParameters,
    ILayerParameters,
    THelicalLayer,
    THoopLayer,
    TSkipLayer,
)
from .machine import WinderMachine
from helpers import rad_to_deg, deg_to_rad
from .cust_types import ECoordinateAxes, ELayerType

def planWind(windingParameters: IWindParameters, verboseOutput: bool = False) -> List[str]:

    machine = WinderMachine(windingParameters["mandrelParameters"]["diameter"], verboseOutput)

    headerParameters = {
        "mandrel": windingParameters["mandrelParameters"],
        "tow": windingParameters["towParameters"],
    }
    machine.insertComment(f"Parameters {headerParameters}")
    machine.addRawGCode("G0 X0 Y0 Z0")
    machine.setFeedRate(windingParameters["defaultFeedRate"])

    encounteredTerminalLayer = False
    layerIndex = 0
    cumulativeTimeS = 0
    cumulativeTowUseM = 0

    for layer in windingParameters["layers"]:
        if encounteredTerminalLayer:
            print("WARNING: Attempting to plan a layer after a terminal layer, aborting...")
            break

        layerComment = f"Layer {layerIndex + 1} of {len(windingParameters["layers"])}: {layer.windType}"
        print(layerComment)
        machine.insertComment(layerComment)

        if layer.windType == ELayerType.HOOP:
            planHoopLayer(machine, {
                "parameters": layer,
                "mandrelParameters": windingParameters["mandrelParameters"],
                "towParameters": windingParameters["towParameters"],
            })
            encounteredTerminalLayer = encounteredTerminalLayer or layer.terminal

        elif layer.windType == ELayerType.HELICAL:
            planHelicalLayer(machine, {
                "parameters": layer,
                "mandrelParameters": windingParameters["mandrelParameters"],
                "towParameters": windingParameters["towParameters"],
            })

        elif layer.windType == ELayerType.SKIP:
            planSkipLayer(machine, {
                "parameters": layer,
                "mandrelParameters": windingParameters["mandrelParameters"],
                "towParameters": windingParameters["towParameters"],
            })

        layerIndex += 1

        print(f"Layer time estimate: {machine.getGCodeTimeS() - cumulativeTimeS} seconds")
        print(f"Layer tow required: {machine.getTowLengthM() - cumulativeTowUseM} meters")

        cumulativeTimeS = machine.getGCodeTimeS()
        cumulativeTowUseM = machine.getTowLengthM()

        print("-" * 80)

    print(f"\nTotal time estimate: {cumulativeTimeS} seconds")
    print(f"Total tow required: {cumulativeTowUseM} meters\n")

    return machine.getGCode()

def planHoopLayer(machine: WinderMachine, layerParameters: Dict) -> None:

    lockDegrees = 180

    windAngle = 90 - rad_to_deg(
        (layerParameters["mandrelParameters"].diameter / layerParameters["towParameters"].width)
    )
    mandrelRotations = (
        layerParameters["mandrelParameters"].windLength / layerParameters["towParameters"].width
    )
    farMandrelPositionDegrees = lockDegrees + (mandrelRotations * 360)
    farLockPositionDegrees = farMandrelPositionDegrees + lockDegrees
    nearMandrelPositionDegrees = farLockPositionDegrees + (mandrelRotations * 360)
    nearLockPositionDegrees = nearMandrelPositionDegrees + lockDegrees

    machine.move({
        ECoordinateAxes.CARRIAGE: 0,
        ECoordinateAxes.MANDREL: lockDegrees,
        ECoordinateAxes.DELIVERY_HEAD: 0,
    })
    machine.move({ECoordinateAxes.DELIVERY_HEAD: -windAngle})
    machine.move({
        ECoordinateAxes.CARRIAGE: layerParameters["mandrelParameters"].windLength,
        ECoordinateAxes.MANDREL: farMandrelPositionDegrees,
    })
    machine.move({
        ECoordinateAxes.MANDREL: farLockPositionDegrees,
        ECoordinateAxes.DELIVERY_HEAD: 0,
    })

    if layerParameters["parameters"].terminal:
        return

    machine.move({ECoordinateAxes.DELIVERY_HEAD: windAngle})
    machine.move({
        ECoordinateAxes.CARRIAGE: 0,
        ECoordinateAxes.MANDREL: nearMandrelPositionDegrees,
    })
    machine.move({
        ECoordinateAxes.MANDREL: nearLockPositionDegrees,
        ECoordinateAxes.DELIVERY_HEAD: 0,
    })
    machine.zeroAxes(nearLockPositionDegrees)

def planHelicalLayer(machine: WinderMachine, layerParameters: Dict) -> None:

    deliveryHeadPassStartAngle = -10
    leadOutDegrees = layerParameters["parameters"].leadOutDegrees
    windLeadInMM = layerParameters["parameters"].leadInMM
    lockDegrees = layerParameters["parameters"].lockDegrees
    deliveryHeadAngleDegrees = -1 * (90 - layerParameters["parameters"].windAngle)
    mandrelCircumference = 3.14159 * layerParameters["mandrelParameters"].diameter
    towArcLength = (
        layerParameters["towParameters"].width /
        (deg_to_rad(layerParameters["parameters"].windAngle))
    )
    numCircuits = int(mandrelCircumference / towArcLength)
    patternStepDegrees = 360 * (1 / numCircuits)
    passRotationMM = layerParameters["mandrelParameters"].windLength * (
        deg_to_rad(layerParameters["parameters"].windAngle)
    )
    passRotationDegrees = 360 * (passRotationMM / mandrelCircumference)
    passDegreesPerMM = passRotationDegrees / layerParameters["mandrelParameters"].windLength
    patternNumber = layerParameters["parameters"].patternNumber
    numberOfPatterns = numCircuits // patternNumber
    leadInDegrees = passDegreesPerMM * windLeadInMM
    mainPassDegrees = passDegreesPerMM * (
        layerParameters["mandrelParameters"].windLength - windLeadInMM
    )

    passParameters = [
        {
            "deliveryHeadSign": 1,
            "leadInEndMM": windLeadInMM,
            "fullPassEndMM": layerParameters["mandrelParameters"].windLength,
        },
        {
            "deliveryHeadSign": -1,
            "leadInEndMM": layerParameters["mandrelParameters"].windLength - windLeadInMM,
            "fullPassEndMM": 0,
        },
    ]

    print(f"Doing helical wind, {numCircuits} circuits")

    if numCircuits % layerParameters["parameters"].patternNumber != 0:
        print(
            f"WARNING: Circuit number {numCircuits} not divisible by pattern number {layerParameters['parameters'].patternNumber}"
        )
        return

    mandrelPositionDegrees = 0

    for patternIndex in range(numberOfPatterns):
        for inPatternIndex in range(patternNumber):
            for passParams in passParameters:
                machine.move({
                    ECoordinateAxes.MANDREL: mandrelPositionDegrees,
                    ECoordinateAxes.DELIVERY_HEAD: 0,
                })
                machine.move({
                    ECoordinateAxes.DELIVERY_HEAD: passParams["deliveryHeadSign"] * deliveryHeadPassStartAngle,
                })
                mandrelPositionDegrees += leadInDegrees
                machine.move({
                    ECoordinateAxes.CARRIAGE: passParams["leadInEndMM"],
                    ECoordinateAxes.MANDREL: mandrelPositionDegrees,
                    ECoordinateAxes.DELIVERY_HEAD: passParams["deliveryHeadSign"] * deliveryHeadAngleDegrees,
                })
                mandrelPositionDegrees += mainPassDegrees
                machine.move({
                    ECoordinateAxes.CARRIAGE: passParams["fullPassEndMM"],
                    ECoordinateAxes.MANDREL: mandrelPositionDegrees,
                })
                mandrelPositionDegrees += lockDegrees - leadOutDegrees - (passRotationDegrees % 360)

            mandrelPositionDegrees += patternStepDegrees * numCircuits / patternNumber

        mandrelPositionDegrees += patternStepDegrees

    mandrelPositionDegrees += lockDegrees
    machine.move({
        ECoordinateAxes.MANDREL: mandrelPositionDegrees,
        ECoordinateAxes.DELIVERY_HEAD: 0,
    })

    machine.zeroAxes(mandrelPositionDegrees)

def planSkipLayer(machine: WinderMachine, layerParameters: Dict) -> None:
    machine.move({
        ECoordinateAxes.CARRIAGE: 0,
        ECoordinateAxes.MANDREL: layerParameters["parameters"].mandrelRotation,
        ECoordinateAxes.DELIVERY_HEAD: 0,
    })
    machine.setPosition({ECoordinateAxes.MANDREL: 0})
