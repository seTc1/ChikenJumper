import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, FPS, TILE_SIZE, TEXTURE_FOLDER, LEVEL_NAMES, FONT_PATH, \
    FONT_SIZE, BACKGROUND_COLOR, PLAYER_TEXTURE
from tilemap import TileMap
from player_controller import Player
from hud import HUD
from main_menu import MainMenu


# Функция инициализации экрана и часов игры
def initialize_screen():
    pygame.init()  # Инициализация Pygame
    pygame.display.set_caption("Chicken Jump")  # Установка заголовка окна
    # Создание экрана с указанными размерами, если FULLSCREEN включен — полноэкранный режим
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0)
    return screen, pygame.time.Clock()  # Возвращаем экран и объект часов для управления FPS


# Функция отображения главного меню
def display_main_menu(screen, clock):
    menu = MainMenu(screen)  # Создаем объект главного меню
    while True:
        for event in pygame.event.get():  # Обрабатываем события в игровом цикле
            if event.type == pygame.QUIT:  # Если нажали закрыть окно
                pygame.quit()
                return False

            action = menu.handle_event(event)  # Обработка события в меню
            if action == "start_game":  # Если выбрано начать игру
                return True
            elif action == "exit":  # Если выбрано выйти
                pygame.quit()
                return False

        menu.draw()  # Отрисовка меню
        pygame.display.flip()  # Обновление экрана
        clock.tick(FPS)  # Ограничение FPS


# Функция загрузки уровня
def load_level(screen):
    global curent_level_id
    print(LEVEL_NAMES[curent_level_id])  # Вывод имени уровня в консоль
    tile_map = TileMap(LEVEL_NAMES[curent_level_id], TEXTURE_FOLDER, TILE_SIZE,
                       screen)  # Создание карты уровня
    try:
        tile_map.set_font(FONT_PATH, FONT_SIZE)  # Установка шрифта для отображения текста на карте
    except FileNotFoundError as e:
        print(e)  # Вывод ошибки, если файл шрифта не найден

    # Проверяем, указаны ли начальная и конечная позиции игрока на карте
    if tile_map.start_pos is None or tile_map.end_pos is None:
        print("Ошибка: Начальная или конечная позиция не указаны в уровне.")
        return None, None, None  # Возвращаем пустые значения, если данных нет

    # Создаем объект игрока с текстурой и начальной позицией
    player = Player(os.path.join(TEXTURE_FOLDER, PLAYER_TEXTURE), tile_map.start_pos, TILE_SIZE)
    hud = HUD(screen)  # Создаем объект интерфейса (HUD)
    return tile_map, player, hud  # Возвращаем созданные объекты


# Функция отрисовки игры
def draw_game(screen, tile_map, player, hud, offset_x, offset_y):
    screen.fill(BACKGROUND_COLOR)  # Заливка экрана фоновым цветом
    tile_map.draw(offset_x, offset_y)  # Отрисовка карты с учетом смещения
    player.draw(screen, offset_x, offset_y)  # Отрисовка игрока
    hud.draw_hp(player.hp)  # Отображение здоровья игрока
    pygame.display.flip()  # Обновление экрана


def restart_level(screen):
    global curent_level_id
    print(curent_level_id)

    return load_level(screen)


def new_level(screen):
    global curent_level_id
    curent_level_id += 1
    return load_level(screen)  # Теперь возвращаем объекты, как в restart_level


curent_level_id = 0


# Главная функция игры
def main():
    screen, clock = initialize_screen()

    global curent_level_id  # Индекс текущего уровня
    if not display_main_menu(screen, clock):
        return

    tile_map, player, hud = load_level(screen)
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
                        case pygame.K_r:  # Перезапуск уровня при нажатии "R"
                            tile_map, player, hud = restart_level(screen)
                            if tile_map is None or player is None or hud is None:
                                return
                        case pygame.K_n:  # Допустим, кнопка "N" для загрузки нового уровня
                            tile_map, player, hud = new_level(screen)
                            if tile_map is None or player is None or hud is None:
                                return

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


# Запуск игры
if __name__ == "__main__":
    main()
