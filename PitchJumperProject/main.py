import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, FPS, TILE_SIZE, TEXTURE_FOLDER, LEVEL_FILE, FONT_PATH, \
    FONT_SIZE, BACKGROUND_COLOR, PLAYER_TEXTURE
from tilemap import TileMap
from player import Player
from hud import HUD
from main_menu import MainMenu


def main():
    pygame.init()
    pygame.display.set_caption("Chicken Jump")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0)
    clock = pygame.time.Clock()

    # Главное меню
    menu = MainMenu(screen)
    in_menu = True

    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            action = menu.handle_event(event)
            if action == "start_game":
                in_menu = False
            elif action == "exit":
                pygame.quit()
                return

        menu.draw()
        pygame.display.flip()
        clock.tick(FPS)

    # Создание карты уровня
    tile_map = TileMap(LEVEL_FILE, TEXTURE_FOLDER, TILE_SIZE, screen)
    try:
        tile_map.set_font(FONT_PATH, FONT_SIZE)
    except FileNotFoundError as e:
        print(e)

    if tile_map.start_pos is None or tile_map.end_pos is None:
        print("Ошибка: Начальная или конечная позиция не указаны в уровне.")
        return

    # Создание игрока
    player = Player(os.path.join(TEXTURE_FOLDER, PLAYER_TEXTURE), tile_map.start_pos, TILE_SIZE)

    # Создание интерфейса
    hud = HUD(screen)

    # Вычисление размеров карты
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
                            player.move(0, -1, tile_map)
                        case pygame.K_s:
                            player.move(0, 1, tile_map)
                        case pygame.K_a:
                            player.move(-1, 0, tile_map)
                        case pygame.K_d:
                            player.move(1, 0, tile_map)

        offset_x = (screen.get_width() - map_width) // 2 - player.x * TILE_SIZE + map_width // 2 - TILE_SIZE // 2
        offset_y = (screen.get_height() - map_height) // 2 - player.y * TILE_SIZE + map_height // 2 - TILE_SIZE // 2

        screen.fill(BACKGROUND_COLOR)

        tile_map.draw(offset_x, offset_y)
        player.draw(screen, offset_x, offset_y)
        hud.draw_hp(player.hp)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
