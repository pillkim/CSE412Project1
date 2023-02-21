# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from game import Directions
    #Stack in first in first out, which is what is required for DFS. A nodes children are the first ones searched, and the children are also most recently added to the stack
    frontier = util.Stack()
    expanded = [] #Keeps track of what has already been expanded
    startState = problem.getStartState()
    if problem.isGoalState(startState): #If we are starting at the goal state, then there is no path to get there. Youre already there
        return []
    else:
        expanded.append(startState)
        for i in problem.getSuccessors(startState):
            frontier.push((i[0],[i[1]])) #i[0] is the coordinate value ie (1,1). [i[1]] is a list of directions ie 'north' that will become the path. Since it is the successor to the start state there is only one direction

    while frontier:
        node = frontier.pop() #nodes have the format of (coordinate of current location, list of directions to get to current location)
        goalState = problem.isGoalState(node[0])
        if goalState:
            print(node)
            return node[1] #returns path to current location, which is goal state
        if node[0] not in expanded:
           expanded.append(node[0]) #if the current locations hasn't been visited before, make it visited
        for i in problem.getSuccessors(node[0]):
            if i[0] not in expanded:
                path = node[1].copy() #Makes a copy of the path to the current node
                path.append(i[1]) #adds the direction to reach the successor node. Iterates through all successor nodes
                frontier.push((i[0], path)) #adds new node to frontier
    #Understand this to understand the rest of the algorithms best
    return []
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    from game import Directions
    #Instead of a stack, we use a queue here. A queue is last in first out, meaning that the most senior nodes added to the queue are looked at next
    frontier = util.Queue()
    expanded = []
    startState = problem.getStartState()
    if problem.isGoalState(startState):
        return []
    else:
        expanded.append(startState)
        for i in problem.getSuccessors(startState):
            frontier.push((i[0],[i[1]])) #Same structure to a node as DFS
            expanded.append(i[0])

    while frontier:
        node = frontier.pop()
        goalState = problem.isGoalState(node[0])
        if goalState:
            print(node)
            return node[1]
        for i in problem.getSuccessors(node[0]):
            if i[0] not in expanded:
                path = node[1].copy()
                path.append(i[1])
                frontier.push((i[0], path))
                expanded.append(i[0])

    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    #We use a priority queue here. The priority queue automatically reorganizes so that the next node looked at is the one with the lowest "cost". In UCS, cost is the distance to a node
    frontier = util.PriorityQueue()
    expanded = {} #Expanded is a dictionary now because it keeps track of which nodes have been expanded and the cost to get to each
    startState = problem.getStartState()

    if problem.isGoalState(startState):
        return []
    else:
        expanded[startState] = 0
        for i in problem.getSuccessors(startState):
            #The node has a slightly different structure. i[0] and [i[1]] are the same. i[2] is the cost to get to the next node. 
            #Since this is the first successor, the cost to get to that node is just 0+ the cost of the single move. In the future we will add the cost
            #of getting to the previous node plus the cost of the single move, which is why we have to both record the current cost in the node and in the PQueue
            frontier.update((i[0],[i[1]],i[2]),i[2]) 
            expanded[i[0]]=i[2]

    while frontier:
        node = frontier.pop()
        print(node)
        goalState = problem.isGoalState(node[0])
        print
        if goalState:
            print(node)
            return node[1]
        for i in problem.getSuccessors(node[0]):
            #If the last time we visited a node, the cost to get there the first time was more than the cost to get there now
            #then we add that node to the frontier again and update it's cost in Expanded. This is more important when cost is not uniform
            #You can image that we visited a node with a cost of 10, but discovered a new way that costs 5. Now it's children cost less as well so we must reexplore
            if (i[0] not in expanded) or (i[0] in expanded and (i[2]+node[2])<expanded.get(i[0])):
                path = node[1].copy()
                path.append(i[1])
                frontier.update((i[0], path,i[2]+node[2]),i[2]+node[2])# you can see how we add the cost to get to the successor node plus the cost to get to the current node
                expanded[i[0]] = i[2]+node[2]

    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    frontier = util.PriorityQueue()
    expanded = {}
    startState = problem.getStartState()

    if problem.isGoalState(startState):
        return []
    else:
        expanded[startState] = 0
        for i in problem.getSuccessors(startState):
            frontier.push((i[0],[i[1]],i[2]),i[2]+heuristic(i[0],problem))
            expanded[i[0]]=i[2]+heuristic(i[0],problem)

    while frontier:
        node = frontier.pop()
        goalState = problem.isGoalState(node[0])
        if goalState:
            print(node)
            return node[1]
        for i in problem.getSuccessors(node[0]):
            if (i[0] not in expanded) or (i[0] in expanded and (i[2]+node[2]+heuristic(i[0],problem))<expanded.get(i[0])):
                path = node[1].copy()
                path.append(i[1])
                #Only difference is adding the heuristic to the PQueue. We do this because the heuristic is important for prioritizing which nodes to explore next
                #but the heuristic does not actually impact the cost of getting to a node. So we record actual cost in the node and actual cost + heuristic in the PQueue
                frontier.push((i[0], path,i[2]+node[2]),i[2]+node[2]+heuristic(i[0],problem))
                #For the same reasons as above we do the same change to expanded
                expanded[i[0]] = i[2]+node[2]+heuristic(i[0],problem)

    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
