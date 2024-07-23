import pygame
import sys

from src.board import Board
from src.player import Player
from src.config import SQUARE_SIZE, CONSOLE_WIDTH, screen, RED, GREEN, BLUE, YELLOW, LIGHT_WHITE, Direction
from src.config import GRID_SIZE, WHITE, BLACK, SCREEN_HEIGHT

# Initialize Pygame
pygame.init()


def draw_console(current_player, show_continue_text=False):
    pygame.draw.rect(screen, BLACK, (0, 0, CONSOLE_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Player: {current_player.name}", True, current_player.color)
    screen.blit(text, (10, 10))

    h_option_rect = pygame.Rect(10, 60, 180, 50)
    v_option_rect = pygame.Rect(10, h_option_rect.bottom + 10, 180, 50)

    pygame.draw.rect(screen, current_player.color if selected_orientation == 'h' else WHITE, h_option_rect)
    pygame.draw.rect(screen, current_player.color if selected_orientation == 'v' else WHITE, v_option_rect)

    h_text = font.render("Horizontal", True, BLACK)
    v_text = font.render("Vertical", True, BLACK)

    screen.blit(h_text, (20, 70))
    screen.blit(v_text, (20, 130))

    if show_continue_text:
        continue_font = pygame.font.Font(None, 24)
        continue_text = continue_font.render("Press Enter to continue", True, WHITE)
        screen.blit(continue_text, (10, v_option_rect.bottom + 20))  # Adjust the position as needed

    # New code to display the player's remaining walls
    walls_left_text = font.render(f"Walls left: {current_player.walls_left}", True, current_player.color)
    screen.blit(walls_left_text, (10, v_option_rect.bottom + 50))  # Adjust the Y position as needed to place it under the continue text




def handle_key_press(event, current_player, players):
    new_x, new_y = current_player.x, current_player.y
    if event.key == pygame.K_UP:
        new_y -= 1
    elif event.key == pygame.K_DOWN:
        new_y += 1
    elif event.key == pygame.K_LEFT:
        new_x -= 1
    elif event.key == pygame.K_RIGHT:
        new_x += 1
        current_player.x, current_player.y = new_x, new_y
        return True
    return False

#TODO: make game object
#TODO: make main
def main():
    global selected_orientation
    clock = pygame.time.Clock()
    board = Board()
    players = [
        Player(RED, "Red", Direction.UP),  # Red
        Player(GREEN, "Green", Direction.DOWN),  # Green
        Player(BLUE, "Blue", Direction.LEFT),  # Blue
        Player(YELLOW, "Yellow", Direction.RIGHT)  # Yellow
    ]
    current_player_index = 0
    selected_orientation = 'h'
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                if mouse_x < CONSOLE_WIDTH:
                    if 60 <= mouse_y <= 110:
                        selected_orientation = 'h'
                    elif 120 <= mouse_y <= 170:
                        selected_orientation = 'v'
                elif players[current_player_index].walls_left > 0:
                    grid_x = (mouse_x - CONSOLE_WIDTH) // SQUARE_SIZE
                    grid_y = mouse_y // SQUARE_SIZE

                    if mouse_y % SQUARE_SIZE < SQUARE_SIZE // 2:
                        if grid_y > 0:
                            grid_y -= 1
                    if (mouse_x - CONSOLE_WIDTH) % SQUARE_SIZE < SQUARE_SIZE // 2:
                        if grid_x > 0:
                            grid_x -= 1

                    if selected_orientation == 'h':
                        if not grid_y < GRID_SIZE - 1:
                            continue
                    elif selected_orientation == 'v':
                        if not grid_x < GRID_SIZE - 1:
                            continue
                    if board.place_wall(grid_x, grid_y, selected_orientation, players):
                        players[current_player_index].walls_left -= 1
                        current_player_index = (current_player_index + 1) % len(players)
            elif event.type == pygame.KEYDOWN:

                current_player = players[current_player_index]

                key_to_move = {
                    pygame.K_UP: ((0, -1), Direction.UP),
                    pygame.K_DOWN: ((0, 1), Direction.DOWN),
                    pygame.K_LEFT: ((-1, 0), Direction.LEFT),
                    pygame.K_RIGHT: ((1, 0), Direction.RIGHT),
                }

                if event.key in key_to_move:
                    move, direction = key_to_move[event.key]
                    new_x, new_y = current_player.x + move[0], current_player.y + move[1]

                    # if there is a player in the new position, check if it is possible to jump over it
                    player_jump_to_win = False
                    for player in players:
                        if player.x == new_x and player.y == new_y:
                            if board.is_move_legal(new_x, new_y, [], direction):
                                if board.check_win_condition(current_player.goal, new_x, new_y):
                                    player_jump_to_win = True
                                else:
                                    new_x += move[0]
                                    new_y += move[1]
                                break

                    if player_jump_to_win or board.is_move_legal(new_x, new_y, players, direction):
                        pseudo_player = Player((128, 128, 128), "pseudo", x=new_x, y=new_y)
                        pseudo_player.draw()
                        draw_console(players[current_player_index], show_continue_text=True)

                        pygame.display.flip()

                        # Initialize a variable to None to store the next event
                        next_event = None

                        # Loop until a KEYDOWN or MOUSEBUTTONDOWN event is encountered
                        while True:
                            event = pygame.event.wait()  # Wait for the next event
                            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                                next_event = event
                                break

                        # Check if the next event is a KEYDOWN event and the key is K_RETURN (Enter key)
                        if next_event.type == pygame.KEYDOWN and next_event.key == pygame.K_RETURN:
                            current_player.x, current_player.y = new_x, new_y
                            if board.check_win_condition(current_player.goal, current_player.x, current_player.y):
                                screen.fill(LIGHT_WHITE)
                                board.draw()
                                for player in players:
                                    player.draw()
                                pygame.draw.rect(screen, LIGHT_WHITE, (0, 0, CONSOLE_WIDTH, SCREEN_HEIGHT))
                                font = pygame.font.Font(None, 30)
                                text = font.render(f"{current_player.name} player wins!", True, current_player.color)
                                screen.blit(text, (10, SCREEN_HEIGHT // 2))
                                while True:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                    pygame.display.flip()
                                    clock.tick(60)
                            current_player_index = (current_player_index + 1) % len(players)
                else:
                    continue



        screen.fill(LIGHT_WHITE)
        board.draw()
        for player in players:
            player.draw()

        draw_console(players[current_player_index])

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
