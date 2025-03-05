import sys
import numpy as np
import random
from collections import deque
from abc import ABC

def read_environment(file_path):
    """
    Reads the environment file and returns grid size, dirt values, moves, and initial position.
    """
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]  # Strip extra spaces

    # Parse the grid size
    grid_size = tuple(map(int, lines[0].split(":")[1].strip().split()))

    # Find the index for the dirt grid
    dirt_start_idx = next(i for i, line in enumerate(lines) if line.startswith("DIRT:")) + 1

    # Read dirt values dynamically
    dirt_values = []
    for i in range(dirt_start_idx, dirt_start_idx + grid_size[0]):
        dirt_values.append(list(map(float, lines[i].split())))
    
    dirt_grid = np.array(dirt_values)

    # Find MOVES dynamically
    moves = int(next(line.split(":")[1].strip() for line in lines if line.startswith("MOVES:")))

    # Find INITIAL position dynamically
    initial_pos = tuple(map(int, next(line.split(":")[1].strip().split() for line in lines if line.startswith("INITIAL:"))))
    print(f"Initial Position: {initial_pos}")
    # Convert (row, col) from 1-based to 0-based index
    initial_pos = (initial_pos[0] - 1, initial_pos[1] - 1)

    return grid_size, dirt_grid, moves, initial_pos


class VacuumEnvironment:
    """
    The environment class for the vacuum world.
    Handles agent movements, dirt levels, and performance tracking.
    """

    def __init__(self, grid_size, dirt_grid, max_moves, initial_pos):
        self.rows, self.cols = grid_size
        self.dirt_grid = dirt_grid  # Grid with dirt levels (0-1)
        self.max_moves = max_moves  # Allowed moves
        self.agent_pos = initial_pos  # Current position of the agent
        self.moves_left = max_moves  # Remaining moves
        self.dirt_collected = 0  # Total dirt collected
        self.move_count = 0  # Track the number of moves made

    def perform_action(self, action):

        if self.moves_left <= 0:
            print("No more moves left!")
            return  

        # x,y -> row, col
        r, c = self.agent_pos 

        # map action to next agent pos/state
        if action == 'L' and c > 0:
            self.agent_pos = (r, c - 1)
        elif action == 'R' and c < self.cols - 1:
            self.agent_pos = (r, c + 1)
        elif action == 'U' and r > 0:
            self.agent_pos = (r - 1, c)
        elif action == 'D' and r < self.rows - 1:
            self.agent_pos = (r + 1, c)
        elif action == 'S':  # Suck up dirt
            self.dirt_collected += self.dirt_grid[r, c]
            self.dirt_grid[r, c] = 0  # Clean the square
        
        self.moves_left -= 1  # Each action reduces available moves
        self.move_count += 1  # Increase move count

        # Print the action and updated performance score
        print(f"{action} : {self.dirt_collected:.1f}")

        # only display the grid every 5 steps 
        if self.move_count % 5 == 0:
            self.display()

    def get_percept(self):
        """
        Returns the dirt level at the agent's current position.
        """
        r, c = self.agent_pos
        return self.dirt_grid[r, c]

    def get_neighbors(self):
        """
        Returns a dictionary of valid neighboring squares and their dirt levels.
        can be thought of as a node in which adjacent nodes are valid next states
        """
        r, c = self.agent_pos
        neighbors = {}

        moves: dict[str:set] = {'L': (r, c - 1), 'R': (r, c + 1), 'U': (r - 1, c), 'D': (r + 1, c)}

        for action, (nr, nc) in moves.items():
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbors[action] = self.dirt_grid[nr, nc]

        return neighbors

    def is_done(self):
        """
        Checks if all moves are used up.
        """
        return self.moves_left <= 0

    def display(self):
        """
        Should print each iteration
        Displays the current state of the environment with agent position marked as [ ].
        """
        print()
        for i in range(self.rows):
            row_str = ""
            for j in range(self.cols):
                if (i, j) == self.agent_pos:
                    row_str += "[ ] "
                else:
                    row_str += f"{self.dirt_grid[i, j]:.1f} "
            print(row_str)
        print()


class Agent(ABC):
    """Agent Base class that establishes API for an agent to interact with environment"""
    def __init__(self) -> None:
        """Initilizes attributes to give agent a sense of 'memory'."""
        pass

    def choose_action(self, action) -> str:
        """
        Selects the agent's action: 'L', 'R', 'U', 'D', or 'S'.
        """
        pass

    def run(self, environment) -> None:
        """Runs the agent."""
        while not environment.is_done():
            action = self.choose_action(environment)
            environment.perform_action(action)

class ReflexVacuumAgent(Agent):
    """
    A simple reflex agent (no memory)
    """

    def __init__(self):
        #nothing for now
        pass

    def choose_action(self, environment) -> str:
        """
        If dirty, suck dirt.
        Otherwise, move randomly.
        While this is pretty primitive behavior, it does satisfy the definition of a reflex agent
        It has no memory and abides by a set of rules (choosing a random action)
        """
        if environment.get_percept() > 0:
            print("SUCKING")
            return 'S'  # Suck dirt
        
        a = random.choice(['L', 'R', 'U', 'D'])  # Move randomly
        print('a: ',a)
        return a

class GreedyVacuumAgent(Agent):
    """
    A greedy reflex agent that moves to the dirtiest visible square.
    """

    def __init__(self):
        pass

    def choose_action(self, environment):
        """
        If dirty, suck dirt.
        Otherwise, move to the highest dirt.
        """
        if environment.get_percept() > 0:
            return 'S'

        neighbors = environment.get_neighbors()

        # Find move leading to highest dirt
        max_dirt = max(neighbors.values(), default=0)
        best_moves = [move for move, dirt in neighbors.items() if dirt == max_dirt]
        # if there are multiple max dirt squares, just pick a random one
        return random.choice(best_moves) if best_moves else 'L'  # Randomize ties

class ModelBasedVacuumAgent(Agent):
    """
    A model-based vacuum agent with memory.
    """

    def __init__(self):
        self.visited = set()  # Memory of visited squares

    def bfs_nearest_dirty(self, environment):
        """
        BFS to find shortest path to nearest dirty square.
        Returns the first step in the direction toward that square.
        """
        queue = deque([(environment.agent_pos, [])])  # (current_position, path_to_reach)
        visited = set()

        while queue:
            (r, c), path = queue.popleft()
            visited.add((r, c))

            # If we find a dirty square, return the first move in that path
            if environment.dirt_grid[r, c] > 0:
                return path[0] if path else None  

            # Explore neighboring cells in priority order (Up, Left, Right, Down)
            for action, (nr, nc) in [('U', (r-1, c)), ('L', (r, c-1)), ('R', (r, c+1)), ('D', (r+1, c))]:
                if (0 <= nr < environment.rows and 0 <= nc < environment.cols and (nr, nc) not in visited):
                    queue.append(((nr, nc), path + [action]))

        return None  # No dirt found

    def choose_action(self, environment):
        """
        if dirty suck dirt
        else move to the best available dirty square or explore new areas.
        """
        r, c = environment.agent_pos
        dirt_level = environment.get_percept()
        self.visited.add((r, c))

        # suck dirt if present
        if dirt_level > 0:
            return 'S'  

        # get neighbors and their dirt values
        neighbors = environment.get_neighbors()
        best_move = None
        best_score = -1  

        # Prioritize moving to the dirtiest square
        for action, dirt in neighbors.items():
            score = dirt  
            if (r, c) not in self.visited:
                score += 0.5  # Slightly prioritize unvisited squares

            if score > best_score:
                best_score = score
                best_move = action

        # If no good options exist, use BFS to find the nearest dirt
        if not best_move or best_score == 0:
            best_move = self.bfs_nearest_dirty(environment)

        # If BFS fails (meaning no dirt at all), move randomly
        if not best_move:
            best_move = random.choice(['L', 'R', 'U', 'D'])

        return best_move




if __name__ == "__main__":
    env_file = sys.argv[1]
    
    results = []

    for agent_class, name in [(ReflexVacuumAgent, "A: Reflex Agent"),
                              (GreedyVacuumAgent, "B: Greedy Agent"),
                              (ModelBasedVacuumAgent, "C: Model-Based Agent")]:
        print(f"\nRunning {name}...\n")

        grid_size, dirt_grid, max_moves, initial_pos = read_environment(env_file)
        vacuum_env = VacuumEnvironment(grid_size, dirt_grid, max_moves, initial_pos)
        
        agent = agent_class()
        agent.run(vacuum_env)

        results.append((name, vacuum_env.dirt_collected))

    print("\nPerformance Comparison:")
    print("----------------------")
    for name, score in results:
        print(f"{name}: {score:.2f} dirt collected")
