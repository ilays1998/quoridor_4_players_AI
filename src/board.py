import pygame
from src.config import SQUARE_SIZE, CONSOLE_WIDTH, screen, GRID_SIZE, WALL_THICKNESS, WHITE, BROWN, GRID_COLOR, \
    Direction

# TODO: draw as static function that get Board as parameter
# TODO: player jump on tile of another player
def _get_goal_positions(goal_direction):
    if goal_direction == Direction.UP:
        return {(row, 0) for row in range(GRID_SIZE)}
    elif goal_direction == Direction.DOWN:
        return {(row, GRID_SIZE - 1) for row in range(GRID_SIZE)}
    elif goal_direction == Direction.LEFT:
        return {(0, col) for col in range(GRID_SIZE)}
    elif goal_direction == Direction.RIGHT:
        return {(GRID_SIZE - 1, col) for col in range(GRID_SIZE)}



class Board:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.h_walls = [[False for _ in range(GRID_SIZE - 1)] for _ in range(GRID_SIZE - 1)]
        self.v_walls = [[False for _ in range(GRID_SIZE - 1)] for _ in range(GRID_SIZE - 1)]

    def draw(self):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * SQUARE_SIZE + CONSOLE_WIDTH, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)

        for x in range(GRID_SIZE - 1):
            for y in range(GRID_SIZE - 1):
                if self.h_walls[y][x]:
                    wall_rect = pygame.Rect(x * SQUARE_SIZE + CONSOLE_WIDTH,
                                            (y + 1) * SQUARE_SIZE - WALL_THICKNESS // 2,
                                            SQUARE_SIZE * 2, WALL_THICKNESS)
                    pygame.draw.rect(screen, BROWN, wall_rect)

                if self.v_walls[y][x]:
                    wall_rect = pygame.Rect((x + 1) * SQUARE_SIZE + CONSOLE_WIDTH - WALL_THICKNESS // 2,
                                            y * SQUARE_SIZE,
                                            WALL_THICKNESS, SQUARE_SIZE * 2)
                    pygame.draw.rect(screen, BROWN, wall_rect)

    def can_place_wall(self, x, y, orientation):
        if x >= GRID_SIZE - 1 or y >= GRID_SIZE - 1:
            return False
        if orientation == 'h' and self.h_walls[y][x]:
            return False
        if orientation == 'v' and self.v_walls[y][x]:
            return False
        if orientation == 'h' and (self.v_walls[y][x] or (x > 0 and self.h_walls[y][x - 1]) or (
                x < GRID_SIZE - 2 and self.h_walls[y][x + 1])):
            return False
        if orientation == 'v' and (self.h_walls[y][x] or (y > 0 and self.v_walls[y - 1][x]) or (
                y < GRID_SIZE - 2 and self.v_walls[y + 1][x])):
            return False
        return True

    def set_wall(self, x, y, orientation, players):
        wall_mapping = {'h': self.h_walls, 'v': self.v_walls}
        wall_mapping[orientation][y][x] = True
        for player in players:
            if not self.can_player_win(player):
                wall_mapping[orientation][y][x] = False  # Rollback if a player is blocked
                return False
        return True

    def place_wall(self, x, y, orientation, players):
        if self.can_place_wall(x, y, orientation):
            return self.set_wall(x, y, orientation, players)
        return False

    def is_move_legal(self, new_x, new_y, players, direction):
        if new_x < 0 or new_x >= GRID_SIZE or new_y < 0 or new_y >= GRID_SIZE:
            return False

        # Check that the new position is not occupied by another player
        for player in players:
            if player.x == new_x and player.y == new_y:
                return False

        # Check that the new position is not blocked by a wall
        if direction == Direction.UP:
            if new_x < GRID_SIZE - 1 and self.h_walls[new_y][new_x]:
                return False
            if self.h_walls[new_y][new_x - 1]:
                return False
        elif direction == Direction.DOWN:
            if new_x < GRID_SIZE - 1 and self.h_walls[new_y - 1][new_x]:
                return False
            if self.h_walls[new_y - 1][new_x - 1]:
                return False
        elif direction == Direction.LEFT:
            if new_y < GRID_SIZE - 1 and self.v_walls[new_y][new_x]:
                return False
            if self.v_walls[new_y - 1][new_x]:
                return False
        elif direction == Direction.RIGHT:
            if new_y < GRID_SIZE - 1 and self.v_walls[new_y][new_x - 1]:
                return False
            if self.v_walls[new_y - 1][new_x - 1]:
                return False
        return True

    def check_win_condition(self, player_goal, player_x, player_y):
        if player_goal == Direction.UP and player_y == 0:
            return True
        if player_goal == Direction.DOWN and player_y == GRID_SIZE - 1:
            return True
        if player_goal == Direction.LEFT and player_x == 0:
            return True
        if player_goal == Direction.RIGHT and player_x == GRID_SIZE - 1:
            return True
        return False

    def can_player_win(self, player):
        from collections import deque

        goal_positions = _get_goal_positions(player.goal)
        start = (player.x, player.y)
        queue = deque([start])
        visited = set([start])

        while queue:
            x, y = queue.popleft()
            if (x, y) in goal_positions:
                return True  # Found a path to the goal

            for move in [((-1, 0), Direction.LEFT), ((1, 0), Direction.RIGHT),
                         ((0, -1), Direction.UP), ((0, 1), Direction.DOWN)]:
                new_x, new_y = x + move[0][0], y + move[0][1]
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in visited:
                    if self.is_move_legal(new_x, new_y, [], move[1]):
                        queue.append((new_x, new_y))
                        visited.add((new_x, new_y))

        return False  # No path to the goal was found

    # with print the path
    # def can_player_win(self, player, players):
    #     from collections import deque
    #
    #     goal_positions = _get_goal_positions(player.goal)
    #     start = (player.x, player.y)
    #     queue = deque([start])
    #     visited = set([start])
    #     predecessor = {start: None}  # Track the predecessor of each cell
    #
    #     while queue:
    #         x, y = queue.popleft()
    #         if (x, y) in goal_positions:
    #             # Reconstruct the path from goal to start
    #             path = []
    #             current = (x, y)
    #             while current is not None:
    #                 path.append(current)
    #                 current = predecessor[current]
    #             path.reverse()  # Reverse to get the path from start to goal
    #             print("Winning Path:", path)  # Print or return the path
    #             return True  # Found a path to the goal
    #
    #         for move in [((-1, 0), Direction.LEFT), ((1, 0), Direction.RIGHT),
    #                      ((0, -1), Direction.UP), ((0, 1), Direction.DOWN)]:
    #             new_x, new_y = x + move[0][0], y + move[0][1]
    #             if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in visited:
    #                 if self.is_move_legal(new_x, new_y, players, move[1]):
    #                     queue.append((new_x, new_y))
    #                     visited.add((new_x, new_y))
    #                     predecessor[(new_x, new_y)] = (x, y)  # Set the predecessor
    #
    #     return False  # No path to the goal was found
