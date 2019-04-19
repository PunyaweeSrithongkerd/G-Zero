import arcade
from models import World

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40


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


class MazeDrawer():
    def __init__(self, maze):
        self.maze = maze
        self.width = self.maze.width
        self.height = self.maze.height

        self.wall_sprite = arcade.Sprite('images/wall.png')

    def get_sprite_position(self, r, c):
        x = c * BLOCK_SIZE + (BLOCK_SIZE // 2)
        y = r * BLOCK_SIZE + (BLOCK_SIZE + (BLOCK_SIZE // 2))
        return x,y

    def draw_sprite(self, sprite, r, c):
        x, y = self.get_sprite_position(r, c)
        sprite.set_position(x, y)
        sprite.draw()

    def draw(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.maze.has_wall_at(r, c):
                    self.draw_sprite(self.wall_sprite, r, c)


class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE)
        self.hinu_sprite = ModelSprite('images/hinugundam.png',
                                       model=self.world.gundam)
        self.enemy_sprite = ModelSprite('images/enemy.png',
                                        model=self.world.enemy)
        self.hinu_sprite.set_position(300, 300)
        self.enemy_sprite.set_position(600, 600)
        self.wall = MazeDrawer(self.world.interface)

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def update(self, delta):
        self.world.update(delta)

    def on_draw(self):
        arcade.start_render()
        self.world.beam_list.draw()
        self.enemy_sprite.draw()
        self.wall.draw()
        self.hinu_sprite.draw()



def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
