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

    def __init__(self):
        self.deck = [(s,r) for s in SUITE for r in RANKS] # list of all cards
        print(f"{len(self.deck)} card deck created")

    def split(self):
        print("Deck has been split")
        return (self.deck[:26],self.deck[26:]) # first half / second half

    def shuffle(self):
        print("Deck has been shuffled")
        return shuffle(self.deck)

class Hand:
    '''
    This is the Hand class. Each player has a Hand, and can add or remove
    cards from that hand. There should be an add and remove card method here.
    '''

    def __init__(self,hand):
        self.hand = hand

    def __str__(self):
        return f'Contains {len(self.cards)} cards'

    def add(self,dealt):
        self.hand.extend(dealt)

    def remove(self):
        return self.hand.pop()

class Player:
    """
    This is the Player class, which takes in a name and an instance of a Hand
    class object. The Player can then play cards and check if they still have cards.
    """
    def __init__(self,name,cards):
        self.name = name
        self.cards = cards
        print(f"{self.name} has been created")

    def play(self):
        drawn = self.cards.remove()
        print(f'{self.name} has placed: {drawn}')
        print()
        return drawn

    def remove_war(self):
        war = [] # grabs war cards
        if len(self.cards.hand) < 3:
            return self.cards.hand
        else:
            for x in range(3):
                war.append(self.cards.hand.pop())
            return war

    def exist(self):
        return len(self.cards.hand) != 0

######################
#### GAME PLAY #######
######################
print("Welcome to War, let's begin...")

# Use the 3 classes along with some logic to play a game of war!

# Game setup
d = Deck()
d.shuffle()
h1,h2 = d.split()

p1 = Player('Arthur',Hand(h1))
p2 = Player('Michael',Hand(h2))

p1.cards.hand
p2.cards

rounds = 0
war_count = 0

while p1.exist() and p2.exist():
    rounds += 1
    print('New round!')
    print('Standings: ')
    print(p1.name + " has the count: " + str(len(p1.cards.hand)))
    print(p2.name + " has the count: " + str(len(p2.cards.hand)))
    print('Play a card!')
    print('\n')

    table = [] # 'pot'

    p1_card = p1.play()
    p2_card = p2.play()

    table.append(p1_card)
    table.append(p2_card)

    if p1_card[1] == p2_card[1]: # WAR
        war_count += 1

        print("WAR!")

        table.extend(p1.remove_war())
        table.extend(p2.remove_war())

        # .index was the solution!
        if RANKS.index(p1_card[1]) < RANKS.index(p2_card[1]):
            p1.cards.add(table)
        else:
            p2.cards.add(table)

    else:
        if RANKS.index(p1_card[1]) < RANKS.index(p2_card[1]):
            p1.cards.add(table)
        else:
            p2.cards.add(table)

print("Game over! number of rounds: " + str(rounds))
print("War happened: " + str(war_count) + " times")

# MY OLD REDUNDANT CODE:
# ======================================================
# # The Play:
# flip1 = p1.play()
# flip2 = p2.play()
#
# # if condition and may need to add 'value' class attribute or
# # split card, grab 0, check 1-10, j > q > k > a conditions
# # problem: values j, q, k, a are not integers nor assigned values
# flip1
# flip2
#
# if int(flip1[0]) > int(flip2[0]):
#     p1Hand.add(flip1)
#     p1Hand.add(flip2)
# else:
#     p2Hand.add(flip1)
#     p2Hand.add(flip2)
#
# p1.cards
# p2.cards
#
# # If the cards are the same rank, it is War. Each player turns up three cards face
# # down and one card face up. The player with the higher cards takes both piles
# # (six cards). If the turned-up cards are again the same rank, each player places
# # another card face down and turns another card face up. The player with the
# # higher card takes all 10 cards, and so on.
# #
# if flip1[0] == flip2[0]:
#     print("WAR!")
#     p1_flip1 = p1.play()
#     p1_flip2 = p1.play()
#     p1_flip3 = p1.play()
#
#     p2_flip1 = p2.play()
#     p2_flip2 = p2.play()
#     p2_flip3 = p2.play()
