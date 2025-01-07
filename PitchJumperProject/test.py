import pygame
import numpy as np
import pyaudio

# Настройки
WIDTH, HEIGHT = 800, 600
FPS = 60
SAMPLE_RATE = 44100
CHUNK = 1024
MIN_PITCH = 200  # Минимальная частота для отображения
MAX_PITCH = 400  # Максимальная частота для отображения
SMOOTHING_FACTOR = 0.1  # Коэффициент сглаживания

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Инициализация PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

def get_pitch(data, rate):
    audio_data = np.frombuffer(data, dtype=np.int16)
    fft = np.fft.rfft(audio_data)
    frequencies = np.fft.rfftfreq(len(audio_data), d=1/rate)
    magnitude = np.abs(fft)
    peak_idx = np.argmax(magnitude)
    return frequencies[peak_idx]

# Переменная для хранения сглаженного значения частоты
smoothed_pitch = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Захват аудиоданных
    data = stream.read(CHUNK, exception_on_overflow=False)

    # Воспроизведение аудиоданных
    stream.write(data)

    pitch = get_pitch(data, SAMPLE_RATE)

    # Сглаживание частоты
    smoothed_pitch = smoothed_pitch * (1 - SMOOTHING_FACTOR) + pitch * SMOOTHING_FACTOR

    # Нормализация частоты для отображения
    normalized_pitch = (smoothed_pitch - MIN_PITCH) / (MAX_PITCH - MIN_PITCH)
    normalized_pitch = min(max(normalized_pitch, 0), 1)
    bar_height = int(normalized_pitch * HEIGHT)

    # Отображение полоски
    pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 50, HEIGHT - bar_height, 100, bar_height))

    pygame.display.flip()
    clock.tick(FPS)

# Завершение работы
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()
