from machine import Pin
import time

pino_botao_esquerdo = Pin(5, Pin.IN, Pin.PULL_UP)
pino_botao_direito = Pin(6, Pin.IN, Pin.PULL_UP)

pino_led_verde = Pin(11, Pin.OUT)
pino_led_azul = Pin(12, Pin.OUT)
pino_led_vermelho = Pin(13, Pin.OUT)

def desligar_tudo():
    pino_led_verde.value(0)
    pino_led_azul.value(0)
    pino_led_vermelho.value(0)

while True:
    if pino_botao_direito.value() == 0 and pino_botao_esquerdo.value() == 0:
        desligar_tudo()
        pino_led_vermelho.value(1)
    
    elif pino_botao_esquerdo.value() == 0:
        desligar_tudo()
        pino_led_azul.value(1)
        
    elif pino_botao_direito.value() == 0:
        desligar_tudo()
        pino_led_verde.value(1)
        
    time.sleep(0.1)
    
    
