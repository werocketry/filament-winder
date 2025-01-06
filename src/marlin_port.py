import serial
import threading
from queue import Queue
from typing import Optional
from helpers import is_object


class MarlinPort:
    def __init__(self, port_path: str, verbose: bool = False, baud_rate: int = 115200):
        self.port_path = port_path
        self.verbose = verbose
        self.baud_rate = baud_rate

        self.is_initialized = False
        self.port: Optional[serial.Serial] = None
        self.command_queue = Queue()
        self.has_command_waiting = False

        self.pausing = False
        self.paused = False
        self.resuming = False

    def initialize(self):
        if self.is_initialized:
            return

        self.has_command_waiting = False

        self.port = serial.Serial(
            port=self.port_path,
            baudrate=self.baud_rate,
            timeout=1,
            write_timeout=1
        )

        if not self.port.is_open:
            try:
                self.port.open()
            except serial.SerialException as error:
                if is_object(error):
                    raise Exception(f"Error opening port: {str(error)}")
                raise

        print(f"Port '{self.port_path}' opened at {self.baud_rate} baud.")
        self.is_initialized = True

        # Start a thread to read responses from the serial port
        threading.Thread(target=self._read_serial, daemon=True).start()
        self._try_next_command()

    def reset(self):
        self.has_command_waiting = False
        self.command_queue = Queue()
        self.is_initialized = False

    def queue_command(self, line: str):
        self.command_queue.put(line)
        self._try_next_command()

    def pause(self):
        if self.paused or self.pausing or self.resuming:
            print("Cannot pause when already paused or resuming!")
            return
        self.pausing = True
        self._write_command("M0")

    def complete_pause(self):
        self.pausing = False
        self.paused = True
        print("Machine paused.")

    def is_paused(self) -> bool:
        return self.paused or self.pausing

    def resume(self):
        if not self.paused or self.resuming:
            print("Cannot resume when already resuming or not paused!")
            return
        self.resuming = True
        self._write_command("M108")

    def complete_resume(self):
        if not self.paused or not self.resuming:
            print("Cannot complete resume while not paused or resuming!")
            return
        self.pausing = False
        self.paused = False
        self.resuming = False
        self._try_next_command()

    def _read_serial(self):
        while self.is_initialized and self.port and self.port.is_open:
            try:
                line = self.port.readline().decode("utf-8").strip()
                if line:
                    self._process_serial_response_line(line)
            except serial.SerialException as error:
                print(f"Serial read error: {str(error)}")
                break

    def _process_serial_response_line(self, line: str):
        if line == "ok":
            self.has_command_waiting = False
            self._try_next_command()
        elif line in ["echo:busy: processing", "echo:busy: paused for user"]:
            pass  # Do nothing
        elif line == "//action:notification Click to Resume...":
            self.complete_pause()
        elif line == "//action:notification 3D Printer Ready.":
            if not self.resuming:
                print("Saw resume response while not resuming!")
                return
            self.complete_resume()
        else:
            print(f"Got unexpected response: '{line}'")

    def _try_next_command(self):
        if self.has_command_waiting or self.command_queue.empty() or self.paused:
            return

        command_to_send = self.command_queue.get()
        # Check for comments
        if command_to_send.startswith(";"):
            print(command_to_send[1:].strip())
            self._try_next_command()
            return

        if self.verbose:
            print(f"Sending '{command_to_send}'")

        self.has_command_waiting = True
        self._write_command(command_to_send)

    def _write_command(self, command: str):
        if self.port and self.port.is_open:
            self.port.write(f"{command}\n".encode("utf-8"))
