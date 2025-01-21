import pygame
import os
from constants import TILE_SIZE, PLAYER_TEXTURE, PASSABLE_TILES, FPS


class Player:
    def __init__(self, texture, position, tile_size):
        self.image = pygame.image.load(texture).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.x, self.y = position
        self.target_x, self.target_y = self.x, self.y
        self.tile_size = tile_size
        self.game_over = False
        self.hp = 10
        self.moving = False
        self.speed = TILE_SIZE / (FPS // 5)
        self.offset_x = 0
        self.offset_y = 0
        self.move_dx = 0
        self.move_dy = 0

    def draw(self, screen, offset_x, offset_y):
        if self.game_over: return
        screen.blit(self.image, ((self.x * self.tile_size + offset_x) + self.offset_x,
                                 (self.y * self.tile_size + offset_y) + self.offset_y))

    def move(self, dx, dy, tile_map, screen):
        from main import new_level
        if self.game_over or self.moving: return
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < len(tile_map.tiles[0]) and 0 <= new_y < len(tile_map.tiles):
            tile_name, tile_value = tile_map.parse_tile_name(tile_map.tiles[new_y][new_x])
            if tile_name in PASSABLE_TILES:
                self.target_x = new_x
                self.target_y = new_y
                self.moving = True
                self.move_dx = dx * self.speed
                self.move_dy = dy * self.speed
                if tile_map.check_if_end((new_x, new_y)):
                    new_level(screen)
                total_hp_change = -1
                if tile_value is not None:
                    total_hp_change += tile_value
                self.change_hp(total_hp_change)
                tile_map.clear_tile_value(new_x, new_y)

    def update(self):
        if self.moving:
            self.offset_x += self.move_dx
            self.offset_y += self.move_dy

            if abs(self.offset_x) >= TILE_SIZE or abs(self.offset_y) >= TILE_SIZE:
                self.x = self.target_x
                self.y = self.target_y
                self.offset_x = 0
                self.offset_y = 0
                self.moving = False

    def change_hp(self, amount):
        self.hp = max(0, self.hp + amount)
        if self.hp <= 0:
            self.game_over = True
