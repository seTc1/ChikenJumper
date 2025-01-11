import pygame
import sys
import os


class TileMap:
    def __init__(self, level_file, texture_folder, tile_size, screen):
        # Инициализация параметров карты тайлов
        self.level_file = level_file  # Файл уровня, содержащий макет тайлов
        self.texture_folder = texture_folder  # Папка с текстурами тайлов
        self.tile_size = tile_size  # Размер одного тайла
        self.screen = screen  # Экран для отрисовки
        self.textures = {}  # Словарь загруженных текстур
        self.tiles = []  # Список тайлов карты
        self.font = pygame.font.SysFont(None, 24)  # Шрифт по умолчанию для текста на клетках

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
        # Чтение файла уровня и заполнение списка тайлов
        with open(self.level_file, "r") as file:
            for line in file:
                self.tiles.append(line.strip().split())

    def set_font(self, font_path, size):
        # Установка пользовательского шрифта для текста
        if os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, size)
        else:
            raise FileNotFoundError(f"Файл шрифта {font_path} не найден.")

    def draw(self, offset_x, offset_y):
        # Отрисовка карты тайлов с учётом смещения
        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile_name in enumerate(row):
                if tile_name == "Null":  # Пропуск пустых тайлов
                    continue

                name, value = self.parse_tile_name(tile_name)  # Разделение имени и значения

                if name in self.textures:  # Отрисовка текстуры
                    x = col_idx * self.tile_size + offset_x
                    y = row_idx * self.tile_size + offset_y
                    self.screen.blit(self.textures[name], (x, y))

                if value is not None:  # Если значение есть, рисуем его поверх текстуры
                    if value > 0:
                        text_color = (0, 255, 0)
                        value = f"+{str(value)}"
                    elif value == 0:
                        text_color = (111, 111, 111)
                        value = f"+{str(value)}"
                    else:
                        text_color = (255, 0, 0)  # Цвет текста в зависимости от значения
                        value = f"-{str(value)[1:]}"

                    text_surface = self.font.render(str(value), True, text_color)
                    text_rect = text_surface.get_rect(center=(col_idx * self.tile_size + offset_x + self.tile_size // 2,
                                                              row_idx * self.tile_size + offset_y + self.tile_size // 2))
                    self.screen.blit(text_surface, text_rect)

    def parse_tile_name(self, tile_name):
        # Парсинг имени тайла и извлечение значения в скобках, если оно есть
        if "(" in tile_name and ")" in tile_name:
            name, value = tile_name.split("(")
            value = int(value.strip("()"))
            return name, value
        return tile_name, None


def main():
    pygame.init()
    pygame.display.set_caption("Chicken Jump")  # Заголовок окна
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    running = True
    FPS = 60
    clock = pygame.time.Clock()

    tile_size = 64  # Размер тайла в пикселях
    level_file = "testlevel.txt"  # Файл уровня
    texture_folder = "Textures"  # Папка с текстурами
    tile_map = TileMap(level_file, texture_folder, tile_size, screen)


    try:
        custom_font_path = "pixel.otf"
        custom_font_size = 24
        tile_map.set_font(custom_font_path, custom_font_size)
    except FileNotFoundError as e:
        print(e)  # Вывод ошибки, если файл шрифта не найден

    # Расчет смещения для центрирования карты
    map_width = len(tile_map.tiles[0]) * tile_size
    map_height = len(tile_map.tiles) * tile_size
    offset_x = (screen.get_width() - map_width) // 2
    offset_y = (screen.get_height() - map_height) // 2

    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False

        screen.fill((91, 145, 76))
        tile_map.draw(offset_x, offset_y)  # Отрисовка карты с учётом смещения

        clock.tick(FPS)  # Ограничение FPS
        pygame.display.flip()  # Обновление экрана
    pygame.quit()


if __name__ == "__main__":
    main()
