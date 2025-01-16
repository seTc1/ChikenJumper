import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, FPS, TILE_SIZE, TEXTURE_FOLDER, LEVEL_NAMES, FONT_PATH, \
    FONT_SIZE, BACKGROUND_COLOR, PLAYER_TEXTURE
from tilemap import TileMap
from player_controller import Player
from hud import HUD
from main_menu import MainMenu


def initialize_screen():
    pygame.init()
    pygame.display.set_caption("Chicken Jump")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0)
    return screen, pygame.time.Clock()


def display_main_menu(screen, clock):
    menu = MainMenu(screen)
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
        clock.tick(FPS)


def load_level(level_id, screen):
    print(LEVEL_NAMES[level_id])
    tile_map = TileMap(LEVEL_NAMES[level_id], TEXTURE_FOLDER, TILE_SIZE, screen)
    try:
        tile_map.set_font(FONT_PATH, FONT_SIZE)
    except FileNotFoundError as e:
        print(e)

    if tile_map.start_pos is None or tile_map.end_pos is None:
        print("Ошибка: Начальная или конечная позиция не указаны в уровне.")
        return None, None, None

    player = Player(os.path.join(TEXTURE_FOLDER, PLAYER_TEXTURE), tile_map.start_pos, TILE_SIZE)
    hud = HUD(screen)
    return tile_map, player, hud

def draw_game(screen, tile_map, player, hud, offset_x, offset_y):
    screen.fill(BACKGROUND_COLOR)
    tile_map.draw(offset_x, offset_y)
    player.draw(screen, offset_x, offset_y)
    hud.draw_hp(player.hp)
    pygame.display.flip()


def main():
    screen, clock = initialize_screen()
    curent_level_id = 0
    if not display_main_menu(screen, clock):
        return

    tile_map, player, hud = load_level(curent_level_id, screen)
    if tile_map is None or player is None or hud is None:
        return

    map_width = len(tile_map.tiles[0]) * TILE_SIZE
    map_height = len(tile_map.tiles) * TILE_SIZE

    running = True
    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            running = False
                        case pygame.K_w:
                            player.move(0, -1, tile_map, screen)
                        case pygame.K_s:
                            player.move(0, 1, tile_map, screen)
                        case pygame.K_a:
                            player.move(-1, 0, tile_map, screen)
                        case pygame.K_d:
                            player.move(1, 0, tile_map, screen)

        offset_x = (screen.get_width() - map_width) // 2 - player.x * TILE_SIZE + map_width // 2 - TILE_SIZE // 2
        offset_y = (screen.get_height() - map_height) // 2 - player.y * TILE_SIZE + map_height // 2 - TILE_SIZE // 2


        draw_game(screen, tile_map, player, hud, offset_x, offset_y)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
