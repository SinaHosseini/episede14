import random
import time
import arcade
from enemy import Enemy
from bullet import Bullet
from space_ship import Spaceship


class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=680, height=720, title="star's game")
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.background = arcade.load_texture(
            ":resources:images/backgrounds/stars.png")
        self.space_ship = Spaceship(self.width)
        self.enemies = []

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.width, self.height, self.background)

        self.space_ship.draw()

        for enemy in self.enemies:
            enemy.draw()

        for bullet in self.space_ship.bullets:
            bullet.draw()

        arcade.finish_render()

    def on_key_press(self, symbol, modifiers: int):
        if symbol == arcade.key.A:
            self.space_ship.change_x = -1

        elif symbol == arcade.key.D:
            self.space_ship.change_x = 1

        elif symbol == arcade.key.SPACE:
            self.space_ship.fire()

    def on_key_release(self, symbol, modifiers: int):
        self.space_ship.change_x = 0

    def on_update(self, delta_time):
        for enemy in self.enemies:
            if arcade.check_for_collision(self.space_ship, enemy):
                print("Game Over ☠️")
                exit(0)

        for bullet in self.space_ship.bullets:
            bullet.move()

        for enemy in self.enemies:
            for bullet in self.space_ship.bullets:
                if arcade.check_for_collision(enemy, bullet):
                    self.enemies.remove(enemy)
                    self.space_ship.bullets.remove(bullet)

        self.space_ship.move()

        for enemy in self.enemies:
            if enemy.center_y < 0:
                self.enemies.remove(enemy)

        for enemy in self.enemies:
            enemy.move()

        while time.sleep(3):
            self.enemy = Enemy(self)
            self.enemies.append(self.enemy)


window = Game()

arcade.run()
