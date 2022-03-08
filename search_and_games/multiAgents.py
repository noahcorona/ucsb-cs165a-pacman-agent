# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(self.index)

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(self.index, action)
        newPos = successorGameState.getPacmanPosition(self.index)
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()

        if len(newFood.asList()):
            fooddist = util.manhattanDistance(newPos, newFood.asList()[0])
        else:
            fooddist = 0

        return successorGameState.getScore()[self.index] - fooddist

def scoreEvaluationFunction(currentGameState, index):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition(index)
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()

    if len(newFood.asList()):
        fooddist = util.manhattanDistance(newPos, newFood.asList()[0])
    else:
        fooddist = 0

    return currentGameState.getScore()[index] - fooddist


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent.
    """

    def __init__(self, index = 0, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = index # Pacman is always agent index 0
        self.evaluationFunction = lambda state:util.lookup(evalFn, globals())(state, self.index)
        self.depth = int(depth)


class MultiPacmanAgent(MultiAgentSearchAgent):
    """
    This is my implementation of a minimax agent.

    We recursively check for the optimal solution for pacman, assuming
    that ghost agents move randomly
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        return self.minimax(gameState=gameState, agentIndex=self.index, depth=0)

    def minimax(self, gameState, agentIndex, depth):
        """
        The recursive minimax function for both pacman (-> max) and ghost (-> min) agents

        gameState: state of the current (prospective) game
        agentIndex: index of the current agent (0 for pacman, 1, 2, ... for each ghost)
        depth: depth of the current (prospective) game, i.e. number of moves forward we're looking

        The base cases for the recursion
            1. We have reached the specified max depth (return score)
            2. We are playing pacman and have reached a winning game state (return score + incentive)
               and there are no more states to explore
            3. We are playing pacman and have reached a losing game state (return score - incentive)
               and there are no more states to explore
        """

        if depth == self.depth:
            # Base case #1: max depth reached
            return gameState.getScore()[0], None
        else:
            if agentIndex == 0:
                # agent index = 0 -> the current move is as the pacman agent

                # Base case #2: pacman moves to winning game state
                if gameState.isWin():
                    return gameState.getScore()[0] + 1000, None
                # Base case #3: pacman moves to winning game state
                elif gameState.isLose():
                    return gameState.getScore()[0] - 1000, None
                else:
                    # look at all legal moves, get minimax values

            else:
                # agent index > 0 -> the current move is as a ghost agent

        
class RandomAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions(self.index)
        return random.choice(legalMoves)




