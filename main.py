import pygame

# Define colors
WHITE = 255,255,255
BLACK = 0,0,0
RED = 255,0,0
TAN = 210, 180, 140
BROWN = 150,75,0
GREEN = 0,255,0

# Define
PAWN = 0
KING = 1

# Set the screen size
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 700
CLOCK = pygame.time.Clock()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Checkers")
    # checkers = [[BLACK, KING, [5,2]],[BLACK, PAWN, [7,2]],[WHITE, PAWN, [4,1]],[WHITE, KING, [6,3]],[WHITE, PAWN, [7,4]]]
    checkers = [[BLACK, PAWN, [1,0]], [BLACK, PAWN, [3,0]], [BLACK, PAWN, [5,0]], [BLACK, PAWN, [7,0]], 
                [BLACK, PAWN, [0,1]], [BLACK, PAWN, [2,1]], [BLACK, PAWN, [4,1]], [BLACK, PAWN, [6,1]], 
                [BLACK, PAWN, [1,2]], [BLACK, PAWN, [3,2]], [BLACK, PAWN, [5,2]], [BLACK, PAWN, [7,2]],
                [WHITE, PAWN, [0,5]], [WHITE, PAWN, [2,5]], [WHITE, PAWN, [4,5]], [WHITE, PAWN, [6,5]], 
                [WHITE, PAWN, [1,6]], [WHITE, PAWN, [3,6]], [WHITE, PAWN, [5,6]], [WHITE, PAWN, [7,6]], 
                [WHITE, PAWN, [0,7]], [WHITE, PAWN, [2,7]], [WHITE, PAWN, [4,7]], [WHITE, PAWN, [6,7]]]
    run = True
    turn_indicator = WHITE
    query_made = False
    selection_made = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # tic the clock
        CLOCK.tick(30)

        # update the board
        pygame.display.update()
        screen.fill(WHITE)
        draw_board(screen)

        # get the state of the mouse
        mouse_pos = pygame.mouse.get_pos() # get the coordinates of the mouse
        mouse_grid_pos = [mouse_pos[0]//(SCREEN_HEIGHT//8), mouse_pos[1]//(SCREEN_HEIGHT//8)] # get the grid space that the mouse is currently on
        mouse_key = pygame.mouse.get_pressed()

        # if the mouse is clicked
        if mouse_key[0]:
            if query_made:
                # check if the user clicked on a square to move a checker to
                for move in possible_moves:
                    if move == mouse_grid_pos: # if the user clicked on an available spot
                        # move the checker
                        pre_move_grid_pos = checkers[index][2]
                        checkers[index][2] = move
                        selection_made = True
                        # remove the piece that was jumped if a piece was jumped
                        if abs(pre_move_grid_pos[0] - move[0]) >= 2: # if a piece was jumped
                            # remove the piece that was jumped
                            checkers.pop(get_checkers_index([pre_move_grid_pos[0]-((pre_move_grid_pos[0]-move[0])//2), pre_move_grid_pos[1]-((pre_move_grid_pos[1]-move[1])//2)], checkers))
                                
            # Check to see if the user clicked on a checker that is available to be moved
            if legal_selection(turn_indicator, checkers, mouse_grid_pos):
                selected_grid_pos = mouse_grid_pos
                query_made = True
            else:
                query_made = False
        
                # if a query has been made, display possible moves based on the selected grid position
        if query_made:
            index = get_checkers_index(selected_grid_pos, checkers) # returns the index of the checker that was selected
            possible_moves = get_possible_moves(selected_grid_pos, checkers, turn_indicator, index)
            display_possible_moves(screen, possible_moves)

        # draw the checkers
        for checker in checkers:
            draw_checker(screen, checker)

        # if a selection has been made, toggle to the next players turn
        if selection_made:
            selection_made = False
            query_made = False                

            # toggle the turn indicator
            if turn_indicator == WHITE:
                # check if the checker has become a king
                if checkers[index][2][1] == 0:
                    checkers[index][1] = KING
                turn_indicator = BLACK
            else:
                # check if the checker has become a king
                if checkers[index][2][1] == 7:
                    checkers[index][1] = KING
                turn_indicator = WHITE
            win_var = check_for_win(checkers)
            if win_var != 0:
                run = False
            
def check_for_win(checkers):
    # returns a 0 if the game is not over, 1 if white has won or 2 if black has won
    white_alive = False
    black_alive = False
    for checker in checkers:
        if checker[0] == WHITE:
            white_alive = True
        elif checker[0] == BLACK:
            black_alive = True
    if white_alive and black_alive:
        return 0
    elif white_alive:
        return 1
    else:
        return 2

def get_checkers_index(selected_grid_pos, checkers):
    for i in range(len(checkers)):
        if checkers[i][2] == selected_grid_pos:
            return i
    return -1 # no checker was found in that grid space

def legal_selection(turn_indicator, checkers, mouse_grid_pos):
    # return true only if a checkers piece of the correct color was pressed
    for checker in checkers:
        checker_color = checker[0]
        checker_grid_pos = checker[2]
        if checker_grid_pos == mouse_grid_pos and checker_color == turn_indicator: # if a checker piece of the correct color was selected
            return True
    return False

def get_possible_moves(selected_grid_pos, checkers, turn_indicator, index):
    possible_moves = []
    x = selected_grid_pos[0]
    y = selected_grid_pos[1]
    
    if checkers[index][1] == PAWN:
        # the checker can move one space forwards if it's white or backwards if it's black
        if turn_indicator == WHITE:
            y -= 1
        else:
            y += 1
        potential_moves = [[x-1,y],[x+1,y]]
    else: # the checker is a king
        potential_moves = [[x-1,y-1],[x-1,y+1],[x+1,y-1],[x+1,y+1]]

    # verify the potential_moves list by making sure a move is not blocked and or show that a jump is available
    for position in potential_moves:
        vacant_space = True
        for checker in checkers:
            if position == checker[2]: # if there is already a checker in the position
                # check if you can jump the checker
                if checker[0] != turn_indicator: # if the checker is on the other team
                    # jump the checker
                    # adjust y coordinate
                    if checkers[index][1] == PAWN:
                        # pawn y coordinate only has to go forwards
                        if turn_indicator == WHITE:
                            position[1] -= 1
                        else:
                            position[1] += 1
                    else:
                        # king y coordinates need to go forwards and backwards
                        if position[1] < y:
                            position[1] -= 1
                        else:
                            position[1] += 1

                    # adjust x coordinate
                    if position[0] < x:
                        position[0] -= 1
                    else:
                        position[0] += 1

                    # Verify that the spot the piece is landing in is empty
                    for c in checkers:
                        if position == c[2]: # if there is already a checker in the new position
                            # Signal that the spot is not vacant
                            vacant_space = False

                else: # the spot is not available
                    vacant_space = False
                break # make sure that you only check for the first checker that was in the way

        if vacant_space:
            if position[0] < 8 and position[0] >= 0 and position[1] < 8 and position[1] >= 0: # make sure the position is in bounds
                possible_moves.append(position)

    return possible_moves
        
def display_possible_moves(screen, possible_moves):
    for position in possible_moves:
        highlight_square(screen, position)

def highlight_square(screen, grid_coordinates):
    x = grid_coordinates[0]
    y = grid_coordinates[1]
    pygame.draw.polygon(screen, GREEN, [((SCREEN_HEIGHT//8) * x, (SCREEN_HEIGHT//8) * y),
                                        ((SCREEN_HEIGHT//8) * x, ((SCREEN_HEIGHT//8) * y) + SCREEN_HEIGHT//8),
                                        (((SCREEN_HEIGHT//8) * x) + SCREEN_HEIGHT//8, ((SCREEN_HEIGHT//8) * y) + SCREEN_HEIGHT//8),
                                        (((SCREEN_HEIGHT//8) * x) + SCREEN_HEIGHT//8, (SCREEN_HEIGHT//8) * y)])

def draw_checker(screen, checker):
    color = checker[0]
    status = checker[1]

    # decode the board coordinate to be actual screen coordinates
    coordinate = checker[2]
    x = (coordinate[0] * (SCREEN_HEIGHT//8)) + SCREEN_HEIGHT//16
    y = (coordinate[1] * (SCREEN_HEIGHT//8)) + SCREEN_HEIGHT//16

    # circle(surface, color, center, radius)
    pygame.draw.circle(screen, color, (x,y), SCREEN_HEIGHT//16)
    
    if status == KING:
        pygame.draw.circle(screen, RED, (x,y), SCREEN_HEIGHT//32)

# polygon(surface, color, points, width=0) -> Rect
def draw_board(screen):
    for y in range(8):
        for x in range(8):
            if ((y % 2 == 0) and (x % 2 == 0)) or ((y % 2 == 1) and (x % 2 == 1)):
                color = TAN
            else:
                color = BROWN
            pygame.draw.polygon(screen, color, [((SCREEN_HEIGHT//8) * x, (SCREEN_HEIGHT//8) * y),
                                              ((SCREEN_HEIGHT//8) * x, ((SCREEN_HEIGHT//8) * y) + SCREEN_HEIGHT//8),
                                              (((SCREEN_HEIGHT//8) * x) + SCREEN_HEIGHT//8, ((SCREEN_HEIGHT//8) * y) + SCREEN_HEIGHT//8),
                                              (((SCREEN_HEIGHT//8) * x) + SCREEN_HEIGHT//8, (SCREEN_HEIGHT//8) * y)])

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()