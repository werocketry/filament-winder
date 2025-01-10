from io import BytesIO
from PIL import Image, ImageDraw
from typing import List, Dict, Optional
from .plot_helpers import generate_coordinates
from planner.cust_types import IMandrelParameters, ITowParameters


class WindParameters:
    def __init__(self, mandrel: IMandrelParameters, tow: ITowParameters):
        self.mandrel = mandrel
        self.tow = tow


def plot_gcode(gcode: List[str]) -> Optional[BytesIO]:
    """
    Plot G-code instructions onto a canvas.

    Args:
        gcode (List[str]): A list of G-code strings.

    Returns:
        Optional[BytesIO]: A PNG image stream if successful, or None if invalid.
    """
    # Check for a header in the first line
    header_line_parts = gcode[0].split(" ")
    if not (header_line_parts[0] == ";" and header_line_parts[1] == "Parameters"):
        print("Did not find header comment in the first line")
        return None

    # Parse the winding parameters
    winding_parameters = WindParameters(
        **eval(" ".join(header_line_parts[2:]))
    )  # Ensure input is sanitized in real-world usage

    # Create the canvas
    canvas_width = int(winding_parameters.mandrel["windLength"])
    canvas_height = 360
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(canvas)

    x_coord, y_coord = 0, 0

    for line in gcode:
        line_parts = line.split(" ")
        if line_parts[0] == ";":
            # Comment, skip processing
            continue

        if line_parts[0] != "G0":
            print(f"Unknown G-code line: '{line}', skipping")
            continue

        next_x_coord = x_coord
        next_y_coord = y_coord

        for coordinate in line_parts[1:]:
            if coordinate[0] == "X":
                next_x_coord = float(coordinate[1:])
            if coordinate[0] == "Y":
                next_y_coord = float(coordinate[1:])

        for segment in generate_coordinates(
            {"x": x_coord, "y": y_coord}, {"x": next_x_coord, "y": next_y_coord}
        ):
            # Draw the outer layer
            draw.line(
                [(point["x"], point["y"]) for point in segment],
                fill="rgb(73, 0, 168)",
                width=int(winding_parameters.tow["width"]),
            )
            # Draw the inner layer
            draw.line(
                [(point["x"], point["y"]) for point in segment],
                fill="rgb(252, 211, 3)",
                width=int(winding_parameters.tow["width"] * 0.75),
            )

        x_coord = next_x_coord
        y_coord = next_y_coord

    # Save the canvas to a PNG stream
    output_stream = BytesIO()
    canvas.save(output_stream, format="PNG")
    output_stream.seek(0)
    return output_stream
