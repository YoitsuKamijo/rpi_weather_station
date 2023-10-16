import sys
sys.path.insert(1, './libs')

import board
from bme680 import BME680, constants as bme680_constants
from pms5003.uart import PMS5003_UART
from ThinkInk.think_ink import ThinkInkDisplay
from tsl2591 import TSL2591
import time
from WaveSharePaper.ws2in7_display import WaveShare2In7Display

fontdir = os.path.join(os.path.dirname(os.path.realpath('./WaveSharePaper')), 'fonts')
font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 18)
font35 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 35)

class WeatherStation:
    def __init__(self):
        # Initilize I2C interface
        self.i2c = board.I2C()
        # Monochrome display
        # self._init_thinkink_display()
        self._init_waveshare_display()
        # Air quality sensor
        self._init_pms5003()
        # Brightness sensor
        self._init_tsl2591()
        # Gas, temperature, humidity and pressure sensor
        self._init_bme680()

        time.sleep(7)

    def _init_bme680(self):
        self.weather_sensor = BME680()
        print("hit", bme680_constants.FILTER_SIZE_3)
    
    def _init_pms5003(self):
        self.aqi_sensor = PMS5003_UART()
        self.aqi_sensor.on()
    
    def _init_thinkink_display(self):
        self.display = ThinkInkDisplay("ADAFRUIT_SSD1680")
    
    def _init_tsl2591(self):
        self.lux_sensor = TSL2591(self.i2c)
    
    def _init_waveshare_display(self):
        self.display = WaveShare2In7Display()
    
    def display_all_data(self):
        data = self.get_all_data()
        self.display_data(data)

    def display_data(self, data):
        text = ""
        for key in ("pm25", "temperature", "brightness", "humidity", "pressure"):
            if data.get(key) is None: continue
            val, unit = data[key]
            if key == "pm25":
                text += f"{unit} {val}\n"
            else:
                text += f"{val} {unit}\n"
        self.display.get_canvas().text(
            (5, 5),
            text,
            font=font18,
            fill=BLACK,
            align="left")
        self.display.display()

    def get_all_data(self):
        data = {}
        data["brightness"] = self.get_brightness()
        data["pm25"] = self.get_pm25()
        data.update(self.get_weather_data())
        return data

    def get_brightness(self):
        try:
            lux = self.lux_sensor.lux
            return (round(lux, 2), "lux")
        except Exception as e:
            print(e)
            return ("Error", "lux")

    def get_pm25(self):
        try:
            res = self.aqi_sensor.read()
            for k, v in res.items():
                if k != "pm_25_standard": continue
                return (v["value"], v["name"])
        except Exception as e:
            print(e)
            return ("Error", "Air quality")

    def get_weather_data(self):
        try:
            if not self.weather_sensor.get_sensor_data(): return None
            data = self.weather_sensor.data
            return {
                "temperature": (data.temperature, "C"),
                "pressure": (data.pressure, "hPa"),
                "humidity": (data.humidity, "%RH")
            }
        except Exception as e:
            print(e)
            return ("Error", "Weather")

def main():
    ws = WeatherStation()	
    while True:
        ws.display_all_data()
        time.sleep(30)

main()
