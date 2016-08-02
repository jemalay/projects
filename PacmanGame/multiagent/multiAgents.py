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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

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
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        "*** YOUR CODE HERE ***"
        walls = successorGameState.getWalls()
        a1,a2,a3 = 0,0,0
        lst = []
        lst2 = []
        l = []
        i =0
        go = True

        for x in newFood.asList():
          if manhattanDistance(newPos,x) !=0 and not walls[x[0]][x[1]]:
            lst.append(1/manhattanDistance(newPos,x))

        for y in successorGameState.getGhostPositions():
          if newScaredTimes[i] >=0 and manhattanDistance(newPos,y) !=0:
            l.append(manhattanDistance(newPos,y))

          if manhattanDistance(newPos,y) != 0:

            lst2.append(1/manhattanDistance(newPos,y))
          i = i+1


        if go:
          
          if lst2 != [] and max(newScaredTimes) == 0:

            a2 = min(lst2)*(-1)
            if lst != []:
              a1 = max(lst)*(10)

            if successorGameState.getScore() != 0:
              a3 = successorGameState.getScore()*2
            return a1+ a2 + a3

          if lst2 != [] and max(newScaredTimes) != 0:
            if min(l) !=0:
              a2 = 1/max(l)
            if lst != [] and max(lst) != 0:
              a1 = max(lst)*(1)
            if successorGameState.getScore() != 0:
              a3 = successorGameState.getScore()*2
            return a1+ a2+ a3



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
        
        self.position = 0
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
        "*** YOUR CODE HERE ***"
   
        def max_value(State,d):
          if ((d == self.depth) or State.isWin() or State.isLose()):
            return (self.evaluationFunction(State),None)
          
          v = float("-inf")
          agentIndex = 0
          actions = State.getLegalActions(agentIndex)
          best_action = actions[0]

          for action in actions:
            x= State.generateSuccessor(agentIndex,action)
            min_val = min_value(x, agentIndex + 1, d)[0] 
            if min_val > v:
              best_action = action
            v = max(v, min_val)
            
          return (v,best_action)
            
            
            
        def min_value(State,agentIndex,d):
          if (State.isWin() or State.isLose() or (d == self.depth)):
            return (self.evaluationFunction(State),None)

          actions = State.getLegalActions(agentIndex)
          best_action = actions[0]
          v = float("inf")
      
          for action in actions:
            x=State.generateSuccessor(agentIndex,action)
            if agentIndex == State.getNumAgents()-1 :

              max_val = max_value(x,d+1)[0]
              if max_val < v:
                best_action = action
              v = min(v,max_val)
            else:
              max_val = min_value(x,agentIndex + 1,d)[0]
              if max_val < v:
                best_action = action
              v = min(v,max_val)

          return (v,best_action)

          
        v = float("-inf")
        actions = gameState.getLegalActions()
        best_action = actions[0]
        
        for action in actions:
          x=gameState.generateSuccessor(self.index,action)
          min_val = min_value(x,self.index+1,0)[0]
          if min_val > v:
            best_action = action
          v = max(v,min_val)
        
        return best_action



        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def max_value(State,d,a,b):
          if ((d == self.depth) or State.isWin() or State.isLose()):
            return (self.evaluationFunction(State),None)
          
          v = float("-inf")
          agentIndex = 0
          actions = State.getLegalActions(agentIndex)
          best_action = actions[0]

          for action in actions:
            x= State.generateSuccessor(agentIndex,action)
            min_val = min_value(x, agentIndex + 1, d,a,b)[0] 
            if min_val > v:
              best_action = action
            v = max(v, min_val)
            if v > b: return (v,best_action)
            a = max(a,v)

            
          return (v,best_action)
            
            
            
        def min_value(State,agentIndex,d,a,b):
          if (State.isWin() or State.isLose() or (d == self.depth)):
            return (self.evaluationFunction(State),None)

          actions = State.getLegalActions(agentIndex)
          best_action = actions[0]
          v = float("inf")
      
          for action in actions:
            x=State.generateSuccessor(agentIndex,action)
            if agentIndex == State.getNumAgents()-1 :

              max_val = max_value(x,d+1,a,b)[0]
              if max_val < v:
                best_action = action
              v = min(v,max_val)
              if v < a: return (v,best_action)
              b = min(b,v)
            else:
              max_val = min_value(x,agentIndex + 1,d,a,b)[0]
              if max_val < v:
                best_action = action
              v = min(v,max_val)
              if v < a: return (v,best_action)
              b = min(b,v)

          return (v,best_action)

        a = float("-inf")
        b = float("inf")
        v = float("-inf")
        actions = gameState.getLegalActions()
        best_action = actions[0]
        
        for action in actions:
          x=gameState.generateSuccessor(self.index,action)
          min_val = min_value(x,self.index+1,0,a,b)[0]
          if min_val > v:
            best_action = action
          v = max(v,min_val)

          if v > b: return (v,best_action)
          a = max(a,v)

          
        return best_action
        # util.raiseNotDefined()

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
        "*** YOUR CODE HERE ***"
        def max_value(State,d):
          if ((d == self.depth) or State.isWin() or State.isLose()):
            return (self.evaluationFunction(State),None)
          
          v = float("-inf")
          agentIndex = 0
          actions = State.getLegalActions(agentIndex)
          best_action = actions[0]

          for action in actions:
            x= State.generateSuccessor(agentIndex,action)
            min_val = exp_value(x, agentIndex + 1, d)[0] 
            if min_val > v:
              best_action = action
            v = max(v, min_val)
            
          return (v,best_action)
            
            
            
        def exp_value(State,agentIndex,d):
          if (State.isWin() or State.isLose() or (d == self.depth)):
            return (self.evaluationFunction(State),None)

          actions = State.getLegalActions(agentIndex)
          best_action = actions[0]
          v = 0.0
          p = float(len(actions))
          for action in actions:
            x=State.generateSuccessor(agentIndex,action)
            if agentIndex == State.getNumAgents()-1 :

              max_val = max_value(x,d+1)[0]
              if max_val < v:
                best_action = action
              v = v + (1.0/p)*max_val
            else:
              max_val = exp_value(x,agentIndex + 1,d)[0]
              v = v + (1.0/p)*max_val

          return (v,best_action)

          
        v = float("-inf")
        actions = gameState.getLegalActions()
        best_action = actions[0]
        
        for action in actions:
          x=gameState.generateSuccessor(self.index,action)
          min_val = exp_value(x,self.index+1,0)[0]
          if min_val > v:
            best_action = action
          v = max(v,min_val)
        
        return best_action
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

