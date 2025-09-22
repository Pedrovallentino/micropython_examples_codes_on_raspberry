import time
from neopixel import NeoPixel
from machine import Pin

pin = Pin(7, Pin.OUT)
num_pixels = 25

np = NeoPixel(pin, num_pixels)

def clear():
    for i in range(num_pixels):
        np[i] = (0, 0, 0)
    np.write()

def fill_color(r, g, b):
    for i in range(num_pixels):
        np[i] = (r, g, b)
    np.write()

while True:
    fill_color(255, 0, 0)
    time.sleep(1)
    
    fill_color(0, 255, 0)
    time.sleep(1)

    fill_color(0, 0, 255)
    time.sleep(1)
    
    clear()
    np[0] = (255, 255, 255) 
    np.write()
    time.sleep(1)
    clear()

    for i in range(num_pixels):
        np[i] = (255, 255, 255)
        np.write()
        time.sleep(0.05)
        np[i] = (0, 0, 0)
        
    clear()
    time.sleep(1)