from random import randrange

def get_shot(guesses):
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


def check_shot(shot, boat_1, boat_2, boat_3, boat_4, boat_5, boat_6, hit, miss, comp, sinked_boats):
# input: shot, all the boats, hit, miss, comp, sinked_boats
# this func checks if the shot is in boat, 
# if yes, remove the block of the boat that is hitted by the shot
# append the shot to hit or comp. If comp, sinked_boats += 1
# if not, append the shot to miss
# return: all the boats, hit, miss, comp
    if shot in boat_1:
        boat_1.remove(shot)
        if len(boat_1) < 1:
            comp.append(shot)
            sinked_boats += 1
        else:
            hit.append(shot)
    elif shot in boat_2:
        boat_2.remove(shot)
        if len(boat_2) < 1:
            comp.append(shot)
            sinked_boats += 1
        else:
            hit.append(shot)
    elif shot in boat_3:
        boat_3.remove(shot)
        if len(boat_3) < 1:
            comp.append(shot)
            sinked_boats += 1
        else:
            hit.append(shot)
    elif shot in boat_4:
        boat_4.remove(shot)
        if len(boat_4) < 1:
            comp.append(shot)
            sinked_boats += 1
        else:
            hit.append(shot)
    elif shot in boat_5:
        boat_5.remove(shot)
        if len(boat_5) < 1:
            comp.append(shot)
            sinked_boats += 1
        else:
            hit.append(shot)
    elif shot in boat_6:
        boat_6.remove(shot)
        if len(boat_6) < 1:
            comp.append(shot)
            sinked_boats += 1
        else:
            hit.append(shot)          
    else:
        miss.append(shot)
    return boat_1, boat_2, boat_3, boat_4, boat_5, boat_6, hit, miss, comp, sinked_boats


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
    return ships


hit = []
miss = []
comp = []
sinked_boats = 0 # when a boat sinks, sinked_boats += 1
num_boats = [5, 4, 3, 3, 2, 2] #this list contains all boats. Each boat is represented by its length 

ships = make_all_boats(num_boats)
while sinked_boats < 6:
    guesses = hit + miss + comp
    shot = get_shot(guesses)
    ships[0], ships[1], ships[2], ships[3], ships[4], ships[5], hit, miss, comp, sinked_boats = check_shot(shot, ships[0], ships[1], ships[2], ships[3], ships[4], ships[5], hit, miss, comp, sinked_boats)
    create_playground(hit, miss, comp)
    if sinked_boats == 6:
        print("you won")
        break



