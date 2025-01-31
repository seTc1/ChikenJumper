import pygame
import os
from constants import FONT_PATH, BACKGROUND_COLOR, LEFT_ARROW_SPRITE, SOUNDS_FOLDER


class MainMenu:
    def __init__(self, screen, font_size=48, arrow_scale=0.35, text_space_size=80):
        self.screen = screen
        self.font = pygame.font.Font(FONT_PATH, font_size) if FONT_PATH else pygame.font.SysFont(None, font_size)
        self.menu_items = ["Начать игру", "Выход"]
        self.selected_index = 0
        self.bg_color = BACKGROUND_COLOR
        self.text_space_size = text_space_size
        self.text_color = (255, 255, 255)
        self.selected_color = (255, 0, 0)

        # Загрузка изображения стрелки и его масштабирование
        arrow_image = pygame.image.load(LEFT_ARROW_SPRITE)
        arrow_width = int(arrow_image.get_width() * arrow_scale)
        arrow_height = int(arrow_image.get_height() * arrow_scale)
        self.arrow_sprite = pygame.transform.scale(arrow_image, (arrow_width, arrow_height))
        self.button_click_sound = self.load_sound("button_click.wav")

    def load_sound(self, file_name):
        sound_path = os.path.join(SOUNDS_FOLDER, file_name)
        if os.path.exists(sound_path):
            return pygame.mixer.Sound(sound_path)
        else:
            print(f"Warning: Sound file '{file_name}' not found in '{SOUNDS_FOLDER}'.")
            return None

    def play_sound(self, sound):
        if sound:
            sound.play()

    def draw(self):
        self.screen.fill(self.bg_color)  # Заливка фона
        screen_width, screen_height = self.screen.get_size()

        for index, item in enumerate(self.menu_items):
            # Выбор цвета текста в зависимости от выбранного элемента
            color = self.selected_color if index == self.selected_index else self.text_color

            # Создание текстового объекта
            text_surface = self.font.render(item, True, color)
            text_rect = text_surface.get_rect(
                center=(screen_width // 2, screen_height // 2 + index * self.text_space_size))
            self.screen.blit(text_surface, text_rect)  # Отрисовка текста

            # Если элемент выбран, рисуем стрелку справа от текста
            if index == self.selected_index:
                arrow_rect = self.arrow_sprite.get_rect(midleft=(text_rect.right + 10, text_rect.centery))
                self.screen.blit(self.arrow_sprite, arrow_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.play_sound(self.button_click_sound)
            if event.key == pygame.K_w:  # Перемещение вверх по меню
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_s:  # Перемещение вниз по меню
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:  # Подтверждение выбора
                if self.menu_items[self.selected_index] == "Начать игру":
                    return "start_game"
                elif self.menu_items[self.selected_index] == "Выход":
                    return "exit"
        return None
