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

    def draw(self, screen, offset_x, offset_y):
        # Рисование персонажа на экране
        screen.blit(self.image, (self.x * self.tile_size + offset_x, self.y * self.tile_size + offset_y))

    def move(self, dx, dy, tile_map):
        # Перемещение персонажа
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < len(tile_map.tiles[0]) and 0 <= new_y < len(tile_map.tiles):  # Проверка границ карты
            tile_name, _ = tile_map.parse_tile_name(tile_map.tiles[new_y][new_x])
            if tile_name in PASSABLE_TILES:  # Проверяем, является ли тайл проходимым
                self.x = new_x
                self.y = new_y