from .cust_types import TCoordinateAxes, ECoordinateAxes
from typing import List


class Helpers:
    @staticmethod
    def serialize_coordinate(coordinate: TCoordinateAxes) -> str:
        """
        Turn a coordinate into a nicely formatted string.
        """
        return f"{{{coordinate[ECoordinateAxes.CARRIAGE]} {coordinate[ECoordinateAxes.MANDREL]} {coordinate[ECoordinateAxes.DELIVERY_HEAD]}}}"

    @staticmethod
    def interpolate_coordinates(
        start: TCoordinateAxes, end: TCoordinateAxes, steps: int
    ) -> List[TCoordinateAxes]:
        """
        Create an array of evenly-spaced coordinates between two coordinates.
        """
        if steps <= 0:
            raise ValueError("Steps cannot be less than 1")
        if steps == 1:
            return [end]

        coordinates: List[TCoordinateAxes] = []

        carriage_step = (end[ECoordinateAxes.CARRIAGE] - start[ECoordinateAxes.CARRIAGE]) / (steps - 1)
        mandrel_step = (end[ECoordinateAxes.MANDREL] - start[ECoordinateAxes.MANDREL]) / (steps - 1)
        delivery_head_step = (end[ECoordinateAxes.DELIVERY_HEAD] - start[ECoordinateAxes.DELIVERY_HEAD]) / (steps - 1)

        for step in range(steps):
            coordinates.append({
                ECoordinateAxes.CARRIAGE: start[ECoordinateAxes.CARRIAGE] + step * carriage_step,
                ECoordinateAxes.MANDREL: start[ECoordinateAxes.MANDREL] + step * mandrel_step,
                ECoordinateAxes.DELIVERY_HEAD: start[ECoordinateAxes.DELIVERY_HEAD] + step * delivery_head_step
            })

        return coordinates
