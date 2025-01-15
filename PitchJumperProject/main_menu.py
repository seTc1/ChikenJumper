import pygame


class MainMenu:
    def __init__(self, screen, font_path=None, font_size=48):
        self.screen = screen
        self.font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.SysFont(None, font_size)
        self.menu_items = ["Start Game", "Exit"]
        self.selected_index = 0
        self.bg_color = (0, 50, 0)
        self.text_color = (200, 200, 200)
        self.selected_color = (255, 0, 0)

    def draw(self):
        self.screen.fill(self.bg_color)
        screen_width, screen_height = self.screen.get_size()
        for index, item in enumerate(self.menu_items):
            color = self.selected_color if index == self.selected_index else self.text_color
            text_surface = self.font.render(item, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + index * 60))
            self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_s:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                if self.menu_items[self.selected_index] == "Start Game":
                    return "start_game"
                elif self.menu_items[self.selected_index] == "Exit":
                    return "exit"
        return None
