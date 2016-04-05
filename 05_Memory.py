# implementation of card game - Memory

import simplegui
import random


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 100
NUMBERS = 8
CARD_WIDTH = CANVAS_WIDTH // (NUMBERS*2)
FONT_SIZE = 30
NUMBER_X = int(CARD_WIDTH * 0.32)
NUMBER_Y = int(CANVAS_HEIGHT * 0.6)
 

card_deck = []
exposed = []
turns = 0
state = 0

first_card = second_card = 0

# helper function to initialize globals
def new_game():
    global card_deck, exposed
    global state
    global turns

    card_deck = range(NUMBERS) * 2
    random.shuffle(card_deck)
    exposed = [False] * len(card_deck)
    
    state = 0
    
    turns = 0
    label.set_text("Turns = "+ str(turns))
    
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state
    global turns
    global first_card, second_card
    clicked = pos[0] // CARD_WIDTH
    
    if exposed[clicked] == False:
        exposed[clicked] = True
        
        if state == 0:      
            exposed[clicked] = True
            first_card = clicked
            state = 1
        elif state == 1:
            second_card = clicked
            turns += 1
            label.set_text("Turns = "+ str(turns))
            state = 2
        else:
            if card_deck[first_card] != card_deck[second_card]:
                exposed[first_card] = False
                exposed[second_card] = False
        
            exposed[clicked] = True
            first_card = clicked
            state = 1
     
                           
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(len(card_deck)):
        if exposed[i] == False:
            canvas.draw_polygon([[CARD_WIDTH*i, 0], [CARD_WIDTH*(i+1), 0], [CARD_WIDTH*(i+1), CANVAS_HEIGHT], [CARD_WIDTH*i, CANVAS_HEIGHT]], 1, 'Black', 'Green')
        else:
            canvas.draw_text(str(card_deck[i]), [NUMBER_X+CARD_WIDTH*i, NUMBER_Y], FONT_SIZE, 'White')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric