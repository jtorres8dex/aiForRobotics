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
Pacman agents (in search_agents.py).
"""

from builtins import object
import util
import os

def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tiny_maze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tiny_maze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depth_first_search(problem):
    
    # What does this function need to return?
    #     list of actions (actions shown below) that reaches the goal
    # 
    # What data is available?
    #     start_state = problem.get_start_state() # returns a string
    # 
    #     problem.is_goal_state(start_state) # returns boolean
    # 
    #     transitions = problem.get_successors(start_state)
    #     transitions[0].state
    #     transitions[0].action
    #     transitions[0].cost
    # 
    #     print(transitions) # would look like the list-of-lists on the next line
    #     [
    #         [ "B", "0:A->B", 1.0, ],
    #         [ "C", "1:A->C", 2.0, ],
    #         [ "D", "2:A->D", 4.0, ],
    #     ]
    # 
    # Example:
    #     start_state = problem.get_start_state()
    #     transitions = problem.get_successors(start_state)
    #     example_path = [  transitions[0].action  ]
    #     path_cost = problem.get_cost_of_actions(example_path)
    #     return example_path
    
    util.raise_not_defined()


def breadth_first_search(problem):
    from util import Queue

    start_state = problem.get_start_state()
    frontier = Queue()
    frontier.push((start_state, []))  # (state, path)
    
    visited = set()  # Track visited states

    while not frontier.is_empty():
        state, path = frontier.pop()
        if problem.is_goal_state(state):  # If goal state is reached, return path
            return path
        
        if state not in visited:
            visited.add(state)  # Mark state as visited
            
            # Expand the current state
            for successor, action, step_cost in problem.get_successors(state):
                if successor not in visited:
                    new_path = path + [action]  # Update path
                    frontier.push((successor, new_path))  # Push new state to frontier

    return []  # If no solution is found, return empty list        


def uniform_cost_search(problem, heuristic=None):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


# 
# heuristics
# 
def a_really_really_bad_heuristic(position, problem):
    from random import random, sample, choices
    return int(random()*1000)

def null_heuristic(state, problem=None):
    return 0

# def your_heuristic(state, problem=None):
#     from search_agents import FoodSearchProblem
    
#     # 
#     # heuristic for the find-the-goal problem
#     # 
#     if isinstance(problem, SearchProblem):
#         # data
#         pacman_x, pacman_y = state
#         goal_x, goal_y     = problem.goal
        
#         # YOUR CODE HERE (set value of optimisitic_number_of_steps_to_goal)
        
#         optimisitic_number_of_steps_to_goal = 0
#         return optimisitic_number_of_steps_to_goal
#     # 
#     # traveling-salesman problem (collect multiple food pellets)
#     # 
#     elif isinstance(problem, FoodSearchProblem):
#         # the state includes a grid of where the food is (problem isn't ter)
#         position, food_grid = state
#         pacman_x, pacman_y = position
        
#         # YOUR CODE HERE (set value of optimisitic_number_of_steps_to_goal)
        
#         optimisitic_number_of_steps_to_goal = 0
#         return optimisitic_number_of_steps_to_goal

def your_heuristic(state, problem):
    """
    A heuristic for the CornersProblem.
    Estimates the cost to visit all remaining corners using Manhattan distance.
    """
    position, visited_corners = state
    unvisited_corners = [corner for corner in problem.corners if corner not in visited_corners]

    if not unvisited_corners:
        return 0  # If all corners are visited, no remaining cost

    # Compute the maximum Manhattan distance to any unvisited corner
    distances = [util.manhattan_distance(position, corner) for corner in unvisited_corners]
    
    # Use the maximum distance to an unvisited corner as a heuristic estimate
    return max(distances)


def a_star_search(problem, heuristic=your_heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    """
    Here is my implementation of aStar. For the heuristic, we will elect to use a simple Manhattan Distance to goal
    """
    
    # pQueue to store states, with (priority, state, path, cost)
    frontier = util.PriorityQueue()
    # set to store visited states
    visited = set()
    # Push the initial state with priority f(n) = g(n) + h(n)
    start_state = problem.get_start_state()
    # cost of path <- priority
    frontier.push((start_state, [], 0), 0 + heuristic(start_state, problem))

    # while there is unexplored space 
    while not frontier.is_empty():
        # pop state with lowest f(n)
        state, path, cost = frontier.pop()

        # end case: if state is a goal--> return path
        if problem.is_goal_state(state):
            return path
        
        # skip already visited states
        if state in visited:
            continue
        visited.add(state)

        # expand current state and push successors to pQueue
        for successor, action, step_cost, in problem.get_successors(state):
            if successor not in visited:
                new_cost = cost + step_cost
                new_priority = new_cost + heuristic(successor, problem)
                frontier.push((successor, path + [action], new_cost), new_priority)
        
    return [] # return empty path if no solution found 




# (you can ignore this, although it might be helpful to know about)
# This is effectively an abstract class
# it should give you an idea of what methods will be available on problem-objects
class SearchProblem(object):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, step_cost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'step_cost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()

if os.path.exists("./hidden/search.py"): from hidden.search import *
# fallback on a_star_search
for function in [breadth_first_search, depth_first_search, uniform_cost_search, ]:
    try: function(None)
    except util.NotDefined as error: exec(f"{function.__name__} = a_star_search", globals(), globals())
    except: pass

# Abbreviations
bfs   = breadth_first_search
dfs   = depth_first_search
astar = a_star_search
ucs   = uniform_cost_search