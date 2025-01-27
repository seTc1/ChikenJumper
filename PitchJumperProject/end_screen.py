import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, OVERLAY_COLOR, FONT_PATH, FONT_SIZE_LARGE, TEXT_COLOR


def show_end_screen(screen, clock, next_level, start_new_level_callback):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font(FONT_PATH, FONT_SIZE_LARGE)
    text_surface = font.render("Уровень пройден!", True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text_surface, text_rect)

    instruction_text = "Нажмите N, чтобы перейти на следующий уровень" if next_level else "Нажмите любую клавишу, чтобы продолжить"
    instruction_surface = font.render(instruction_text, True, TEXT_COLOR)
    instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(instruction_surface, instruction_rect)

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
