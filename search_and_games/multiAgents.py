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
import random, util, time

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
    newGhostPositions = currentGameState.getGhostPositions()

    if len(newFood.asList()):
        fooddist = util.manhattanDistance(newPos, newFood.asList()[0])
    else:
        fooddist = 0

    newGhostDistances = list()
    for ghostPos in newGhostPositions:
        ghostDist = util.manhattanDistance(newPos, ghostPos)
        newGhostDistances.append(ghostDist)
    minGhostDist = min(newGhostDistances)
    # need to incentivize moving toward the average food area
    print(minGhostDist)
    print(fooddist)
    return currentGameState.getScore()[index] - 20 * fooddist + 30 * minGhostDist


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent.
    """

    def __init__(self, index=0, evalFn='scoreEvaluationFunction', depth='3'):
        self.index = index  # Pacman is always agent index 0
        self.evaluationFunction = lambda state: util.lookup(evalFn, globals())(state, self.index)
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
        best_action, best_score = self.minimax(game_state=gameState, agent_index=self.index, depth=0)
        print('making move, ', best_action)
        return best_action

    def minimax(self, game_state, agent_index, depth):
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
        newPos = game_state.getPacmanPosition(0)
        newFood = game_state.getFood()
        newGhostPositions = game_state.getGhostPositions()

        if len(newFood.asList()):
            fooddist = util.manhattanDistance(newPos, newFood.asList()[0])
        else:
            fooddist = 0

        newGhostDistances = list()
        for ghostPos in newGhostPositions:
            ghostDist = util.manhattanDistance(newPos, ghostPos)
            newGhostDistances.append(ghostDist)
        minGhostDist = min(newGhostDistances)

        print(minGhostDist)
        print(fooddist)

        # need to incentivize moving toward the average food area
        

        prospective_score = game_state.getScore()[0] - 20 * fooddist + 30 * minGhostDist

        if depth == self.depth:
            # Base case #1: max depth reached
            return None, prospective_score
        # Base case #2: pacman moves to winning game state
        elif game_state.isWin():
            return None, prospective_score + 1000
        # Base case #3: pacman moves to winning game state
        elif game_state.isLose():
            return None, prospective_score - 1000
        else:
            indent = ''
            for i in range(depth):
                indent += '   '
            # get all legal moves for this game state
            prospective_moves = game_state.getLegalActions(agent_index)
            prospective_scores = list()

            if agent_index == 0:
                # agent index = 0 -> the current move is as the pacman agent
                # find max of potential moves recursively
                max_score = -9999999
                max_score_move = None

                for move in prospective_moves:
                    next_agent = agent_index + 1
                    next_depth = depth

                    if next_agent == game_state.getNumAgents():
                        next_agent = 0
                        next_depth = depth + 1

                    print(indent, 'evaluating pacman move: ', move)
                    prospective_state = game_state.generatePacmanSuccessor(0, move)
                    _, prospective_score = self.minimax(game_state=prospective_state, agent_index=next_agent,
                                                        depth=next_depth)
                    if prospective_score > max_score:
                        max_score = prospective_score
                        max_score_move = move
                    print(indent, '    giving prospective score of ', prospective_score)
                    prospective_scores.append(prospective_score)
                # after finding all potential move scores & max one, return the max

                print(indent, 'moves are: ', prospective_moves)
                print(indent, 'max score move: ', max_score_move)
                print(indent, 'score is ', max_score)
                return max_score_move, max_score
            else:
                # find min of potential moves recursively
                min_score = 9999999
                min_score_move = None

                for move in prospective_moves:
                    next_agent = agent_index + 1    # move to next agent
                    next_depth = depth              # keep depth unless we are currently the last agent

                    if next_agent == game_state.getNumAgents():
                        next_agent = 0          # if we are currently last ghost, set agent to pacman
                        next_depth = depth + 1  # also increase depth, as we have calculated next move for all agents

                    # generate next state and get score
                    prospective_state = game_state.generateSuccessor(agent_index, move)
                    _, prospective_score = self.minimax(game_state=prospective_state, agent_index=next_agent,
                                                        depth=next_depth)
                    # if next score less than current min, set new min and move that led to it
                    if prospective_score < min_score:
                        min_score = prospective_score
                        min_score_move = move
                    prospective_scores.append(prospective_score)
                # after finding all potential move scores & min one, return the min
                return min_score_move, min_score


class RandomAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions(self.index)
        return random.choice(legalMoves)
