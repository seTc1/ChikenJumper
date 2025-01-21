import pygame
import os
from constants import TILE_SIZE, PLAYER_TEXTURE, PASSABLE_TILES


class Player:
    def __init__(self, texture, position, tile_size):
        # Инициализация персонажа
        self.image = pygame.image.load(texture).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.x, self.y = position  # Позиция персонажа в координатах сетки
        self.tile_size = tile_size
        self.game_over = False
        self.hp = 10  # Здоровье игрока

    def draw(self, screen, offset_x, offset_y):
        # Рисование персонажа на экране
        if self.game_over: return
        screen.blit(self.image, (self.x * self.tile_size + offset_x, self.y * self.tile_size + offset_y))

    def move(self, dx, dy, tile_map, screen):
        from main import new_level  # Импорт здесь предотвращает циклический импорт
        if self.game_over: return
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < len(tile_map.tiles[0]) and 0 <= new_y < len(tile_map.tiles):
            tile_name, tile_value = tile_map.parse_tile_name(tile_map.tiles[new_y][new_x])
            if tile_name in PASSABLE_TILES:
                self.x = new_x
                self.y = new_y
                if tile_map.check_if_end((new_x, new_y)):
                    new_level(screen)
                total_hp_change = -1
                if tile_value is not None:
                    total_hp_change += tile_value
                self.change_hp(total_hp_change)
                tile_map.clear_tile_value(new_x, new_y)

    def change_hp(self, amount):
        # Изменение здоровья
        self.hp = max(0, self.hp + amount)
        if self.hp <= 0:
            self.game_over = True
