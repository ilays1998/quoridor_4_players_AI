import pygame
from src.config import CONSOLE_WIDTH, SCREEN_HEIGHT, LIGHT_WHITE, BLACK, SQUARE_SIZE, WHITE, GRID_SIZE, WALL_THICKNESS, \
    BROWN, GRID_COLOR


class Draw:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)  # You can use a custom font file here
        self.button_color = (50, 50, 150)
        self.hover_color = (70, 70, 200)
        self.text_color = (255, 255, 255)

    def draw_message(self, message, color, size, position):
        font = pygame.font.Font(None, size)  # You can adjust the font size as needed
        text_surface = font.render(message, True, color)
        self.screen.blit(text_surface, position)

    def draw_player(self, player):
        pygame.draw.circle(self.screen, player.color,
                           (player.x * SQUARE_SIZE + SQUARE_SIZE // 2 + CONSOLE_WIDTH,
                            player.y * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 4)

    def draw_game_screen(self, board, players, current_player_index, selected_orientation, show_continue_text=False):
        self.screen.fill(LIGHT_WHITE)
        self.draw_board(board)  # Assuming board.draw() is adapted to accept a screen parameter
        for player in players:
            self.draw_player(player)
        self.draw_console(players[current_player_index], selected_orientation, show_continue_text)

    def draw_console(self, current_player, selected_orientation, show_continue_text=False):
        pygame.draw.rect(self.screen, BLACK, (0, 0, CONSOLE_WIDTH, SCREEN_HEIGHT))
        self.draw_message(f"Player: {current_player.name}", current_player.color, 36, (10, 10))

        h_option_rect = pygame.Rect(10, 60, 180, 50)
        v_option_rect = pygame.Rect(10, h_option_rect.bottom + 10, 180, 50)

        pygame.draw.rect(self.screen, current_player.color if selected_orientation == 'h' else WHITE, h_option_rect)
        pygame.draw.rect(self.screen, current_player.color if selected_orientation == 'v' else WHITE, v_option_rect)

        self.draw_message("Horizontal", BLACK, 36, (20, 70))
        self.draw_message("Vertical", BLACK, 36, (20, 130))

        if show_continue_text:
            self.draw_message("Press Enter to continue", WHITE, 24, (10, v_option_rect.bottom + 20))

        # New code to display the player's remaining walls
        self.draw_message(f"Walls left: {current_player.walls_left}", current_player.color, 36, (
            10, v_option_rect.bottom + 50))

    def draw_winner_message(self, board, players, current_player):
        self.screen.fill(LIGHT_WHITE)
        self.draw_board(board)  # Assuming board.draw() is adapted to accept a screen parameter
        for player in players:
            self.draw_player(player)
        self.draw_player(current_player)
        pygame.draw.rect(self.screen, LIGHT_WHITE, (0, 0, CONSOLE_WIDTH, SCREEN_HEIGHT))
        self.draw_message(f"{current_player.name} player wins!", current_player.color, 30,
                          (10, SCREEN_HEIGHT // 2))

    def draw_board(self, board):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * SQUARE_SIZE + CONSOLE_WIDTH, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

        for x in range(GRID_SIZE - 1):
            for y in range(GRID_SIZE - 1):
                if board.h_walls[y][x]:
                    wall_rect = pygame.Rect(x * SQUARE_SIZE + CONSOLE_WIDTH,
                                            (y + 1) * SQUARE_SIZE - WALL_THICKNESS // 2,
                                            SQUARE_SIZE * 2, WALL_THICKNESS)
                    pygame.draw.rect(self.screen, BROWN, wall_rect)

                if board.v_walls[y][x]:
                    wall_rect = pygame.Rect((x + 1) * SQUARE_SIZE + CONSOLE_WIDTH - WALL_THICKNESS // 2,
                                            y * SQUARE_SIZE,
                                            WALL_THICKNESS, SQUARE_SIZE * 2)
                    pygame.draw.rect(self.screen, BROWN, wall_rect)

    def draw_pseudo_move(self, pseudo_plyer, current_player, selected_orientation):
        self.draw_player(pseudo_plyer)
        self.draw_console(current_player, selected_orientation, show_continue_text=True)

    @staticmethod
    def update_screen():
        # Call this method at the end of all drawing operations for a frame
        pygame.display.flip()

    def draw_rounded_rect(self, rect, color, radius=20):
        pygame.draw.rect(self.screen, color, rect, border_radius=radius)

    def draw_new_game_options(self, board):
        self.draw_empty_screen(board)
        screen_width, screen_height = self.screen.get_size()
        rect_width, rect_height = 200, 50
        center_x = (screen_width - rect_width) // 2

        four_players_rect = pygame.Rect(center_x, 100, rect_width, rect_height)
        two_players_rect = pygame.Rect(center_x, 200, rect_width, rect_height)

        mouse_pos = pygame.mouse.get_pos()
        if four_players_rect.collidepoint(mouse_pos):
            self.draw_rounded_rect(four_players_rect, self.hover_color)
        else:
            self.draw_rounded_rect(four_players_rect, self.button_color)

        if two_players_rect.collidepoint(mouse_pos):
            self.draw_rounded_rect(two_players_rect, self.hover_color)
        else:
            self.draw_rounded_rect(two_players_rect, self.button_color)

        self.draw_message("4 Players", self.text_color, 36, (center_x + 10, 110))
        self.draw_message("2 Players", self.text_color, 36, (center_x + 10, 210))

    def draw_ai_player_options(self, num_players, board):
        self.draw_empty_screen(board)
        screen_width, screen_height = self.screen.get_size()
        rect_width, rect_height = 200, 50
        center_x = (screen_width - rect_width) // 2

        mouse_pos = pygame.mouse.get_pos()
        for i in range(num_players + 1):
            ai_option_rect = pygame.Rect(center_x, 100 + i * 100, rect_width, rect_height)
            if ai_option_rect.collidepoint(mouse_pos):
                self.draw_rounded_rect(ai_option_rect, self.hover_color)
            else:
                self.draw_rounded_rect(ai_option_rect, self.button_color)
            self.draw_message(f"{i} AI Players", self.text_color, 36, (center_x + 10, 110 + i * 100))

    def is_four_players_option_clicked(self, x, y):
        screen_width, _ = self.screen.get_size()
        rect_width = 200
        center_x = (screen_width - rect_width) // 2
        return center_x <= x <= center_x + rect_width and 100 <= y <= 150

    def is_two_players_option_clicked(self, x, y):
        screen_width, _ = self.screen.get_size()
        rect_width = 200
        center_x = (screen_width - rect_width) // 2
        return center_x <= x <= center_x + rect_width and 200 <= y <= 250

    def is_ai_option_clicked(self, x, y, num_players):
        screen_width, _ = self.screen.get_size()
        rect_width = 200
        center_x = (screen_width - rect_width) // 2
        for i in range(num_players + 1):
            if center_x <= x <= center_x + rect_width and 100 + i * 100 <= y <= 150 + i * 100:
                return i
        return -1

    def draw_empty_screen(self, board):
        self.screen.fill(LIGHT_WHITE)
        self.draw_board(board)