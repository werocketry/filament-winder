from typing import List, Dict
from types import TCoordinate, ECoordinateAxes, AxisLookup, TCoordinateAxes
from src.helpers import interpolate_coordinates, serialize_coordinate  # Helpers inside src
from helpers import strip_precision  # Helpers outside src


class WinderMachine:
    def __init__(self, mandrel_diameter: float, verbose_output: bool = False):
        self.verbose_output = verbose_output
        self.gcode: List[str] = []

        # Profiler state
        self.feed_rate_mm_per_min = 0
        self.total_time_s = 0
        self.total_tow_length_mm = 0
        self.last_position: TCoordinateAxes = {
            ECoordinateAxes.CARRIAGE: 0,
            ECoordinateAxes.MANDREL: 0,
            ECoordinateAxes.DELIVERY_HEAD: 0,
        }
        self.mandrel_diameter = mandrel_diameter

    def get_gcode(self) -> List[str]:
        return self.gcode

    def add_raw_gcode(self, command: str) -> None:
        self.gcode.append(command)

    def set_feed_rate(self, feed_rate_mm_per_min: float) -> None:
        self.feed_rate_mm_per_min = feed_rate_mm_per_min
        self.gcode.append(f"G0 F{strip_precision(feed_rate_mm_per_min)}")

    def move(self, position: TCoordinate) -> None:
        complete_end_position = {**self.last_position, **position}
        do_segment_move = (
            self.last_position[ECoordinateAxes.CARRIAGE]
            != complete_end_position[ECoordinateAxes.CARRIAGE]
        )

        if not do_segment_move:
            if self.verbose_output:
                self.insert_comment(
                    f"Move from {serialize_coordinate(self.last_position)} "
                    f"to {serialize_coordinate(complete_end_position)} as a simple move"
                )
            return self.move_segment(position)

        num_segments = (
            round(
                abs(
                    self.last_position[ECoordinateAxes.CARRIAGE]
                    - complete_end_position[ECoordinateAxes.CARRIAGE]
                )
            )
            + 1
        )

        if self.verbose_output:
            self.insert_comment(
                f"Move from {serialize_coordinate(self.last_position)} "
                f"to {serialize_coordinate(complete_end_position)} in {num_segments} segments"
            )

        for intermediate_position in interpolate_coordinates(
            self.last_position, complete_end_position, num_segments
        ):
            self.move_segment(intermediate_position)

    def set_position(self, position: TCoordinate) -> None:
        command = "G92"
        for axis, value in position.items():
            raw_axis = AxisLookup[axis]
            command += f" {raw_axis}{strip_precision(value)}"
            self.last_position[axis] = value

        self.gcode.append(command)

    def zero_axes(self, current_angle_degrees: float) -> None:
        self.set_position(
            {
                ECoordinateAxes.CARRIAGE: 0,
                ECoordinateAxes.MANDREL: current_angle_degrees % 360,
                ECoordinateAxes.DELIVERY_HEAD: 0,
            }
        )

        self.move({ECoordinateAxes.MANDREL: 360})

        self.set_position({ECoordinateAxes.MANDREL: 0})

    def insert_comment(self, text: str) -> None:
        self.gcode.append(f"; {text}")

    def get_gcode_time_s(self) -> float:
        return self.total_time_s

    def get_tow_length_m(self) -> float:
        return self.total_tow_length_mm / 1000

    def set_mandrel_diameter(self, mandrel_diameter: float) -> None:
        self.mandrel_diameter = mandrel_diameter

    def move_segment(self, position: TCoordinate) -> None:
        total_distance_marlin_units_sq = 0
        tow_length_mm_sq = 0
        command = "G0"

        for axis, value in position.items():
            raw_axis = AxisLookup[axis]
            command += f" {raw_axis}{strip_precision(value)}"

            move_component = value - self.last_position[axis]
            total_distance_marlin_units_sq += move_component**2

            if axis == ECoordinateAxes.MANDREL:
                arc_length_mm = (
                    move_component / 360 * self.mandrel_diameter * 3.14159
                )
                tow_length_mm_sq += arc_length_mm**2
            elif axis == ECoordinateAxes.CARRIAGE:
                tow_length_mm_sq += move_component**2

            self.last_position[axis] = value

        self.total_time_s += (
            total_distance_marlin_units_sq**0.5 / self.feed_rate_mm_per_min * 60
        )
        self.total_tow_length_mm += tow_length_mm_sq**0.5

        self.gcode.append(command)
