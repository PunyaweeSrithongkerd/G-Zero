import arcade
from models import World

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "G-ZERO"
BLOCK_SIZE = 40
TEXT_X = 80
TEXT_Y = 90
FONT_SIZE = 24
FONT_COLOUR = arcade.color.WHITE
INSTRUCTIONS_PAGE = 0
GAME_RUNNING = 1
GAME_OVER = 2

# All Hi-Nu Gundam sprite rip from Super Robot Taisen D and sprite sheet from http://srw-shrine.tripod.com/id9.html
# Enemy Sprite are rip from Super Robot Taisen J and sprite sheet from https://www.spriters-resource.com
# Beam sound from Star Wars and download from https://www.soundboard.com/sb/sound/918041
# Explosion sound from https://www.freesoundeffects.com
# Background image from https://acregames.files.wordpress.com/2013/03/space-bg2.png
# This Submit have some minor change to the game due a bug that found during presentation


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


class InterfaceDrawer:
    def __init__(self, interface):
        self.interface = interface
        self.width = self.interface.width
        self.height = self.interface.height

        self.wall_sprite = arcade.Sprite('images/wall.png')

    def get_sprite_position(self, r, c):
        x = c * BLOCK_SIZE + (BLOCK_SIZE // 2)
        y = r * BLOCK_SIZE + (BLOCK_SIZE + (BLOCK_SIZE // 2))
        return x, y

    def draw_sprite(self, sprite, r, c):
        x, y = self.get_sprite_position(r, c)
        sprite.set_position(x, y)
        sprite.draw()

    def draw(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.interface.has_wall_at(r, c):
                    self.draw_sprite(self.wall_sprite, r, c)


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE)
        self.hinu_sprite = ModelSprite('images/hinugundam.png',
                                       model=self.world.gundam)
        self.enemy_sprite1 = ModelSprite('images/enemy.png',
                                         model=self.world.enemy1)
        self.enemy_sprite2 = ModelSprite('images/enemy.png',
                                         model=self.world.enemy2)
        self.enemy_sprite3 = ModelSprite('images/enemy.png',
                                         model=self.world.enemy3)
        self.enemy_sprite4 = ModelSprite('images/enemy.png',
                                         model=self.world.enemy4)
        self.enemy_pack = [self.enemy_sprite1,
                           self.enemy_sprite2,
                           self.enemy_sprite3,
                           self.enemy_sprite4]
        self.wall = InterfaceDrawer(self.world.interface)
        self.background = arcade.Sprite('images/space_background.png')
        self.background.set_position(400, 300)
        self.instructions = []
        texture = arcade.load_texture("images/introduce_menu.png")
        self.instructions.append(texture)
        self.current_state = INSTRUCTIONS_PAGE

    def restart_game(self):
        self.world.score = 0
        self.world.life_point = 1000
        self.world.restart()
        self.current_state = GAME_RUNNING
        self.hinu_sprite = ModelSprite('images/hinugundam.png',
                                       model=self.world.gundam)

    def on_key_press(self, key, key_modifiers):
        if self.current_state == INSTRUCTIONS_PAGE and key == arcade.key.Z:
            self.current_state = GAME_RUNNING
            self.world.start()
        elif self.current_state == GAME_RUNNING:
            if not self.world.is_started():
                self.world.start()
            self.world.on_key_press(key, key_modifiers)
        elif self.current_state == GAME_OVER and key == arcade.key.R:
            self.restart_game()

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def draw_instructions_page(self, page_number):
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

    def draw_game_over(self):
        output_1 = "Game Over"
        arcade.draw_text(output_1, 240, 400, FONT_COLOUR, 54)

        output_2 = "Press R to restart"
        arcade.draw_text(output_2, 290, 350, FONT_COLOUR, FONT_SIZE)

        high_score = f'High Scores: {self.world.high_score}'
        arcade.draw_text(high_score, 290, 300, FONT_COLOUR, FONT_SIZE)

        total_score = f"Total scores: {self.world.score}"
        arcade.draw_text(total_score, 290, 270, FONT_COLOUR, FONT_SIZE)

    def draw_report(self):
        life = f"Life: {self.world.life_point}"
        score = f"Score: {self.world.score}"
        energy = f"Energy: {self.world.bullet}"
        high_score = f'High Score: {self.world.high_score}'

        arcade.draw_text(life, TEXT_X, TEXT_Y + 70, FONT_COLOUR, FONT_SIZE)
        arcade.draw_text(energy, TEXT_X, TEXT_Y, FONT_COLOUR, FONT_SIZE)
        arcade.draw_text(score, TEXT_X * 6, TEXT_Y, FONT_COLOUR, FONT_SIZE)
        arcade.draw_text(high_score, TEXT_X * 6, TEXT_Y + 70, FONT_COLOUR, FONT_SIZE)

    def draw_game(self):
        self.background.draw()
        self.world.beam_list.draw()
        for i in range(len(self.enemy_pack)):
            self.enemy_pack[i].draw()
        self.wall.draw()
        self.hinu_sprite.draw()
        self.draw_report()

    def update(self, delta):
        self.world.update(delta)
        if self.world.gundam.shoot is True:
            self.hinu_sprite = ModelSprite('images/hinugundam_shoot.png',
                                           model=self.world.gundam)
        else:
            self.hinu_sprite = ModelSprite('images/hinugundam.png',
                                           model=self.world.gundam)
        if self.world.life_point == 0:
            self.current_state = GAME_OVER
            self.hinu_sprite = ModelSprite('images/hinugundam.png',
                                           model=self.world.gundam)

    def on_draw(self):
        arcade.start_render()
        if self.current_state == INSTRUCTIONS_PAGE:
            self.draw_instructions_page(0)

        elif self.current_state == GAME_RUNNING:
            self.draw_game()
        else:
            self.draw_game()
            self.draw_game_over()


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
