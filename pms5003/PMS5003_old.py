from enum import Enum
import struct

class PMS5003Values(Enum):
    START_1 = b'\x42'
    START_2 = b'\x4d'

class PMS5003:
    def __init__(self) -> None:
        # rad, ok make our internal buffer!
        self._buffer = bytearray(32)
        self.data = {
            "pm_10_standard": None,
            "pm_25_standard": None,
            "pm_100_standard": None,
            "pm_10_env": None,
            "pm_25_env": None,
            "pm_100_env": None,
            "particles_03_um": None,
            "particles_05_um": None,
            "particles_10_um": None,
            "particles_25_um": None,
            "particles_50_um": None,
            "particles_100_um": None,
        }

    def on(self):
        raise NotImplementedError()

    def off(self):
        raise NotImplementedError()

    def _decode_data(self) -> None:
        """Low level buffer filling function, to be overridden"""
        raise NotImplementedError()

    def read(self) -> dict:
        """Read any available data from the air quality sensor and
        return a dictionary with available particulate/quality data
        Note that "standard" concentrations are those when corrected to
        standard atmospheric conditions (288.15 K, 1013.25 hPa), and
        "environmental" concentrations are those measure in the current
        atmospheric conditions.
        """
        self._decode_data()

        if not self._buffer[0:2] == b"BM":
            raise RuntimeError("Invalid PMS5003 header")

        frame_len = struct.unpack(">H", self._buffer[2:4])[0]
        if frame_len != 28:
            raise RuntimeError("Invalid PM2.5 frame length")

        checksum = struct.unpack(">H", self._buffer[30:32])[0]
        check = sum(self._buffer[0:30])
        if check != checksum:
            raise RuntimeError("Invalid PM2.5 checksum")

        # unpack data
        (
            self.data["pm_10_standard"],
            self.data["pm_25_standard"],
            self.data["pm_100_standard"],
            self.data["pm_10_env"],
            self.data["pm_25_env"],
            self.data["pm_100_env"],
            self.data["particles_03_um"],
            self.data["particles_05_um"],
            self.data["particles_10_um"],
            self.data["particles_25_um"],
            self.data["particles_50_um"],
            self.data["particles_100_um"],
        ) = struct.unpack(">HHHHHHHHHHHH", self._buffer[4:28])

        return self.data
