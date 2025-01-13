import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, FPS, TILE_SIZE, TEXTURE_FOLDER, LEVEL_FILE, FONT_PATH, FONT_SIZE, BACKGROUND_COLOR, PLAYER_TEXTURE
from tilemap import TileMap
from player import Player
from hud import HUD

def main():
    pygame.init()
    pygame.display.set_caption("Chicken Jump")  # Установка заголовка окна
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0)
    clock = pygame.time.Clock()  # Часы для ограничения FPS

    # Создание карты уровня
    tile_map = TileMap(LEVEL_FILE, TEXTURE_FOLDER, TILE_SIZE, screen)
    try:
        tile_map.set_font(FONT_PATH, FONT_SIZE)  # Установка пользовательского шрифта
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
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_w:
                        player.move(0, -1, tile_map)
                    elif event.key == pygame.K_s:
                        player.move(0, 1, tile_map)
                    elif event.key == pygame.K_a:
                        player.move(-1, 0, tile_map)
                    elif event.key == pygame.K_d:
                        player.move(1, 0, tile_map)

        # Вычисление смещения для камеры
        offset_x = (screen.get_width() - map_width) // 2 - player.x * TILE_SIZE + map_width // 2 - TILE_SIZE // 2
        offset_y = (screen.get_height() - map_height) // 2 - player.y * TILE_SIZE + map_height // 2 - TILE_SIZE // 2

        # Очистка экрана
        screen.fill(BACKGROUND_COLOR)

        # Отрисовка элементов
        tile_map.draw(offset_x, offset_y)
        player.draw(screen, offset_x, offset_y)
        hud.draw_hp(player.hp)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
