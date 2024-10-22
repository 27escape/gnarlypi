#!/usr/bin/env python3
# based on the blinkt code

import signal
import sys
import time
import math
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

# ----------------------------------------------------------------------------
FONT_SIZE = 24
DISPLAY_HEIGHT = 135
DISPLAY_WIDTH = 240
ROTATION = 90
# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

TIME_COLOR = "#FFFFFF"
FILE_COLOR = "#FFFF00"
COPY_COLOR = "#FF0000"
SD_COLOR = "#FF00FF"
HD_COLOR = "#00FFFF"
NEW_LINE = FONT_SIZE + 4
ORANGE="#ffa500"
RED="#FF0000"
GREEN="#00FF00"
LIGHT_GREEN="#20a020"
PURPLE="#800080"


# ----------------------------------------------------------------------------
# this is the board hardware
def init_board():
    # Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = None

    # Setup SPI bus using hardware SPI:
    spi = board.SPI()

    # Create the ST7789 display:
    disp = st7789.ST7789(
        spi,
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        baudrate=BAUDRATE,
        # display is rotated so this is why these are the wrong way around
        width=DISPLAY_HEIGHT,
        height=DISPLAY_WIDTH,
        x_offset=53,
        y_offset=40,
    )
    # Turn on the backlight
    backlight = digitalio.DigitalInOut(board.D22)
    backlight.switch_to_output()
    backlight.value = True
    # enable the buttons    #
    buttonA = digitalio.DigitalInOut(board.D23)
    buttonB = digitalio.DigitalInOut(board.D24)
    buttonA.switch_to_input()
    buttonB.switch_to_input()

    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image, ROTATION)

    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image, ROTATION)

    # load a TTF font
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZE
    )

    return {
        "font": font,
        "draw": draw,
        "disp": disp,
        "image": image,
        "font": font,
        "height": height,
        "width": width,
    }


# ----------------------------------------------------------------------------
def button_actions():
    if buttonA.value and buttonB.value:
        backlight.value = False  # turn off backlight
    else:
        backlight.value = True  # turn on backlight
    if buttonB.value and not buttonA.value:  # just button A pressed
        display.fill(color565(255, 0, 0))  # red
    if buttonA.value and not buttonB.value:  # just button B pressed
        display.fill(color565(0, 0, 255))  # blue
    if not buttonA.value and not buttonB.value:  # none pressed
        display.fill(color565(0, 255, 0))  # green


# ----------------------------------------------------------------------------
# version of https://stackoverflow.com/questions/71773998/how-to-draw-a-progress-bar-with-pillow
def progress_bar(x, y, width, height, progress, fg="#FFFFFF", bg="#000000"):
    # Draw the background for the full width
    draw.rectangle( (x, y, x + width, y + height), fill=bg)
    width = int(width * progress)
    draw.rounded_rectangle( (x , y, x + width, y + height), fill=fg, radius=5)

def show_progress_bar( text, y, progress, color="#FFFFFF", bg="#000000"):
    draw.text((0, y), text, font=font, fill=color)
    progress_bar( 70, y, 170, FONT_SIZE, progress, color)


# ----------------------------------------------------------------------------

def cls():
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, tft["width"], tft["height"]), outline=0, fill=0)
    # Display image
    disp.image(image, ROTATION)

def clr_line( line):
    y = line * NEW_LINE
      # Draw the background for the full width
    draw.rectangle( (0, y, DISPLAY_WIDTH, y + NEW_LINE), fill=0)


# see https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
#  for centering and justification of text
# ordering of the anchor letters is important!

# center text on the middle of the display
def display_center_text( txt, color="#FFFFFF"):
    cls()
    # print( f"display_center_text {txt}")
    draw.text((DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2), txt, font=font, fill=color, anchor="mm")
    disp.image(image, ROTATION)

# center text on the middle of the given line
def center_line( txt, line=2, color="#FFFFFF"):
    clr_line( line)
    # print( f"center_line {txt}")
    draw.text((DISPLAY_WIDTH/2, (line * NEW_LINE)+(FONT_SIZE/2)), txt, font=font, fill=color, anchor="mm")
    disp.image(image, ROTATION)

def print_line( txt, line=2, color="#FFFFFF"):
    clr_line( line)
    # print( f"print_line {txt}")
    draw.text((0, line * NEW_LINE), txt, font=font, fill=color)
    disp.image(image, ROTATION)


def show_time( line=0):
    clr_line( line)
    now = time.strftime('%X')
    # draw.text((0, 0), "TIME", font=font, fill=TIME_COLOR)
    # draw.text((78, 0), f"{now}", font=font, fill=TIME_COLOR)
    # disp.image(image, ROTATION)
    center_line( now, 0)

def show_copy( percent, line=1):
    show_progress_bar( "Copy", line * NEW_LINE, percent, COPY_COLOR)
    disp.image(image, ROTATION)

def show_files( percent, line=2):
    show_progress_bar( "Files", line * NEW_LINE, percent, FILE_COLOR)
    disp.image(image, ROTATION)

def show_sd( percent, line=3):
    show_progress_bar( "SD", line * NEW_LINE, percent, SD_COLOR)
    disp.image(image, ROTATION)

def show_hd( percent, line=4):
    show_progress_bar( "HD", line * NEW_LINE, percent, HD_COLOR)
    disp.image(image, ROTATION)


# ----------------------------------------------------------------------------
def signal_handler(sig, frame):
    # print("You pressed Ctrl+C!")
    cls()
    display_center_text( 'display offline', PURPLE)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


# ----------------------------------------------------------------------------
def status_error(topic, data):
    """status_error"""
    cls() ;
    show_time()
    center_line("error", 2, RED)


# ----------------------------------------------------------------------------
def status_ready(topic, data):
    """status_ready"""
    show_time()
    clr_line( 3)
    center_line("Insert SD card", 2, GREEN)


# ----------------------------------------------------------------------------
def status_startcopy(topic, data):
    """status_startcopy"""
    # print_line("start copy")
    cls()
    show_time() ;


# ----------------------------------------------------------------------------
def status_endcopy(topic, data):
    """status_endcopy"""
    # print_line("end copy ")
    cls()

# ----------------------------------------------------------------------------
def status_copydata(topic, data):
    """status_copydata"""

    data["size"] != 1
    # percent = data["copied"] / data["size"]
    # print(
    #     f"copy {data['fromfile']} to {data['tofile']}, {percent}, overall {data['files_copied']}/{data['files_total']}",
    #     end="\r",
    # )

    show_time() ;
    show_copy( data["copied"]/ data["size"])
    show_files( data["files_copied"]/ data["files_total"])

# ----------------------------------------------------------------------------
def status_waitremove(topic, data):
    """status_waitremove"""
    center_line("Remove SD Card", 2, ORANGE)

# ----------------------------------------------------------------------------
def quick_perc( free, size):
  return (size - free) / size

# ----------------------------------------------------------------------------
def status_devicedata(topic, data):
    """status_devicedata"""

    # get the used sizes from the size and free values
    # print(
    #     f"SD data: {data['sd_size']-data['sd_free']}/{data['sd_size']}, target: {data['hd_size']-data['hd_free']}/{data['hd_size']}"
    # )
    # get used (size-free) over size
    if data['sd_size']:
      show_sd(  quick_perc(data['sd_free'], data['sd_size']))

    if data['hd_size']:
      show_hd(  quick_perc(data['hd_free'], data['hd_size']))


# ----------------------------------------------------------------------------
def general_status(topic, data):
    """status_devicedata"""
    cls() ;
    print_line("general status blue ")


# ----------------------------------------------------------------------------
def status_diskfull(topic, data):
    """status_devicedata"""
    cls() ;
    print_line("HD disk full")

# ----------------------------------------------------------------------------
# display a small message
def status_fivelines(topic, data):
    """status_fivelines"""


    color=LIGHT_GREEN
    cls() ;
    # exists and is valid
    if "color" in data and data["color"]:
      color=data["color"]

    # get index and the array value, max 5 lines
    for line, txt in enumerate( data["lines"][:5]):
      center_line(txt, line, color)


# ----------------------------------------------------------------------------
# we only get keep alives when the system is not doing anything else, so
# we can update the time
def status_keepalive(topic, data):
    """status_devicedata"""
    show_time( 0)

# ----------------------------------------------------------------------------
# clea the display
def status_cls(topic, data):
    """status_devicedata"""
    cls()



# ----------------------------------------------------------------------------

if __name__ == "__main__":
    # setup hardware
    tft = init_board()

    # make these globals for ease of use
    draw = tft["draw"]
    font = tft["font"]
    image = tft["image"]
    disp = tft["disp"]

    cls()

    status_fivelines( "/somethng", {"lines":["this", "is", "working", "",""], "color": "#FFFF00"} )
