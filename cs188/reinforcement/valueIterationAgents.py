# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()
        

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # totalcount sums up count
        # argmax max of value

          
        current_iteration = 0
        

       
        while current_iteration < self.iterations:

          values_copy = self.values.copy()
          
          for x in self.mdp.getStates():
            
            max_so_far = float("-inf")
            

            total_sum = 0
            actions = self.mdp.getPossibleActions(x)

            for a in actions:
              total_sum = self.computeQValueFromValues(x,a)
              max_so_far = max(max_so_far,total_sum)
            
            if max_so_far != float("-inf"):
              values_copy[x] = max_so_far
            

          current_iteration += 1
          self.values = values_copy







    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        total_sum = 0
        for nextState,prob in self.mdp.getTransitionStatesAndProbs(state,action):
          
           
          total_sum += prob* (self.mdp.getReward(state,action,nextState) + (self.discount* self.values[nextState]))
          
        return total_sum
        # util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)

        if actions == []:
          return None
        max_so_far = (float("-inf"),None)
        for a in actions:

          temp = (self.computeQValueFromValues(state,a),a)
          if temp[0] > max_so_far[0]:
            max_so_far = temp



        return max_so_far[1]
        # util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        current_iteration = 0
        

        end = len(self.mdp.getStates())
        i = 0
        while current_iteration < self.iterations:
          
          values_copy = self.values.copy()
          
          
            
          max_so_far = float("-inf")
          

          total_sum = 0
          actions = self.mdp.getPossibleActions(self.mdp.getStates()[i])

          for a in actions:
            total_sum = self.computeQValueFromValues(self.mdp.getStates()[i],a)
            max_so_far = max(max_so_far,total_sum)
          
          if max_so_far != float("-inf"):
            values_copy[self.mdp.getStates()[i]] = max_so_far
            
          if i == end-1:
            i = 0
          else:
            i+= 1

          current_iteration += 1
          self.values = values_copy

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        
        predecessors = {}
        
        for state in self.mdp.getStates():
          actions = self.mdp.getPossibleActions(state)
          for action in actions:
            
            for nextState,prob in self.mdp.getTransitionStatesAndProbs(state,action):
              if prob > 0 and not self.mdp.isTerminal(nextState):
                if nextState not in predecessors:
                  predecessors[nextState] = set([state])
                  
                else:
                  predecessors[nextState].add(state)

        current_queue = util.PriorityQueue()
        
        

        for state in self.mdp.getStates():
          max_so_far = float("-inf")
          q_value = 0
          if not self.mdp.isTerminal(state):
            actions = self.mdp.getPossibleActions(state)
            for action in actions:
              q_value = self.computeQValueFromValues(state, action)
              max_so_far = max(q_value,max_so_far)

            diff = abs(self.values[state] - max_so_far)
            current_queue.push(state, -diff)
            

        for x in range(self.iterations):
          if current_queue.isEmpty():
            break
          s = current_queue.pop()
          
          
          if not self.mdp.isTerminal(s):
            max_so_far = float("-inf")
            total_sum = 0
            actions = self.mdp.getPossibleActions(s)

            for a in actions:
              total_sum = self.computeQValueFromValues(s,a)
              max_so_far = max(max_so_far,total_sum)
            
            
            self.values[s] = max_so_far


          
          for p in predecessors[s]:
            actions = self.mdp.getPossibleActions(p)
            max_so_far = float("-inf")
            q_value = 0
            for action in actions:
              q_value = self.computeQValueFromValues(p, action)
              max_so_far = max(q_value,max_so_far)

            diff = abs(self.values[p] - max_so_far)

            if diff > self.theta:
              current_queue.update(p, -diff)







          
         













