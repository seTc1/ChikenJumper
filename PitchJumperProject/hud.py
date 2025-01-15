import pygame
from constants import HEART_TEXTURE, HEART_SIZE, HP_TEXT_SIZE, FONT_PATH

class HUD:
    def __init__(self, screen):
        # Инициализация HUD
        self.screen = screen
        self.heart_image = pygame.image.load(HEART_TEXTURE).convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (HEART_SIZE, HEART_SIZE))
        self.font = pygame.font.Font(FONT_PATH, HP_TEXT_SIZE)

    def draw_hp(self, hp):
        # Отображение здоровья игрока
        screen_width = self.screen.get_width()
        heart_x = screen_width // 2 - HEART_SIZE - 10
        heart_y = 20
        text_x = screen_width // 2 + 10
        text_y = heart_y + (HEART_SIZE // 2)

        self.screen.blit(self.heart_image, (heart_x, heart_y))  # Рисование сердца
        hp_text = self.font.render(f"{hp}", True, (255, 255, 255))  # Рисование текста
        self.screen.blit(hp_text, hp_text.get_rect(midleft=(text_x, text_y)))