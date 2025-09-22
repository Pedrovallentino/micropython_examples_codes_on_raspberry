# micropython_examples_codes_on_raspberry

Coleção de exemplos em *MicroPython* para Raspberry Pi Pico / BitDogLab (RP2040).  
Este repositório apresenta scripts que demonstram funcionalidades como leitura de botões, controle de LEDs, buzzer via PWM e matrizes de LEDs do tipo NeoPixel. Cada exemplo contém explicações detalhadas e código comentado para facilitar o aprendizado.

---

## Índice

- [Visão Geral](#visão-geral)  
- [Requisitos](#requisitos)  
- [Como Executar](#como-executar)  
- [Ligações / Wiring](#ligações--wiring)  
- [Exemplos Detalhados](#exemplos-detalhados)  
  - [botoes/botao_ex01.py](#botoesbotao_ex01py)  
  - [botoes/botao_ex02.py](#botoesbotao_ex02py)  
  - [buzzer/buzzer.py](#buzzerbuzzerpy)  
  - [leds/blink.py](#ledsblinkpy)  
  - [matriz_led/matriz_led.py](#matriz_ledmatriz_ledpy)  
- [Boas Práticas & Dicas de Depuração](#boas-práticas--dicas-de-depuração)  
- [Diagnósticos Rápidos (REPL)](#diagnósticos-rápidos-repl)  
- [Licença & Créditos](#licença--créditos)

---

## Visão Geral

Este repositório destina-se a servir como base para quem está aprendendo MicroPython com hardware como Raspberry Pi Pico ou BitDogLab. Os exemplos incluem:

- Alternância de cores via LED RGB com botão;  
- Leitura de dois botões para acionar diferentes LEDs;  
- Tocar melodia com buzzer via PWM;  
- Piscar múltiplos LEDs sequencialmente;  
- Controle de matriz/fita NeoPixel com efeitos visuais.

---

## Requisitos

- Placa RP2040 compatível (ex: Raspberry Pi Pico, BitDogLab).  
- Firmware MicroPython recente para a placa.  
- IDE recomendada: *Thonny*.  
- Biblioteca neopixel instalada (normalmente já incluída em builds compatíveis).  

---

## Como Executar

1. Conectar a placa ao computador via USB.  
2. Abrir Thonny, selecionar interpretador: *MicroPython (Raspberry Pi Pico)*.  
3. Copiar os arquivos de exemplo para a placa (File → Save as... → Raspberry Pi Pico).  
4. Executar com Run (F5) ou salvar como main.py para execução automática no boot (testar antes de usar como main.py).  
5. Verificar no REPL mensagens de erro ou prints, ajustar pinos conforme hardware físico.

---

## Ligações / Wiring

- *Botões*: um terminal do botão → GPIO configurado como IN, PULL_UP; outro terminal → GND.  
- *LED externo*: GPIO → resistor (220-330Ω) → anodo do LED; cátodo do LED → GND.  
- *LED onboard* (Pico padrão): geralmente GP25.  
- *Buzzer passivo*: GPIO → buzzer (+), buzzer (-) → GND. Se necessário, usar transistor se corrente for alta.  
- *NeoPixel / strip WS2812*: Data pin (ex: GP7) → DIN do strip; VCC do strip → alimentação adequada; GND em comum com placa; resistores/capacitores recomendados para estabilidade.

---

## Exemplos Detalhados

### botoes/botao_ex01.py

```python
# botoes/botao_ex01.py
# Alterna entre LED vermelho, verde, azul a cada pressione de botão

from machine import Pin
import time

# Configurações iniciais
# Botão conectado ao GPIO 5 com pull-up interno
pino_botao = Pin(5, Pin.IN, Pin.PULL_UP)

# LEDs como saídas digitais
led_vermelho = Pin(13, Pin.OUT)
led_verde    = Pin(11, Pin.OUT)
led_azul     = Pin(12, Pin.OUT)

# Controle da cor atual: 0 = vermelho, 1 = verde, 2 = azul
cor_atual = 0

def desligar_leds():
    """Desliga todos os LEDs para evitar sobreposição de cores."""
    led_vermelho.value(0)
    led_verde.value(0)
    led_azul.value(0)

# Loop principal
while True:
    # Se botão pressionado (valor 0 porque usamos pull_up)
    if pino_botao.value() == 0:
        # Incrementa a cor, volta para 0 após 2
        cor_atual = (cor_atual + 1) % 3
        # Desliga todos antes de acender um novo
        desligar_leds()
        # Acende LED correspondente
        if cor_atual == 0:
            led_vermelho.value(1)
        elif cor_atual == 1:
            led_verde.value(1)
        elif cor_atual == 2:
            led_azul.value(1)
        # Pequeno atraso para evitar múltiplas leituras rápidas do mesmo clique
        time.sleep(0.3)
```

```python
# botoes/botao_ex02.py
# Leitura de dois botões para acionar LEDs diferentes

from machine import Pin
import time

# Botões com pull-up
pino_botao_esquerdo = Pin(5, Pin.IN, Pin.PULL_UP)
pino_botao_direito  = Pin(6, Pin.IN, Pin.PULL_UP)

# LEDs
pino_led_verde    = Pin(11, Pin.OUT)
pino_led_azul     = Pin(12, Pin.OUT)
pino_led_vermelho = Pin(13, Pin.OUT)

def desligar_tudo():
    pino_led_verde.value(0)
    pino_led_azul.value(0)
    pino_led_vermelho.value(0)

# Loop principal
while True:
    # Se ambos os botões pressionados
    if pino_botao_direito.value() == 0 and pino_botao_esquerdo.value() == 0:
        desligar_tudo()
        pino_led_vermelho.value(1)
    # Se só o esquerdo
    elif pino_botao_esquerdo.value() == 0:
        desligar_tudo()
        pino_led_azul.value(1)
    # Se só o direito
    elif pino_botao_direito.value() == 0:
        desligar_tudo()
        pino_led_verde.value(1)
    # Delay curto para evitar leituras contínuas muito rápidas
    time.sleep(0.1)
```

```python

# buzzer/buzzer.py
# Tocar melodia com buzzer via PWM

from machine import Pin, PWM
import time

# Cria PWM no pino 10 para buzzer
buzzer = PWM(Pin(10))
# Ajuste inicial de frequência; será mudado por nota
buzzer.freq(10000)

# Dicionário de notas musicais com suas frequências em Hz
notas = {
    "C4": 262, "D4": 294, "E4": 330, "F4": 349, "G4": 392, "A4": 440, "B4": 494,
    "C5": 523, "D5": 587, "E5": 659, "F5": 698, "G5": 784,
    "P": 0   # "P" para pausa / silêncio
}

# Lista de tuplas (nota, duração em segundos)
# Melodia: “Parabéns Pra Você” (versão simples)
melodia = [
    ("C4", 0.3), ("C4", 0.3), ("D4", 0.6), ("C4", 0.6), ("F4", 0.6), ("E4", 1.2),
    ("P", 0.3),
    ("C4", 0.3), ("C4", 0.3), ("D4", 0.6), ("C4", 0.6), ("G4", 0.6), ("F4", 1.2),
    ("P", 0.3),
    ("C4", 0.3), ("C4", 0.3), ("C5", 0.6), ("A4", 0.6), ("F4", 0.6), ("E4", 0.6), ("D4", 1.2),
    ("P", 0.3),
    ("B4", 0.3), ("B4", 0.3), ("A4", 0.6), ("F4", 0.6), ("G4", 0.6), ("F4", 1.2)
]

def tocar_nota(frequencia, duracao):
    """Reproduz uma nota: configura frequência e duty, espera duração e silencia."""
    if frequencia > 0:
        buzzer.freq(frequencia)        # define a nota
        buzzer.duty_u16(32768)          # duty 50% para gerar som
    # pausa se frequência = 0
    time.sleep(duracao)
    buzzer.duty_u16(0)                  # silencia
    time.sleep(0.01)                    # pequena separação entre notas

# Loop infinito para repetir a melodia
while True:
    for nota, duracao in melodia:
        frequencia = notas[nota]
        tocar_nota(frequencia, duracao)
    time.sleep(2)  # espera antes de repetir melodia

```

```python

# leds/blink.py
# Pisca LEDs verde, azul e vermelho em sequência

from machine import Pin
import time

# Configura os LEDs como saída
pino_led_verde    = Pin(11, Pin.OUT)
pino_led_azul     = Pin(12, Pin.OUT)
pino_led_vermelho = Pin(13, Pin.OUT)

# Loop que pisca cada LED por 1 segundo
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
```

```python

# matriz_led/matriz_led.py
# Controla uma matriz ou fita NeoPixel com múltiplos efeitos

import time
from neopixel import NeoPixel
from machine import Pin

# Pino de dados para NeoPixel
pin = Pin(7, Pin.OUT)
# Número de LEDs no array
num_pixels = 25

# Criação do objeto NeoPixel
np = NeoPixel(pin, num_pixels)

def clear():
    """Apaga todos os pixels (colore com preto)."""
    for i in range(num_pixels):
        np[i] = (0, 0, 0)
    np.write()

def fill_color(r, g, b):
    """Preenche todos os pixels com a cor (r, g, b)."""
    for i in range(num_pixels):
        np[i] = (r, g, b)
    np.write()

# Loop com efeitos
while True:
    fill_color(255, 0, 0)  # vermelho
    time.sleep(1)

    fill_color(0, 255, 0)  # verde
    time.sleep(1)

    fill_color(0, 0, 255)  # azul
    time.sleep(1)

    clear()
    np[0] = (255, 255, 255)  # primeiro LED em branco
    np.write()
    time.sleep(1)
    clear()

    # varredura: acende um LED por vez em branco
    for i in range(num_pixels):
        np[i] = (255, 255, 255)
        np.write()
        time.sleep(0.05)
        np[i] = (0, 0, 0)

    clear()
    time.sleep(1)
```
