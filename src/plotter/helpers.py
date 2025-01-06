from typing import List, Dict


def generate_coordinates(start: Dict[str, float], end: Dict[str, float]) -> List[List[Dict[str, float]]]:
    """
    Turn two machine coordinate endpoints into a set of screen-space line segments.

    Args:
        start (Dict[str, float]): Starting point with 'x' and 'y' coordinates.
        end (Dict[str, float]): Ending point with 'x' and 'y' coordinates.

    Returns:
        List[List[Dict[str, float]]]: List of line segments in screen-space coordinates.
    """
    # Are both endpoints in the same modulo? If so, mod360 and return
    if int(start["y"] // 360) == int(end["y"] // 360):
        return [[
            {"x": start["x"], "y": start["y"] % 360},
            {"x": end["x"], "y": end["y"] % 360},
        ]]

    # If not, calculate the intersection point between the ray and the relevant edge
    slope = (end["y"] - start["y"]) / (end["x"] - start["x"])

    current_segment_end_y = 0
    next_segment_start_y = 360 * (start["y"] // 360)
    next_segment_start_y_adj = -0.001  # TODO: Refactor to avoid edge-case adjustment

    if end["y"] > start["y"]:
        current_segment_end_y = 360
        next_segment_start_y = 360 * ((start["y"] // 360) + 1)
        next_segment_start_y_adj = 0.001

    current_segment_end_x = start["x"] + ((next_segment_start_y - start["y"]) * (1 / slope))

    return [
        [
            {"x": start["x"], "y": start["y"] % 360},
            {"x": current_segment_end_x, "y": current_segment_end_y},
        ]
    ] + generate_coordinates(
        {"x": current_segment_end_x, "y": next_segment_start_y + next_segment_start_y_adj},
        end,
    )
