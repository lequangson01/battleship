from random import randrange
import random

"""
both user and computer funcs:
"""
def check_ok(boat, taken_positions):
# input: boat, taken_positions 
# this func checks if the boat outside the playground or the position of the boat is already in taken_position
# return: boat. boat will returned as [-1] or its specific position
    boat.sort()
    for i in range(len(boat)):
        if boat[i] in taken_positions:
        #this condition checks if the block boat[i] is already in the list taken_positions
            boat = [-1]
            break            
        elif boat[i] > 99 or boat[i] < 0:
        #this condition checks border 1 and 3
            boat = [-1]
            break
        elif boat[i] % 10 == 9 and i < len(boat) - 1:
        #this condition checks border 2 and 4
            if boat[i + 1] % 10 == 0:
                boat = [-1]
                break
            
        if i != 0:
        # this condition checks if there is any hole in the boat
            if boat[i] != boat[i - 1] + 1 and boat[i] != boat[i - 1] + 10:
                boat = [-1]
                break
    return boat    


def check_shot(shot, ships, hit, miss, comp, sinked_boats):
# input: shot, all the boats (ships), hit, miss, comp, sinked_boats
# this func initially assumes that the shot is missed (cond = 0)
# given a shot, this func uses a for-loop that goes through all ships to see if the shot hits one of the ships 
# if yes, remove the block of the boat that is hitted by the shot
# append the shot to hit or comp. If comp, sinked_boats += 1
# if not, append the shot to miss
# return: all the boats (ships), hit, miss, comp, cond, sinked_boats
    cond = 0 # miss
    for i in range(len(ships)):
        if shot in ships[i]:
            ships[i].remove(shot)
            if len(ships[i]) > 0:
                hit.append(shot)
                cond = 1 # hit
            else:
                comp.append(shot)
                cond = 2 # comp
                sinked_boats += 1      
    if cond == 0: # miss
        miss.append(shot) 
    return ships, hit, miss, comp, cond, sinked_boats


def create_playground(hit, miss, comp):
# input: hit, miss, comp
# this func creates the playground with the status of each block 
# print the playground
    print("           battleship")
    print("    0  1  2  3  4  5  6  7  8  9")
    
    block = 0 #this variable keep track of the spot of the block
    for i in range(10):
        #create each row
        row = ""
        for j in range(10):
        #create each spot on the specific row
            character = "_  "
            if block in miss:
                character = "x  "
            elif block in hit:
                character = "o  "               
            elif block in comp:
                character = "Q  "
            row += character
            block += 1 #the block var increments 1 after each character is add to row
        print(i, " ", row)
        print("")


def check_empty(ships):
# input: ships
# [] = False, [#have element] = True
# this func checks each ship in the 2D list ships
# if ship is empty, return True, and vice versa
# if all ships are empty, return True, else return False
# return True or False 
    return all([not elem for elem in ships])


"""
user - 2 funcs:
"""
def create_ships_u(taken_positions, num_boats):
# input: num_boats
# this func has a loop that makes all boats,
# which calls the get_ship(len_of_boat, taken_positions) that creates a single boat
# return: ships, which are the 2D list has len(num_boats) that contains the positions of all boats
    ships = [] #this is a 2D list contains the positions of all boats
    for len_of_boat in num_boats:
        ship, taken_positions = get_ship(len_of_boat, taken_positions)
        ships.append(ship)
    return ships, taken_positions

  
def create_playground_u(taken_positions):
    print("            battleships    ")
    print("     0  1  2  3  4  5  6  7  8  9")
  
    place = 0
    for x in range(10):
        row = ""
        for y in range(10):
            ch = " _ "
            if place in taken_positions:
                ch = " o " 
            row = row + ch
            place = place + 1
              
        print(x," ",row)


def get_ship(len_of_boat, taken_positions):
# input: len_of_boat, taken_positions
# this func gets the boat's position from the user's input
# this func checks both the type of the input(is it int) and if the boat is inside playground/in taken_positions/in correct order   
# return a valid ship   
    while True:
        ship = []
        print("enter your ship of length", len_of_boat)
        for i in range(len_of_boat):
            while True:
                try:
                    boat_num = input("please enter a number: ")
                    ship.append(int(boat_num))
                except ValueError: # better try again... Return to the start of the loop
                    print("wrong type of input")
                    continue
                else: # is is a correct input, and we're ready to exit the loop
                    break
            ship = check_ok(ship, taken_positions)

        if -1 not in ship: # check if a ship is valid. If yes, add the ship to taken_positions and break
            taken_positions += ship
            break
        else:
            print("invalid number - please enter again")
    return ship, taken_positions


def get_shot_user(guesses):
# input: guesses is the combined list of hit, miss, comp
# this funcs asks the user to enter the shot, then checks the validity of the shot 
# return: the valid shot
    while True:
        try:
            shot = int(input("Enter your shot: "))
            if shot < 0 or shot > 99:
                shot = int(input("Enter your shot:"))
            elif shot in guesses:
                print("already guessed - please enter again")
            else:
                return shot
        except:
            print("incorrect - please enter integer only")


"""
computer - 1 funcs:
"""
def create_ships_c(taken_positions, num_boats):
# input: num_boats
# this funcs has a loop that makes all boats,
# which calls the create_boat() that creates a single boat
# return: ships, which are the 2D list has len(num_boats) that contains the positions of all boats
    ships = [] #this is a 2D list contains the positions of all boats
    for len_of_boat in num_boats:
        boat_position = [-1] #create the initial position of every boat is [-1]
        while -1 in boat_position:
            boat_start = randrange(99) #boat starting point
            boat_direction = randrange(1, 4) #{1: "up", 2: "right", 3: "down", 4: "left"}
            boat_position = create_boat(len_of_boat, boat_start, boat_direction, taken_positions) #return the position of boat
        #a new boat is created after finishing the while loop
        ships.append(boat_position)
        taken_positions += boat_position #add all positions of the newly created boat to the list taken_positions
    return ships, taken_positions


def create_boat(len_of_boat, boat_start, boat_direction, taken_positions):
# input: len_of_boat, boat_start, boat_direction, taken_positions
# this func initializes boat = []
# with len_of_boat, boat_start, boat_direction, this func create the position of the boat
# calls check_ok(boat, taken_positions) to see if the boat outside playground or the position of the boat is already in taken_position
# return: boat. boat will returned as [-1] or its specific position
    boat = []
    if boat_direction == 1:
        for i in range(len_of_boat):
            boat.append(boat_start - i * 10) # already have the position of boat after this line
            boat = check_ok(boat, taken_positions)
    elif boat_direction == 2:
        for i in range(len_of_boat):
            boat.append(boat_start + i)
            boat = check_ok(boat, taken_positions)
    elif boat_direction == 3:
        for i in range(len_of_boat):
            boat.append(boat_start + i * 10)
            boat = check_ok(boat, taken_positions)
    elif boat_direction == 4:
        for i in range(len_of_boat):
            boat.append(boat_start - i)
            boat = check_ok(boat, taken_positions)
    return boat


def get_shot_comp(guesses, tactics):
# input: guesses (all moves), tactics(which is the list of all valid possible moves for the shot)
# in the first mơve, tactics = []
# this func checks if len(tactics) > 0
# if yes, pick shot = tactics[0]
# if no, pick shot = randrange(99)
# this func check if shot not in guesses(which is the list of all moves) 
# if yes, guess.append(shot), and break
# return: the valid shot, guesses
    while True:
        try:
            if len(tactics) > 0:
                shot = tactics[0]
            else:
                shot = randrange(99)
            
            if shot not in guesses:
                guesses.append(shot)
                break
        except:
            print("incorrect - please enter integer only")
    return shot, guesses


def calculate_tactics(shot, tactics, guesses, hit):
# input: shot, tactics, guesses, hit
# this function takes the newly shot, and changes the tactics list accordingly
# the list temp is the possible positions that the next shot can be
# if the shot hits the first time, len(tactics) = 0. Then, temp is the list contains 4 blocks around the shot
# else, the list temp will be created based on the last 2 shots
# candidate is the list of valid possible shots that is created from temp
# shuffle the order of elements inside candidate
# return: candidate (candidate is tactics)
    temp = []
    if len(tactics) < 1:
    # got 1 hit the first time 
        temp = [shot - 1, shot + 1, shot - 10, shot + 10] # temporary places that the next shot could be  
    else: 
    # got at least 2 hits 
    # checks to see if the 4 spots around is in hit
        if shot - 1 in hit: # east
            temp = [shot + 1]
            for num in [2, 3, 4, 5, 6, 7, 8]:
                if shot - num not in hit:
                    temp.append(shot - num) 
                    break

        elif shot + 1 in hit: # west
            temp = [shot - 1]
            for num in [2, 3, 4, 5, 6, 7, 8]:
                if shot + num not in hit:
                    temp.append(shot + num) 
                    break
        
        elif shot - 10 in hit: # south
            temp = [shot + 10]
            for num in [20, 30, 40, 50, 60, 70, 80]:
                if shot - num not in hit:
                    temp.append(shot - num) 
                    break
        
        elif shot + 10 in hit: # north. Ex: first shot is 50, next shot is 40
            temp = [shot - 10]
            for num in [20, 30, 40, 50, 60, 70, 80]:
                if shot + num not in hit:
                    temp.append(shot + num) 
                    break
    
    candidate = [] # list of valid places that the next shot could be
    for i in range(len(temp)):
        if temp[i] not in guesses and temp[i] < 100 and temp[i] > -1: #checks the validity of places in temp
            candidate.append(temp[i])
    random.shuffle(candidate) # shuffle the element order of the list candidate
    return candidate



"""
main program:
"""
num_boats = [5, 4, 3, 3, 2, 2] # this list contains all boats. Each boat is represented by its length 

# before game
# computer - 1
hit1 = []
miss1 = []
comp1 = []
guesses1 = []
cond1 = 0
tactics1 = [] # list of possible moves after a boat is hitted. After a boat is sunked, tactics reset to []
taken_positions1 = []
sinked_boats1 = []

# user - 2
hit2 = []
miss2 = []
comp2 = []
guesses2 = []
cond2 = 0
tactics2 = []
taken_positions2 = []
sinked_boats2 = []

# computer creates ships for player 1
ships1, taken_positions1 = create_ships_c(taken_positions1, num_boats) 
# user creates boat for player 2 - show board
ships2, taken_positions2 = create_ships_u(taken_positions2, num_boats)
create_playground_u(taken_positions2)

# loop for user and computer takes turn to shoot, and repeat until finding a winner:
turns = 0
while True: 
    turns += 1

# USER SHOOTS: using 1 because it is checking the data of computer
    guesses1 = hit1 + miss1 + comp1
    shot1 = get_shot_user(guesses1)
    ships1, hit1, miss1, comp1, cond1, sinked_boats1 = check_shot(shot1, ships1, hit1, miss1, comp1, sinked_boats1)
    create_playground(hit1, miss1, comp1)

# check if all of the computer ships are empty:
    if check_empty(ships1):
        print("end of game - winner in", turns)
        break

# COMPUTER SHOOTS:
    guesses2 = hit2 + miss2 + comp2
    shot2, guesses2 = get_shot_comp(guesses2, tactics2) 
    ships2, hit2, miss2, comp2, cond2, sinked_boats2 = check_shot(shot2, ships2, hit2, miss2, comp2, sinked_boats2)
    create_playground(hit2, miss2, comp2)

    if cond2 == 1:
        # got 1 hit
        tactics2 = calculate_tactics(shot2, tactics2, guesses2, hit2)
    elif cond2 == 2:
        # comp, and sunk the boat
        # reset tactics = []
        tactics2 = []
    elif len(tactics2) > 0: #len(tactics) > 0 means that there are still possible moves
        # got 1 hit, then miss
        # remove the newly shot from tactics
        tactics2.pop(0)
    # in case all 3 statements above are False, which means there is no hit in the first place, tactics is still []

# check if all of the computer ships are empty:
    if check_empty(ships2):
            print("end of game - computer wins in", turns)
            break

# after both the user and computer shoot, start a new loop:

