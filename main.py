# File:         CS437Final_LundbergDanny.py
# Author:       Danny Lundberg
# Class:        CMSC 437
# Professor:    Squire
# Execute:      python CS437Final_LundbergDanny.py

# Last updated: Dec 14, 2021

# Description:  This program is a version of the game 
#               Dots-and-Boxes, which can be played in 
#               3 different size boards with up to 4 
#               players. The user may choose to play 
#               against AI, or against fellow humans 
#               sharing the device. 

import time
from tkinter.constants import ALL
import numpy as np
import tkinter as tk
import tkinter.messagebox

# ---------------------------------------------------------------
# Dots_Boxes_App is the main class of this application, 
# setting up the 'options' menu upon startup, then 
# running the game based on options selected
# ---------------------------------------------------------------
class Dots_Boxes_App(tk.Tk):
    # Default setup variables
    SETUP_SIZE = 500
    SETUP_OFFSET = 10
    board_size = 300
    num_dots = 3
    num_players = 2
    dot_color = '#808080'
    p1_color = '#1667c7'
    p1_square_color = '#669fe2'
    p2_color = '#D09215'
    p2_square_color = '#E4BB68'
    p3_color = '#13c330'
    p3_square_color = '#55DA6B'
    p4_color = '#E60EC4'
    p4_square_color = '#F360DC'
    # Ideal dot size=20px, line size=10 
    # (dots bigger than lines)
    dot_size = 20
    line_size = 10
    space_btwn_dots = board_size/num_dots
    restart_game = False
    running = False
    curr_turn = 1
    new_box_flag = False
    ai = False
    p1_score = 0
    p2_score = 0
    p3_score = 0
    p4_score = 0


    # ---------------------------------------------------------------
    # Initialization Functions of class Dots_Boxes_App
    # ---------------------------------------------------------------
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Dots and Boxes Game")
        self.geometry('%dx%d+%d+%d' % (self.SETUP_SIZE, self.SETUP_SIZE, self.SETUP_OFFSET, self.SETUP_OFFSET))
        self.canvas = tk.Canvas(self, width=self.SETUP_SIZE, height=self.SETUP_SIZE)
        self.canvas.pack()
        self.setup_game()


    def start_game(self):
        self.running = True
        self.canvas.delete(ALL)
        self.geometry('%dx%d+%d+%d' % (self.board_size+300, self.board_size, 10, 0))
        self.canvas.config(width=self.board_size, height=self.board_size)
        self.canvas.pack()
        self.bind("<Button-1>", self.click)
        self.play_game()


    def reset_game(self):
        self.p1_score = 0
        self.p2_score = 0
        self.p3_score = 0
        self.p4_score = 0
        self.running = False
        self.restart_game = False
        self.curr_turn = 1
        self.ai = False
        self.canvas.delete(ALL)
        self.hide_scores()
        self.geometry('%dx%d+%d+%d' % (self.SETUP_SIZE, self.SETUP_SIZE, self.SETUP_OFFSET, self.SETUP_OFFSET))
        self.canvas.config(width=self.SETUP_SIZE, height=self.SETUP_SIZE)
        self.setup_game()


    def play_game(self):
        self.setup_board()
        # Setup arrays that represent the rows, columns, and boxes internally:
        self.box_array = np.zeros(shape=(self.num_dots-1, self.num_dots-1))
        self.row_array = np.zeros(shape=(self.num_dots, self.num_dots-1))
        self.col_array = np.zeros(shape=(self.num_dots-1, self.num_dots))
        self.player_box_array = np.zeros(shape=(self.num_dots-1, self.num_dots-1))
        self.start_time = time.time()

        self.turn_text = []
        self.show_turn()


    # ---------------------------------------------------------------
    # Logic/Math Functions of class Dots_Boxes_App
    # ---------------------------------------------------------------
    # next_turn is simple helper function that handles 
    # incrementing self.curr_turn; if the player scored 
    # however, they get to take another turn
    def next_turn(self):
        if not self.new_box_flag:
            # if at last player turn, set back to 
            # player 1 else just increment it
            if(self.curr_turn == self.num_players):
                self.curr_turn = 1 
            else:
                self.curr_turn += 1
        else:
            # reset flag before same user takes another turn
            self.new_box_flag = False


    def curr_color(self):
        if self.curr_turn == 1:
            color = self.p1_color
        elif self.curr_turn == 2:
            color = self.p2_color
        elif self.curr_turn == 3:
            color = self.p3_color
        elif self.curr_turn == 4:
            color = self.p4_color
        return color


    def convert_click_to_position(self, event_pos):
        xy_pos = np.array(event_pos)
        # math to get where click was
        pos = (xy_pos-self.space_btwn_dots/4)//(self.space_btwn_dots/2)
        line_type = False
        row_col_pos = []
        if (pos[0] % 2 == 0) and ((pos[1]-1) % 2 == 0):
            r = int(pos[0] // 2)
            c = int((pos[1]-1 ) // 2)
            line_type = 'col'
            row_col_pos = [r,c]
        elif(pos[1] % 2 == 0) and ((pos[0]-1) % 2 == 0):
            r = int((pos[0]-1 ) // 2)
            c = int(pos[1] // 2)
            line_type = 'row'
            row_col_pos = [r,c]

        return row_col_pos, line_type


    def line_exists(self, line_type, row_col_pos):
        r = row_col_pos[0]
        c = row_col_pos[1]
        exists = True

        if line_type == 'row' and self.row_array[c][r]==0:
            exists = False
        if line_type == 'col' and self.col_array[c][r]==0:
            exists = False
        return exists


    def update_internal_arrays(self, line_type, row_col_pos):
        r = row_col_pos[0]
        c = row_col_pos[1]
        if line_type == 'row':
            self.row_array[c][r] = 1
            if c==0:
                self.box_array[c][r] += 1
            elif c==self.num_dots-1:
                self.box_array[c-1][r] += 1
            else:
                self.box_array[c][r] += 1
                self.box_array[c-1][r] += 1
            
            if c == self.num_dots-1:
                if self.box_array[c-1][r] == 4:
                    self.new_box_flag = True
            else:
                if self.box_array[c][r] == 4 or self.box_array[c-1][r] == 4:
                    self.new_box_flag = True

        elif line_type == 'col':
            self.col_array[c][r] = 1
            if r==0:
                self.box_array[c][r] += 1
            elif r==self.num_dots-1:
                self.box_array[c][r-1] += 1
            else:
                self.box_array[c][r] += 1
                self.box_array[c][r-1] += 1

            if r == self.num_dots-1:
                if self.box_array[c][r-1] == 4:
                    self.new_box_flag = True
            else:
                if self.box_array[c][r] == 4 or self.box_array[c][r-1] == 4:
                    self.new_box_flag = True

        # *** debugging, rm later ***
        print(self.box_array)


    def update_player_box_array(self, line_type, row_col_pos):
        r = row_col_pos[0]
        c = row_col_pos[1]

        if(self.new_box_flag):
            for i in range(self.num_dots-1):
                for j in range(self.num_dots-1):
                    if self.box_array[i][j] == 4:
                        self.player_box_array[i][j] = self.curr_turn
                        # set self.box_array value =/= 4 
                        # so don't overwrite on next scored box
                        self.box_array[i][j] = -1

        # ***debugging, rm later ***
        print(self.player_box_array)

        self.draw_box()
        self.update_score()


    def update_score(self):
        p1 = 0
        p2 = 0 
        p3 = 0
        p4 = 0
        for i in range(self.num_dots-1):
            for j in range(self.num_dots-1):
                if self.player_box_array[i][j]==1:
                    p1 += 1
                elif self.player_box_array[i][j]==2:
                    p2 += 1
                elif self.player_box_array[i][j]==3:
                    p3 += 1
                elif self.player_box_array[i][j]==4:
                    p4 += 1

        self.p1_score = p1
        self.p2_score = p2
        self.p3_score = p3
        self.p4_score = p4


    def game_over(self):
        game_over = True
        if (self.player_box_array == 0).any():
            game_over = False
        return game_over


    def on_game_over(self):
        print("game over!")
        self.restart_game = True
        time_played = self.format_time()
        mid = self.board_size/2
        text = "Click anywhere to reset!"
        self.canvas.create_text(mid, mid, anchor='c', text=text, font=('arial', 15, 'bold'), fill='black')

        self.withdraw()
        splash = Splash_Game_Over(self, self.num_players, self.p1_score, 
                                  self.p2_score, self.p3_score, self.p4_score,
                                  self.p1_color, self.p2_color, self.p3_color,
                                  self.p4_color, time_played)
        self.deiconify()


    def restart_or_quit(self):
        user_input = tkinter.messagebox.askquestion("Try Again?", "Would you like to reset the game?\n(click 'Yes' to restart, click 'No' to quit)")
        if user_input == 'yes':
            self.reset_game()
        else:
            self.destroy()


    def format_time(self):
        openTime = time.time() - self.start_time
        min = int(openTime/60)
        sec = int(openTime%60)
        closeMin = str(min)
        closeSec = str(sec)
        if sec < 10:
            closeSec = "0" + str(sec)
        return ("Time: " + str(closeMin) + ":" + str(closeSec))


    def make_ai_move(self):
        best_flag = False
        medi_flag = False
        for i in range(self.num_dots-1):
            for j in range(self.num_dots-1):
                if self.box_array[i][j]==3:
                    # almost completed box, AI should finish it
                    best_flag = True
                    best_capture = [i, j]
                elif self.box_array[i][j]==1:
                    medi_flag = True
                    medi_capture = [i, j]
                elif self.box_array[i][j]!=-1:
                    any_move = [i, j]

        if best_flag:
            if self.row_array[best_capture[0]][best_capture[1]]==0:
                line_type = 'row'
                move = [best_capture[1], best_capture[0]]
            elif self.row_array[best_capture[0]+1][best_capture[1]]==0:
                line_type = 'row'
                move = [best_capture[1], best_capture[0]+1]
            elif self.col_array[best_capture[0]][best_capture[1]]==0:
                line_type = 'col'
                move = [best_capture[1], best_capture[0]]
            elif self.col_array[best_capture[0]][best_capture[1]+1]==0:
                line_type = 'col'
                move = [best_capture[1]+1, best_capture[0]]
        elif not best_flag and medi_flag:
            if self.row_array[medi_capture[0]][medi_capture[1]]==0:
                line_type = 'row'
                move = [medi_capture[1], medi_capture[0]]
            elif self.row_array[medi_capture[0]+1][medi_capture[1]]==0:
                line_type = 'row'
                move = [medi_capture[1], medi_capture[0]+1]
            elif self.col_array[medi_capture[0]][medi_capture[1]]==0:
                line_type = 'col'
                move = [medi_capture[1], medi_capture[0]]
            elif self.col_array[medi_capture[0]][medi_capture[1]+1]==0:
                line_type = 'col'
                move = [medi_capture[1]+1, medi_capture[0]]
        else:
            if self.row_array[any_move[0]][any_move[1]]==0:
                line_type = 'row'
                move = [any_move[1], any_move[0]]
            elif self.row_array[any_move[0]+1][any_move[1]]==0:
                line_type = 'row'
                move = [any_move[1], any_move[0]+1]
            elif self.col_array[any_move[0]][any_move[1]]==0:
                line_type = 'col'
                move = [any_move[1], any_move[0]]
            elif self.col_array[any_move[0]][any_move[1]+1]==0:
                line_type = 'col'
                move = [any_move[1]+1, any_move[0]]

        self.update_internal_arrays(line_type, move)
        self.draw_line(line_type, move)
        self.update_player_box_array(line_type, move)
        self.setup_board()
        self.next_turn()

        if self.game_over():
            print("reached self.end_game==True")
            self.on_game_over()
        else:
            self.show_turn()


    # ---------------------------------------------------------------
    # UI/Drawing Functions of class Dots_Boxes_App
    # ---------------------------------------------------------------
    # setup_game allows user to select starting options
    def setup_game(self):
        self.s1 = tk.Label(self)
        self.s2 = tk.Label(self)
        self.s3 = tk.Label(self)
        self.s4 = tk.Label(self)
        DEFAULT_BOARD_SIZE = 300
        DEFAULT_NUM_DOTS = 3
        DEFAULT_NUM_PLAYERS = 2
        self.board_size = DEFAULT_BOARD_SIZE
        self.num_dots = DEFAULT_NUM_DOTS
        self.num_players = DEFAULT_NUM_PLAYERS
        self.bind('<Button-1>', self.click_setup)
        self.canvas.create_text(250, 50, anchor="c", text="Dots and Boxes Game", font=('arial', 20, 'bold'))
        self.canvas.create_rectangle(180, 75, 320, 125, fill='white')
        self.canvas.create_text(250, 100, anchor="c", text="How to Play", font=('arial', 14))
        self.canvas.create_rectangle(150, 440, 350, 490, fill='green')
        self.canvas.create_text(250, 465, text="Start Game", font=('arial', 20, 'bold'))
        sizes = ["S (2x2)", "M (4x4)", "L (6x6)"]

        # create # players buttons
        self.canvas.create_text(250, 150, anchor="c", text="Select number of players:", font=('arial', 14))
        self.canvas.create_text(250, 325, anchor="c", text="Select board size:", font=('arial', 14))
        for i in range(3):
            self.canvas.create_rectangle(25+150*i, 175, 150+150*i, 225, fill='yellow')
            self.canvas.create_text(125+150*i, 200, anchor="w", text=('%d' % (i+2)), font=('arial', 14))
            self.canvas.create_rectangle(25+150*i, 350, 150+150*i, 400, fill='yellow')
            self.canvas.create_text(125+150*i, 375, anchor="e", text=(sizes[i]), font=('arial', 14))
        self.canvas.create_text(25, 262, anchor='w', text="Play versus AI?", font=('arial', 14))
        for j in range(2):
            self.canvas.create_rectangle(200+150*j, 250, 250+150*j, 275, fill='yellow')
        self.canvas.create_text(245, 262, anchor="e", text="N", font=('arial', 14))
        self.canvas.create_text(395, 262, anchor="e", text="Y", font=('arial', 14))

        # auto-check 2 Players, S board, 'no' vs AI
        self.check_player = self.canvas.create_text(75, 200, anchor="c", text="\u2713", font=('consolas', 15))
        self.check_board = self.canvas.create_text(50, 375, anchor="c", text="\u2713", font=('consolas', 15))
        self.check_AI = self.canvas.create_text(225, 262, anchor="c", text='\u2713', font=('consolas', 15))
        self.canvas.update()


    # setup_board keeps the background setup of the board intact
    def setup_board(self):
        # Draw the num_dots*num_dots matrix 
        for i in range(self.num_dots):
            for j in range(self.num_dots):
                # Get start, end of (x,y) coords in pixels to make circles
                xy_start = (i * self.space_btwn_dots) + (self.space_btwn_dots/2)
                xy_end = (j * self.space_btwn_dots) + (self.space_btwn_dots/2)
                # Get exact (x) and (y) coords for drawings
                x0 = xy_start - (self.dot_size/2)
                y0 = xy_end - (self.dot_size/2)
                x1 = xy_start + (self.dot_size/2)
                y1 = xy_end + (self.dot_size/2)
                self.canvas.create_oval(x0, y0, x1, y1, fill=self.dot_color, outline=self.dot_color)

        # Draw lines over the matrix of dots
        # !!! could be done more efficiently; just draw the # rows/col lines instead of going by num_dots
        # BUT this works so not changing it as of now
        for i in range(self.num_dots):
            x_start = (i*self.space_btwn_dots) + (self.space_btwn_dots/2)
            x0 = x_start
            y0 = self.space_btwn_dots/2
            x1 = x_start
            y1 = self.board_size-self.space_btwn_dots/2
            # draw vertical lines
            self.canvas.create_line(x0, y0, x1, y1, fill='gray', dash=(2,2))
            # draw horizontal lines
            self.canvas.create_line(y0, x0, y1, x1, fill='gray', dash=(2,2))

        self.draw_score()


    def show_turn(self):
        text = "Current turn: Player "
        color = self.curr_color()
        if self.curr_turn:
            text += str(self.curr_turn)
            if self.ai and self.curr_turn!=1:
                text += " (AI)"
        else:
            text += "error getting curr_turn"

        self.canvas.delete(self.turn_text)
        x = (self.board_size/2)
        y = (self.space_btwn_dots/8)
        self.turn_text = self.canvas.create_text(x, y, font=('arial', 18, 'bold'), text=text, fill=color)
        

    def draw_line(self, line_type, row_col_pos):
        if line_type == 'row':
            x0 = (self.space_btwn_dots/2) + (row_col_pos[0]*self.space_btwn_dots)
            x1 = x0 + self.space_btwn_dots
            y0 = (self.space_btwn_dots/2) + (row_col_pos[1]*self.space_btwn_dots)
            y1 = y0
        elif line_type == 'col':
            y0 = (self.space_btwn_dots/2) + (row_col_pos[1]*self.space_btwn_dots)
            y1 = y0 + self.space_btwn_dots
            x0 = (self.space_btwn_dots/2) + (row_col_pos[0]*self.space_btwn_dots)
            x1 = x0

        color = self.curr_color()
        self.canvas.create_line(x0, y0, x1, y1, fill=color, width=self.line_size)


    def draw_box(self):
        boxes = np.argwhere(self.player_box_array == self.curr_turn)
        if self.curr_turn == 1:
            color = self.p1_square_color
        elif self.curr_turn == 2:
            color = self.p2_square_color
        elif self.curr_turn == 3:
            color = self.p3_square_color
        elif self.curr_turn == 4:
            color = self.p4_square_color

        for box in boxes:
            x0 = (self.space_btwn_dots/2) + (box[1]*self.space_btwn_dots) + (self.line_size/2)
            y0 = (self.space_btwn_dots/2) + (box[0]*self.space_btwn_dots) + (self.line_size/2)
            x1 = x0 + self.space_btwn_dots - self.line_size
            y1 = y0 + self.space_btwn_dots - self.line_size
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='')
     

    def draw_score(self):
        y_offset = 0.1*(self.num_players-1)
        self.s1.config(text=("Player 1: %d" % self.p1_score), font=('arial', 15), fg=self.p1_color)
        self.s1.place(relx=0.0, rely=1.0-y_offset, anchor='sw')
        self.s2.config(text=("Player 2: %d" % self.p2_score), font=('arial', 15), fg=self.p2_color)
        self.s2.place(relx=0.0, rely=1.0-y_offset+0.1, anchor='sw')
        if self.num_players >= 3:
            self.s3.config(text=("Player 3: %d" % self.p3_score), font=('arial', 15), fg=self.p3_color)
            self.s3.place(relx=0.0, rely=1.0-y_offset+0.2, anchor='sw')
        if self.num_players == 4:
            self.s4.config(text=("Player 4: %d" % self.p4_score), font=('arial', 15), fg=self.p4_color)
            self.s4.place(relx=0.0, rely=1.0-y_offset+0.3, anchor='sw')
        
        
    def hide_scores(self):
        self.s1.destroy()
        self.s2.destroy()
        self.s3.destroy()
        self.s4.destroy()


    def show_instructions(self):
        text = ("How to Play Dots and Boxes:\n\n" +
                "On start up screen, select number of players and board size.\n" +
                "You may choose to play against human opponents, or versus the computer.\n\n" +
                "The aim of the game is to capture as many boxes as possible.\n\n" +
                "On each turn, each player places a line between any two dots where a line does not already exist.\n" +
                "If the player creates a new box, the player gets to take an additional turn.\n\n" +
                "(If playing with AI, the user must click during the AI players' turns to prompt the AI to move)\n\n" +
                "The game ends when all boxes have been claimed.")
        tkinter.messagebox.showinfo("Dots and Boxes - Instructions", text)


    # ---------------------------------------------------------------
    # Mouse Event Functions of Class Dots_Boxes_App
    # ---------------------------------------------------------------
    def click(self, event):
        if not self.restart_game:
            if not self.ai or (self.ai and self.curr_turn==1):
                event_pos = [event.x, event.y]
                row_col_pos, line_type = self.convert_click_to_position(event_pos)
                if line_type and not self.line_exists(line_type, row_col_pos):
                    self.update_internal_arrays(line_type, row_col_pos)
                    self.draw_line(line_type, row_col_pos)
                    self.update_player_box_array(line_type, row_col_pos)
                    self.setup_board()
                    self.next_turn()

                    if self.game_over():
                        print("reached self.end_game==True")
                        self.on_game_over()
                    else:
                        self.show_turn()
            elif(self.ai and self.curr_turn!=1):
                self.make_ai_move()

        else:
            self.restart_or_quit()  


    def click_setup(self, event):
        x = event.x
        y = event.y
        if not self.running:
            if 75 <= y <= 125:
                if 180 <= x <= 320:
                    self.show_instructions()
            if 175 <= y <= 225:
                if 25 <= x <= 150:
                    self.canvas.delete(self.check_player)
                    self.num_players = 2
                    self.check_player = self.canvas.create_text(75, 200, anchor="c", text="\u2713", font=('consolas', 15))
                elif 175 <= x <= 300:
                    self.canvas.delete(self.check_player)
                    self.num_players = 3
                    self.check_player = self.canvas.create_text(225, 200, anchor="c", text="\u2713", font=('consolas', 15))
                elif 325 <= x <= 450:
                    self.canvas.delete(self.check_player)
                    self.num_players = 4
                    self.check_player = self.canvas.create_text(375, 200, anchor="c", text="\u2713", font=('consolas', 15))
            if 250 <= y <= 275:
                if 200 <= x <= 250:
                    self.canvas.delete(self.check_AI)
                    self.ai = False
                    self.check_AI = self.canvas.create_text(225, 262, anchor="c", text='\u2713', font=('consolas', 15))
                elif 350 <= x <= 400:
                    self.canvas.delete(self.check_AI)
                    self.ai = True
                    self.check_AI = self.canvas.create_text(375, 262, anchor="c", text='\u2713', font=('consolas', 15))
            if 350 <= y <= 400:
                if 25 <= x <= 150:
                    self.canvas.delete(self.check_board)
                    self.board_size = 300
                    self.num_dots = 3
                    self.check_board = self.canvas.create_text(50, 375, anchor="c", text="\u2713", font=('consolas', 15))
                elif 175 <= x <= 300:
                    self.canvas.delete(self.check_board)
                    self.board_size = 500
                    self.num_dots = 5
                    self.check_board = self.canvas.create_text(200, 375, anchor="c", text="\u2713", font=('consolas', 15))
                elif 325 <= x <= 450:
                    self.canvas.delete(self.check_board)
                    self.board_size = 700
                    self.num_dots = 7
                    self.check_board = self.canvas.create_text(350, 375, anchor="c", text="\u2713", font=('consolas', 15))

            if 440 <= y <= 490:
                if 150 <= x <= 350:
                    self.start_game()
# -----------------------------------------------------
# end of class Dots_Boxes_App
# -----------------------------------------------------

# -----------------------------------------------------
# Splash_Game_Over is an extra class for 
# displaying the splash screen upon the game ending
# -----------------------------------------------------
class Splash_Game_Over(tk.Toplevel):
    height = 400
    width = 200
    offset = 50
    x_off = width / 2
    y_off = 0
    count = 10
    countdown_txt = ("(Auto-exit in %d seconds...)" % count)

    # ---------------------------------------------------------------
    # Initialization Functions of class Splash_Game_Over
    # ---------------------------------------------------------------
    def __init__(self, parent, num_players, s1, s2, s3, s4, c1, c2, c3, c4, time):
        tk.Toplevel.__init__(self, parent)
        self.title("End Game")
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.offset, self.offset))
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.y_off = (self.height / (num_players + 2))
        self.canvas.create_text(self.x_off, 30, anchor='c', text="GAME OVER!\n", font=('arial', 15, 'bold'))
        self.format_score(num_players, s1, s2, s3, s4, c1, c2, c3, c4, time)
        self.bind("<Button-1>", self.click)


    def destroy_splash(self):
        self.destroy()


    # ---------------------------------------------------------------
    # Logic Functions of class Splash_Game_Over
    # ---------------------------------------------------------------
    def cycle(self):
        if self.count > 0:
            self.countdown_txt = ("(Auto-close in %d seconds...)" % self.count)
            self.canvas.delete(self.countdown)
            self.countdown = self.canvas.create_text(self.x_off, self.height-10, anchor='c', text=self.countdown_txt, font=('arial', 10))
            self.count -= 1
        else:
            self.timeout()
        self.after(1000, self.cycle)


    def timeout(self, event=None):
        self.after(0, self.destroy_splash)

    # ---------------------------------------------------------------
    # UI/Drawing Functions of class Splash_Game_Over
    # ---------------------------------------------------------------
    def format_score(self, num_players, s1, s2, s3, s4, c1, c2, c3, c4, time):
        score_p1 = "Player 1: " + str(s1) + '\n'
        self.canvas.create_text(self.x_off, self.y_off+30, anchor='c', text=score_p1, font=('arial', 15, 'bold'), fill=c1)
        score_p2 = "Player 2: " + str(s2) + '\n'
        self.canvas.create_text(self.x_off, self.y_off*2+30, anchor='c', text=score_p2, font=('arial', 15, 'bold'), fill=c2)
        if (num_players >= 3):
            score_p3 = "Player 3: " + str(s3) +'\n'
            self.canvas.create_text(self.x_off, self.y_off*3+30, anchor='c', text=score_p3, font=('arial', 15, 'bold'), fill=c3)
        if (num_players == 4):
            score_p4 = "Player 4: " + str(s4) + '\n'
            self.canvas.create_text(self.x_off, self.y_off*4+30, anchor='c', text=score_p4, font=('arial', 15, 'bold'), fill=c4)
        self.canvas.create_text(self.x_off, self.height-50, anchor='c', text=time, font=('arial', 13, 'bold'))
        click_txt = "Click to exit game over splash."
        self.canvas.create_text(self.x_off, self.height-20, anchor='c', text=click_txt, font=('arial', 10))
        self.countdown = self.canvas.create_text(self.x_off, self.height-10, anchor='c', text=self.countdown_txt, font=('arial', 10))
        self.cycle()

    # ---------------------------------------------------------------
    # Mouse Event Functions of class Splash_Game_Over
    # ---------------------------------------------------------------
    def click(self, event=None):
        self.destroy_splash()
# -----------------------------------------------------
# end of class Splash_Game_Over
# -----------------------------------------------------



# -----------------------------------------------------
# Main loop, launch point for python
# -----------------------------------------------------
def main():
    app = Dots_Boxes_App()
    app.mainloop()

if __name__ == "__main__":
    main()
# -----------------------------------------------------
# end of CS437Final_LundbergDanny.py
# -----------------------------------------------------