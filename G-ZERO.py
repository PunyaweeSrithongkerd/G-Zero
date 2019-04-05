import arcade
from models import World

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()

class Wall:
    def __init__(self):
        self.sprite = arcade.Sprite('images\wall.png')
    def draw(self,wall_list):
        for wall in wall_list:
            self.sprite.set_position(wall[0],wall[1])
            self.sprite.draw()
class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.hinu_sprite = ModelSprite('images/hinugundam.png',
                                       model=self.world.gundam)
        self.enemy_sprite = ModelSprite('images/enemy.png',
                                        model=self.world.enemy)
        self.hinu_sprite.set_position(300, 300)
        self.enemy_sprite.set_position(600, 600)
        self.wall = Wall()

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def update(self, delta):
        self.world.update(delta)

    def on_draw(self):
        arcade.start_render()
        self.hinu_sprite.draw()
        self.enemy_sprite.draw()
        self.wall.draw(self.world.interface.wall)
        

def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
