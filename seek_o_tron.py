from __future__ import division
import pyglet
import seek_lang

from game import game_state


class SeekOTron:
    BOARD_WIDTH = 3
    BOARD_HEIGHT = 3
    MAX_MOVES = 10

    def __init__(self):
        self.game_state = game_state.GameState(self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.window = pyglet.window.Window(resizable=True)
        self.arrow_input_enabled = False  # Are keyboard arrow inputs being accepted
        self.buffered_moves_made = 0  # The number of moves made from the current buffer
        self.buffered_moves = []  # The movements buffered for the robot
        self.processing_moves = False  # Is the game currently processing movement
        self.loot_image = pyglet.image.load('img/loot.png')
        self.robot_image = pyglet.image.load('img/robot.png')
        self.moving_banner_image = pyglet.image.load('img/moving_text.png')
        self.win_banner_image = pyglet.image.load('img/win_text.png')

        @self.window.event
        def on_draw():
            self.window.clear()
            self.draw_grid()
            self.draw_loot()
            self.draw_robot()
            if self.processing_moves:
                self.draw_moving_banner()
            if self.game_state.is_won():
                self.draw_win_banner()

        @self.window.event
        def on_key_press(symbol, modifiers):
            self.handle_keys(symbol)

    def update(self, dt):
        self.process_move()

    def handle_keys(self, symbol):
        if self.game_state.is_won():
            # If on win screen, start new game on any key
            self.game_state = game_state.GameState(self.BOARD_WIDTH, self.BOARD_HEIGHT)
        elif symbol == pyglet.window.key.Q:
            exit()
        elif self.processing_moves:
            # Don't accept keyboard input while processing movement
            return
        elif symbol == pyglet.window.key.SPACE:
            self.process_instructions()
        elif symbol == pyglet.window.key.K:
            self.arrow_input_enabled = not self.arrow_input_enabled
            if self.arrow_input_enabled:
                print("Hey, I'm now listening for arrow input")
            else:
                print("Hey, I'm no longer listening for arrow input")
        elif symbol == pyglet.window.key.D:
            print("Debug output follows...")
            print("Player location: " + str(self.game_state.player_position))
            print("Loot location: " + str(self.game_state.loot_position))
        elif self.arrow_input_enabled:
            if symbol == pyglet.window.key.RIGHT:
                self.game_state.move_right()
            elif symbol == pyglet.window.key.LEFT:
                self.game_state.move_left()
            elif symbol == pyglet.window.key.UP:
                self.game_state.move_up()
            elif symbol == pyglet.window.key.DOWN:
                self.game_state.move_down()

    def process_instructions(self):
        moves = seek_lang.driver.evaluate_seek_lang(self.game_state.player_position, self.game_state.loot_position)
        self.buffered_moves_made = 0
        if not moves:  # fail if unable to parse
            self.buffered_moves = []
        else:
            self.processing_moves = True
            self.buffered_moves = moves

    def draw_grid(self):
        # Draw horizontal lines
        for row in range(1, self.game_state.height):
            y = (self.window.get_size()[1] // self.game_state.height) * row
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                 ('v2i', (0, y, self.window.get_size()[0], y)),
                                 ('c3B', (255, 255, 255, 255, 255, 255))
                                 )

        # Draw vertical lines
        for col in range(1, self.game_state.width):
            x = (self.window.get_size()[0] // self.game_state.width) * col
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                 ('v2i', (x, 0, x, self.window.get_size()[1])),
                                 ('c3B', (255, 255, 255, 255, 255, 255))
                                 )

    def get_tile_size(self):
        return (self.window.get_size()[0] // self.game_state.width,
                self.window.get_size()[1] // self.game_state.height)

    def get_tile_aspect_ratio(self):
        tile_size = self.get_tile_size()
        return tile_size[0] / tile_size[1]

    def draw_robot(self):
        sprite = pyglet.sprite.Sprite(self.robot_image)
        self.scale_sprite_to_tile(sprite)
        # Position sprite
        tile_size = self.get_tile_size()
        robot_square_x, robot_square_y = self.game_state.player_position
        sprite_horizontal_buffer = (tile_size[0] - sprite.width) // 2
        sprite.x = robot_square_x * tile_size[0] + sprite_horizontal_buffer
        sprite_vertical_buffer = (tile_size[1] - sprite.height) // 2
        sprite.y = robot_square_y * tile_size[1] + sprite_vertical_buffer
        # Draw it
        sprite.draw()

    def draw_loot(self):
        sprite = pyglet.sprite.Sprite(self.loot_image)
        self.scale_sprite_to_tile(sprite)
        # Position sprite
        tile_size = self.get_tile_size()
        loot_square_x, loot_square_y = self.game_state.loot_position
        sprite_horizontal_buffer = (tile_size[0] - sprite.width) // 2
        sprite.x = loot_square_x * tile_size[0] + sprite_horizontal_buffer
        sprite_vertical_buffer = (tile_size[1] - sprite.height) // 2
        sprite.y = loot_square_y * tile_size[1] + sprite_vertical_buffer
        # Draw it
        sprite.draw()

    def draw_moving_banner(self):
        sprite = pyglet.sprite.Sprite(self.moving_banner_image)
        self.scale_sprite_to_window(sprite)
        # Position sprite
        sprite_horizontal_buffer = (self.window.get_size()[0] - sprite.width) // 2
        sprite.x = sprite_horizontal_buffer
        sprite_vertical_buffer = (self.window.get_size()[1] - sprite.height) // 2
        sprite.y = sprite_vertical_buffer
        # Draw it
        sprite.draw()

    def draw_win_banner(self):
        sprite = pyglet.sprite.Sprite(self.win_banner_image)
        self.scale_sprite_to_window(sprite)
        # Position sprite
        sprite_horizontal_buffer = (self.window.get_size()[0] - sprite.width) // 2
        sprite.x = sprite_horizontal_buffer
        sprite_vertical_buffer = (self.window.get_size()[1] - sprite.height) // 2
        sprite.y = sprite_vertical_buffer
        # Draw it
        sprite.draw()

    def process_move(self):
        if len(self.buffered_moves) == 0:
            self.processing_moves = False
            return
        move = self.buffered_moves.pop(0)
        if move == "right":
            self.game_state.move_right()
        elif move == "left":
            self.game_state.move_left()
        elif move == "up":
            self.game_state.move_up()
        elif move == "down":
            self.game_state.move_down()
        self.buffered_moves_made += 1
        if self.game_state.is_won():
            self.stop_processing_moves()
        elif self.buffered_moves_made > self.MAX_MOVES:
            print("Max moves (" + str(self.MAX_MOVES) + ") reached, stopping!")
            self.stop_processing_moves()

    def scale_sprite_to_tile(self, sprite):
        sprite_aspect_ratio = sprite.width / sprite.height
        tile_size = self.get_tile_size()
        tile_aspect = self.get_tile_aspect_ratio()
        if tile_aspect > sprite_aspect_ratio:  # tiles are relatively wider, scale based on tile height
            scaling_coeff = tile_size[1] / sprite.height
        else:  # tiles are relatively taller, scale based on tile width
            scaling_coeff = tile_size[0] / sprite.width
        sprite.scale = scaling_coeff - 0.01  # scale just a little smaller so image always fits

    def scale_sprite_to_window(self, sprite):
        sprite_aspect_ratio = sprite.width / sprite.height
        window_aspect = self.window.get_size()[0] / self.window.get_size()[1]
        if window_aspect > sprite_aspect_ratio:  # window is relatively wider, scale based on window height
            scaling_coeff = self.window.get_size()[1] / sprite.height
        else:  # window is relatively taller, scale based on window width
            scaling_coeff = self.window.get_size()[0] / sprite.width
        sprite.scale = scaling_coeff - 0.01  # scale just a little smaller so image always fits

    def stop_processing_moves(self):
        self.buffered_moves = []
        self.processing_moves = False

    def game_loop(self):
        pyglet.clock.schedule_interval(self.update, 0.3)
        pyglet.app.run()


if __name__ == "__main__":
    game = SeekOTron()
    game.game_loop()
