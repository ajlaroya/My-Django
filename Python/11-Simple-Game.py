###########################
## PART 10: Simple Game ###
### --- CODEBREAKER --- ###
## --Nope--Close--Match--  ##
###########################

# It's time to actually make a simple command line game so put together everything
# you've learned so far about Python. The game goes like this:

# 1. The computer will think of 3 digit number that has no repeating digits.
# 2. You will then guess a 3 digit number
# 3. The computer will then give back clues, the possible clues are:
#
#     Close: You've guessed a correct number but in the wrong position
#     Match: You've guessed a correct number in the correct position
#     Nope: You haven't guess any of the numbers correctly
#
# 4. Based on these clues you will guess again until you break the code with a
#    perfect match!

# There are a few things you will have to discover for yourself for this game!
# Here are some useful hints:

# Try to figure out what this code is doing and how it might be useful to you
def generate():
    import random
    digits = list(range(10))
    random.shuffle(digits)
    print(digits[:3])
    return digits[:3]

# Another hint:
def guess():
    guess = input("What is your guess? ")
    seq = []
    for num in range(len(guess)):
        seq.append(int(guess[num])) # converts string input to an array

    print(seq)
    return seq

def check(x,digits):
    status = 0

    for i in range(3):
        if x[i] == digits[:3][i]:
            status += 1
    print(status)
    return status

def codebreaker(status):
    if status == 3:
        print("Congrats! You've broken the code!")
    elif status == 2:
        print("Match: You've guessed a correct number in the correct position")
    elif status == 1:
        print("Close: You've guessed a correct number but in the wrong position")
    else:
        print("Nope: You haven't guess any of the numbers correctly")

# Game logic:
gameOn = True
guessed = False

while gameOn == True:
    print("Welcome to CODEBREAKER!")
    digits = generate()

    while guessed == False:
        x = guess()
        status = check(x,digits)
        codebreaker(status)

        if status == 3:
            gameOn = False
            guessed = True


# Think about how you will compare the input to the random number, what format
# should they be in? Maybe some sort of sequence? Watch the Lecture video for more hints!
