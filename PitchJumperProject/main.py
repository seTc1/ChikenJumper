import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, FPS, TILE_SIZE, TEXTURE_FOLDER, LEVEL_NAMES, FONT_PATH, \
    FONT_SIZE, BACKGROUND_COLOR, PLAYER_TEXTURE, VICTORY_TEXT, GAME_OVER_TEXT, OVERLAY_COLOR, FONT_SIZE_LARGE, TEXT_COLOR
from tilemap import TileMap
from player_controller import Player
from hud import HUD
from main_menu import MainMenu


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chicken Jump")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0, vsync=1)
        self.clock = pygame.time.Clock()
        self.current_level_id = 0
        self.running = True
        self.tile_map = None
        self.player = None
        self.hud = None
        self.camera_x = 0
        self.camera_y = 0

    def display_main_menu(self):
        menu = MainMenu(self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                action = menu.handle_event(event)
                if action == "start_game":
                    return True
                elif action == "exit":
                    pygame.quit()
                    return False
            menu.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    def show_end_screen(self, message):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(OVERLAY_COLOR)
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(FONT_PATH, FONT_SIZE_LARGE)
        text_surface = font.render(message, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def load_level(self):
        print(LEVEL_NAMES[self.current_level_id])
        self.tile_map = TileMap(LEVEL_NAMES[self.current_level_id], TEXTURE_FOLDER, TILE_SIZE, self.screen)
        try:
            self.tile_map.set_font(FONT_PATH, FONT_SIZE)
        except FileNotFoundError as e:
            print(e)

        if self.tile_map.start_pos is None or self.tile_map.end_pos is None:
            print("Ошибка: Начальная или конечная позиция не указаны в уровне.")
            return False

        self.player = Player(os.path.join(TEXTURE_FOLDER, PLAYER_TEXTURE), self.tile_map.start_pos, TILE_SIZE)
        self.hud = HUD(self.screen)
        self.camera_x = self.player.x * TILE_SIZE
        self.camera_y = self.player.y * TILE_SIZE
        return True

    def restart_level(self):
        return self.load_level()

    def next_level(self):
        self.current_level_id += 1
        if self.current_level_id >= len(LEVEL_NAMES):
            self.current_level_id = 0  # Возврат к первому уровню, если достигнут конец списка
        return self.load_level()

    def draw_game(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.camera_x += (self.player.x * TILE_SIZE + self.player.offset_x - self.camera_x) * 0.1
        self.camera_y += (self.player.y * TILE_SIZE + self.player.offset_y - self.camera_y) * 0.1
        offset_x = SCREEN_WIDTH // 2 - self.camera_x - TILE_SIZE // 2
        offset_y = SCREEN_HEIGHT // 2 - self.camera_y - TILE_SIZE // 2
        self.tile_map.draw(offset_x, offset_y)
        self.player.draw(self.screen, offset_x, offset_y)
        self.hud.draw_hp(self.player.hp)
        pygame.display.flip()

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r:
                        if not self.restart_level():
                            return
                    elif event.key == pygame.K_n:
                        if not self.next_level():
                            return
                    elif event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                        moves = {pygame.K_w: (0, -1), pygame.K_s: (0, 1), pygame.K_a: (-1, 0), pygame.K_d: (1, 0)}
                        self.player.move(*moves[event.key], self.tile_map, self.screen)

            self.player.update()
            if self.player.hp <= 0:
                self.show_end_screen(GAME_OVER_TEXT)
                self.restart_level()
                return

            if self.tile_map.check_if_end((self.player.x, self.player.y)):
                self.show_end_screen(VICTORY_TEXT)
                self.next_level()
                return

            self.draw_game()
            self.clock.tick(FPS)

    def run(self):
        if not self.display_main_menu():
            return
        if not self.load_level():
            return
        self.game_loop()


if __name__ == "__main__":
    Game().run()