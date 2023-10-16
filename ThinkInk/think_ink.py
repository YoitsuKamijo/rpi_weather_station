#Install the following packages before running the code
# wget https://github.com/adafruit/Adafruit_CircuitPython_framebuf/raw/main/examples/font5x8.bin
# sudo apt-get install python3-pip
# pip3 install adafruit-circuitpython-epd
# sudo apt-get install fonts-dejavu
# sudo apt-get install python3-pil

from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1675 import Adafruit_SSD1675
from adafruit_epd.ssd1680 import Adafruit_SSD1680
import board
import busio
import digitalio
from enum import Enum
from PIL import Image, ImageDraw, ImageFont
import struct
import time

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class ThinkInkModels(Enum):
    ADAFRUIT_SSD1675 = (
        Adafruit_SSD1675,
        {"width": 122, "height": 250, "ecs": board.CE0, "dc": board.D22, "rst": board.D27, "busy": board.D17, "srcs": None}
    )
    ADAFRUIT_SSD1680 = (
        Adafruit_SSD1680,
        {"width": 122, "height": 250, "ecs": board.CE0, "dc": board.D22, "rst": board.D27, "busy": board.D17, "srcs": None}
    )
  
class ThinkInkDisplay():
    def __init__(self, model):
        think_ink_display, attrs = ThinkInkModels[model].value
        # create the spi device and pins we will need
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        ecs = digitalio.DigitalInOut(attrs["ecs"])
        dc = digitalio.DigitalInOut(attrs["dc"])
        rst = digitalio.DigitalInOut(attrs["rst"])    # can be None to not use this pin
        busy = digitalio.DigitalInOut(attrs["busy"])   # can be None to not use this pin
        srcs = attrs["srcs"]

        print("Initializing eink display...", think_ink_display)
        self._display = think_ink_display(attrs["width"], attrs["height"], spi, 
            cs_pin=ecs,
            dc_pin=dc,
            sramcs_pin=srcs,
            rst_pin=rst,
            busy_pin=busy,
        )
        self._display.rotation = 1
        
        self.small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        self.medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        self.large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        # ~ icon_font = ImageFont.truetype("./meteocons.ttf", 48)

        
    
    def draw(self, text="Hello World"):
        # ~ self._display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self._display.width, self._display.height), color=WHITE)
        draw = ImageDraw.Draw(image)
        
        (font_width, font_height) = self.medium_font.getsize(text)
        draw.text(
            (5, 5),
            text,
            font=self.medium_font, fill=BLACK,
            align="left"
        )

        self._display.image(image)
        self._display.display()
