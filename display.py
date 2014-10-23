#!/usr/bin/python`
import time


from scapy.all import *

import Adafruit_CharLCD as LCD


# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()

buttons = ( (LCD.SELECT, 'Select'),
            (LCD.LEFT,   'Left'  ),
            (LCD.UP,     'Up'    ),
            (LCD.DOWN,   'Down'  ),
            (LCD.RIGHT,  'Right' ) )

colors={"white":(1.0, 1.0, 1.0), "red":(1.0, 0.0, 0.0),
    "green":(0.0, 1.0, 0.0), "blue":(0.0, 0.0, 1.0),
    "yellow":(1.0, 1.0, 0.0), "cyan":(0.0, 1.0, 1.0),
    "magenta":(1.0, 0.0, 1.0)}

welcome = "Welcome to PiNetInfo"

def getIPAddress():
    return subprocess.check_output("ip addr show dev eth0 | grep inet | awk '{print $2}'", shell=True)

def getGateway():
    return subprocess.check_output("ip route | grep default", shell=True).split(" ")[2]

menuItems = [
    {
      "name": "IP Address",
      "function": getIPAddress,
      "static": True
    },
    {
      "name": "Gateway",
      "function": getGateway,
      "static": True
    }
]

def updateScreen(message):
    lcd.clear()
    lcd.message(message)

def main():
    menuLength = len(menuItems)
    menuLocation = 0
    inMenu = False
    color = "white"
    lcd.set_color(colors[color][0], colors[color][1], colors[color][2])
    lcd.set_backlight(1)
    updateScreen(welcome)
    while True:
        if lcd.is_pressed(LCD.SELECT) and inMenu:
            if menuItems[menuLocation]["static"] == True:
                updateScreen(menuItems[menuLocation]["function"]())
            else:
                menuItems[menuLocation]["function"]()
        elif lcd.is_pressed(LCD.SELECT) and not inMenu:
            updateScreen(menuItems[menuLocation]["name"])
            inMenu = True
        elif lcd.is_pressed(LCD.UP) and inMenu:
            menuLocation += 1
            if menuLocation > menuLength - 1:
                menuLocation = 0
            updateScreen(menuItems[menuLocation]["name"])
        elif lcd.is_pressed(LCD.DOWN) and inMenu:
            menuLocation -= 1
            if menuLocation < 0:
                menuLocation = menuLength - 1
            updateScreen(menuItems[menuLocation]["name"])
        elif lcd.is_pressed(LCD.LEFT) and inMenu:
            updateScreen(menuItems[menuLocation]["name"])
            inMenu = True
        time.sleep(.1)


try:
  main()
except KeyboardInterrupt:
  lcd.set_backlight(0)
  lcd.clear()
