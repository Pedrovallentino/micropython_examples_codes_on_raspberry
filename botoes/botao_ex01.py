from machine import Pin
import time

# Define o pino do botão (GPIO 05) com resistor PULL_UP
pino_botao = Pin(5, Pin.IN, Pin.PULL_UP)

# Define os pinos dos LEDs RGB (vermelho, verde e azul)
led_vermelho = Pin(13, Pin.OUT)
led_verde = Pin(11, Pin.OUT)
led_azul = Pin(12, Pin.OUT)

# Variável para controlar a cor atual (0=vermelho, 1=verde, 2=azul)
cor_atual = 0

# Função para desligar todos os LEDs
def desligar_leds():
    led_vermelho.value(0)
    led_verde.value(0)
    led_azul.value(0)

# Loop principal
while True:
    # Verifica se o botão foi pressionado (o valor é 0 por causa do PULL_UP)
    if pino_botao.value() == 0:
        # Incrementa a cor_atual e volta para 0 se chegar a 3
        cor_atual = (cor_atual + 1) % 3
        
        # Desliga todos os LEDs antes de acender o próximo
        desligar_leds()
        
        # Lógica para mudar a cor
        if cor_atual == 0:
            led_vermelho.value(1)  # Acende o LED vermelho
        elif cor_atual == 1:
            led_verde.value(1)     # Acende o LED verde
        elif cor_atual == 2:
            led_azul.value(1)      # Acende o LED azul
            
        # Pequeno atraso para evitar leituras múltiplas (debounce)
        time.sleep(0.3)