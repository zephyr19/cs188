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
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        foodList = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        foodNum = successorGameState.getNumFood() + 1
        # print("successorGameState:\n" + str(successorGameState))
        # print("new Position: " + str(newPos))
        # print("newScaredTimes" + str(newScaredTimes))
        providedScore = successorGameState.getScore()

        capsules = successorGameState.getCapsules()
        distanceToCapsules = 1
        for capsule in capsules:
            distanceToCapsules += manhattanDistance(newPos, capsule)

        chase_ghost = 1
        agentNum = successorGameState.getNumAgents()
        ghost_pos = []
        for i in range(1, agentNum):
            ghost_action = currentGameState.getLegalActions(i)
            for act in ghost_action:
                ghost_pos.append(currentGameState.generateSuccessor(i, act).getGhostPosition(i))
        if sum(newScaredTimes) == 0:
            if newPos in ghost_pos:
                return -99999
        else:
            for ghost in ghost_pos:
                chase_ghost += manhattanDistance(newPos, ghost)
        distances = []
        for food in foodList:
            distances.append(manhattanDistance(newPos, food))
        if sum(distances) == 0:
            return providedScore + 1 / foodNum
        return providedScore + 1 / foodNum + 1 / min(distances) + 1 / sum(distances) + 10 / distanceToCapsules + 5 / chase_ghost

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        def value(game_state, timer, agent):
            if game_state.isWin() or game_state.isLose() or timer >= game_state.getNumAgents() * self.depth:
                return (self.evaluationFunction(game_state), 1)
            agent %= game_state.getNumAgents()
            if agent == 0:
                return max_value(game_state, timer, agent)
            else:
                return min_value(game_state, timer, agent)

        def max_value(game_state, timer, agent):
            state = []
            for action in game_state.getLegalActions(agent):
                state.append((value(game_state.generateSuccessor(agent, action), timer+1, agent+1)[0], action))
            return max(state, key=lambda state: state[0])

        def min_value(game_state, timer, agent):
            state = []
            for action in game_state.getLegalActions(agent):
                state.append((value(game_state.generateSuccessor(agent, action), timer+1, agent+1)[0], action))
            return min(state, key=lambda state: state[0])

        return value(gameState, 0, 0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        def value(game_state, timer, agent, alpha, beta):
            if game_state.isWin() or game_state.isLose() or timer >= game_state.getNumAgents() * self.depth:
                return (self.evaluationFunction(game_state), 1)
            agent %= game_state.getNumAgents()
            if agent == 0:
                return max_value(game_state, timer, agent, alpha, beta)
            else:
                return min_value(game_state, timer, agent, alpha, beta)

        def max_value(game_state, timer, agent, alpha, beta):
            state = (-float('inf'), 1)
            for action in game_state.getLegalActions(agent):
                v = value(game_state.generateSuccessor(agent, action), timer+1, agent+1, alpha, beta)[0]
                state = max((v, action), state, key=lambda state: state[0])
                if state[0] > beta:
                    return state
                alpha = max(alpha, v)
            return state

        def min_value(game_state, timer, agent, alpha, beta):
            state = (float('inf'), 1)
            for action in game_state.getLegalActions(agent):
                v = value(game_state.generateSuccessor(agent, action), timer+1, agent+1, alpha, beta)[0]
                state = min((v, action), state, key=lambda state: state[0])
                if state[0] < alpha:
                    return state
                beta = min(beta, v)
            return state

        return value(gameState, 0, 0, -float('inf'), float('inf'))[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        def value(game_state, timer, agent):
            if game_state.isWin() or game_state.isLose() or timer >= game_state.getNumAgents() * self.depth:
                return (self.evaluationFunction(game_state), 1)
            agent %= game_state.getNumAgents()
            if agent == 0:
                return max_value(game_state, timer, agent)
            else:
                return exp_value(game_state, timer, agent)

        def max_value(game_state, timer, agent):
            state = []
            for action in game_state.getLegalActions(agent):
                state.append((value(game_state.generateSuccessor(
                    agent, action), timer+1, agent+1)[0], action))
            # print('totalStates: ' + str(state))
            # print('timer: ' + str(timer))
            bestScore = max(state, key=lambda state: state[0])[0]
            bestIndices = [index for index in range(len(state)) if state[index][0] == bestScore]
            chosenIndex = random.choice(bestIndices) # Pick randomly among the best
            # print('bests: ' + str([item for i, item in enumerate(state) if i in bestIndices]))
            # print('bestIndices: ' + str(bestIndices))
            # print('chosenState: ' + str(state[chosenIndex]))
            return state[chosenIndex]

        def exp_value(game_state, timer, agent):
            state = []
            for action in game_state.getLegalActions(agent):
                state.append(value(game_state.generateSuccessor(
                    agent, action), timer+1, agent+1)[0])
            return (sum(state) / len(state), 1)

        v = value(gameState, 0, 0)
        # print('-------------------->finalState: ' + str(v))
        return v[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    if currentGameState.isWin():
        return currentGameState.getScore() + 99999999
    elif currentGameState.isLose():
        return -float('inf')

    # using providedScore as basic guide
    providedScore = currentGameState.getScore()

    # search for foods
    newPos = currentGameState.getPacmanPosition()
    foodNum = currentGameState.getNumFood()
    foodList = currentGameState.getFood().asList()
    distances = []
    for food in foodList:
        distances.append(manhattanDistance(newPos, food))

    # eating capsules
    capsules = currentGameState.getCapsules()
    distanceToCapsules = 1
    for capsule in capsules:
        distanceToCapsules += manhattanDistance(newPos, capsule)
    
    # chasing ghosts
    newScaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]
    distanceToGhost = 1
    if sum(newScaredTimes) != 0:
        agentNum = currentGameState.getNumAgents()
        for i in range(1, agentNum):
            ghost_action = currentGameState.getLegalActions(i)
            for act in ghost_action:
                distanceToGhost += manhattanDistance(currentGameState.generateSuccessor(i, act).getGhostPosition(i), newPos)
    return currentGameState.getScore() + 1 / foodNum + 1 / min(distances) + 1 / sum(distances) + 5 / distanceToCapsules + 1 / distanceToGhost

# Abbreviation
better = betterEvaluationFunction
