import pygame
import crt_shader
from ClockTab import ClockTab
from pygame.locals import *
# Credit:
# The `Graphic_engine` class and its functionality (e.g., `render`, `change_shader`, `Full_screen`)
# are adapted from the work by JingShing.
# Repository: https://github.com/JingShing-Python/ModernGL-Shader-with-pygame/tree/main
from crt_shader import Graphic_engine


class MainApp:
    """
    MainApp class to handle the overall application logic, including initializing the Pygame window,
    rendering the clock tab, and managing user input events like mouse clicks.

    Attributes:
        SCREEN_WIDTH (int): Width of the screen.
        SCREEN_HEIGHT (int): Height of the screen.
        SCREEN_SIZE (tuple): Tuple containing screen width and height.
        screen (pygame.Surface): Pygame surface representing the screen.
        crt_shader (Graphic_engine): Instance of Graphic_engine class for rendering shaders.
        tab_font (pygame.font.Font): Font used for tab names.
        PIP_COLOUR (tuple): Color used for drawing text and elements.
        DARK_PIP_COLOUR (tuple): Dark color for backgrounds and borders.
        background (pygame.Surface): Background surface for the screen.
        clock_tab (ClockTab): Instance of the ClockTab class for rendering and interacting with the clock.
    """

    def __init__(self):
        """
        Initializes the MainApp instance, setting up the Pygame environment,
        screen dimensions, shaders, fonts, and creating a ClockTab instance.
        """
        pygame.init()

        # Screen setup
        self.SCREEN_WIDTH = 480
        self.SCREEN_HEIGHT = 320
        self.SCREEN_SIZE = (480, 320)
        self.screen = pygame.Surface((480, 320)).convert((255, 65282, 16711681, 0))
        pygame.display.set_caption("PAUL-BOY")
        pygame.display.set_mode(self.SCREEN_SIZE, DOUBLEBUF | OPENGL)
        self.crt_shader = Graphic_engine(self.screen)

        # Fonts
        self.tab_font = pygame.font.Font("media/monofonto rg.otf", 30)

        # Colors
        self.PIP_COLOUR = (18, 220, 21)
        self.DARK_PIP_COLOUR = (1, 50, 9)

        # Background
        self.background = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.background.fill((0, 0, 0))  # Black background

        # ClockTab instance
        self.clock_tab = ClockTab(self.screen)

    def draw_tabs(self):
        """
        Draws the tab names at the top of the screen: "CLOCK", "CLNDR", and "RADIO".

        This method renders the text for the tab names using the specified font
        and positions them at fixed locations on the screen.
        """
        clock_tab_name = self.tab_font.render("CLOCK", True, self.PIP_COLOUR, None)
        calendar_tab_name = self.tab_font.render("CLNDR", True, self.PIP_COLOUR, None)
        music_tab_name = self.tab_font.render("RADIO", True, self.PIP_COLOUR, None)

        self.screen.blit(clock_tab_name, (90, 5))
        self.screen.blit(calendar_tab_name, (220, 5))
        self.screen.blit(music_tab_name, (350, 5))

    def handle_click(self, pos):
        """
        Handles mouse click events on the screen, checking if clicks occurred within
        specific areas (dial, alarm button, snooze button).

        Args:
            pos (tuple): The (x, y) position of the mouse click.
        """
        # Check if the click occurred within the dial area
        dial_h = pygame.Rect(175, 190, 50, 30)
        dial_m = pygame.Rect(255, 190, 50, 30)
        alarm_btn = pygame.Rect(190, 230, 100, 50)
        snooze_btn = pygame.Rect(216, 180, 40, 30)
        if dial_h.collidepoint(pos):
            self.clock_tab.increment_dial_H()
        elif dial_m.collidepoint(pos):
            self.clock_tab.increment_dial_M()
        elif alarm_btn.collidepoint(pos):
            self.clock_tab.set_alarm()
        elif snooze_btn.collidepoint(pos):
            self.clock_tab.snooze()

    def run(self):
        """
        Main game loop that handles events, updates the screen, and renders the clock and tabs.

        This loop continuously listens for user input, updates the display, and calls the necessary
        methods to render the UI elements and handle user interactions.
        """
        run = True
        while run:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            # Clear screen
            self.screen.blit(self.background, (0, 0))

            # Draw tabs
            self.draw_tabs()

            # Render ClockTab
            self.clock_tab.render()

            # Check alarm
            self.clock_tab.check_alarm()

            # Update display
            pygame.display.flip()
            crt_shader.Graphic_engine.__call__(self.crt_shader)
            pygame.time.delay(60)  # Small delay to reduce CPU usage

        pygame.quit()


if __name__ == "__main__":
    app = MainApp()
    app.run()
