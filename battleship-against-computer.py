from random import randrange
import random

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


def create_playground_comp(taken_positions):
# input: hit, miss, comp
# this func creates the playground with the status of each block 
# print the playground
    print("")
    print("           battleship")
    print("    0  1  2  3  4  5  6  7  8  9")
    
    block = 0 #this variable keep track of the spot of the block
    for i in range(10):
        #create each row
        row = ""
        for j in range(10):
        #create each spot on the specific row
            character = "_  "
            if block in taken_positions:
                character = "o  "
            row += character
            block += 1 #the block var increments 1 after each character is add to row
        print(i, " ", row)
        print("")


def create_playground(hit, miss, comp):
# input: hit, miss, comp
# this func creates the playground with the status of each block 
# print the playground
    print("")
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


def check_ok(boat, taken_positions):
# input: boat, taken_positions 
# this func checks if the boat outside the playground or the position of the boat is already in taken_position
# return: boat. boat will returned as [-1] or its specific position
    for i in range(len(boat)):
        if boat[i] in taken_positions:
        #this condition checks if the block boat[i] is already in the list taken_positions
            boat = [-1]
            break            
        elif boat[i] > 99 or boat[i] < 0:
        #this condition checks border 1 and 3
            boat = [-1]
            break
        elif boat[i] % 10 == 9 and i < len(boat)-1:
        #this condition checks border 2 and 4
            if boat[i+1] % 10 == 0:
                boat = [-1]
                break
    return boat    


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


def make_all_boats(num_boats):
# input: num_boats
# this funcs has a loop that makes all boats,
# which calls the create_boat() that creates a single boat
# return: ships, which are the 2D list has len(num_boats) that contains the positions of all boats
    taken_positions = [] #this list contains all blocks that are already have boats on them    
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
    else: # got 2 hits 
        # 4. shot = 40, tactics = [40, 60], guesses = [49, 50, 51, 40], hit = [50, 40]
        if shot - 1 in hit: # checks to see if the 4 spots around is in hit
            if shot - 2 in hit:
                temp = [shot - 3, shot + 1]
            else:
                temp = [shot - 2, shot + 1]

        elif shot + 1 in hit:
            if shot + 2 in hit:
                temp = [shot + 3, shot - 1]
            else:
                temp = [shot + 2, shot - 1]
        
        elif shot - 10 in hit:
            if shot - 20 in hit:
                temp = [shot - 30, shot + 10]
            else:
                temp = [shot - 20, shot + 10]
        
        elif shot + 10 in hit:
            if shot + 20 in hit:
                temp = [shot + 30, shot - 10]
            else:
                temp = [shot + 20, shot - 10]
    
    candidate = [] # list of valid places that the next shot could be
    for i in range(len(temp)):
        if temp[i] not in guesses and temp[i] < 100 and temp[i] > -1: #checks the validity of places in temp
            candidate.append(temp[i])
            # 2. candidate = [51, 40, 60]
            # 4. candidate = [60, 30]
    random.shuffle(candidate) # shuffle the element order of the list candidate
    return candidate

# main func
hit = []
miss = []
comp = []
guesses = []
num_boats = [5, 4, 3, 3, 2, 2] #this list contains all boats. Each boat is represented by its length 
sinked_boats = 0 # when a boat sinks, sinked_boats += 1
tactics = [] # list of possible moves after a boat is hitted. After a boat is sunked, tactics reset to []

ships, taken_positions = make_all_boats(num_boats) 
create_playground_comp(taken_positions) # first, create a visible playground with ships that the user can see their positions

turns = 0
while sinked_boats != len(num_boats):
    # for example, ships =[[40, 50, 60]]
    shot, guesses = get_shot_comp(guesses, tactics) 
    # 1. shot spot 49
    # 2. shot spot 50
    # 3. shot spot 51
    # 4. shot spot 40
    # 5. shot spot 30
    # 6. shot spot 60
    ships, hit, miss, comp, cond, sinked_boats = check_shot(shot, ships, hit, miss, comp, sinked_boats)
    # 1. spot 49 is missed. return cond = 0
    # 2. spot 50 is hitted. return cond = 1
    # 3. spot 51 is missed. return cond = 0
    # 4. spot 40 is hitted. return cond = 1
    # 5. spot 30 is missed. return cond = 0
    # 6. spot 60 is hitted. return cond = 2
    if cond == 1:
        tactics = calculate_tactics(shot, tactics, guesses, hit)
        # 2. shot = 50, tactics = [], guesses = [49, 50], hit = [50]
        # return tactics = [51, 40, 60]. len(tactics) = 3
        # 4. shot = 40, tactics = [40, 60], guesses = [49, 50, 51, 40], hit = [50, 40]
        # return tactics = [60, 30]. len(tactics) = 2
    elif cond == 2:
        # sunk the boat
        # reset tactics = []
        # 6. tactics = []
        tactics = []
    elif len(tactics) > 0: #len(tactics) > 0 means that there are still possible moves
        # got 1 hit, then miss
        # remove the newly shot from tactics
        # 3. tactics = [40, 60]
        tactics.pop(0)
    # in case all 3 statements above are False, which means there is no hit in the first place, tactics is still []
    turns += 1
create_playground(hit, miss, comp)
print(turns)