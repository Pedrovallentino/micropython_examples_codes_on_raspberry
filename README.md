# Coleção de exemplos em *MicroPython* para Raspberry Pi Pico / BitDogLab (RP2040).  
Este repositório contém pequenos exemplos didáticos que demonstram o uso de botões, LEDs, buzzer (PWM) e uma matriz/strip NeoPixel (WS2812) em MicroPython. Abaixo você encontrará descrições detalhadas de cada arquivo, propósito, explicação linha a linha / bloco a bloco, diagramas de ligação (wiring), dicas de depuração e observações sobre temporização, debounce e PWM.

_Nota: as referências às APIs MicroPython usadas aqui (por exemplo machine.Pin, machine.PWM, e neopixel) estão documentadas na documentação oficial do MicroPython_

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
- [Conclusão](#conclusão)

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

## Como Executar (Thonny)

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

Explicação e código comentado — todos os exemplos
- Abaixo está cada script com comentários linha a linha/ bloco a bloco para tornar o aprendizado o mais didático possível. Copie e cole cada bloco no Thonny para testar.

---
**Propósito:** alternar sequencialmente a cor de um conjunto RGB (3 LEDs separados — vermelho, verde, azul) a cada pressionamento de botão.
Pinos usados (exemplo): botão → GP5 (input com PULL_UP), LED vermelho → GP13, LED verde → GP11, LED azul → GP12.
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
Pin(..., Pin.IN, Pin.PULL_UP) configura o pino como entrada com resistor de pull-up interno. Botões com pull-up lógicos são lidos como 1 quando soltos e 0 quando pressionados (por conexão a GND).

**Observações práticas:**

- O debounce por sleep funciona, mas não é o mais elegante. Para aplicações sensíveis a tempo, considere implementar debounce por verificação do estado por N ms ou usar interrupções.
- Se os LEDs forem parte de um LED RGB (único pacote com 3 pinos), confirme se os pinos são cátodo comum ou ânodo comum e ajuste lógica (0/1) conforme necessário.

---
**Propósito**: demonstrar leitura de dois botões (esquerdo/direito) e acionar diferentes LEDs dependendo do estado (botões individuais ou ambos pressionados).
Pinos usados (exemplo): botões GP5 e GP6; LEDs GP11 (verde), GP12 (azul), GP13 (vermelho).

**Lógica principal (resumo):**
- Se ambos os botões pressionados → acende vermelho.
- Se apenas botão esquerdo pressionado → acende azul.
- Se apenas botão direito pressionado → acende verde.

### botoes/botao_ex02.py
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
**Observação:**

- A ordem das condições importa: primeiro checa ambos, depois cada um individual. Isso evita interpretação ambígua quando dois botões são pressionados simultaneamente.
- Debounce: o script usa time.sleep(0.1) para reduzir leituras muito rápidas; conforme no botao_ex01, para aplicações mais robustas prefira debounce por software que verifica estabilidade do sinal por X ms.

---
**Propósito:** tocar uma melodia (versão simplificada de “Parabéns pra Você”) usando um buzzer controlado por PWM.
Pinos usados (exemplo): buzzer em GP10 (via PWM(Pin(10))).

**Conceitos chave:**

- PWM gera uma onda quadrada numa frequência configurada (freq) e com duty cycle ajustável (duty_u16) — aqui duty_u16(32768) corresponde a ~50% (32768 / 65535). 
docs.micropython.org
- O dicionário notas mapeia nomes de notas (C4, D4...) para frequências em Hz.
- Nota 'P' representa pausa (frequência 0): ao tocar pausa, o PWM é mantido desligado (duty_u16(0)).

**Função tocar_nota(frequencia, duracao):**

- Se frequencia > 0 configura buzzer.freq() e buzzer.duty_u16(32768) para reproduzir a nota.
- Usa time.sleep(duracao) para a duração desejada e depois duty_u16(0) para silenciar brevemente entre notas.


### buzzer/buzzer.py
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
**Observações práticas:**

- Se o buzzer for ativo (gera tom próprio ao ser energizado), definir frequência não terá efeito — nesse caso, apenas ligar/desligar o pino é suficiente. Para buzzer passivo (é só um transdutor), é necessário PWM.
- Evite manter duty muito baixo em alguns ports/boards; certas portas ou implementações podem tratar valores muito baixos de forma diferente (ver issues conhecidas sobre duty_u16 em RP2040). 

---
**Propósito:** exemplo simples de blink sequencial dos três LEDs (vermelho, azul, verde) — útil para testar conexões e comportamento de saídas digitais.
Pinos usados (exemplo): GP11, GP12, GP13.

**Fluxo:**
-Liga um LED por 1s, desliga e passa para o próximo; ciclo contínuo.

leds/blink.py
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
**Observações:**

- Ideal para testes iniciais de fiação e verificação do estado dos pinos.
- Se quiser um comportamento não bloqueante (para realizar outras tarefas enquanto pisca), substitua time.sleep() por um laço com utime.ticks_ms() e checagens de tempo.

---
**Propósito:** demonstrar controle de uma matriz/strip NeoPixel WS2812 (25 LEDs) com padrão de preenchimento, limpeza e “varredura” (chase / one-by-one).
Pinos usados (exemplo): GP7 como linha de dados para NeoPixels; num_pixels = 25.

API usada: módulo neopixel — cria np = NeoPixel(pin, num_pixels). Cada elemento np[i] recebe uma tupla (R, G, B) com valores 0..255. Para aplicar mudanças deve-se chamar np.write() que envia o buffer com o protocolo de tempo preciso para WS2812.

**Funções utilitárias:**

- clear() — zera todas as LEDs (preto).
- fill_color(r,g,b) — preenche todos os pixels com a cor indicada.

**Sequência do loop:**

- Preenche vermelho, aguarda 1s.
- Preenche verde, 1s.
- Preenche azul, 1s.
- Limpa, define np[0] como branco (ponto), escreve e limpa.
- Efeito varredura: acende cada LED branco um por um com 50 ms entre eles.
- Limpa e repete.

matriz_led/matriz_led.py
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
**Observações de hardware:**

- NeoPixels demandam alimentação estável de 5V (dependendo do modelo) ou 3.3V em alguns; verifique a tensão suportada e forneça alimentação adequada com GND comum ao Pico.
- Os NeoPixels exigem um sinal digital com timing rigoroso; o módulo neopixel cuida disso, mas alguns adaptadores ou linhas longas podem exigir nível-shifter se o strip for 5V e o Pico gerar 3.3V.

---

##Conclusão

Este conjunto de exemplos oferece uma base prática e didática para quem quer explorar os fundamentos de automação e interfaces físicas com MicroPython em placas como o Raspberry Pi Pico ou BitDogLab. Cada script demonstra conceitos importantes como:

- leitura de botões com pull-up,
- controle de LEDs digitais,
- geração de som via PWM,
- efeitos visuais com NeoPixels,
- gestão de loops, atrasos (delays) e debounce.

Ao estudar e modificar esses exemplos, o usuário adquire compreensão prática das APIs de MicroPython (machine.Pin, machine.PWM, neopixel), aprende a configurar hardware (ligar botões, LEDs, buzzer, matrizes de LEDs) corretamente, e ganha experiência para identificar e corrigir problemas comuns (erros de pino, polaridade, alimentação, sincronização de sinais).
