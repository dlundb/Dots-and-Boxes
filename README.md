README.md of CS437Final_LundbergDanny.py

(forked from https://github.com/aqeelanwar/Dots-and-Boxes as 
a starting point; my additions include a simple AI, and user 
choice to play against up to 3 other players instead of just
a 1v1 hot seat game)

Installations required:
 - Python 3.8+
 - python module numpy
 - python module tkinter

To execute, cd to directory with CS437Final_LundbergDanny.py, 
then execute with `python CS437Final_LundbergDanny.py` in 
terminal or your favorite editor.

The game is intended for a minimum of 2 players, and a maximum 
of 4. The size of the board can be picked at the beginning, 
(smaller boards take less time to complete while larger boards 
take longer). The user can also choose to play against AI or 
his fellow humans. If the user wants to play against AI, all 
other players besides player 1 will be AI. In the future I'd 
like to modify this to pick how many humans/AI the user 
wants, and have the user be able to play with a mix (2 humans 
versus 2 AI's for example).

The goal of the game is to make as many boxes between the dots 
as possible. One by one, the players place lines between dots. 
If the line completes a square, the player who placed the line 
captures the completed box and gets to take another turn. The 
game ends when all boxes have been taken.

The AI is relatively simple: it prefers to capture any boxes 
that are 1 line away from being complete; if a move of this 
type does not exist then it prefers to make a second line on 
any box that only has a single line so far. If no such box 
exists, it will place a line on any other box. In the future 
I would like to modify this to add some randomness; at the 
moment it simply takes the first row available that does not 
put itself at a disadvantage, if no rows are available it 
takes a column with the least disadvantage. 