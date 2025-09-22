from machine import Pin, PWM
import time

# Define o pino do buzzer (GPIO 10) como um objeto PWM
# A frequência inicial é 0 para o buzzer ficar em silêncio
buzzer = PWM(Pin(10))
buzzer.freq(10000)

# Dicionário com as frequências das notas musicais
# Dica: Adicionar notas e frequências pode expandir o repertório
notas = {
    "C4": 262, "D4": 294, "E4": 330, "F4": 349, "G4": 392, "A4": 440, "B4": 494,
    "C5": 523, "D5": 587, "E5": 659, "F5": 698, "G5": 784,
    "P": 0   # "P" para pausa
}

# Define a música como uma lista de tuplas (nota, duração em segundos)
# Parabéns pra Você (em uma versão simplificada)
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
    if frequencia > 0:
        buzzer.freq(frequencia)
        buzzer.duty_u16(32768)  # Habilita o PWM com 50% de duty cycle
    
    time.sleep(duracao)
    buzzer.duty_u16(0)  # Desliga o PWM para a próxima nota
    time.sleep(0.01)    # Pequena pausa entre as notas

# Inicia o loop para tocar a melodia
while True:
    for nota, duracao in melodia:
        frequencia = notas[nota]
        tocar_nota(frequencia, duracao)
    
    # Adiciona um pequeno atraso antes de repetir a música
    time.sleep(2)