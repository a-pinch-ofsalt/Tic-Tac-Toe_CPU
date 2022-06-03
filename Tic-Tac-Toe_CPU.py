#Please note I'm not exactly sure how to properly document classes so I'm just going on what I found on stackoverflow, feedback appreciated :)

import random
import logging

logging.basicConfig(level=logging.DEBUG)

autowin = False

class board:
    """
    An imaginary tic-tac-toe board (perhaps with pieces on it).
    
    Attributes:
        openspaces      a list of all spaces on the board that are unoccupied.
        occupiedspaces  a list of all spaces on the board that are occupied,
                        along with information describing space's occupant
        visualization   a string that visualizes the state of the board. '#' symbols
                        represent open spaces.
    """
    def __init__(self, boardstate):
        
        self.openspaces = [v[0] for i, v in enumerate(boardstate) if not v[1]]
        
        self.occupiedspaces = [[v[0], v[2]] for i, v in enumerate(boardstate) if v[1]]
        self.visualization = "#########"
        for i, v in enumerate(self.occupiedspaces):
            self.visualization = self.visualization[:v[0] - 1]+v[1]+self.visualization[v[0]:]


def cpumove(diff, boardinstance, playerpiec):
    """
    Decides on the most optimal move and plays it (or doesn't,
    depending on the player's chosen difficulty)

    Args:
        
        diff (str): The player's desired difficulty, determines whether
        the most optimal move will be played. More info in comments
        
        boardinstance (board): a board instance containing all of the
        necessary information for the CPU to decide on the most optimal move

        playerpiec (str): The player's piece type (x or o).
    
    Returns:
        int: represents CPU's move on the current board
    """
    
    global autowin
    cpupiece = None
    
    #Randomly decide whether to play perfectly or randomly. Higher difficulty
    #raises chance of perfect move. Easy difficulty will never move perfectly,
    #and Impossible difficulty will always move perfectly
    
    perfection, perfectionchance, perfectionmove = False, 0, False

    if diff == "EASY":
        perfection = False
    elif diff == "MEDIUM":
        perfection, perfectionchance = True, 3
    elif diff == "HARD":
        perfection, perfectionchance = True, 2
    
    if perfection and random.randrange(1, perfectionchance + 1) == 1 or diff == "IMPOSSIBLE":
        perfectionmove = True
        

    #Algorithm for perfect move
    
    rows = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    columns = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    diagonals = [[1, 5, 9], [3, 5, 7]]

    center = [5]
    corners = [1, 3, 7, 9]
    sides = [2, 4, 6, 8]
    
    orderofpriority = [center, corners, sides]
    
    if len(boardinstance.occupiedspaces) == 0 and center in boardinstance.openspaces:
        return center
    
    if playerpiec == "X": cpupiece = "O"
    elif playerpiec == "O": cpupiece = "X"
        
    cpupiecelocations = [v[0] for i, v in enumerate(boardinstance.occupiedspaces) if v[2] == cpupiece]
    playerpiecelocations = [v[0] for i, v in enumerate(boardinstance.occupiedspaces) if v[2] == playerpiec]
    

    ##Detect if there are any obvious moves (blocking opponent or winning)
    if perfectionmove == True:
        for i, v in enumerate([rows, columns, diagonals]):
            
            #Search for open win opportunities
            for a, b in enumerate(v):
                count = 0
                notfound = 0
                for c, d in enumerate(b):
                    if d in cpupiecelocations:
                        count += 1
                    else: notfound = d
                if count == 2 and notfound in boardinstance.openspaces:
                        return notfound
            
            #Search for imminent loss opportunities
            for a, b in enumerate(v):
                count = 0
                opening = 0
                for c, d in enumerate(b):
                    if d in playerpiecelocations:
                        count += 1
                    else: opening = d
                if count == 2 and opening in boardinstance.openspaces:
                        return opening
        
        #Avoid the classic trap of triple corners
        if cpupiece == "O" and len(cpupiecelocations) == 1:
            if 1 in playerpiecelocations and 9 in playerpiecelocations:
                return random.choice(sides)
            elif 3 in playerpiecelocations and 7 in playerpiecelocations:
                return random.choice(sides)
        
        #If O's first move is on a side, X has an automatic win. This code block allows the cpu to take advantage of that.
        if cpupiece == "X":
            if len(playerpiecelocations) == 1 and playerpiecelocations[0] in sides:
                autowin = True
        
        if autowin == True and len(playerpiecelocations) == 2:
            for i, v in enumerate(corners):
                if v in boardinstance.openspaces:
                    if v == 1 or v == 7:
                        if v + 1 not in playerpiecelocations and 4 not in playerpiecelocations:
                            return v
                    if v == 3 or v == 9:
                        if v - 1 not in playerpiecelocations and 6 not in playerpiecelocations:
                            return v
        
        #As a last resort, just pick the one in highest order of priority
        for i, v in enumerate(orderofpriority):
            for a, b in enumerate(v):
                if b in boardinstance.openspaces:
                    return b
    
    #If CPU decides not to move perfectly, just move randomly on an open space
    return random.choice(boardinstance.openspaces)


def gameinstance(difficulty, playerpiece):
    
    """
    Creates a game, except I didn't really feel like making a class for this lol
    
    Args:
        
        difficulty (str): The player's desired difficulty

        playerpiece (str): The player's piece type (x or o)

    Returns:
        Nothing, it only prints out the result of the game (win, loss, tie)
        and returns nothing to end the script.
    """

    rows = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    columns = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    diagonals = [[1, 5, 9], [3, 5, 7]]
    
    newboard = board([[i, False] for i in range(1, 10)])
    
    #Displays board visualization
    print(newboard.visualization[:3]+"\n"+newboard.visualization[3:6]+"\n"+newboard.visualization[6:])
    
    playerturn = False
    
    #Repeats turn-based pattern (cpu, player, cpu, ...) until win, loss, or tie
    while True:
        
        if newboard.openspaces == []:
            print("Tie!")
            return
        
        if playerpiece == "X":
            opponentpiece = "O"
            if len(newboard.occupiedspaces) == 0:
                playerturn = True
        elif playerpiece == "O":
            opponentpiece = "X"
        
        #Gives bot info about the game, then the bot returns its move selection
        #and it is processed into the game
        if not playerturn:
            cpuoption = cpumove(difficulty, newboard, playerpiece)
            newboard.openspaces.remove(cpuoption)
            newboard.occupiedspaces.append([cpuoption, True, opponentpiece])
            newboard.visualization = newboard.visualization[:cpuoption - 1]+opponentpiece+newboard.visualization[cpuoption:]
            print("\nCPU goes:\n"+newboard.visualization[:3]+"\n"+newboard.visualization[3:6]+"\n"+newboard.visualization[6:])
            playerturn = True
        
        #Prompts player their desired move given the information provided in the display,
        #takes player's move and processes it into the game
        elif playerturn:
            playeroption = int(input("Player goes (please input the number of the space you want to go in. If you're confused on what number to input, just look at a phone keypad and you'll understand.):"))
            if playeroption not in newboard.openspaces:
                print("The move you played was illegal (a piece was already there, or the desired move wasn't on the board). Unfortunately, I am far too lazy to code a retry function so I guess you'll just have to restart (sorry) :P")
                return
            newboard.openspaces.remove(playeroption)
            newboard.occupiedspaces.append([playeroption, True, playerpiece])
            newboard.visualization = newboard.visualization[:playeroption - 1]+playerpiece+newboard.visualization[playeroption:]
            print("\nPlayer goes:\n"+newboard.visualization[:3]+"\n"+newboard.visualization[3:6]+"\n"+newboard.visualization[6:])
            playerturn = False
        
        playerpiecelocs = [v[0] for i, v in enumerate(newboard.occupiedspaces) if v[2] == playerpiece]
        opponentpiecelocs = [v[0] for i, v in enumerate(newboard.occupiedspaces) if v[2] == opponentpiece]
        
        for i, v in enumerate([rows, columns, diagonals]):
            for a, b in enumerate(v):
                cpucount = 0
                playercount = 0
                for c, d in enumerate(b):
                    if d in opponentpiecelocs:
                        cpucount += 1
                    if d in playerpiecelocs:
                        playercount += 1
                if cpucount == 3:
                    print("CPU won!")
                    return
                elif playercount == 3:
                    print("You won!")
                    return
        
def startup():
    """
    Prompts player for their desired piece and difficulty, then
    starts a game
    """
    hardness = input("Please type desired difficulty (easy, medium, hard, impossible): ")
    if hardness.lower() not in "easy medium hard impossible".split(): 
        print("The difficulty type is invalid. Please restart.")
        return
    piece = input("Please type desired piece type (x or o): ")
    
    if piece.upper() not in "XO": 
        print("The piece type is invalid. Please restart.")
        return
    
    print("The game has begun. Good luck!")
    gameinstance(hardness.upper(), piece.upper())
startup()

