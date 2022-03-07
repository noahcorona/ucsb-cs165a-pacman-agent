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
        print('legal moves:', legalMoves)
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        newGhostPositions = successorGameState.getGhostPositions()

        if currentGameState.getPacmanPosition(self.index) == newPos:
            return -1000

        newGhostDistances = list()
        for ghostPos in newGhostPositions:
            ghostDist = util.manhattanDistance(newPos, ghostPos)
            newGhostDistances.append(ghostDist)
        minGhostDist = min(newGhostDistances)

        if len(newFood.asList()):
            newFoodDistances = list()
            for foodPos in newFood.asList():
                foodDist = util.manhattanDistance(newPos, foodPos)
                newFoodDistances.append(foodDist)
            minFoodDist = min(newFoodDistances)
        else:
            minFoodDist = 0

        print('food dist: ', minFoodDist)
        print('min ghost dist', newGhostDistances[0])
        score = successorGameState.getScore()[self.index] - 2 * minFoodDist + 3 * minGhostDist
        print('move score (' + str(action) + '): ' + str(score))

        return score


def scoreEvaluationFunction(currentGameState, index):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()[index]


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, index=0, evalFn='scoreEvaluationFunction', depth='1'):
        self.index = index  # Pacman is always agent index 0
        self.evaluationFunction = lambda state: util.lookup(evalFn, globals())(state, self.index)
        self.depth = int(depth)


class MultiPacmanAgent(MultiAgentSearchAgent):
    """
    You implementation here
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.

        Some functions you may need:
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        legalMoves = gameState.getLegalActions(agent)
        legalNextState = [gameState.generateSuccessor(agent, action)
                          for action in legalMoves]
        """

        # pacman index = 0
        index = self.index

        # we look recursively up to a depth of self.depth, starting from the current game state
        # start in the current state

        # Collect legal moves and successor states
        legal_moves = gameState.getLegalActions(self.index)
        legal_moves.remove('Stop')
        legal_next_states = [gameState.generateSuccessor(self.index, action)
                             for action in legal_moves]
        next_move_scores = [self.evaluationFunction(nextLegalState)
                            for nextLegalState in legal_next_states]

        # from the legal moves, select those with equal scores
        best_next_score = max(next_move_scores)
        best_next_score_moves = [index for index in range(len(next_move_scores))
                                 if next_move_scores[index] == best_next_score]
        chosen_index = random.choice(best_next_score_moves)  # Pick randomly among the best

        print('Evaluating from ', legal_moves)
        for idx, move, score in zip(range(len(legal_moves)), legal_moves, next_move_scores):
            if idx != chosen_index:
                print(move, score)
            else:
                print(move, score, " < ---")

        return legal_moves[chosen_index]

def maxPointsMove():
    return 0
    #return legal_moves[chosen_index]


class RandomAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        legal_moves = gameState.getLegalActions(self.index)
        return random.choice(legal_moves)
