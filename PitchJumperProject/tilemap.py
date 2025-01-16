import os
import pygame

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
                        self.start_pos = (col_idx, row_idx)  # Установка стартовой позиции
                        row.append(tile_name[6:])
                    elif tile_name.startswith("end_"):
                        self.end_pos = (col_idx, row_idx)  # Установка конечной позиции
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
                if tile_name == "Null":  # Пропускаем пустые клетки
                    continue
                name, value = self.parse_tile_name(tile_name)
                if name in self.textures:  # Рисование текстуры клетки
                    x = col_idx * self.tile_size + offset_x
                    y = row_idx * self.tile_size + offset_y
                    self.screen.blit(self.textures[name], (x, y))
                if (col_idx, row_idx) == self.end_pos and "SeedsPack" in self.textures:
                    # Рисование текстуры конечной позиции
                    x = col_idx * self.tile_size + offset_x
                    y = row_idx * self.tile_size + offset_y
                    self.screen.blit(self.textures["SeedsPack"], (x, y))
                if value is not None:  # Рисование текста на клетке
                    text_color = (0, 255, 0) if value > 0 else (111, 111, 111) if value == 0 else (255, 0, 0)
                    value = f"+{str(value)}" if value >= 0 else f"-{str(value)[1:]}"
                    text_surface = self.font.render(str(value), True, text_color)
                    text_rect = text_surface.get_rect(center=(
                        col_idx * self.tile_size + offset_x + self.tile_size // 2,
                        row_idx * self.tile_size + offset_y + self.tile_size // 2
                    ))
                    self.screen.blit(text_surface, text_rect)

    def clear_tile_value(self, x, y):
        tile_name, _ = self.parse_tile_name(self.tiles[y][x])
        self.tiles[y][x] = tile_name  # Сбрасываем значение клетки, оставляя только её имя

    def parse_tile_name(self, tile_name):
        # Разделение имени тайла и значения, если оно есть
        if "(" in tile_name and ")" in tile_name:
            name, value = tile_name.split("(")
            value = int(value.strip("()"))
            return name, value
        return tile_name, None

    def check_if_end(self, check_pos):
        if self.end_pos == check_pos:
            return True
        else:
            return False
