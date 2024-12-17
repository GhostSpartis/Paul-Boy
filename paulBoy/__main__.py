import pygame
from time import strftime

# Initialize Pygame
pygame.init()

SCREEN_WIDTH =480

SCREEN_LENGTH = 320

SCREEN_SETTING = (SCREEN_WIDTH,SCREEN_LENGTH)

PIP_COLOUR = (18, 220, 21)
MID_PIP_COLOUR = (1, 100, 9)
DARK_PIP_COLOUR = (1, 50, 9)

# Set up screen
screen = pygame.display.set_mode(SCREEN_SETTING)
pygame.display.set_caption("PAUL-BOY")

# Load background image
imp = pygame.Surface(SCREEN_SETTING)  # Replace with actual background loading
imp.fill((0, 0, 0))  # Black background

#-------------Clock_Tab-----------------
def clock_tab():
    """Returns the clock text surface."""
    string = strftime('%I:%M %p')
    clockFont = pygame.font.Font("monofonto rg.otf", 70)
    clock = clockFont.render(string, True, PIP_COLOUR, None)

    pygame.draw.rect(screen,MID_PIP_COLOUR,pygame.Rect(3,40,2,8))

    pygame.draw.rect(screen, MID_PIP_COLOUR, pygame.Rect(3, 40, 77, 2))
    pygame.draw.rect(screen, MID_PIP_COLOUR, pygame.Rect(80, 20, 2, 22))
    pygame.draw.rect(screen, MID_PIP_COLOUR, pygame.Rect(80, 20, 5, 2))

    pygame.draw.rect(screen, MID_PIP_COLOUR, pygame.Rect(170, 20, 2, 22))
    pygame.draw.rect(screen, MID_PIP_COLOUR, pygame.Rect(165, 20, 5, 2))
    pygame.draw.rect(screen, MID_PIP_COLOUR, pygame.Rect(170, 40, 305, 2))

    pygame.draw.rect(screen, MID_PIP_COLOUR, pygame.Rect(475, 40, 2, 8))

    return clock

def alarm_button():
    alarmFont = pygame.font.Font("monofonto rg.otf", 20)
    alarm = alarmFont.render("Set Alarm", True, PIP_COLOUR, None)
    return alarm

def date_print():
    dateString= strftime("%m.%d.%Y")
    dateFont = pygame.font.Font("monofonto rg.otf", 20)
    date = dateFont.render(dateString, True, PIP_COLOUR, None)
    return date


# Main loop
run = True
while run:

    tabFont = pygame.font.Font("monofonto rg.otf", 30)
    clockTabName = tabFont.render("CLOCK", True, PIP_COLOUR, None)
    calendarTabName = tabFont.render("CLNDR", True, PIP_COLOUR, None)
    musicTabName = tabFont.render("RADIO", True, PIP_COLOUR, None)
    screen.blit(clockTabName,(90,5))
    screen.blit(calendarTabName,(220,5))
    screen.blit(musicTabName, (350, 5))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Remove previous clock text by filling the clock's area with black
    # Coordinates (100, 100) to (300, 140) match the area for the text
    screen.fill((0, 0, 0), (100, 80, 300, 300))  # Clear previous clock area

    # Draw updated clock text
    screen.blit(clock_tab(), (100, 80))


    screen.fill(DARK_PIP_COLOUR, (3, 280, 157, 30))
    screen.blit(date_print(),(5,283))

    screen.fill(DARK_PIP_COLOUR, (163, 280, 130, 30))
    screen.blit(alarm_button(),(165,282))

    screen.fill(DARK_PIP_COLOUR, (296, 280, 180, 30))

    # Update the screen
    pygame.display.flip()
    pygame.time.delay(100)  # Small delay to reduce CPU usage

pygame.quit()
