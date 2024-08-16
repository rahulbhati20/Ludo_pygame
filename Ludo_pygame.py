import pygame
from pygame import mixer
import random
import time  
import sys
import pygame.locals as pygame_locals
import   ui
import tkinter as tk

# Initializing pygame2
if __name__ == "__main__":
    pygame.init()
    number_of_players, player_names = ui.get_player_information()

    if number_of_players is None or player_names is None:
        exit()  # Exit if the user canceled the input
    
# Loading Images
board = pygame.image.load('img/Board.jpg')
star  = pygame.image.load('img/star.png')
one   = pygame.image.load('img/1.png')
two   = pygame.image.load('img/2.png')
three = pygame.image.load('img/3.png')
four  = pygame.image.load('img/4.png')
five  = pygame.image.load('img/5.png')
six   = pygame.image.load('img/6.png') 

red    = pygame.image.load('img/red2.png')
blue   = pygame.image.load('img/blue1.png')
green  = pygame.image.load('img/green2.png')
yellow = pygame.image.load('img/yellow2.png')

DICE  = [one, two, three, four, five, six]
color = [red, green, yellow, blue]

# Loading Sounds
killSound   = mixer.Sound("sound/Killed.wav")
tokenSound  = mixer.Sound("sound/Token Movement.wav")
diceSound   = mixer.Sound("sound/Dice Roll.wav")
winnerSound = mixer.Sound("sound/Reached Star.wav")

# Initializing Variables
number        = 1
currentPlayer = 0
playerKilled  = False
diceRolled    = False
winnerRank = []  # List to store winner(s)
runnerUpRank = []  # List to store runner-up(s)

# Rendering Text
font = pygame.font.Font('freesansbold.ttf', 11)
FONT = pygame.font.Font('freesansbold.ttf', 16)
currentPlayerText = font.render('Current Player', True, (0, 0, 0))
line = font.render('------------------------------------', True, (0, 0, 0))

# Defining Important Coordinates
HOME = [[(110, 58),  (61, 107),  (152, 107), (110, 152)],  # Red
        [(466, 58),  (418, 107), (509, 107), (466, 153)],  # Green
        [(466, 415), (418, 464), (509, 464), (466, 510)],  # Yellow
        [(110, 415), (61, 464),  (152, 464), (110, 510)]]  # Blue

        # Red      # Green    # Yellow    # Blue
SAFE = [(50, 240), (328, 50), (520, 328), (240, 520),
        (88, 328), (240, 88), (482, 240), (328, 482)]

position = [[[110, 58],  [61, 107],  [152, 107], [110, 152]],  # Red
            [[466, 58],  [418, 107], [509, 107], [466, 153]],  # Green
            [[466, 415], [418, 464], [509, 464], [466, 510]],  # Yellow
            [[110, 415], [61, 464],  [152, 464], [110, 510]]]  # Blue

jump = {(202, 240): (240, 202),  # R1 -> G3
        (328, 202): (368, 240),  # G1 -> Y3
        (368, 328): (328, 368),  # Y1 -> B3
        (240, 368): (202, 328)}  # B1 -> R3

         # Red        # Green     # Yellow    # Blue
WINNER = [[240, 284], [284, 240], [330, 284], [284, 330]]

# Only keep players up to the specified number of players
player_names = player_names[:number_of_players]
position = position[:number_of_players]

# Blit Token Movement
def show_token(x, y):
    screen.fill((255, 255, 255))
    screen.blit(board, (0, 0))

    for i in SAFE[4:]:
        screen.blit(star, i)

    for i in range(len(position)):
        for j in position[i]:
            screen.blit(color[i], j)

    screen.blit(DICE[number-1], (605, 270))

    if position[x][y] in WINNER:
        winnerSound.play()
    else:
        tokenSound.play()

    pygame.display.update()
    time.sleep(0.3)

# Blitting in while loop
def blit_all(player_names):
    for i in SAFE[4:]:
        screen.blit(star, i)

    for i in range(len(position)):
        for j in position[i]:
            screen.blit(color[i], j)

    screen.blit(DICE[number-1], (605, 270))

    # Display the current player's name and color
    if 0 <= currentPlayer < len(player_names):
        current_player_name = player_names[currentPlayer][0]  # Get the current player's name
        current_player_color = color[currentPlayer]  # Get the current player's color
        current_player_text = FONT.render(f'Current Player:', True, ('goldenrod1' ))
        current_player_name_text = FONT.render(f'{current_player_name}', True, (0, 0, 0))

        # Display the "Current Player" text
        screen.blit(current_player_text, (600, 40))

        # Display the color next to the player's name
        screen.blit(current_player_color, (600, 70))

        # Display the current player's name below the "Current Player" text
        screen.blit(current_player_name_text, (640, 80))  # Adjust x-coordinate as needed

    # Display the line separator
    screen.blit(line, (592, 30))
    screen.blit(line, (592, 100))

def to_home(x, y): # starting of carpet
    #  R2
    if (position[x][y][1] == 284 and position[x][y][0] <= 202 and x == 0) \
            and (position[x][y][0] + 38*number > WINNER[x][0]):
        return False

    #  Y2
    elif (position[x][y][1] == 284 and 368 < position[x][y][0] and x == 2) \
            and (position[x][y][0] - 38*number < WINNER[x][0]):
        return False
    #  G2
    elif (position[x][y][0] == 284 and position[x][y][1] <= 202 and x == 1) \
            and (position[x][y][1] + 38*number > WINNER[x][1]):
        return False
    #  B2
    elif (position[x][y][0] == 284 and position[x][y][1] >= 368 and x == 3) \
            and (position[x][y][1] - 38*number < WINNER[x][1]):
        return False

    return True


# Way to WINNER position
def checkWinnerEntryPath(x, y, remainingNumber):

    movedToken = False
    #  R2
    if position[x][y][1] == 284 and position[x][y][0] <= 202 and x == 0 \
            and (position[x][y][0] + 38*number <= WINNER[x][0]):
        movedToken = True
        for i in range(remainingNumber):
            position[x][y][0] += 38
            show_token(x, y)
            
    #  Y2
    elif position[x][y][1] == 284 and position[x][y][0] >= 368 and x == 2 \
            and (position[x][y][0] - 38*number >= WINNER[x][0]):
        movedToken = True
        for i in range(remainingNumber):
            position[x][y][0] -= 38
            show_token(x, y)
    #  G2
    elif position[x][y][0] == 284 and position[x][y][1] <= 202 and x == 1 \
            and (position[x][y][1] + 38*number <= WINNER[x][1]):
        movedToken = True
        for i in range(remainingNumber):
            position[x][y][1] += 38
            show_token(x, y)
    #  B2
    elif position[x][y][0] == 284 and position[x][y][1] >= 368 and x == 3 \
            and (position[x][y][1] - 38*number >= WINNER[x][1]):
        movedToken = True
        for i in range(remainingNumber):
            position[x][y][1] -= 38
            show_token(x, y)
            
    return movedToken

# Moving the token
def move_token(x, y):
    global currentPlayer, diceRolled

    # Taking Token out of HOME
    if tuple(position[x][y]) in HOME[currentPlayer] and number == 6:
        position[x][y] = list(SAFE[currentPlayer])
        tokenSound.play()
        diceRolled = False

    # Moving token which is not in HOME
    elif tuple(position[x][y]) not in HOME[currentPlayer]:
        diceRolled = False

        if not number == 6:
            currentPlayer = (currentPlayer+1) % 4

        #  R2
        if position[x][y][1] == 284 and position[x][y][0] <= 202 and x == 0 \
                and (position[x][y][0] + 38*number <= WINNER[x][0]):
            for i in range(number):
                position[x][y][0] += 38
                show_token(x, y)
                

        #  Y2
        elif position[x][y][1] == 284 and position[x][y][0] >= 368 and x == 2 \
                and (position[x][y][0] - 38*number >= WINNER[x][0]):
            for i in range(number):
                position[x][y][0] -= 38
                show_token(x, y)

        #  G2
        elif position[x][y][0] == 284 and position[x][y][1] <= 202 and x == 1 \
                and (position[x][y][1] + 38*number <= WINNER[x][1]):
            for i in range(number):
                position[x][y][1] += 38
                show_token(x, y)

        #  B2
        elif position[x][y][0] == 284 and position[x][y][1] >= 368 and x == 3 \
                and (position[x][y][1] - 38*number >= WINNER[x][1]):
            for i in range(number):
                position[x][y][1] -= 38
                show_token(x, y)

        # Other Paths
        else:
            remainingNumber = number
            for _ in range(number):

                tokenMoved = checkWinnerEntryPath(x, y, remainingNumber)
                # if the token moved into winner path then break the loop
                if tokenMoved:
                    break

                #  R1, Y3
                if (position[x][y][1] == 240 and position[x][y][0] < 202) \
                        or (position[x][y][1] == 240 and 368 <= position[x][y][0] < 558):
                    position[x][y][0] += 38
                
                # R3 -> R2 -> R1
                elif (position[x][y][0] == 12 and position[x][y][1] > 240):
                    position[x][y][1] -= 44

                #  R3, Y1
                elif (position[x][y][1] == 328 and 12 < position[x][y][0] <= 202) \
                        or (position[x][y][1] == 328 and 368 < position[x][y][0]):
                    position[x][y][0] -= 38
   
                #  Y3 -> Y2 -> Y1
                elif (position[x][y][0] == 558 and position[x][y][1] < 328):
                    position[x][y][1] += 44

                #  G3, B1
                elif (position[x][y][0] == 240 and 12 < position[x][y][1] <= 202) \
                        or (position[x][y][0] == 240 and 368 < position[x][y][1]):
                    position[x][y][1] -= 38
                
                # G3 -> G2 -> G1
                elif (position[x][y][1] == 12 and 240 <= position[x][y][0] < 328):
                    position[x][y][0] += 44

                #  B3, G1
                elif (position[x][y][0] == 328 and position[x][y][1] < 202) \
                        or (position[x][y][0] == 328 and 368 <= position[x][y][1] < 558):
                    position[x][y][1] += 38
                
                #  B3 -> B2 -> B1
                elif (position[x][y][1] == 558 and position[x][y][0] > 240):
                    position[x][y][0] -= 44
                
                else:
                    for i in jump:
                        if position[x][y] == list(i):
                            position[x][y] = list(jump[i])
                            break
                
                remainingNumber = remainingNumber - 1
                show_token(x, y)

        # Killing Player
        if tuple(position[x][y]) not in SAFE:
            for i in range(len(position)):
                for j in range(len(position[i])):
                    if position[i][j] == position[x][y] and i != x:
                        position[i][j] = list(HOME[i][j])
                        killSound.play()
                        diceRolled = False
                        currentPlayer = (currentPlayer+3) % 4




# Checking Winner
def check_winner():
    global currentPlayer, winnerRank

    if currentPlayer < len(position):
        if currentPlayer not in winnerRank:
            for i in position[currentPlayer]:
                if i not in WINNER:
                    return
            winnerRank.append(currentPlayer)
        else:
            currentPlayer = (currentPlayer + 1) % len(position)
    else:
        currentPlayer = 0
  

def has_valid_path(currentPlayer):
    for j in range(len(position[currentPlayer])):
        if tuple(position[currentPlayer][j]) in HOME[currentPlayer]:
            continue  # Skip tokens in HOME
        if to_home(currentPlayer, j):
            continue  # Skip tokens that can be taken out of HOME
        if checkWinnerEntryPath(currentPlayer, j, number):
            return True
    return False

#main loop
def main():
    global number, currentPlayer, diceRolled, running
    def display_winner(winner_name):
        winner_window = tk.Tk()
        winner_window.title("Winner!")
        winner_window.geometry("300x200+385+100")

        winner_label = tk.Label(winner_window, text=f"Winner: {winner_name}", font=("Arial", 24))
        winner_label.pack(pady=20)

        ok_button = tk.Button(winner_window, text="OK", font=("Arial", 18), command=winner_window.destroy)
        ok_button.pack(pady=10)

        winner_window.mainloop()

    # Initialize diceRolled here
    diceRolled = False
    running = True
    game_over = False
    flag = False
    

    while running and not game_over:
        screen.fill((255, 255, 255))
        screen.blit(board, (0, 0))  # Blit Board
        check_winner()
        if currentPlayer in winnerRank:
            winner_name = player_names[currentPlayer][0]
            display_winner(winner_name)
            break  # Stop the game

        coordinate = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            # Event QUIT
            if event.type == pygame.QUIT:
                running = False

            # Event KEYDOWN
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame_locals.K_SPACE:
                    if not diceRolled: 
                        number = random.randint(1, 6)
                        diceSound.play()
                        flag = True

                        for i in range(len(position[currentPlayer])):
                            if tuple(position[currentPlayer][i]) not in HOME[currentPlayer] and to_home(currentPlayer, i):
                                flag = False

                        if (flag and number == 6) or not flag:
                            diceRolled = True
                        else:
                            currentPlayer = (currentPlayer + 1) % 4
          
            # Event MOUSEBUTTONDOWN
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not diceRolled and (605 <= coordinate[0] <= 669) and (270 <= coordinate[1] <= 334):
                    number = random.randint(1, 6)
                    diceSound.play()
                    flag = True

                    for i in range(len(position[currentPlayer])):
                        if tuple(position[currentPlayer][i]) not in HOME[currentPlayer] and to_home(currentPlayer, i):
                            flag = False

                    if (flag and number == 6) or not flag:
                        diceRolled = True
                    else:
                        currentPlayer = (currentPlayer + 1) % 4

                if diceRolled:
                    
                    for j in range(len(position[currentPlayer])):
                        if position[currentPlayer][j][0] <= coordinate[0] <= position[currentPlayer][j][0] + 31 \
                                and position[currentPlayer][j][1] <= coordinate[1] <= position[currentPlayer][j][1] + 31:
                            move_token(currentPlayer, j)
                            break
        # check_winner()                    
        blit_all(player_names)
        pygame.display.update()

    pygame.quit()

# Set up the display
screen_width, screen_height = 750, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Loading Screen")

# Function to display a loading screen with a filling straight line animation
def display_loading_screen_with_image(duration):
    start_time = time.time()  # Get the start time

    # Load the background image
    background_image = pygame.image.load('img/bg1.png')  # Replace with the actual path
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Adjust the size as needed

    while time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill((255, 255, 255))

        # Display the background image
        screen.blit(background_image, (0, 0))

        # Display the "Loading..." text
        loading_font = pygame.font.Font('freesansbold.ttf', 40)
        loading_text = loading_font.render('Loading.....', True, (0, 0, 0))
        text_rect = loading_text.get_rect(center=(screen_width // 1.9, screen_height // 1.4))
        screen.blit(loading_text, text_rect)

        # Calculate the progress of the loading animation (0 to 1)
        progress = (time.time() - start_time) / duration
        line_length = min(500, int(progress * 500))  # Maximum line length is 500
        
        # Draw the filling line
        pygame.draw.line(screen, ('black'), (100, text_rect.bottom + 20), (100 + line_length, text_rect.bottom + 20), 10)
        pygame.display.update()

    # Display the loading screen for the specified duration
    time.sleep(0.3)  # Add a slight delay before starting the game

# Main Startup
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Ludo")
    screen = pygame.display.set_mode((750, 600))
    icon = pygame.image.load('icon.ico') 
    pygame.display.set_icon(icon)

    display_loading_screen_with_image(3)  # Display loading screen for 3 seconds
    main()
