import pygame
import sys
import os


class TileMap:
    def __init__(self, level_file, texture_folder, tile_size, screen):
        # Инициализация карты тайлов
        self.level_file = level_file
        self.texture_folder = texture_folder
        self.tile_size = tile_size
        self.screen = screen
        self.textures = {}  # Словарь для хранения загруженных текстур
        self.tiles = []  # Список строк уровня
        self.font = pygame.font.SysFont(None, 24)  # Шрифт для отображения текста на клетках

        self.start_pos = None  # Начальная позиция персонажа
        self.end_pos = None  # Конечная позиция уровня

        self.load_textures()  # Загрузка текстур
        self.load_level()  # Загрузка уровня

    def load_textures(self):
        # Загрузка всех текстур из указанной папки
        for texture_name in os.listdir(self.texture_folder):
            texture_path = os.path.join(self.texture_folder, texture_name)
            if os.path.isfile(texture_path):
                texture_surface = pygame.image.load(texture_path).convert_alpha()
                self.textures[os.path.splitext(texture_name)[0]] = pygame.transform.scale(
                    texture_surface, (self.tile_size, self.tile_size)
                )

    def load_level(self):
        # Загрузка уровня из файла и определение стартовой и конечной позиций
        with open(self.level_file, "r") as file:
            for row_idx, line in enumerate(file):
                row = []
                for col_idx, tile_name in enumerate(line.strip().split()):
                    if tile_name.startswith("start_"):
                        self.start_pos = (col_idx, row_idx)
                        row.append(tile_name[6:])
                    elif tile_name.startswith("end_"):
                        self.end_pos = (col_idx, row_idx)
                        row.append(tile_name[4:])
                    else:
                        row.append(tile_name)
                self.tiles.append(row)

    def set_font(self, font_path, size):
        # Установка пользовательского шрифта для отображения текста
        if os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, size)
        else:
            raise FileNotFoundError(f"Файл шрифта {font_path} не найден.")

    def draw(self, offset_x, offset_y):
        # Рисование карты уровня
        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile_name in enumerate(row):
                if tile_name == "Null":
                    continue

                name, value = self.parse_tile_name(tile_name)

                if name in self.textures:
                    x = col_idx * self.tile_size + offset_x
                    y = row_idx * self.tile_size + offset_y
                    self.screen.blit(self.textures[name], (x, y))

                if (col_idx, row_idx) == self.end_pos and "SeedsPack" in self.textures:
                    x = col_idx * self.tile_size + offset_x
                    y = row_idx * self.tile_size + offset_y
                    self.screen.blit(self.textures["SeedsPack"], (x, y))

                if value is not None:
                    # Определение цвета текста в зависимости от значения
                    if value > 0:
                        text_color = (0, 255, 0)
                        value = f"+{str(value)}"
                    elif value == 0:
                        text_color = (111, 111, 111)
                        value = f"+{str(value)}"
                    else:
                        text_color = (255, 0, 0)
                        value = f"-{str(value)[1:]}"

                    # Рисование текста на клетке
                    text_surface = self.font.render(str(value), True, text_color)
                    text_rect = text_surface.get_rect(center=(col_idx * self.tile_size + offset_x + self.tile_size // 2,
                                                              row_idx * self.tile_size + offset_y + self.tile_size // 2))
                    self.screen.blit(text_surface, text_rect)

    def parse_tile_name(self, tile_name):
        # Разделение имени тайла и значения, если оно есть
        if "(" in tile_name and ")" in tile_name:
            name, value = tile_name.split("(")
            value = int(value.strip("()"))
            return name, value
        return tile_name, None


class Player:
    def __init__(self, texture, position, tile_size):
        # Инициализация персонажа
        self.image = pygame.image.load(texture).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.x, self.y = position  # Позиция персонажа в координатах сетки
        self.tile_size = tile_size

    def draw(self, screen, offset_x, offset_y):
        # Рисование персонажа на экране
        screen.blit(self.image, (self.x * self.tile_size + offset_x, self.y * self.tile_size + offset_y))

    def move(self, dx, dy, tile_map):
        new_x = self.x + dx
        new_y = self.y + dy

        # Проверка границ карты
        if 0 <= new_x < len(tile_map.tiles[0]) and 0 <= new_y < len(tile_map.tiles):
            tile_name, _ = tile_map.parse_tile_name(tile_map.tiles[new_y][new_x])

            # Проверяем, является ли тайл проходимым
            if tile_name in ["PathTile1", "PathTile2", "PathTile3"]:  # Только дорожки
                self.x = new_x
                self.y = new_y


def main():
    pygame.init()
    pygame.display.set_caption("Chicken Jump")
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)  # Полноэкранный режим
    running = True
    FPS = 60
    clock = pygame.time.Clock()

    tile_size = 64
    level_file = "testlevel.txt"
    texture_folder = "Textures"
    tile_map = TileMap(level_file, texture_folder, tile_size, screen)

    try:
        custom_font_path = "pixel.otf"  # Путь к пользовательскому шрифту
        custom_font_size = 24  # Размер шрифта
        tile_map.set_font(custom_font_path, custom_font_size)
    except FileNotFoundError as e:
        print(e)

    if tile_map.start_pos is None or tile_map.end_pos is None:
        print("Ошибка: Начальная или конечная позиция не указаны в уровне.")
        return

    player = Player(os.path.join(texture_folder, "ChikenIdle.png"), tile_map.start_pos, tile_size)

    map_width = len(tile_map.tiles[0]) * tile_size
    map_height = len(tile_map.tiles) * tile_size

    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                case pygame.KEYDOWN:  # Обрабатываем только нажатие клавиш
                    if event.key == pygame.K_w:
                        player.move(0, -1, tile_map)
                    if event.key == pygame.K_s:
                        player.move(0, 1, tile_map)
                    if event.key == pygame.K_a:
                        player.move(-1, 0, tile_map)
                    if event.key == pygame.K_d:
                        player.move(1, 0, tile_map)

        # Вычисление смещения для центрирования камеры на персонаже
        offset_x = (screen.get_width() - map_width) // 2 - player.x * tile_size + map_width // 2 - tile_size // 2
        offset_y = (screen.get_height() - map_height) // 2 - player.y * tile_size + map_height // 2 - tile_size // 2

        # Очистка экрана и обновление кадра
        screen.fill((91, 145, 76))  # Цвет фона
        tile_map.draw(offset_x, offset_y)  # Рисование карты
        player.draw(screen, offset_x, offset_y)  # Рисование персонажа

        clock.tick(FPS)  # Ограничение FPS
        pygame.display.flip()  # Обновление экрана
    pygame.quit()


if __name__ == "__main__":
    main()
