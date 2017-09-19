#-*- coding: utf-8 -*-

import curses
from random import randrange, choice 
from collections import defaultdict 

#Defines valid inputs to not allow for input errors 
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
lettercodes = [ord(ch) for ch in 'WASDRQwasdrq']
actions_dict = dict(zip(lettercodes, actions * 2))

# Character not in dictonary so it adds it to the dictionary to make it recongized
def get_user_action(keyboard):
    char = 'N'
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]

# Transpose of matrix to determine tile moveability
def transpose(field):
    return [list(row) for row in zip(*field)]

# Inversion of matrix to determine tile moveability
def invert(field):
    return [row[::-1] for row in field]

#Defines game terms: 4x4 matrix, if you get 2048 you win anf 
class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height = height 
        self.width = width 
        self.win_value = 2048
        self.score = 0
        self.highscore = 0
        self.reset()
# Randomly inputs a either 2 or 4 into the board after a move has been made
    def spawn(self):
        new_element = 4 if randrange(100) > 89 else 2
        (i, j) = choice([(i, j) for i in range(self.width) for j in\
                         range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element
 # resets score but if a highscore it updates highscore first
    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score 
        self.score = 0
        self.field = [[0 for i in range(self.width)] for j in
                       range(self.height)]
        self.spawn()
        self.spawn()
 #Defines all the movements in the the game
    def move(self, direction):
        def move_row_left(row):
            #Collapses one row once 2 tiles are merged
            def tighten(row):
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row
            #merges 2 tiles if they are equal and multiplies the value by itself of the new tile. Them upates the score accordingly
            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else: #if same value will append the 2 tiles
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row 
            return tighten(merge(tighten(row)))
        #Shows valid moves for each direction
        moves = {}
        moves['Left'] = lambda field: [move_row_left(row) for row in field]
        moves['Right'] = lambda field:\
                invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field:\
                transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field:\
                transpose(moves['Right'](transpose(field)))
        # if move is valid it will spawn a new random tile (2 or 4)
        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False 
    # win if 2048 is reached
    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)
    #game is over if no possible moves on field 
    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)
# Draws to screen depending on action
    def draw(self, screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '    (R)Restart (Q)Exit'
        gameover_string = '         GAME OVER'
        win_string = '      YOU WIN!'
        def cast(string):
            screen.addstr(string + '\n')
#seperator for horizontal tile sqaures
        def draw_hor_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(draw_hor_separator, "counter"):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1
#draws rows to create table to play game
        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for
                         num in row) + '|')
        screen.clear()
        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            cast('HGHSCORE: ' + str(self.highscore))
        for row in self.field:
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()
        if self.is_win(): # if you win print you win string
            cast(win_string)
        else:
            if self.is_gameover(): # if you lose print game over string
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)
# checks if valid move is possible for tile 
    def move_is_possible(self, direction):
        def row_is_left_movable(row):
            def change(i):
                if row[i] == 0 and row[i + 1] != 0:
                    return True
                if row[i] != 0 and row[i + 1] == row[i]:
                    return True
                return False 
            return any(change(i) for i in range(len(row) - 1))
# checks the directions in which a tile can move
        check = {}
        check['Left'] = lambda field:\
                 any(row_is_left_movable(row) for row in field)
        check['Right'] = lambda field:\
                check['Left'](invert(field))
        check['Up'] = lambda field:\
                check['Left'](transpose(field))
        check['Down'] = lambda field:\
                check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False 
# main class to run game
def main(stdscr):
    # initalize game
    def init():
        #重置游戏棋盘
        game_field.reset()
        return 'Game'
#gives options if game is open but not in play
    def not_game(state):
        #画出 GameOver 的画面
        #读取用户输入判断是Restart还是Exit
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        responses = defaultdict(lambda: state)
        responses['Restart'], responses['Exit'] = 'Init', 'Exit'
        return responses[action]
    
    def game():
# based on response will act appropriately (user says restart it will restart)
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'
# defines the 4 possible actions that the user can be in
    state_actions = {
        'Init' : init,
        'Win' : lambda: not_game('Win'),
        'Gameover': lambda: not_game('Gameover'),
        'Game': game 
    }
    #As long as user doesnt exit keep game going
    curses.use_default_colors()
    game_field = GameField(win = 32)
    state = 'Init'
    while state != 'Exit':
        state = state_actions[state]()

curses.wrapper(main)


            






