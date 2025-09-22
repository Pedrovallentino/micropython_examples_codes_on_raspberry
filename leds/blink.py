from machine import Pin
import time

pino_led_verde = Pin(11, Pin.OUT)
pino_led_azul = Pin(12, Pin.OUT)
pino_led_vermelho = Pin(13, Pin.OUT)

while True:
    pino_led_verde.value(1)
    time.sleep(1)
    pino_led_verde.value(0)
    time.sleep(1)
    
    pino_led_azul.value(1)
    time.sleep(1)
    pino_led_azul.value(0)
    time.sleep(1)
     
    pino_led_vermelho.value(1)
    time.sleep(1)
    pino_led_vermelho.value(0)
    time.sleep(1)
    
    
    
    


     
    