import random
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
 
# directory = os.path.join(os.path.dirname(__file__), 'assets')
 
# print(directory)
pygame.init()
pygame.font.init()

crash_sound = pygame.mixer.Sound('assets/gameover.wav')
clear_sound = pygame.mixer.Sound('assets/clear.wav')
key_press = pygame.mixer.Sound('assets/key_press.wav')
image = pygame.image.load('assets/Blockbusters.png')
 

__pdoc__ = {}
__pdoc__['Piece'] = False
 
# class to represent each of the pieces
class Piece(object):
    def __init__(self, x, y, shape, shape_colors, shapes):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]  # choose color from the shape_color list
        self.rotation = 0                               # chooses the rotation according to index
 
class TetrisEngine(object):
 
    #################################################
    # DOCUMENTATION CONTROL
    ## CLASS VARIABLES
    __pdoc__['TetrisEngine.s_width'] = False
    __pdoc__['TetrisEngine.s_height'] = False
    __pdoc__['TetrisEngine.col'] = False
    __pdoc__['TetrisEngine.row'] = False
    __pdoc__['TetrisEngine.block_size'] = False
    __pdoc__['TetrisEngine.play_width'] = False
    __pdoc__['TetrisEngine.play_height'] = False
    __pdoc__['TetrisEngine.top_left_x'] = False
    __pdoc__['TetrisEngine.top_left_y'] = False
    __pdoc__['TetrisEngine.filepath'] = False
    __pdoc__['TetrisEngine.fontpath'] = False
    __pdoc__['TetrisEngine.fontpath_mario'] = False
    __pdoc__['TetrisEngine.viz_next_piece'] = False
    __pdoc__['TetrisEngine.viz_high_score'] = False
    __pdoc__['TetrisEngine.clock'] = False
    __pdoc__['TetrisEngine.fall_time'] = False
    __pdoc__['TetrisEngine.fall_speed'] = False
    __pdoc__['TetrisEngine.level_time'] = False
    __pdoc__['TetrisEngine.level'] = False
    __pdoc__['TetrisEngine.level_speeds'] = False
    __pdoc__['TetrisEngine.increase_difficulty'] = False
    __pdoc__['TetrisEngine.show_shadow'] = False
    __pdoc__['TetrisEngine.hard_drop'] = False
    __pdoc__['TetrisEngine.game_heading'] = False
    __pdoc__['TetrisEngine.quit_text'] = False
    __pdoc__['TetrisEngine.resume_text'] = False
    __pdoc__['TetrisEngine.restart_text'] = False
    __pdoc__['TetrisEngine.gameover_text'] = False
    __pdoc__['TetrisEngine.nextshape_text'] = False
    __pdoc__['TetrisEngine.level1_text'] = False
    __pdoc__['TetrisEngine.level2_text'] = False
    __pdoc__['TetrisEngine.level3_text'] = False
    __pdoc__['TetrisEngine.start_text'] = False
    __pdoc__['TetrisEngine.game_heading_color'] = False
    __pdoc__['TetrisEngine.gameover_color'] = False
    __pdoc__['TetrisEngine.general_button_color'] = False
    __pdoc__['TetrisEngine.click_color'] = False
    __pdoc__['TetrisEngine.playbndry_color'] = False
    __pdoc__['TetrisEngine.grid_color'] = False
    __pdoc__['TetrisEngine.S'] = False
    __pdoc__['TetrisEngine.Z'] = False
    __pdoc__['TetrisEngine.I'] = False
    __pdoc__['TetrisEngine.O'] = False
    __pdoc__['TetrisEngine.J'] = False
    __pdoc__['TetrisEngine.L'] = False
    __pdoc__['TetrisEngine.T'] = False
    __pdoc__['TetrisEngine.shapes'] = False
    __pdoc__['TetrisEngine.shape_colors'] = False
    __pdoc__['TetrisEngine.Dict'] = False
    __pdoc__['TetrisEngine.arrow'] = False

    ## CLASS FUNCTIONS
    __pdoc__['TetrisEngine.create_grid'] = False
    __pdoc__['TetrisEngine.convert_shape_format'] = False
    __pdoc__['TetrisEngine.valid_space'] = False
    __pdoc__['TetrisEngine.get_shape'] = False
    __pdoc__['TetrisEngine.draw_text_middle'] = False
    __pdoc__['TetrisEngine.draw_grid'] = False
    __pdoc__['TetrisEngine.draw_next_shape'] = False
    __pdoc__['TetrisEngine.draw_window'] = False
    __pdoc__['TetrisEngine.get_max_score'] = False
    __pdoc__['TetrisEngine.get_hard_position'] = False
    __pdoc__['TetrisEngine.get_ghost_position'] = False
    ######################################################
    
    # GAME VARIABLES 
    
    s_width = 800       # window width
    s_height = 750      # window height
    
    col = 10            
    row = 20            
    block_size = 30     # size of block
 
    play_width = col*block_size    # play window width
    play_height = row*block_size   # play window height
 
    top_left_x = (s_width - play_width) // 2
    top_left_y = s_height - play_height
 
    filepath = 'assets/highscore.txt'
    fontpath = 'assets/arcade.ttf'
    fontpath_mario = 'assets/russian-tetris.ttf'
    arrow = 'assets/arrows.ttf'
 
    viz_next_piece = True
    viz_high_score = True
 
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35
    level_time = 0
 
    level = 0
    level_speeds = [0.35, 0.25, 0.15]
    increase_difficulty = True
    show_shadow = True
    hard_drop = True
 
    game_heading = 'T E T R I S'
    quit_text = 'QUIT'
    resume_text = 'RESUME'
    restart_text = 'RESTART'
    gameover_text = 'GAMEOVER'
    nextshape_text = 'NEXT SHAPE'
    level1_text = 'LEVEL 1'
    level2_text = 'LEVEL 2'
    level3_text = 'LEVEL 3'
    start_text = 'START'
    game_heading_color = (230,230,0)
    gameover_color = (255, 200, 230)
    general_button_color = (255,255,255)
    click_color = (255,255,0)
 
    playbndry_color = (255,255,255)
    grid_color = 120
 
    S = [['.....',
        '.....',
        '..00.',
        '.00..',
        '.....'],
        ['.....',
        '..0..',
        '..00.',
        '...0.',
        '.....']]
 
    Z = [['.....',
        '.....',
        '.00..',
        '..00.',
        '.....'],
        ['.....',
        '..0..',
        '.00..',
        '.0...',
        '.....']]
 
    I = [['.....',
        '..0..',
        '..0..',
        '..0..',
        '..0..'],
        ['.....',
        '0000.',
        '.....',
        '.....',
        '.....']]
 
    O = [['.....',
        '.....',
        '.00..',
        '.00..',
        '.....']]
 
    J = [['.....',
        '.0...',
        '.000.',
        '.....',
        '.....'],
        ['.....',
        '..00.',
        '..0..',
        '..0..',
        '.....'],
        ['.....',
        '.....',
        '.000.',
        '...0.',
        '.....'],
        ['.....',
        '..0..',
        '..0..',
        '.00..',
        '.....']]
 
    L = [['.....',
        '...0.',
        '.000.',
        '.....',
        '.....'],
        ['.....',
        '..0..',
        '..0..',
        '..00.',
        '.....'],
        ['.....',
        '.....',
        '.000.',
        '.0...',
        '.....'],
        ['.....',
        '.00..',
        '..0..',
        '..0..',
        '.....']]
 
    T = [['.....',
        '..0..',
        '.000.',
        '.....',
        '.....'],
        ['.....',
        '..0..',
        '..00.',
        '..0..',
        '.....'],
        ['.....',
        '.....',
        '.000.',
        '..0..',
        '.....'],
        ['.....',
        '..0..',
        '.00..',
        '..0..',
        '.....']]
 
    shapes = [S, Z, I, O, J, L, T]
    shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
    Dict = {'S': 0, 'Z': 1, 'I': 2, 'O': 3, 'J': 4, 'L': 5, 'T': 6}
    
    def __init__(self):
        self.window = pygame.display.set_mode((self.s_width, self.s_height))    
        pygame.display.set_caption('Tetris')
        self.max_score = self.get_max_score()
    
    # INITIALIZE THE GRID
    def create_grid(self):
        grid = [[(0, 0, 0) for x in range(self.col)] for y in range(self.row)]  # grid represented rgb tuples
 
        # locked_positions dictionary
        # (x,y):(r,g,b)
        for y in range(self.row):
            for x in range(self.col):
                if (x, y) in self.locked_positions:
                    color = self.locked_positions[
                        (x, y)]  # get the value color (r,g,b) from the locked_positions dictionary using key (x,y)
                    grid[y][x] = color  # set grid position to color
        return grid
    
    # GET THE 0 . 2D FORMAT
    def convert_shape_format(self, piece):
        positions = []
        shape_format = piece.shape[piece.rotation % len(piece.shape)]  # get the desired rotated shape from piece
 
        # e.g.
        # ['.....',
        #     '.....',
        #     '..00.',
        #     '.00..',
        #     '.....']
        
        for i, line in enumerate(shape_format):  # i gives index; line gives string
            row = list(line)  # makes a list of char from string
            for j, column in enumerate(row):  # j gives index of char; column gives char
                if column == '0':
                    positions.append((piece.x + j, piece.y + i))
 
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)  # offset according to the input given with dot and zero
 
        return positions
 
 
    # CHECK IF CURRENT POSITION OF GRID IS VALID
    def valid_space(self, piece):
        # makes a 2D list of all the possible (x,y)
        accepted_pos = [[(x, y) for x in range(self.col) if self.grid[y][x] == (0, 0, 0)] for y in range(self.row)]
        # removes sub lists and puts (x,y) in one list; easier to search
        accepted_pos = [x for item in accepted_pos for x in item]
 
        formatted_shape = self.convert_shape_format(piece)
 
        for pos in formatted_shape:
            if pos not in accepted_pos:
                if pos[1] >= 0:
                    return False
        return True
 
 
    # CHOOSE A SHAPE RANDOMLY
    def get_shape(self):
        return Piece(int(self.col/2), 0, random.choice(self.shapes), self.shape_colors, self.shapes)
 
 
    # DRAW TEXT IN MIDDLE
    def draw_text_middle(self,text,surface, c, y):
        font = pygame.font.Font(self.fontpath, 50)
        label = font.render(text, 1, c)
        surface.blit(label, ((self.s_width - label.get_width())//2, y))
        return (self.s_width - label.get_width())//2
 
 
    # DRAW THE PLAY AREA GRID
    def draw_grid(self, surface):
        r = g = b = self.grid_color
        grid_color = (r, g, b)
 
        for i in range(self.row):
            # draw grey horizontal lines
            pygame.draw.line(surface, grid_color, (self.top_left_x, self.top_left_y + i * self.block_size),
                            (self.top_left_x + self.play_width, self.top_left_y + i * self.block_size))
            for j in range(self.col):
                # draw grey vertical lines
                pygame.draw.line(surface, grid_color, (self.top_left_x + j * self.block_size, self.top_left_y),
                                (self.top_left_x + j * self.block_size, self.top_left_y + self.play_height))
 
 
    # DRAW THE UPCOMING PIECE
    def draw_next_shape(self, piece, surface):
        font = pygame.font.Font(self.fontpath, 30)
        label = font.render(self.nextshape_text, 1, self.general_button_color)
 
        start_x = 600
        start_y = 300
 
        shape_format = piece.shape[piece.rotation % len(piece.shape)]
 
        for i, line in enumerate(shape_format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, piece.color, (start_x + j*self.block_size, start_y + i*self.block_size, self.block_size, self.block_size), 0)
 
        surface.blit(label, (start_x, start_y - 30))
 
 
    # DRAW THE WINDOW CONTENT
    def draw_window(self, surface, grid, score=0):
        surface.fill((0, 0, 0))  # fill the surface with black

        font = pygame.font.Font(self.fontpath, 30)
        font2 = pygame.font.Font(self.arrow, 20)
        label1 = font.render("CONTROLS", 1, (255,255,255))
        label3 = font.render("RIGHT   LEFT   ROTATE   DOWN   HARD DROP", 1, (255,255,255))
        label2 = font2.render("e       a       c       g               ", 1, (255,255,255))
        label4 = font.render("d",1,(255,255,255))
        surface.blit(label1, ((self.s_width - label1.get_width())//2, 10))
        surface.blit(label2, ((self.s_width - label2.get_width())//2, 90))
        surface.blit(label3, ((self.s_width - label3.get_width())//2, 50))
        surface.blit(label4, (580, 90))

        # current score
        font = pygame.font.Font(self.fontpath, 30)
        label = font.render('SCORE   ' + str(score) , 1, self.general_button_color)
 
        start_x = 600
        start_y = 500
 
        surface.blit(label, (start_x, start_y))
 
        if self.viz_high_score:
            # last score
            label_hi = font.render('HIGHSCORE   ' + str(self.max_score), 1, self.general_button_color)
 
            start_x_hi = 30
            start_y_hi = 500
 
            surface.blit(label_hi, (start_x_hi, start_y_hi))
 
        # draw content of the grid
        for i in range(self.row):
            for j in range(self.col):
                # pygame.draw.rect()
                # draw a rectangle shape
                # rect(Surface, color, Rect, width=0) -> Rect
                pygame.draw.rect(surface, grid[i][j],
                                (self.top_left_x + j * self.block_size, self.top_left_y + i * self.block_size, self.block_size, self.block_size), 0)
 
        # draw vertical and horizontal grid lines
        self.draw_grid(surface)
 
        # draw rectangular border around play area
        border_color = self.playbndry_color
        pygame.draw.rect(surface, border_color, (self.top_left_x, self.top_left_y, self.play_width, self.play_height), 4)
 
 
    # GET HIGH SCORE FROM FILE
    def get_max_score(self):
        with open(self.filepath, 'r') as file:
            lines = file.readlines()        # reads all the lines and puts in a list
            score = int(lines[0].strip())   # remove \n
 
        return score
    
    def get_hard_position(self):
        while(self.valid_space(self.current_piece)):
            self.current_piece.y += 1

        self.current_piece.y -= 1

    def get_ghost_position(self):
        while(self.valid_space(self.ghost_piece)):
            self.ghost_piece.y += 1

        self.ghost_piece.y -= 1

    def check_lost(self):
        """
        Check if game is lost or not based on the losing condition, default losing condition is that the piece is out of grid bounds
    
        Returns:
            bool : True if game is lost, False if game is not yet lost
    
        """
        for pos in self.locked_positions:
            x, y = pos
            if y < 1:
                return True
        return False
 
 
    def update_highscore(self, new_score):
        """
        Update high score if required
    
        Args:
            new_score (int): New highscore
    
        """
        score = self.get_max_score()
 
        with open(self.filepath, 'w') as file:
            if new_score > score:
                file.write(str(new_score))
                self.max_score = new_score
            else:
                file.write(str(score))
 
    def clear_rows(self):
        """
        Clear rows if required. Also update score and locked positions based on that
    
        """
        
        # need to check if row is clear then shift every other row above down one
        increment = 0
        for i in range(len(self.grid) - 1, -1, -1):      # start checking the grid backwards
            grid_row = self.grid[i]                      # get the last row
            if (0, 0, 0) not in grid_row:           # if there are no empty spaces (i.e. black blocks)
                increment += 1
                # add positions to remove from locked
                index = i                           # row index will be constant
                for j in range(len(grid_row)):
                    try:
                        del self.locked_positions[(j, i)]          # delete every locked element in the bottom row
                    except ValueError:
                        continue
 
        # shift every row one step down
        # delete filled bottom row
        # add another empty row on the top
        # move down one step
        if increment > 0:
            pygame.mixer.Sound.play(clear_sound)
            # sort the locked list according to y value in (x,y) and then reverse
            # reversed because otherwise the ones on the top will overwrite the lower ones
            for key in sorted(list(self.locked_positions), key=lambda a: a[1])[::-1]:
                x, y = key
                if y < index:                       # if the y value is above the removed index
                    new_key = (x, y + increment)    # shift position to down
                    self.locked_positions[new_key] = self.locked_positions.pop(key)
 
        return increment
 
    def init_grid(self):
        """
        Initialize the game grid
    
        """
        self.locked_positions = {}
        self.grid = self.create_grid()
 
    def init_blocks(self):
        """
        Initialize the current block/piece, next piece and boolean variable to bring in next piece when required 
    
        """
        self.current_piece = self.get_shape()
        self.change_piece = False
        self.next_piece = self.get_shape()
        self.ghost_piece = self.get_shape()
 
    def init_clock(self):
        """
        Initialize the game clock 
    
        """
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.fall_speed = self.level_speeds[self.level]
        self.level_time = 0
 
   
    def update_locked_grid(self):
        """
        Update the grid based on locked positions for display
    
        """
        self.grid = self.create_grid()
 
    def draw_current_grid(self):
        """
        Draw the grid at the current moment in time
    
        """
        self.piece_pos = self.convert_shape_format(self.current_piece)
        
        self.ghost_piece.x = self.current_piece.x
        self.ghost_piece.y = self.current_piece.y
        self.ghost_piece.shape = self.current_piece.shape
        self.ghost_piece.rotation = self.current_piece.rotation    
       
        self.ghost_piece.color = (40,40,40)

        self.get_ghost_position()
        self.ghost_pos = self.convert_shape_format(self.ghost_piece)

        if self.show_shadow:
            # draw the ghost piece on the grid by giving color in the piece locations
            for i in range(len(self.ghost_pos)):
                x, y = self.ghost_pos[i]
                if y >= 0:
                    self.grid[y][x] = self.ghost_piece.color
        
        # draw the piece on the grid by giving color in the piece locations
        for i in range(len(self.piece_pos)):
            x, y = self.piece_pos[i]
            if y >= 0:
                self.grid[y][x] = self.current_piece.color
 
    def update_clock(self):
        """
        Update the game clock
    
        """
        # helps run the same on every computer
        # add time since last tick() to fall_time
        self.fall_time += self.clock.get_rawtime()  # returns in milliseconds
        self.level_time += self.clock.get_rawtime()
 
        self.clock.tick()  # updates clock
 
        if self.increase_difficulty:
            if self.level_time/1000 > 5:    # make the difficulty harder every 10 seconds
                self.level_time = 0
                if self.fall_speed > 0.15:   # until fall speed is 0.15
                    self.fall_speed -= 0.005
 
    def shift_piece(self):
        """
        Shift the piece down by gravity effect (no player input) if it has space
    
        """
        if self.fall_time / 1000 > self.fall_speed:
            self.fall_time = 0
            self.current_piece.y += 1
            if not self.valid_space(self.current_piece) and self.current_piece.y > 0:
                self.current_piece.y -= 1
                # since only checking for down - either reached bottom or hit another piece
                # need to lock the piece position
                # need to generate new piece
                self.change_piece = True
                
    def take_user_input(self):
        """
        Take user inputs while game is being played. Piece movement - left, right, up(clockwise rotation), down. Escape key to pause game
    
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                quit()
 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.current_piece.x -= 1  # move x position left
                    if not self.valid_space(self.current_piece):
                        self.current_piece.x += 1
                    return False
 
                elif event.key == pygame.K_RIGHT:
                    self.current_piece.x += 1  # move x position right
                    if not self.valid_space(self.current_piece):
                        self.current_piece.x -= 1
                    return False
 
                elif event.key == pygame.K_DOWN:
                    # move shape down
                    self.current_piece.y += 1
                    if not self.valid_space(self.current_piece):
                        self.current_piece.y -= 1
                    return False
 
                elif event.key == pygame.K_UP:
                    # rotate shape
                    self.current_piece.rotation = self.current_piece.rotation + 1 % len(self.current_piece.shape)
                    if not self.valid_space(self.current_piece):
                        self.current_piece.rotation = self.current_piece.rotation - 1 % len(self.current_piece.shape)
                    return False
                
                elif event.key == pygame.K_ESCAPE:
                    pygame.mixer.Sound.play(key_press)
                    return True
                
                elif self.hard_drop and event.key == pygame.K_d:
                    self.get_hard_position()
                    return False
    
    def current_piece_locked(self):
        """
        Return if it is time to change piece or not - based on if gravity effect has stopped working or not
    
        Returns:
            bool: True or False
    
        """
        return self.change_piece
 
    def spawn(self):
        """
        After a piece is locked, it updates the locked positions - the positions with stationery piece colors at the bottom, and it changes the piece in motion.
    
        """
        for pos in self.piece_pos:
            p = (pos[0], pos[1])
            self.locked_positions[p] = self.current_piece.color       # add the key and value in the dictionary
        self.current_piece = self.next_piece
        self.next_piece = self.get_shape()
        self.change_piece = False
 
    def update_window(self, score):
        """
        Update the rest of the window except playing grid - Display score and next shape.
    
        Args:
            score (int): Current score
    
        """
        self.draw_window(self.window, self.grid, score)
 
        if self.viz_next_piece:
            self.draw_next_shape(self.next_piece, self.window)
        pygame.display.update()
 
    def paused(self):
        """
        Pause the game play and display necessary options
    
        Returns:
            bool: False return corresponds to player choosing to resume game, True return corresponds to player choosing to restart game. No return occurs when player chooses to quit game
    
        """
        self.window.fill((0,0,0))
        self.window.blit(image, (150, 600))
        xresu = self.draw_text_middle(self.resume_text, self.window, self.general_button_color, 230)
        xres = self.draw_text_middle(self.restart_text, self.window, self.general_button_color, 300)
        xquit = self.draw_text_middle(self.quit_text, self.window, self.general_button_color, 370)
        pygame.display.update()
 
        run = True
        while run:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                #checks if a mouse is clicked
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.Sound.play(key_press)
                    
                    if xresu < mouse[0] < self.s_width - xresu and 230 < mouse[1] < 280:
                        self.draw_text_middle(self.resume_text, self.window, self.click_color, 230)
                        pygame.display.update()
                        return False
                    elif xquit < mouse[0] < self.s_width - xquit and 370 < mouse[1] < 420:
                        self.draw_text_middle(self.quit_text, self.window, self.click_color, 370)
                        pygame.display.update()
                        pygame.quit()
                        sys.exit()
                    elif xres < mouse[0] < self.s_width - xres and 300 < mouse[1] < 350:
                        self.draw_text_middle(self.restart_text, self.window, self.click_color, 300)
                        pygame.display.update()
                        return True
 
    def game_over(self):
        """
        Display the game over screen with gameover message and buttons to restart game or quit game.
    
        Returns:
            bool: True if player decides to restart game. Nothing if player decides to quit game
    
        """
        self.window.fill((0,0,0))
        self.window.blit(image, (150, 600))
        font = pygame.font.Font(self.fontpath_mario, 70, bold=True)
        label = font.render(self.gameover_text, 1, self.gameover_color)
        self.window.blit(label, ((self.s_width - label.get_width())//2, 200))
        xres = self.draw_text_middle(self.restart_text, self.window, self.general_button_color, 300)
        xquit = self.draw_text_middle(self.quit_text, self.window, self.general_button_color, 370)
        pygame.display.update()
 
        rrun = True
        while rrun:
            for event in pygame.event.get():
                    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
 
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.Sound.play(key_press)
                    
                    if xquit < mouse[0] < self.s_width - xquit and 370 < mouse[1] < 420:
                        self.draw_text_middle(self.quit_text, self.window, self.click_color, 370)
                        pygame.display.update()
                        pygame.quit()
                        sys.exit()
                    elif xres < mouse[0] < self.s_width - xres and 300 < mouse[1] < 350:
                        self.draw_text_middle(self.restart_text, self.window, self.click_color, 300)
                        pygame.display.update()
                        return True
 
 
    def main_menu(self):
        """
        The main menu screen. It displays the game heading, levels button, start button and quit button. Based on the button clicked, the game settings get updated. 

        """
        pygame.mixer.music.load('assets/theme.wav')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.window.fill((0,0,0))
        self.window.blit(image, (150, 600))
        
        font = pygame.font.Font(self.fontpath_mario, 70, bold=True)
        label = font.render(self.game_heading, 1, self.game_heading_color)  # initialise 'Tetris' text with white
 
        self.window.blit(label, ((self.s_width - label.get_width())//2, 20))
        l1 = self.draw_text_middle(self.level1_text, self.window, self.general_button_color, 100)
        l2 = self.draw_text_middle(self.level2_text, self.window, self.general_button_color, 170)
        l3 = self.draw_text_middle(self.level3_text, self.window, self.general_button_color, 240)
        start = self.draw_text_middle(self.start_text, self.window, self.general_button_color, 310)
        xquit = self.draw_text_middle(self.quit_text, self.window, self.general_button_color, 380)
        pygame.display.update()
        
        run = True
        level = -1
        while run:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                #checks if a mouse is clicked
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.Sound.play(key_press)
                    
                    if l1 < mouse[0] < self.s_width - l1 and 100 < mouse[1] < 150:
                        self.draw_text_middle(self.level1_text, self.window, self.click_color, 100)
                        self.draw_text_middle(self.level2_text, self.window, self.general_button_color, 170)
                        self.draw_text_middle(self.level3_text, self.window, self.general_button_color, 240)
                        pygame.display.update()
                        level = 0
                    elif l2 < mouse[0] < self.s_width - l2 and 170 < mouse[1] < 220:
                        self.draw_text_middle(self.level1_text, self.window, self.general_button_color, 100)
                        self.draw_text_middle(self.level2_text, self.window, self.click_color, 170)
                        self.draw_text_middle(self.level3_text, self.window, self.general_button_color, 240)
                        pygame.display.update()
                        level = 1
                    elif l3 < mouse[0] < self.s_width - l3 and 240 < mouse[1] < 290:
                        self.draw_text_middle(self.level1_text, self.window, self.general_button_color, 100)
                        self.draw_text_middle(self.level2_text, self.window, self.general_button_color, 170)
                        self.draw_text_middle(self.level3_text, self.window, self.click_color, 240)
                        pygame.display.update()
                        level = 2
                    elif start < mouse[0] < self.s_width - start and 310 < mouse[1] < 360 and level != -1:
                        self.draw_text_middle(self.start_text, self.window, self.click_color, 310)
                        pygame.display.update()
                        
                        run = False
                        return level
                    elif xquit < mouse[0] < self.s_width - xquit and 380 < mouse[1] < 430:
                        self.draw_text_middle(self.quit_text, self.window, self.click_color, 380)
                        pygame.display.update()
                        pygame.quit()
                        sys.exit()
            
 
    def initialize_window(self, row, col):
        """
        Initializes the game window. Screen width - s_width(800) and screen height - s_height(750) are fixed.
    
        Args:
            row (int): Number of rows in playing grid
            col (int): Number of columns in playing grid
    
        """
        self.row = row
        self.col = col
        self.play_width = self.col * self.block_size
        self.play_height = self.row * self.block_size
        self.top_left_x = (self.s_width - self.play_width) // 2
        self.top_left_y = self.s_height - self.play_height - 50
 
    def create_block(self, temp_block):
        """
        Creates a custom block(tetriminoe) for the programmer.
    
        Args:
            temp_block (List): List of length 3 - Rotation configurations, color of block, identifier string
            temp_block[0] (List): The different 2D rotation configurations of the block as string lists
            temp_block[0][i] (List): List containing strings of fixed length that give the ith 2D orientation of block
            temp_block[1] (List): R G B values of block denoting its color
            temp_block[2] (string): Identifier string of the block  
    
        """
        self.shapes.append(temp_block[0])
        self.Dict[temp_block[2]] = len(self.shape_colors)
        self.shape_colors.append(tuple(temp_block[1]))
    
    def show_next_piece(self, val):
        """
        Enable or disable showing next block to player
    
        Args:
            val (bool): True or False  
    
        """
        self.viz_next_piece = val
 
    def show_highscore(self, val):
        """
        Enable or disable showing next highscore to player
    
        Args:
            val (bool): True or False  
    
        """
        self.viz_high_score = val
    
    def increase_fall_speed(self, val):
        """
        Enable or disable increasing fall speed as game progresses or in other words increasing difficulty as game progresses
    
        Args:
            val (bool): True or False  
    
        """
        self.increase_difficulty = val
    
    def set_window_caption(self, val):
        """
        Set the game caption shown in the game window
    
        Args:
            val (string): Game window caption  
    
        """
        pygame.display.set_caption(val)
 
    def set_level(self, val):
        """
        Set the game level - from 3 difficulty levels
    
        Args:
            val (int): Difficulty level 1 or 2 or 3  
    
        """
        self.level = val

    def set_level_fallspeed(self, speed_list):
        """
        Set the fall speeds for the 3 difficulty levels
    
        Args:
            speed_list (list): speed of difficulty level 1,2 and 3  
    
        """
        self.level_speeds = speed_list
    
    def enable_shadow(self, val):
        """
        Enable ghost mode i.e. expected locked position of current piece is displayed
    
        Args:
            val (int): Bool value True or False
    
        """
        self.show_shadow = val

    def enable_hard_drop(self, val):
        """
        Enable hard drop i.e. on pressing the 'd' key, the block falls down
    
        Args:
            val (int): Bool value True or False
    
        """
        self.hard_drop= val

    def design_button_text(self, game_heading, quit_text, resume_text, restart_text, gameover_text, level1_text, level2_text, level3_text, start_text):
        """
        Customize the text displayed over buttons or over gameover and game heading text
    
        Args:
            game_heading (string): Game heading text
            quit_text (string): Quit button text
            resume_text (string): Resume button text
            restart_text (string): Restart button text
            gameover_text (string): Gameover message text
            level1_text (string): Level 1 button text  
            level2_text (string): Level 2 button text
            level3_text (string): Level 3 button text
            start_text (string): Start button text
    
        """
        self.game_heading = game_heading
        self.quit_text = quit_text
        self.resume_text = resume_text
        self.restart_text = restart_text
        self.gameover_text = gameover_text
        self.level1_text = level1_text
        self.level2_text = level2_text
        self.level3_text = level3_text
        self.start_text = start_text
 
    def design_button_color(self, game_heading_color, gameover_color, general_button_color, click_color):
        """
        Customize the text color over buttons, button clicks, gameover text and game heading text
    
        Args:
            game_heading_color (tuple): R G B values denoting game heading color
            gameover_color (tuple): R G B values denoting gameover message color
            general_button_color (tuple): R G B values denoting button color prior to click
            click_color (tuple): R G B values denoting button color post clicking
    
        """
        self.game_heading_color = game_heading_color
        self.gameover_color = gameover_color
        self.general_button_color = general_button_color
        self.click_color = click_color
 
    def design_play(self, playbndry_color, grid_color):
        """
        Customize the play boundary color and play grid color
    
        Args:
            playbndry_color (tuple): R G B values denoting play boundary color
            grid_color (tuple): R G B values denoting play grid color
    
        """
        self.playbndry_color = playbndry_color
        self.grid_color = grid_color
 
    def design_block_color(self, block, color):
        """
        Alter the color for the given block.
    
        Args:
            block (string): String identifier of block
            color (tuple): R G B values of block denoting its color
    
        """
        self.shape_colors[self.Dict[block]] = color
        
                    
 
if __name__ == '__main__':
    
    root = TetrisEngine()
    
    root.initialize_window(18, 10)
    # i = [['.....',
    #     '.....',
    #     '..0..',
    #     '..0..',
    #     '.....'],
    #     ['.....',
    #     '..00.',
    #     '.....',
    #     '.....',
    #     '.....']]
    # x = [['.....',
    #     '..0..',
    #     '.000.',
    #     '..0..',
    #     '.....']]
    # temp_block = [i,[128,165,0],'i']
    # temp_block2 = [x,[255,255,0],'x']

    # root.create_block(temp_block)
    # root.create_block(temp_block2)
    # root.design_block_color('i', (255,255,255))
    # root.show_next_piece(True)
    # root.show_highscore(True)
    # root.increase_fall_speed(True)
    # root.set_window_caption('Tetris by blockbusters')
    # root.set_level(1)
 
    play_again = True
    
    while play_again:
        level = root.main_menu()
        root.set_level(level)
 
        run = True
        restart = False
        score = 0
 
        root.init_grid()
        root.init_blocks()
        root.init_clock()
        while run:
            
            root.update_locked_grid()
            root.update_clock()
            root.shift_piece()
            if root.take_user_input():
                restart = root.paused()
                if restart:
                    break
            root.draw_current_grid()
 
            if root.current_piece_locked():
                root.spawn()
                score+=root.clear_rows()
                root.update_highscore(score)
 
            root.update_window(score)
 
            if root.check_lost():
                run = False
 
        if restart:
            continue
        else:
            play_again = root.game_over()
