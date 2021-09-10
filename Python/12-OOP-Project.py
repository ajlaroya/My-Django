#####################################
### WELCOME TO YOUR OOP PROJECT #####
#####################################
# TO DO:
# - add value to deck attribute?
# - find a way to get rank (and suite?) attribute
#
# For this project you will be using OOP to create a card game. This card game will
# be the card game "War" for two players, you an the computer. If you don't know
# how to play "War" here are the basic rules:
#
# The deck is divided evenly, with each player receiving 26 cards, dealt one at a time,
# face down. Anyone may deal first. Each player places his stack of cards face down,
# in front of him.
#
# The Play:
#
# Each player turns up a card at the same time and the player with the higher card
# takes both cards and puts them, face down, on the bottom of his stack.
#
# If the cards are the same rank, it is War. Each player turns up three cards face
# down and one card face up. The player with the higher cards takes both piles
# (six cards). If the turned-up cards are again the same rank, each player places
# another card face down and turns another card face up. The player with the
# higher card takes all 10 cards, and so on.
#
# There are some more variations on this but we will keep it simple for now.
# Ignore "double" wars
#
# https://en.wikipedia.org/wiki/War_(card_game)

from random import shuffle

# Two useful variables for creating Cards.
SUITE = 'Hearts Diamonds Spades Clubs'.split()
RANKS = '2 3 4 5 6 7 8 9 10 Jack Queen King Ace'.split()

class Deck:
    """
    This is the Deck Class. This object will create a deck of cards to initiate
    play. You can then use this Deck list of cards to split in half and give to
    the players. It will use SUITE and RANKS to create the deck. It should also
    have a method for splitting/cutting the deck in half and Shuffling the deck.
    """
    deck = []

    def __init__(self,suite,ranks):
        self.suite = suite
        self.ranks = ranks

        deck = []

        for s in self.suite:
            for r in self.ranks:
                Deck.deck.append(r + ' of ' + s)

        print(f"{len(Deck.deck)} card deck created")

    def split(self):
        p1_deck = Deck.deck[:26]
        p2_deck = Deck.deck[26:]
        return (p1_deck,p2_deck)

    def shuffle(self):
        return shuffle(Deck.deck)

myDeck = Deck(SUITE,RANKS)
myDeck.shuffle()
myDeck.deck
p1Deck = myDeck.split()[0]
p2Deck = myDeck.split()[1]

class Hand:
    '''
    This is the Hand class. Each player has a Hand, and can add or remove
    cards from that hand. There should be an add and remove card method here.
    '''

    def __init__(self,hand):
        print("Hand has been dealt")
        self.hand = hand

    def add(self,dealt):
        self.hand.insert(0,dealt) #'bottom' of deck

    def remove(self,removed):
        self.hand.remove(removed)

myHand = Hand(p1Deck)
myHand.hand
myHand.add('2 of Diamonds')
myHand.remove('2 of Diamonds')

class Player:
    """
    This is the Player class, which takes in a name and an instance of a Hand
    class object. The Player can then play cards and check if they still have cards.
    """
    def __init__(self,name,cards):
        self.name = name
        self.cards = cards
        print(f"{self.name} has been created")

    def __str__(self):
        return self.cards

    def play(self):
        return self.cards.pop()

player1 = Player('Arthur',myHand.hand)
player1.play()
player1.cards

######################
#### GAME PLAY #######
######################
print("Welcome to War, let's begin...")

# Use the 3 classes along with some logic to play a game of war!

# The deck is divided evenly, with each player receiving 26 cards, dealt one at a time,
# face down. Anyone may deal first. Each player places his stack of cards face down,
# in front of him.

# Game setup
deck = Deck(SUITE,RANKS)
deck.shuffle()

p1Hand = Hand(deck.split()[0]) # first half of deck
p2Hand = Hand(deck.split()[1]) # second half of deck

deck.suite

p1 = Player('Arthur',p1Hand.hand)
p2 = Player('Michael',p2Hand.hand)

p1.cards
p2.cards
#p1Hand.add('2 of Diamonds')
#p1Hand.remove('2 of Diamonds')

# The Play:
#
# Each player turns up a card at the same time and the player with the higher card
# takes both cards and puts them, face down, on the bottom of his stack.

flip1 = p1.play()
flip2 = p2.play()

# if condition and may need to add 'value' class attribute or
# split card, grab 0, check 1-10, j > q > k > a conditions
# problem: values j, q, k, a are not integers nor assigned values
flip1
flip2



if int(flip1[0]) > int(flip2[0]):
    p1Hand.add(flip1)
    p1Hand.add(flip2)
else:
    p2Hand.add(flip1)
    p2Hand.add(flip2)

len(p1.cards)
len(p2.cards)

p1.cards
p2.cards

# If the cards are the same rank, it is War. Each player turns up three cards face
# down and one card face up. The player with the higher cards takes both piles
# (six cards). If the turned-up cards are again the same rank, each player places
# another card face down and turns another card face up. The player with the
# higher card takes all 10 cards, and so on.
#
if flip1[0] == flip2[0]:
    print("WAR!")
    p1_flip1 = p1.play()
    p1_flip2 = p1.play()
    p1_flip3 = p1.play()

    p2_flip1 = p2.play()
    p2_flip2 = p2.play()
    p2_flip3 = p2.play()


# There are some more variations on this but we will keep it simple for now.
# Ignore "double" wars
