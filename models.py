import arcade.key
from coldetect import check_player_hit, check_beam_hit
from random import randint

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
SCREEN_WIDTH = 800
ENEMY_START_X_POSITION = 750



class Gundam:
    def __init__(self, world, x, y, interface, block_size):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.interface = interface
        self.block_size = block_size
        self.next_direction = DIR_STILL
        self.move_speed = 8
        self.shoot = False

    def move(self, direction):
        self.x += self.move_speed * DIR_OFFSETS[direction][0]
        self.y += self.move_speed * DIR_OFFSETS[direction][1]

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
        if self.is_at_center():
            if self.check_walls(self.next_direction):
                self.direction = self.next_direction
            else:
                self.direction = DIR_STILL
        self.move(self.direction)


class Enemy:

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.hit = False
        self.enemy_speed = 6

    def update(self, delta):
        self.x -= self.enemy_speed
        if self.x < 0:
            self.x = self.world.width


class Interface:
    def __init__(self, world):
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


class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3

    def __init__(self, width, height, block_size):
        self.beam_hit = []
        self.width = width
        self.height = height
        self.state = World.STATE_FROZEN
        self.interface = Interface(self)
        self.block_size = block_size
        self.gundam = Gundam(self, width // 8, height // 2,
                             self.interface, self.block_size)
        self.enemy1 = Enemy(self, ENEMY_START_X_POSITION, randint(266, 360))
        self.enemy2 = Enemy(self, ENEMY_START_X_POSITION, randint(386, 480))
        self.enemy3 = Enemy(self, ENEMY_START_X_POSITION, randint(506, 534))
        self.enemy_list = [self.enemy1,
                           self.enemy2,
                           self.enemy3]
        self.score = 0
        self.life_point = 1000
        self.hit_list = []
        self.beam_list = arcade.SpriteList()
        self.beam_sound = arcade.sound.load_sound('sounds/beam_rifle_sound.wav')

    def start(self):
        self.state = World.STATE_STARTED

    def freeze(self):
        self.state = World.STATE_FROZEN

    def is_started(self):
        return self.state == World.STATE_STARTED

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.gundam.move_speed = 8
            self.gundam.next_direction = KEY_MAP[key]
        if key == arcade.key.Z and len(self.beam_list) != 3:
            arcade.sound.play_sound(self.beam_sound)
            beam = arcade.Sprite("images/Beam shot.png")
            beam_speed = 5
            beam.angle = 180
            beam.change_x = beam_speed
            beam.set_position(self.gundam.x + 92,
                              self.gundam.y)
            self.beam_list.append(beam)
            self.gundam.shoot = True
        else:
            self.gundam.shoot = False
            pass

    def on_key_release(self, key, modifiers):
        if key in KEY_MAP:
            self.gundam.move_speed = 0

    def is_hit(self):
        return [check_player_hit(self.gundam.x, self.enemy1.x,
                                 self.gundam.y, self.enemy1.y),
                check_player_hit(self.gundam.x, self.enemy2.x,
                                 self.gundam.y, self.enemy2.y),
                check_player_hit(self.gundam.x, self.enemy3.x,
                                 self.gundam.y, self.enemy3.y)]

    def die(self):
        self.state = World.STATE_DEAD

    def is_dead(self):
        return self.state == World.STATE_DEAD

    def score_update(self):
        self.score += 10

    def damage(self):
        self.life_point -= 100

    def respawn_enemy_1(self):
        self.enemy1.x = ENEMY_START_X_POSITION
        self.enemy1.y = randint(266, 360)

    def respawn_enemy_2(self):
        self.enemy2.x = ENEMY_START_X_POSITION
        self.enemy2.y = randint(386, 480)

    def respawn_enemy_3(self):
        self.enemy3.x = ENEMY_START_X_POSITION
        self.enemy3.y = randint(506, 534)

    def restart(self):
        self.respawn_enemy_1()
        self.respawn_enemy_2()
        self.respawn_enemy_3()
        self.gundam.x = 100
        self.gundam.y = 300
        self.beam_list = arcade.SpriteList()

    def difficult_change(self):
        if self.score < 100:
            for enemy in self.enemy_list:
                enemy.enemy_speed = 6
        if 100 <= self.score < 200:
            for enemy in self.enemy_list:
                enemy.enemy_speed = 8
        elif 200 <= self.score < 250:
            for enemy in self.enemy_list:
                enemy.enemy_speed = 10
        elif self.score > 300:
            for enemy in self.enemy_list:
                enemy.enemy_speed = 12

    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return

        self.gundam.update(delta)
        for enemy in self.enemy_list:
            enemy.update(delta)

        self.beam_list.update()
        for beam in self.beam_list:
            if beam.left > SCREEN_WIDTH - 40:
                beam.kill()
            if check_beam_hit(beam.center_x, self.enemy1.x,
                              beam.center_y, self.enemy1.y):
                beam.kill()
                self.respawn_enemy_1()
                self.score_update()
            elif check_beam_hit(beam.center_x, self.enemy2.x,
                                beam.center_y, self.enemy2.y):
                beam.kill()
                self.respawn_enemy_2()
                self.score_update()
            elif check_beam_hit(beam.center_x, self.enemy3.x,
                                beam.center_y, self.enemy3.y):
                beam.kill()
                self.respawn_enemy_3()
                self.score_update()

        self.difficult_change()

        if self.is_hit()[0]:
            self.respawn_enemy_1()
            self.damage()
        elif self.is_hit()[1]:
            self.respawn_enemy_2()
            self.damage()
        elif self.is_hit()[2]:
            self.respawn_enemy_3()
            self.damage()

        if self.life_point == 0:
            self.die()
