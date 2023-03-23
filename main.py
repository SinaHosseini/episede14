import random
import time
import arcade
from enemy import Enemy
from bullet import Bullet
from space_ship import Spaceship
from hearts import Hearts


class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=680, height=720, title="star's game")
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.background = arcade.load_texture(
            ":resources:images/backgrounds/stars.png")
        self.space_ship = Spaceship(self.width)
        self.enemies = []
        self.hearts = []
        self.score = 0
        self.hit_sound = arcade.load_sound(
            ":resources:sounds/hurt5.wav")
        self.game_over_bg = arcade.load_texture(
            "episode14\photo_2023-03-23_21-50-37.jpg")
        self.status = "normal"
        self.time = time.time()

        for i in range(3):
            heart = Hearts(i)
            self.hearts.append(heart)

    def on_draw(self):
        arcade.start_render()

        if self.status == "normal":
            arcade.draw_lrwh_rectangle_textured(
                0, 0, self.width, self.height, self.background)
            score_text = f"Score: {self.score}"
            arcade.draw_text(score_text, self.width - 120,
                             30, arcade.color.WHITE, 20)
            self.space_ship.draw()

            for enemy in self.enemies:
                enemy.draw()

            for bullet in self.space_ship.bullets:
                bullet.draw()

            for heart in self.hearts:
                heart.draw()

        elif self.status == "game over":
            arcade.draw_lrwh_rectangle_textured(
                0, 0, self.width, self.height, self.game_over_bg)

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
        self.space_ship.move()

        if time.time() > self.time + 3:
            self.enemy = Enemy(self)
            self.enemies.append(self.enemy)
            self.enemy.speed += 0.1
            self.time = time.time()

        for enemy in self.enemies:
            enemy.move()

            if arcade.check_for_collision(self.space_ship, enemy):
                self.status = "game over"
                self.on_draw()
                time.sleep(3)
                exit(0)

            if len(self.hearts) > 0:
                if enemy.center_y < 0:
                    self.enemies.remove(enemy)
                    self.hearts.pop()

            else:
                self.status = "game over"
                self.on_draw()
                time.sleep(3)
                exit(0)

        for bullet in self.space_ship.bullets:
            bullet.move()

        for enemy in self.enemies:
            for bullet in self.space_ship.bullets:
                if arcade.check_for_collision(enemy, bullet):
                    arcade.play_sound(self.hit_sound)
                    self.score += 1
                    self.enemies.remove(enemy)
                    self.space_ship.bullets.remove(bullet)

        for bullet in self.space_ship.bullets:
            if bullet.center_y > self.height:
                self.space_ship.bullets.remove(bullet)


window = Game()

arcade.run()
