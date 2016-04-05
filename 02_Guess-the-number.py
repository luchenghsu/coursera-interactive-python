# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math

secret_number = 100
num_range = 100
count = 7

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    secret_number = random.randrange(0, num_range)
    
    global count
    count = math.trunc(math.ceil(math.log(num_range, 2)))
    
    # remove this when you add your code    
    print "New game. Range is from 0 to", num_range
    print "Number of remaining guesses is", count
    print


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
       
    global num_range
    num_range = 100
    
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    
    global num_range
    num_range = 1000
    
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    
    global count
    count = count - 1
    
    guess = int(guess)
    print "Guess was", guess
    
    if guess > secret_number:
        print "Number of remaining guesses is", count
        if count == 0:
            print "You ran out of the guesses. The number was", secret_number
            print
            new_game()
        else:
            print "Lower"
    elif guess < secret_number:
        print "Number of remaining guesses is", count
        if count == 0:
            print "You ran out of the guesses. The number was", secret_number
            print
            new_game()
        else:
            print "Higher"
    else:
        print "Correct"
        print
        new_game()
        
    print


# create frame
f = simplegui.create_frame("Guess the number", 200, 200)


# register event handlers for control elements and start frame
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
