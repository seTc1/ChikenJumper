import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, OVERLAY_COLOR, FONT_PATH, FONT_SIZE_LARGE, TEXT_COLOR, SOUNDS_FOLDER

def load_player_score():
    try:
        with open("player_results.data", "r") as file:
            return int(file.read().strip())
    except Exception as e:
        print(f"Error loading score: {e}")
        return 0

def show_end_screen(screen, clock, next_level, start_new_level_callback):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    screen.blit(overlay, (0, 0))
    button_click_sound = load_sound("button_click.wav")

    font = pygame.font.Font(FONT_PATH, FONT_SIZE_LARGE)
    text_surface = font.render("Уровень пройден!", True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text_surface, text_rect)

    instruction_text = "Нажмите N, чтобы перейти на следующий уровень" if next_level else "Нажмите любую клавишу, чтобы продолжить"
    instruction_surface = font.render(instruction_text, True, TEXT_COLOR)
    instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(instruction_surface, instruction_rect)

    score = load_player_score()
    score_surface = font.render(f"Очки: {score}", True, TEXT_COLOR)
    score_rect = score_surface.get_rect(topright=(SCREEN_WIDTH - 20, 20))
    screen.blit(score_surface, score_rect)

    score_collider = pygame.Rect(score_rect.x, score_rect.y, score_rect.width, score_rect.height)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if next_level and event.key == pygame.K_n:
                    waiting = False
                    start_new_level_callback()
                elif not next_level:
                    waiting = False
                if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_n]:
                    play_sound(button_click_sound)

def load_sound(file_name):
    sound_path = os.path.join(SOUNDS_FOLDER, file_name)
    if os.path.exists(sound_path):
        return pygame.mixer.Sound(sound_path)
    else:
        print(f"Warning: Sound file '{file_name}' not found in '{SOUNDS_FOLDER}'.")
        return None

def play_sound(sound):
    if sound:
        sound.play()