from typing import List, Dict, Optional
from helpers import rad_to_deg, deg_to_rad
from .machine import WinderMachine
from .cust_types import (
    WindParameters,
    MandrelParameters,
    TowParameters,
    HoopLayer,
    HelicalLayer,
    SkipLayer,
    LayerType,
    CoordinateAxes,
)

def plan_wind(winding_parameters: WindParameters, verbose_output: bool = False) -> List[str]:
    machine = WinderMachine(winding_parameters.mandrel_parameters.diameter, verbose_output)

    header_parameters = {
        "mandrel": winding_parameters.mandrel_parameters.__dict__,
        "tow": winding_parameters.tow_parameters.__dict__,
    }
    machine.insert_comment(f"Parameters {header_parameters}")
    machine.add_raw_gcode("G0 X0 Y0 Z0")
    machine.set_feed_rate(winding_parameters.default_feed_rate)

    encountered_terminal_layer = False
    layer_index = 0
    cumulative_time_s = 0
    cumulative_tow_use_m = 0

    for layer in winding_parameters.layers:
        if encountered_terminal_layer:
            print("WARNING: Attempting to plan a layer after a terminal layer, aborting...")
            break

        layer_comment = f"Layer {layer_index + 1} of {len(winding_parameters.layers)}: {layer.wind_type.value}"
        print(layer_comment)
        machine.insert_comment(layer_comment)

        if isinstance(layer, HoopLayer):
            plan_hoop_layer(
                machine,
                layer,
                winding_parameters.mandrel_parameters,
                winding_parameters.tow_parameters,
            )
            encountered_terminal_layer = encountered_terminal_layer or layer.terminal

        elif isinstance(layer, HelicalLayer):
            plan_helical_layer(
                machine,
                layer,
                winding_parameters.mandrel_parameters,
                winding_parameters.tow_parameters,
            )

        elif isinstance(layer, SkipLayer):
            plan_skip_layer(
                machine,
                layer,
                winding_parameters.mandrel_parameters,
                winding_parameters.tow_parameters,
            )

        layer_index += 1

        print(f"Layer time estimate: {machine.get_gcode_time_s() - cumulative_time_s} seconds")
        print(f"Layer tow required: {machine.get_tow_length_m() - cumulative_tow_use_m} meters")

        cumulative_time_s = machine.get_gcode_time_s()
        cumulative_tow_use_m = machine.get_tow_length_m()

        print("-" * 80)

    print(f"\nTotal time estimate: {cumulative_time_s} seconds")
    print(f"Total tow required: {cumulative_tow_use_m} meters\n")

    return machine.get_gcode()


def plan_hoop_layer(machine: WinderMachine, layer: HoopLayer, mandrel_params: MandrelParameters, tow_params: TowParameters) -> None:
    lock_degrees = 180

    wind_angle = 90 - rad_to_deg(mandrel_params.diameter / tow_params.width)
    mandrel_rotations = mandrel_params.wind_length / tow_params.width
    far_mandrel_position_degrees = lock_degrees + (mandrel_rotations * 360)
    far_lock_position_degrees = far_mandrel_position_degrees + lock_degrees
    near_mandrel_position_degrees = far_lock_position_degrees + (mandrel_rotations * 360)
    near_lock_position_degrees = near_mandrel_position_degrees + lock_degrees

    machine.move({CoordinateAxes.CARRIAGE: 0, CoordinateAxes.MANDREL: lock_degrees, CoordinateAxes.DELIVERY_HEAD: 0})
    machine.move({CoordinateAxes.DELIVERY_HEAD: -wind_angle})
    machine.move({CoordinateAxes.CARRIAGE: mandrel_params.wind_length, CoordinateAxes.MANDREL: far_mandrel_position_degrees})
    machine.move({CoordinateAxes.MANDREL: far_lock_position_degrees, CoordinateAxes.DELIVERY_HEAD: 0})

    if layer.terminal:
        return

    machine.move({CoordinateAxes.DELIVERY_HEAD: wind_angle})
    machine.move({CoordinateAxes.CARRIAGE: 0, CoordinateAxes.MANDREL: near_mandrel_position_degrees})
    machine.move({CoordinateAxes.MANDREL: near_lock_position_degrees, CoordinateAxes.DELIVERY_HEAD: 0})
    machine.zero_axes(near_lock_position_degrees)


def plan_helical_layer(machine: WinderMachine, layer: HelicalLayer, mandrel_params: MandrelParameters, tow_params: TowParameters) -> None:
    delivery_head_pass_start_angle = -10
    lead_out_degrees = layer.lead_out_degrees
    wind_lead_in_mm = layer.lead_in_mm
    lock_degrees = layer.lock_degrees
    delivery_head_angle_degrees = -1 * (90 - layer.wind_angle)
    mandrel_circumference = 3.14159 * mandrel_params.diameter
    tow_arc_length = tow_params.width / (deg_to_rad(layer.wind_angle))
    num_circuits = int(mandrel_circumference / tow_arc_length)
    pattern_step_degrees = 360 * (1 / num_circuits)
    pass_rotation_mm = mandrel_params.wind_length * (deg_to_rad(layer.wind_angle))
    pass_rotation_degrees = 360 * (pass_rotation_mm / mandrel_circumference)
    pass_degrees_per_mm = pass_rotation_degrees / mandrel_params.wind_length
    pattern_number = layer.pattern_number
    number_of_patterns = num_circuits // pattern_number
    lead_in_degrees = pass_degrees_per_mm * wind_lead_in_mm
    main_pass_degrees = pass_degrees_per_mm * (mandrel_params.wind_length - wind_lead_in_mm)

    pass_params = [
        {"delivery_head_sign": 1, "lead_in_end_mm": wind_lead_in_mm, "full_pass_end_mm": mandrel_params.wind_length},
        {"delivery_head_sign": -1, "lead_in_end_mm": mandrel_params.wind_length - wind_lead_in_mm, "full_pass_end_mm": 0},
    ]

    print(f"Doing helical wind, {num_circuits} circuits")

    if num_circuits % pattern_number != 0:
        print(f"WARNING: Circuit number {num_circuits} not divisible by pattern number {pattern_number}")
        return

    mandrel_position_degrees = 0

    for pattern_index in range(number_of_patterns):
        for in_pattern_index in range(pattern_number):
            for pass_param in pass_params:
                machine.move({
                    CoordinateAxes.MANDREL: mandrel_position_degrees,
                    CoordinateAxes.DELIVERY_HEAD: 0,
                })

                machine.move({
                    CoordinateAxes.DELIVERY_HEAD: pass_param["delivery_head_sign"] * delivery_head_pass_start_angle,
                })

                mandrel_position_degrees += lead_in_degrees
                machine.move({
                    CoordinateAxes.CARRIAGE: pass_param["lead_in_end_mm"],
                    CoordinateAxes.MANDREL: mandrel_position_degrees,
                    CoordinateAxes.DELIVERY_HEAD: pass_param["delivery_head_sign"] * delivery_head_angle_degrees,
                })

                mandrel_position_degrees += main_pass_degrees
                machine.move({
                    CoordinateAxes.CARRIAGE: pass_param["full_pass_end_mm"],
                    CoordinateAxes.MANDREL: mandrel_position_degrees,
                })

                mandrel_position_degrees += lock_degrees - lead_out_degrees - (pass_rotation_degrees % 360)

            mandrel_position_degrees += pattern_step_degrees * num_circuits / pattern_number

        mandrel_position_degrees += pattern_step_degrees

    mandrel_position_degrees += lock_degrees
    machine.move({CoordinateAxes.MANDREL: mandrel_position_degrees, CoordinateAxes.DELIVERY_HEAD: 0})
    machine.zero_axes(mandrel_position_degrees)


def plan_skip_layer(machine: WinderMachine, layer: SkipLayer, mandrel_params: MandrelParameters, tow_params: TowParameters) -> None:
    machine.move({
        CoordinateAxes.CARRIAGE: 0,
        CoordinateAxes.MANDREL: layer.mandrel_rotation,
        CoordinateAxes.DELIVERY_HEAD: 0,
    })
    machine.set_position({CoordinateAxes.MANDREL: 0})
