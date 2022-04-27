# Dots-and-Boxes, a python-tkinter based code

---

## Installations required:
 - Python 3.8+
 - python module numpy 1.22+
 - python module tkinter 

---

## Running Dots-and-Boxes:

```
git clone https://github.com/dlundb/Dots-and-Boxes.git
cd Dots-and-Boxes
python main.py
```

If `python main.py` does not work, try `python -m main.py`.

---

## Overview

The goal of the game is to make as many boxes between the dots 
as possible. One by one, the players place lines between dots. 
If the line completes a square, the player who placed the line 
captures the completed box and gets to take another turn. The 
game ends when all boxes have been taken.

The game is intended for a minimum of 2 players, and a maximum 
of 4. The size of the board can be picked at the beginning, 
(smaller boards take less time to complete while larger boards 
take longer). The user can also choose to play against AI or 
his fellow humans. If the user wants to play against AI, all 
other players besides player 1 will be AI. 

!["Game selection screen"](~./images/selectionscreen.PNG "Game selection screen for Dots-and-Boxes showing the various options to play from.")

!["2 by 2, 2-player board"](~./images/2by2.PNG "2x2 square board with two human players, before Player 1 takes a turn")

!["4 by 4, 3-player board"](~./images/4by4.PNG "4x4 square board with three human players, at a point where no move can be made that does not place a third side on a box, allowing Player 1 to score first")

!["6 by 6, 4-player board"](~./images/6by6.PNG "6x6 square board with three AI players, and one human player. Board shows how AI will attempt to close any box that has 3 sides, then will try to place where the AI is only putting down the second side over the third side.")

!["Title"](~./images/name.PNG "Desc")

The AI is relatively simple: it prefers to capture any boxes 
that are 1 line away from being complete; if a move of this 
type does not exist then it prefers to make a second line on 
any box that only has a single line so far. If no such box 
exists, it will place a line on any other box. In the future 
I would like to modify this to add some randomness; at the 
moment it simply takes the first horizontal row available that 
does not put itself at a disadvantage, if no rows are available 
it takes a column with the least disadvantage.

!["Simple AI play in Dots-and-Boxes"](~./images/sillyAI.PNG "Demonstration of how the AI is arguably 'boring' right now; it's logic attempts to ideally place the fourth, second, first, and finally third line on the last observed box where the best of those positions is possible. In this example, the AI's continually sought out to place the second line on each box, since the fourth was not immediately available.")

---

### Changes Made:

 1. Altered scorekeeping: awards player 1 point upon being 
 the player to complete any square, and 1 additional turn upon 
 being the player to complete any square (these were familiar 
 rules from childhood games sought to incorporate)
    - in original repo player must have all 4 sides of 
    square to score
 2. Added simple AI & game selection screen: users can choose 
 to play with up to 4 players, human or AI, on three different
 board sizes
    - when playing vs human players, players must share mouse 
    to take turns
    - when playing vs AI, human player must click the 
    screen in order for the AI to complete it's move
    - board sizes form 2x2, 4x4, 6x6 squares
    - each player has a different color
3. Added splash screen at game over; this displays all the 
players' scores and the total time the game took. It also 
auto-closes itself after 10 seconds.

---

### To Do's

 - modify game selection screen to choose which players are 
 human or AI (each player a checkmark, radio buttons under 
 each player to choose if human or AI)
 - modify AI; come up with more complex algorithm to determine 
 optimal moves and add some randomness to the move-making; perhaps 
 develop different difficulties of AI
 - add colorblind mode: edit actual colors and/or when completing 
 a square, place text of the player's number within the square
 - save high scores (time & score amount) and display somehow