import arcade


class Hearts(arcade.Sprite):
    def __init__(self, x):
        super().__init__("episode14\photo_2023-03-23_21-28-40.jpg")
        self.center_x = x*20 +20
        self.center_y = 40
        self.width = 15
        self.height = 15