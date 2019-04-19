import arcade.key

MOVEMENT_SPEED = 4
DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4

DIR_OFFSETS = {DIR_STILL: (0, 0),
               DIR_UP: (0, 1),
               DIR_RIGHT: (1, 0),
               DIR_DOWN: (0, -1),
               DIR_LEFT: (-1, 0)}

KEY_MAP = {arcade.key.UP: DIR_UP,
           arcade.key.DOWN: DIR_DOWN,
           arcade.key.LEFT: DIR_LEFT,
           arcade.key.RIGHT: DIR_RIGHT}

BLOCK_SIZE = 40
BLOCK_CENTER = 20


class Gundam:
    def __init__(self, world, x, y, interface, block_size):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.interface = interface
        self.block_size = block_size
        self.next_direction = DIR_STILL

    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]

    def is_at_center(self):
        half_size = self.block_size // 2
        return (((self.x - half_size) % self.block_size == 0) and
                ((self.y - half_size) % self.block_size == 0))

    def get_row(self):
        return (self.y - self.block_size) // self.block_size

    def get_col(self):
        return self.x // self.block_size

    def check_walls(self, direction):
        new_r = self.get_row() + DIR_OFFSETS[direction][1]
        new_c = self.get_col() + DIR_OFFSETS[direction][0]
        return not self.interface.has_wall_at(new_r, new_c)

    def update(self, delta):
        # print(self.direction, self.x, self.y)
        if self.is_at_center():
            if self.check_walls(self.next_direction):
                self.direction = self.next_direction
            else:
                self.direction = DIR_STILL

        self.move(self.direction)


class Enemy:
    ENEMY_SPEED = 5

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

    def update(self, delta):
        self.x -= Enemy.ENEMY_SPEED
        if self.x < 0:
            self.x = self.world.width


class Interface:
    def __init__(self,world):
        self.map = ['####################',
                    '#..................#',
                    '#..................#',
                    '#..................#',
                    '#..................#',
                    '#..................#',
                    '#..................#',
                    '#..................#',
                    '#..................#',
                    '####################',
                    '#..................#',
                    '#..................#',
                    '#..................#',
                    '####################']
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.map.reverse()

    def has_wall_at(self, r, c):
        return self.map[r][c] == '#'

    def has_dot_at(self, r, c):
        return self.map[r][c] == '.'


class World:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.interface = Interface(self)
        self.block_size = block_size
        self.gundam = Gundam(self, width // 8, height // 2,
                             self.interface, self.block_size)
        self.enemy = Enemy(self, width - 200, height // 2)
        self.beam_list = arcade.SpriteList()

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.gundam.next_direction = KEY_MAP[key]
        if key == arcade.key.SPACE:
            beam = arcade.Sprite("images/Beam shot.png")
            beam_speed = 5
            beam.angle = 180
            beam.change_x = beam_speed
            beam.set_position(self.gundam.x + 92,
                              self.gundam.y)
            self.beam_list.append(beam)

    def update(self, delta):
        screen_width = 800
        self.beam_list.update()
        for beam in self.beam_list:
            if beam.left > screen_width:
                beam.kill()
        self.gundam.update(delta)
        self.enemy.update(delta)



