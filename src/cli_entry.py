import argparse
import json
from marlin_port import MarlinPort
from planner import plan_wind
from plotter import plot_gcode
import sys
from pathlib import Path


def run_gcode(file: str, port: str, verbose: bool):
    """
    Run a G-code file on the machine.
    """
    marlin = MarlinPort(port, verbose)
    marlin.initialize()

    with open(file, "r") as f:
        data = f.read()

    print(f"Sending commands from '{file}'")

    # Handle keypress events
    def keypress_handler():
        print('Press "Space" to pause/resume...')
        while True:
            key = input()
            if key == " ":
                if marlin.is_paused():
                    print("Resuming machine...")
                    marlin.resume()
                else:
                    print("Pausing machine, press 'Space' again to resume after it stops")
                    marlin.pause()

    # Run the keypress handler in a separate thread
    import threading
    threading.Thread(target=keypress_handler, daemon=True).start()

    # Queue commands
    for command in data.strip().split("\n"):
        marlin.queue_command(command)


def generate_gcode(file: str, output: str, verbose: bool):
    """
    Generate G-code from a .wind file.
    """
    with open(file, "r") as f:
        wind_definition = json.load(f)

    wind_commands = plan_wind(wind_definition, verbose)

    with open(output, "w") as f:
        f.write("\n".join(wind_commands))

    print(f"Wrote {len(wind_commands)} commands to '{output}'")


def visualize_gcode(file: str, output: str):
    """
    Visualize the contents of a G-code file as a PNG.
    """
    with open(file, "r") as f:
        file_contents = f.read()

    stream = plot_gcode(file_contents.split("\n"))

    if stream is None:
        print("No image to write")
        return

    with open(output, "wb") as output_file:
        output_file.write(stream.getvalue())

    print(f"The PNG file was created at '{output}'")


def main():
    parser = argparse.ArgumentParser(description="CLI for Filament Winder")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Run Command
    run_parser = subparsers.add_parser("run", help="Run a G-code file on the machine")
    run_parser.add_argument("file", type=str, help="G-code file to run")
    run_parser.add_argument("--port", "-p", type=str, required=True, help="Serial port to connect to")
    run_parser.add_argument("--verbose", "-v", action="store_true", help="Log every command?")

    # Plan Command
    plan_parser = subparsers.add_parser("plan", help="Generate G-code from a .wind file")
    plan_parser.add_argument("file", type=str, help="Wind definition (.wind) file")
    plan_parser.add_argument("--output", "-o", type=str, required=True, help="Output file for G-code")
    plan_parser.add_argument("--verbose", "-v", action="store_true", help="Include comments explaining segmented moves?")

    # Plot Command
    plot_parser = subparsers.add_parser("plot", help="Visualize the contents of a G-code file")
    plot_parser.add_argument("file", type=str, help="G-code file to visualize")
    plot_parser.add_argument("--output", "-o", type=str, required=True, help="PNG file to output")

    args = parser.parse_args()

    if args.command == "run":
        run_gcode(args.file, args.port, args.verbose)
    elif args.command == "plan":
        generate_gcode(args.file, args.output, args.verbose)
    elif args.command == "plot":
        visualize_gcode(args.file, args.output)


if __name__ == "__main__":
    main()
