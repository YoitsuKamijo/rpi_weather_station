import RPi.GPIO as GPIO
import serial
import time
from pms5003 import PMS5003, PMS5003Values

class PMS5003_UART(PMS5003):
    def __init__(self, port= "/dev/ttyS0", pins= {"SET": 23, "RESET": 24}):
        self._uart = serial.Serial(port, baudrate=9600, timeout=3.0)
        self._set_pin, self._reset_pin = pins["SET"], pins["RESET"]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._set_pin, GPIO.OUT)
        GPIO.setup(self._reset_pin, GPIO.OUT)
        super().__init__()
    
    def on(self):
        print("Powering on PMS5003...")
        GPIO.output(self._set_pin, True)
    
    def off(self):
        print("Powering off PMS5003...")
        GPIO.output(self._set_pin, False)
    
    def set_operation_mode(self, mode):
        try:
            if mode not in (PMS5003Values.ACTIVE_MODE.value, PMS5003Values.PASSIVE_MODE.value): raise Exception("inaccurate mode")
            self.mode = mode
            time.sleep(self.MIN_CMD_INTERVAL)
            self._uart.reset_input_buffer()
            cmd = PMS5003Values.CMD_MODE_PASSIVE.value if self.mode == PMS5003Values.PASSIVE_MODE.value else PMS5003Values.CMD_MODE_ACTIVE.value
            self._uart.write(self._build_cmd(cmd))
        except Exception as e:
            return
        time.sleep(self.MIN_CMD_INTERVAL)

    def _load_data(self, frame_len=32) -> None:
        while True:
            b = self._uart.read(1)
            if not b:
                raise RuntimeError("Unable to read from PM2.5 (no start of frame)")
            if b == PMS5003Values.START_1.value:
                break
        # weird byte stuff, if getting a single byte like b[0] it returns the converted value
        self._buffer[0] = b[0]

        remain = self._uart.read(frame_len)
        if not remain or len(remain) != frame_len - 1:
            raise RuntimeError("Unable to read from PM2.5 (incomplete frame)")
        # when setting a range of bytes it somehow works out
        self._buffer[1:] = remain
