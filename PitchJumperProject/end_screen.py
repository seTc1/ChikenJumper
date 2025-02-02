import random

import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, OVERLAY_COLOR, FONT_PATH, FONT_SIZE_LARGE, TEXT_COLOR, SOUNDS_FOLDER, HEART_TEXTURE, HEART_SOUND, HEART_SIZE

def load_player_score():
    try:
        with open("player_results.data", "r") as file:
            return int(file.read().strip())
    except Exception as e:
        print(f"Error loading score: {e}")
        return 0

def save_player_score(score):
    try:
        with open("player_results.data", "w") as file:
            file.write(str(score))
    except Exception as e:
        print(f"Error saving score: {e}")

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


def show_end_screen(screen, clock, next_level, start_new_level_callback, draw_background_callback, player_hp):
    button_click_sound = load_sound("button_click.wav")
    heart_sound = load_sound(HEART_SOUND)
    font = pygame.font.Font(FONT_PATH, FONT_SIZE_LARGE)
    initial_score = load_player_score()
    target_score = initial_score + player_hp
    displayed_score = initial_score
    score_surface = font.render(f"Очки: {displayed_score}", True, TEXT_COLOR)
    score_rect = score_surface.get_rect(topright=(SCREEN_WIDTH - 20, 20))
    heart_image = pygame.image.load(HEART_TEXTURE).convert_alpha()
    heart_image = pygame.transform.scale(heart_image, (HEART_SIZE, HEART_SIZE))
    heart = None
    heart_speed = 55
    hearts_fired = 0
    waiting = True

    while waiting:
        draw_background_callback()
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(OVERLAY_COLOR)
        screen.blit(overlay, (0, 0))

        # Обновляем поверхности и rect для текста
        score_surface = font.render(f"Очки: {displayed_score}", True, TEXT_COLOR)
        score_rect = score_surface.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        screen.blit(score_surface, score_rect)

        title_surface = font.render("Уровень пройден!", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_surface, title_rect)

        if displayed_score == target_score:
            instruction_text = "Нажмите N, чтобы перейти на следующий уровень" if next_level else "Нажмите любую клавишу, чтобы продолжить"
            instruction_surface = font.render(instruction_text, True, TEXT_COLOR)
            instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(instruction_surface, instruction_rect)

        # Логика сердечек
        if hearts_fired < player_hp and heart is None:
            heart = {'pos': [SCREEN_WIDTH / 2, 55]}  # Точка появления сердечка
            hearts_fired += 1

        if heart is not None:
            # Двигаем сердечко к текущей позиции текста
            dest_pos = score_rect.center
            dx = dest_pos[0] - heart['pos'][0]
            dy = dest_pos[1] - heart['pos'][1]
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance > 0:
                heart['pos'][0] += heart_speed * dx / distance
                heart['pos'][1] += heart_speed * dy / distance

            # Создаем rect для сердечка и проверяем коллизию
            heart_rect = heart_image.get_rect(center=(int(heart['pos'][0]), int(heart['pos'][1])))

            if heart_rect.colliderect(score_rect):
                play_sound(heart_sound)
                displayed_score += 1
                heart = None
            else:
                screen.blit(heart_image, heart_rect)

        pygame.display.flip()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and displayed_score == target_score:
                if next_level and event.key == pygame.K_n:
                    play_sound(button_click_sound)
                    waiting = False
                    save_player_score(displayed_score)
                    start_new_level_callback()
                elif not next_level:
                    play_sound(button_click_sound)
                    waiting = False
                    save_player_score(displayed_score)

        clock.tick(60)