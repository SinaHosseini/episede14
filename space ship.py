import random
import arcade


class Bullet(arcade.Sprite):
    def __init__(self, host):
        super().__init__(":resources:images/space_shooter/laserRed01.png")
        self.center_x = host.center_x
        self.center_y = host.center_y
        self.speed = 8
        self.change_x = 0
        self.change_y = 1

    def move(self):
        self.center_y += self.speed


class Spaceship(arcade.Sprite):
    def __init__(self, w):
        super().__init__(":resources:images/space_shooter/playerShip1_blue.png")
        self.center_x = w // 2
        self.center_y = 50
        self.change_x = 0
        self.change_y = 0
        self.width = 60
        self.height = 60
        self.speed = 5
        self.game_width = w
        self.bullets = []

    def move(self):
        if self.change_x == -1:
            if self.center_x > 0:
                self.center_x -= self.speed

        elif self.change_x == 1:
            if self.center_x < self.game_width:
                self.center_x += self.speed

    def fire(self):
        new_bullet = Bullet(self)
        self.bullets.append(new_bullet)


class Enemy(arcade.Sprite):
    def __init__(self, game):
        super().__init__(":resources:images/space_shooter/playerShip3_orange.png")
        self.center_x = random.randint(0, game.width)
        self.center_y = game.height + 30
        self.width = 60
        self.height = 60
        self.angle = 180
        self.speed = 4

    def move(self):
        self.center_y -= self.speed


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
            enemy.move()

        if random.randint(1, 80) == 6:
            self.enemy = Enemy(self)
            self.enemies.append(self.enemy)


window = Game()

arcade.run()
