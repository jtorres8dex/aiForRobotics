import sys
import numpy as np

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
        """
        Executes the agent's action: 'L', 'R', 'U', 'D', or 'S'.
        """
        if self.moves_left <= 0:
            return  # No more moves left

        r, c = self.agent_pos

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
        print(f"{action} {self.dirt_collected:.1f}")

        # Display the grid every 5 steps
        if self.move_count % 5 == 0:
            self.display()

    def get_percept(self):
        """
        Returns the dirt level at the agent's current position.
        """
        r, c = self.agent_pos
        return self.dirt_grid[r, c]

    def is_done(self):
        """
        Checks if all moves are used up.
        """
        return self.moves_left <= 0

    def display(self):
        """
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


class ModelBasedVacuumAgent:
    """
    A model-based reflex agent that cleans the environment strategically.
    """

    def __init__(self):
        self.model = {}  # Internal memory of dirt locations

    def update_state(self, state, action, percept):
        """
        Updates internal state based on perception.
        """
        location, _ = state
        self.model[location] = percept  # Update knowledge of dirt levels

    def choose_action(self, environment):
        """
        Selects the best action: Suck if dirty, otherwise move to the highest dirt.
        """
        r, c = environment.agent_pos
        dirt_level = environment.get_percept()

        if dirt_level > 0:
            return 'S'  # Suck dirt

        # Check possible moves
        moves = {
            'L': (r, c - 1),
            'R': (r, c + 1),
            'U': (r - 1, c),
            'D': (r + 1, c)
        }

        # Find the move leading to the highest dirt
        best_move = None
        best_dirt = -1

        for action, (nr, nc) in moves.items():
            if 0 <= nr < environment.rows and 0 <= nc < environment.cols:
                if environment.dirt_grid[nr, nc] > best_dirt:
                    best_dirt = environment.dirt_grid[nr, nc]
                    best_move = action

        return best_move if best_move else 'L'  # Default move if no better option

    def run(self, environment):
        """
        Executes the agent in the environment until moves run out.
        """
        while not environment.is_done():
            action = self.choose_action(environment)
            environment.perform_action(action)


if __name__ == "__main__":
    # Check if the user provided a file argument
    if len(sys.argv) < 2:
        print("Usage: python vacuum_agent.py <environment_file>")
        sys.exit(1)

    # Read the environment file
    env_file = sys.argv[1]
    grid_size, dirt_grid, max_moves, initial_pos = read_environment(env_file)

    # Create the vacuum environment
    vacuum_env = VacuumEnvironment(grid_size, dirt_grid, max_moves, initial_pos)

    # Create and run the agent
    vacuum_agent = ModelBasedVacuumAgent()
    vacuum_agent.run(vacuum_env)

    # Final results
    print("\nSimulation Complete!")
    print(f"Total Dirt Collected: {vacuum_env.dirt_collected:.2f}")