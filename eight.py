from __future__ import print_function
from queue import PriorityQueue
import sys
import math
import time
import random
import argparse 

# Code for AI Class Programming Assignment 1
# Written by Chris Archibald
# archibald@cs.byu.edu
# Last Updated January 24, 2020

# GOAL: (0 is the blank tile)
# 0 1 2
# 3 4 5
# 6 7 8

class Puzzle():
    """
    This is the 8-puzzle class.  You shouldn't have to modify it at all.
    """  

    def __init__(self, arrangement):
        """
        The state (and arrangement passed in) is a list of length 9, that stores which tile is in each place
        In a solved puzzle, each place number holds the tile of the same number
        i.e. solution is state = [0,1,2,3,4,5,6,7,8]
        """
        self.state = arrangement[:]
        self.blank = None

        for i in range(len(self.state)):
            if self.state[i] == 0:
                self.blank = i

    def print_puzzle(self):
        """
        Print a visual description of the puzzle to the output
        """
        k = 0
        for i in range(3):
            for j in range(3):
                print('', end="") 
                print(self.state[k], end="")
                k = k + 1
            print('')
        
    def get_moves(self):
        """
        The moves correspond to the motion of the tile into the blank space
        it can be U (up), D (down), R (right), or L (left)
        """
        invalid_moves = []
        if self.blank < 3:
            invalid_moves.append('D')
        if self.blank > 5:
            invalid_moves.append('U')
        if self.blank % 3 == 0:
            invalid_moves.append('R')
        if self.blank % 3 == 2:
            invalid_moves.append('L')

        base_moves = ['U', 'D', 'L', 'R']
        valid_moves = []
        for m in base_moves:
            if m not in invalid_moves:
                valid_moves.append(m)

        return valid_moves

    def do_move(self, move):
        """
        Modify the state by performing the given move.
        This assumes that the move is valid
        """
        swapi = 0
        if move == 'U':
            swapi = self.blank + 3
        if move == 'D':
            swapi = self.blank - 3
        if move == 'L':
            swapi = self.blank + 1
        if move == 'R':
            swapi = self.blank - 1

        temp = self.state[swapi]
        self.state[swapi] = self.state[self.blank]
        self.state[self.blank] = temp
        self.blank = swapi

    def undo_move(self, move):
        """
        This modifies the state by undoing the move.  For use in recursive search
        Assumes the move was a valid one
        """
        swapi = 0
        if move == 'D':
            swapi = self.blank + 3
        if move == 'U':
            swapi = self.blank - 3
        if move == 'R':
            swapi = self.blank + 1
        if move == 'L':
            swapi = self.blank - 1

        temp = self.state[swapi]
        self.state[swapi] = self.state[self.blank]
        self.state[self.blank] = temp
        self.blank = swapi
        
    def is_solved(self):
        """
        Returns True if the puzzle is solved, False otherwise
        """
        ######## TASK 1.1 BEGIN ##########
        
        #Add code to determine whether this puzzle is solved
        
        return (self.state == [0,1,2,3,4,5,6,7,8])

        ######## TASK 1.1 END   ##########


    def __repr__(self):
        return "".join([str(i) for i in self.state])

    def id(self):
        """
        Returns the string representation of this puzzle's state. 
        Useful for storing state in a dictionary
        """
        return self.__repr__()

class SearchNode():
    """
    Our search node class
    """
    def __init__(self,cost,puzzle,path,options):
        """
        Initialize all the relevant parts of the search node
        """
        self.cost = cost
        self.puzzle = puzzle
        self.path = path
        self.options = options
        self.h = heuristic(self,self.options)
        self.compute_f_value()
       
    def compute_f_value(self):
        """
        Compute the f-value for this node
        """
        ######## TASK 1.3 BEGIN ##########
        
        #Modify these lines to implement the search algorithms (greedy, Uniform-cost or A*)
        self.h = heuristic(self, self.options)
        self.f_value = 0

        if self.options.type == 'g':
            #greedy search algorithm
            self.f_value = self.h # Change this to implement greedy!

        elif self.options.type == 'u':
            #uniform cost search algorithm
            self.f_value = self.cost # Change this to implement uniform cost search!

        elif self.options.type == 'a':
            #A* search algorithm
            self.f_value = self.h + self.cost # Change this to implement A*!

        else:
            print('Invalid search type (-t) selected: Valid options are g, u, and a')
            sys.exit()

        ######## TASK 1.3 END   ##########

    #Comparison operator. Don't modify this or best-first search might stop working
    def __lt__(self,other):
        """
        Comparison operator so that nodes will be sorted in priority queue based on f-value
        """
        return self.f_value < other.f_value	

def heuristic(node,options):
    """
    This is the function that is called from the SearchNode class to get the heuristic value for a node
    """
    if options.function == 'top':
        return tiles_out_of_place(node.puzzle)
    elif options.function == 'torc':
        return tiles_out_of_row_column(node.puzzle)
    elif options.function == 'md':
        return manhattan_distance_to_goal(node.puzzle)
    else:
        print('Invalid heristic selected. Options are top, torc, and md')
        sys.exit()    

def tiles_out_of_place(puzzle):
    """
    This heuristic counts the number of tiles out of place.    
    """
    #Keep track of the number of tiles out of place
    num_out_of_place = 0
    
    #Cycle through all of the places in the puzzle and see if the right tile is there
    # (We ignore place 0 since that is where the blank tile goes and we shouldn't count it)
    for i in range(1,len(puzzle.state)):
    
        # The tile in place i ( puzzle.state[i] ) should be tile i.  
        # If it isn't increment out of place counter
        # (To compare tile (string) with place (int), we must first convert from string to int as such:
        #  int(puzzle.state[i])
    
        if puzzle.state[i] != i:
            num_out_of_place += 1
 
    return num_out_of_place
    
    
def tiles_out_of_row_column(puzzle):
    """
    This heuristic counts the number of tiles that are in the wrong row, 
    the number of tiles that are in the wrong column
    and returns the sum of these two numbers.
    Remember not to count the blank tile as being out of place, or the heuristic is inadmissible
    """
    ######## TASK 1.4.1 BEGIN   ##########

    # YOUR TASK 1.4.1 CODE HERE
    sins = 0
    for i in range(len(puzzle.state)):
        val = puzzle.state[i]
        if(val == 0):
            continue
        
        actualRow = get_tile_row(i)
        expectedRow = get_tile_row(val)
        if (actualRow != expectedRow):
            sins += 1
        
        actualCol = get_tile_column(i)
        expectedCol = get_tile_row(val)
        if (actualCol != expectedCol):
            sins += 1

    return sins
    
    ######## TASK 1.4.1 END   ##########

def manhattan_distance_to_goal(puzzle):
    """
    This heuristic should calculate the sum of all the manhattan distances for each tile to get to 
    its goal position.  Again, make sure not to include the distance from the blank to its goal.
    """
    
    ######## TASK 1.4.2 BEGIN   #########

    # YOUR TASK 1.4.2 CODE HERE
    
    totalDistance = 0
    for i in range(len(puzzle.state)):
        val = puzzle.state[i]
        if(val == 0):
            continue
        
        actualRow = get_tile_row(i)
        expectedRow = get_tile_row(val)
        totalDistance += abs(expectedRow - actualRow)
        
        actualCol = get_tile_column(i)
        expectedCol = get_tile_row(val)
        totalDistance += abs(expectedCol - actualCol)

    return totalDistance
    
    ######## TASK 1.4.2 END   ##########  

    
def get_tile_row(tile):
    """
    Return the row of the given tile location (Helper function for you to use)
    """
    return int(tile / 3)

def get_tile_column(tile):
    """
    Return the column of the given tile location (Helper function for you to use)
    """
    return tile % 3    
    
def run_iterative_search(start_node):
    """
    Run Iterative Deepening A* (IDA*) search starting from start_node.
    Thresholds increase on the combined g+h cost until a solution is found or limits are hit.
    """
    options = start_node.options

    def heuristic_value(puzzle):
        if options.function == 'top':
            return tiles_out_of_place(puzzle)
        if options.function == 'torc':
            return tiles_out_of_row_column(puzzle)
        if options.function == 'md':
            return manhattan_distance_to_goal(puzzle)
        print('Invalid heuristic selected. Options are top, torc, and md')
        sys.exit()

    # Initial f-cost threshold is the heuristic cost of the start state
    threshold = start_node.cost + heuristic_value(start_node.puzzle)

    max_threshold = 200
    total_expanded = 0

    while threshold <= max_threshold:
        visited = set()
        nodes_expanded = 0
        root_puzzle = Puzzle(start_node.puzzle.state[:])
        visited.add(root_puzzle.id())

        def ida_search(puzzle, path, g_cost, current_threshold):
            nonlocal nodes_expanded
            nodes_expanded += 1

            f_cost = g_cost + heuristic_value(puzzle)
            if f_cost > current_threshold:
                return False, f_cost

            if puzzle.is_solved():
                return True, path

            min_threshold = math.inf

            for move in puzzle.get_moves():
                child = Puzzle(puzzle.state[:])
                child.do_move(move)
                child_id = child.id()

                if child_id in visited:
                    continue

                visited.add(child_id)
                found, result = ida_search(child, path + move, g_cost + 1, current_threshold)
                if found:
                    return True, result
                if result < min_threshold:
                    min_threshold = result
                visited.remove(child_id)

            return False, min_threshold

        found_solution, outcome = ida_search(root_puzzle, start_node.path, start_node.cost, threshold)
        total_expanded += nodes_expanded

        if found_solution:
            print('IDA* SOLVED THE PUZZLE: SOLUTION = ', outcome)
            print('Expanded ', total_expanded, 'nodes')
            return total_expanded, len(outcome)

        if outcome == math.inf:
            break

        threshold = outcome

    return None, None
        
def run_best_first_search(fringe, options):
    """
    Runs an arbitrary best-first search.  To change which search is run, modify the f-value 
    computation in the search nodes

    fringe is a priority queue of search nodes, ordered by f-values
    """
    #Create our data structure to track visited/expanded states
    visited = dict()
    
    #Variable to tell when we are done
    done = False
                
    #Main search loop.  Keep going as long as we are not done and the FRINGE isn't empty
    while not done and not fringe.empty():
        
        #Get the next SearchNode from the FRINGE
        cur_node = fringe.get()
        
        #Add it to our set of visited/expanded states (join creates a string from the state)
        visited[cur_node.puzzle.id()] = True
        
        #Don't continue if the cost is too much
        if cur_node.cost > 200:
            #None of the puzzles are this long, so we shouldn't continue further on this path
            continue
            
        #Check to see if this node's puzzle state is a goal state
        if cur_node.puzzle.is_solved():
            #It is! We are done, print out details
            done = True
            print('Best-First SOLVED THE PUZZLE: SOLUTION = ', cur_node.path)
            print('Expanded ', len(visited), 'states')
            return len(visited), len(cur_node.path)
            
        else:
            #Generate this SearchNode's successors and add them to the FRINGE
            
            #Get the possible moves (actions) for this state
            moves = cur_node.puzzle.get_moves()
            
            #For each move, do the move, create SearchNode from successor, then add to FRINGE
            for m in moves:
                #Create new puzzle that new node will point to
                np = Puzzle(cur_node.puzzle.state)
                
                #Execute the move/action
                np.do_move(m)
                
                #Add to the FRINGE, as long as we haven't visited that puzzle
                if np.id() not in visited:
                    #Create the new SearchNode
                    new_node = SearchNode(cur_node.cost + 1, np, cur_node.path + m, options)
                    
                    #Add it to the FRINGE, along with its f-value (stored inside the node)
                    fringe.put(new_node)

    #We didn't find a solution
    if not done:
        print('NO SOLUTION FOUND!')
        return None,None
        
def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="8-Puzzle Solver.")
    parser.add_argument('file', metavar='FILENAME', type=str, help="File of puzzles to solve")
    parser.add_argument("-s", '--search', help="Search type: Options: ids (iterative deepening search) or bfs (best first search)", default='ids')
    parser.add_argument("-f", '--function', help="Heuristic function used: Options: top (tiles out of place), torc (tiles out of row/column), or md (manhattan distance)",default='top')
    parser.add_argument("-t", '--type', help="Evaluation function type: Options: g (greedy), u (uniform cost), or a (a-star)", default='u')
    options = parser.parse_args(args)
    return options

if __name__ == '__main__':

    #Get command line options
    options = getOptions()
    print(options)
    print('Searching for solutions to puzzles from file: ', sys.argv[1])
    
    #Open puzzle file
    pf = open(options.file,'r')
    
    #You can modify the maximum number of puzzles to solve if you want to test on more puzzles
    max_to_solve = 1
    
    #Variables to keep track of solving statistics
    num_solved = 0
    exp_num = 0
    tot_time = 0.0
    path_length = 0
    
    for ps in pf.readlines():
        print('Searching to find solution to following puzzle:', ps)
        
        #Create puzzle from file line
        a = [int(i) for i in ps.rstrip()]
        p = Puzzle(a)
        
        #Print the puzzle to the screen
        p.print_puzzle()

        #Create the initial search node corresponding to the given puzzle state
        start_node = SearchNode(0,p,'',options)
                            
        #Create the priority Queue to store the SearchNodes in
        pq = PriorityQueue()
        
        #Insert the initial state into the Queue
        pq.put(start_node)
        
        #Get initial timing info
        start = time.time()
        
        #Run the given search search (each returns number of nodes expanded and the length of the path found)        
        if options.search == 'bfs':
            #Run the best-first searches
            exp, pl = run_best_first_search(pq, options)
        elif options.search == 'ids': 
            #Use this line to run the iterative deepening-search
            exp, pl = run_iterative_search(start_node)
        else:
            print("Search option not valid. Can be bfs or ids")
            sys.exit()

        if exp is None:
            print('PUZZLE NOT SOLVED')
            break
            
        #Keep track of statistics so we can compare search methods
        exp_num += exp
        path_length += pl
        print('Solution path length is : ', pl)
            
        #Calculate Timing info
        end = time.time()
        tot_time += end - start
        num_solved += 1
        
        #Stop after we have solved the specified number of puzzles
        if num_solved >= max_to_solve:
            break
            
    print('Done with solving puzzles.\n\n')
            
    #Print out statistics about this batch
    if num_solved > 0:
        print('Solved', num_solved, 'puzzles from file: ', sys.argv[1])
        print('Average nodes expanded: ', float(exp_num) / float(num_solved))
        print('Average search time: ', tot_time / num_solved)
        print('Average solution length: ', path_length / num_solved)
    else:
        print('A puzzle was not solved.  This means you haven\'t correctly implemented something. Please double check your code and try again.')
