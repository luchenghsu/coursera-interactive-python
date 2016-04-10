# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
dialog = "Hit or stand?"

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define globals for Deck, player and dealer hands
deck = None
dealer_hand = None
player_hand = None


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self._cards = []
            
    def __str__(self):
        # return a string representation of a hand
        hand_str = "Hand contains "
        for i in range(len(self._cards)):
            hand_str += str(self._cards[i]) + " "
        return hand_str   

    def add_card(self, card):
        # add a card object to a hand
        self._cards.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        num_ace = 0
        
        for card in self._cards:
            hand_value += VALUES[card.get_rank()] 
            if card.get_rank() == 'A':
                num_ace += 1
        if num_ace == 0:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
        
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for card in self._cards:
            card.draw(canvas, (pos[0]+i*CARD_SIZE[0]*1.2, pos[1]))
            i += 1
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self._cards = []
        for suit in SUITS:
            for rank in RANKS:
                self._cards.append(Card(suit, rank))        

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self._cards)

    def deal_card(self):
        # deal a card object from the deck
        return self._cards.pop(len(self._cards)-1)
    
    def __str__(self):
        # return a string representing the deck
        deck_str = "Deck contains "
        for i in range(len(self._cards)):
            deck_str += str(self._cards[i]) + " "
        return deck_str   



#define event handlers for buttons
def deal():
    global outcome, in_play, dialog, score
    global deck, dealer_hand, player_hand
    
    # your code goes here
    if in_play == True:
        score -= 1
        
    deck = Deck()  
    deck.shuffle()
    
    dealer_hand = Hand()
    player_hand = Hand()
    
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    outcome = ""
    dialog = "Hit or stand?"
    in_play = True


def hit():
    global outcome, score, in_play, dialog
    global deck, player_hand
 
    # if the hand is in play, hit the player
    if in_play == True:
        player_hand.add_card(deck.deal_card())
        
        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome = "You went bust and lose"
            dialog = "New deal?"
            in_play = False
            score -= 1

              
def stand():
    global outcome, score, in_play, dialog
    global deck, player_hand, dealer_hand
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        
        # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            outcome = "Dealer went bust and you win"
            score += 1
        else:
            if dealer_hand.get_value() >= player_hand.get_value():
                outcome = "You lose."
                score -= 1
            else:
                outcome = "You win."
                score += 1
                
        dialog = "New deal?"
        in_play = False    
    

# draw handler    
def draw(canvas):
    global outcome, score, dialog, in_play
    global player_hand, dealer_hand
    
    canvas.draw_text('Blackjack', (100, 100), 30, 'Aqua','sans-serif')
    canvas.draw_text('Score ' + str(score), (400, 100), 25, 'Black','sans-serif')
    
    canvas.draw_text('Dealer', (70, 160), 25, 'Black', 'sans-serif')
    canvas.draw_text(outcome, (200, 160), 25, 'Black', 'sans-serif')
    dealer_hand.draw(canvas, [70, 180])
    
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [70+CARD_BACK_CENTER[0], 180+CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
       
    canvas.draw_text('Player', (70, 400), 25, 'Black', 'sans-serif')
    canvas.draw_text(dialog, (200, 400), 25, 'Black', 'sans-serif')
    player_hand.draw(canvas, [70, 420])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric