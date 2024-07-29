import copy

from src.config import GRID_SIZE, Direction, MOVE_DIRECTIONS, PossibleMoves


# TODO: draw as static function that get Board as parameter


class Board:

    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.h_walls = [[False for _ in range(GRID_SIZE - 1)] for _ in range(GRID_SIZE - 1)]
        self.v_walls = [[False for _ in range(GRID_SIZE - 1)] for _ in range(GRID_SIZE - 1)]

    @staticmethod
    def get_goal_positions(goal_direction):
        if goal_direction == Direction.UP:
            return {(row, 0) for row in range(GRID_SIZE)}
        elif goal_direction == Direction.DOWN:
            return {(row, GRID_SIZE - 1) for row in range(GRID_SIZE)}
        elif goal_direction == Direction.LEFT:
            return {(0, col) for col in range(GRID_SIZE)}
        elif goal_direction == Direction.RIGHT:
            return {(GRID_SIZE - 1, col) for col in range(GRID_SIZE)}

    def can_place_wall(self, x, y, orientation, players):
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
        return self.every_played_can_win(x, y, orientation, players)

    def every_played_can_win(self, x, y, orientation, players):
        wall_mapping = {'h': self.h_walls, 'v': self.v_walls}
        wall_mapping[orientation][y][x] = True
        for player in players:
            if not self.can_player_win(player):
                wall_mapping[orientation][y][x] = False  # Rollback if a player is blocked
                return False
        wall_mapping[orientation][y][x] = False  # Rollback if a player is blocked
        return True

    def set_wall(self, x, y, orientation):
        wall_mapping = {'h': self.h_walls, 'v': self.v_walls}
        wall_mapping[orientation][y][x] = True

    def place_wall(self, x, y, orientation, players):
        if self.can_place_wall(x, y, orientation, players):
            self.set_wall(x, y, orientation)
            return True
        return False

    def is_move_legal(self, new_x, new_y, players, direction, jump: bool):
        if new_x < 0 or new_x >= GRID_SIZE or new_y < 0 or new_y >= GRID_SIZE:
            return False

        # Check that the new position is not occupied by another player
        for player in players:
            if player.x == new_x and player.y == new_y:
                if jump:
                    return False
                else:
                    return self.is_move_legal(new_x + MOVE_DIRECTIONS[direction][0],
                                              new_y + MOVE_DIRECTIONS[direction][1], players,
                                              direction,
                                              jump=True) or self.check_win_condition(player.goal, new_x, new_y)

        # Check that the new position is not blocked by a wall
        if direction == Direction.UP:
            if new_x < GRID_SIZE - 1 and self.h_walls[new_y][new_x]:
                return False
            if new_x > 0 and self.h_walls[new_y][new_x - 1]:
                return False
        elif direction == Direction.DOWN:
            if new_x < GRID_SIZE - 1 and self.h_walls[new_y - 1][new_x]:
                return False
            if new_x > 0 and self.h_walls[new_y - 1][new_x - 1]:
                return False
        elif direction == Direction.LEFT:
            if new_y < GRID_SIZE - 1 and self.v_walls[new_y][new_x]:
                return False
            if new_y > 0 and self.v_walls[new_y - 1][new_x]:
                return False
        elif direction == Direction.RIGHT:
            if new_y < GRID_SIZE - 1 and self.v_walls[new_y][new_x - 1]:
                return False
            if new_y > 0 and self.v_walls[new_y - 1][new_x - 1]:
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

        goal_positions = self.get_goal_positions(player.goal)
        start = (player.x, player.y)
        queue = deque([start])
        visited = set([start])

        while queue:
            x, y = queue.popleft()
            if (x, y) in goal_positions:
                return True  # Found a path to the goal

            for direction, (dx, dy) in MOVE_DIRECTIONS.items():
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in visited:
                    if self.is_move_legal(new_x, new_y, [], direction, jump=False):
                        queue.append((new_x, new_y))
                        visited.add((new_x, new_y))

        return False  # No path to the goal was found
