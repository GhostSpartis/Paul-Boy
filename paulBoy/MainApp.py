import pygame
import crt_shader
from Button import Button
from AlarmClockTab import AlarmClockTab
from CalendarTab import CalendarTab
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
        alarm_clock_tab (AlarmClockTab): Instance of the ClockTab class for rendering and interacting with the clock.
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
        pygame.display.toggle_fullscreen()
        self.crt_shader = Graphic_engine(self.screen)

        # Fonts
        self.tab_font = pygame.font.Font("media/monofonto rg.otf", 30)
        self.dial_font = pygame.font.Font("media/monofonto rg.otf", 40)
        self.alarm_font = pygame.font.Font("media/monofonto rg.otf", 20)

        # Colors
        self.BRIGHT_PIP_COLOUR = (0, 250, 0)
        self.PIP_COLOUR = (5, 250, 5)
        self.MID_PIP_COLOUR = (1, 150, 9)
        self.DARK_PIP_COLOUR = (1, 50, 9)

        # Background
        self.background = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.background.fill((0, 0, 0))  # Black background

        # AlarmClock instance
        self.alarm_clock_tab = AlarmClockTab(self.screen)

        # Calendar instance
        self.calendar_tab = CalendarTab(self.screen)

        # Track the currently highlighted option
        self.current_options_index = 0

    def draw_tabs(self):
        """
        Draws the tab names at the top of the screen: "STAT", "DATA", and "RADIO".

        This method renders the text for the tab names using the specified font
        and positions them at fixed locations on the screen.
        """
        clock_tab_name = self.tab_font.render("STAT", True, self.PIP_COLOUR, None)
        calendar_tab_name = self.tab_font.render("DATA", True, self.PIP_COLOUR, None)
        music_tab_name = self.tab_font.render("RADIO", True, self.PIP_COLOUR, None)

        self.screen.blit(clock_tab_name, (95, 5))
        self.screen.blit(calendar_tab_name, (220, 5))
        self.screen.blit(music_tab_name, (350, 5))

    def alarm_tab(self):
        while True:
            # Background Image for dial Buttons
            dial_img = pygame.image.load("media/black_background.png")
            dial_img = pygame.transform.scale(dial_img, (50, 35))

            # Background Image for alarm Buttons
            alarm_img = pygame.image.load("media/black_background.png")
            alarm_img = pygame.transform.scale(alarm_img, (100, 20))

            cursor_pos = pygame.mouse.get_pos()
            # Clear screen
            self.screen.blit(self.background, (0, 0))

            # Draw tabs
            self.draw_tabs()

            # Render ClockTab
            self.alarm_clock_tab.render()

            # Check alarm
            self.alarm_clock_tab.check_alarm()

            # Builds Bottom Bracket
            self.alarm_clock_tab.build_bottom_bracket()

            # Hour Dial Button Creation
            dial_h = Button(image=dial_img, pos=(195, 215),
                            text_input="{:02d}".format(self.alarm_clock_tab.increment_h), font=self.dial_font,
                            base_color=self.BRIGHT_PIP_COLOUR
                            if self.current_options_index == 1 else self.MID_PIP_COLOUR,
                            hovering_color=self.PIP_COLOUR)

            # Minute Dial Button Creation
            dial_m = Button(image=dial_img, pos=(275, 215),
                            text_input="{:02d}".format(self.alarm_clock_tab.increment_m), font=self.dial_font,
                            base_color=self.BRIGHT_PIP_COLOUR
                            if self.current_options_index == 2 else self.MID_PIP_COLOUR,
                            hovering_color=self.PIP_COLOUR)

            # Alarm Button Creation
            alarm_btn = Button(image=alarm_img, pos=(235, 242),
                               text_input="Set Alarm", font=self.alarm_font,
                               base_color=self.BRIGHT_PIP_COLOUR
                               if self.current_options_index == 3 else self.MID_PIP_COLOUR,
                               hovering_color=self.PIP_COLOUR)

            # Button initialization
            for button in [dial_h, dial_m, alarm_btn]:
                button.change_color(cursor_pos)
                button.update(self.screen)

            # Define selectable options
            options = ["Blank", "HOUR DIAL", "MINUTE DIAL", "SET ALARM"]

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button click
                        # Trigger action based on the current option index
                        if self.current_options_index == 1:
                            self.alarm_clock_tab.increment_dial_h()  # Increment hour
                        elif self.current_options_index == 2:
                            self.alarm_clock_tab.increment_dial_m()  # Increment minute
                        elif self.current_options_index == 3:
                            self.alarm_clock_tab.set_alarm()  # Set alarm
                            self.home()  # Switch Tab To Home
                    if event.button == 3:  # Right mouse button click
                        self.home()   # Switch Tab To Home
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:  # Scroll up
                        self.current_options_index = (self.current_options_index - 1) % len(options)
                    elif event.y < 0:  # Scroll down
                        self.current_options_index = (self.current_options_index + 1) % len(options)

            # Update display
            pygame.display.flip()

            # Adds CRT Filter
            crt_shader.Graphic_engine.__call__(self.crt_shader)
            pygame.time.delay(60)  # Small delay to reduce CPU usage

    def home(self):
        """
        Main game loop that handles events, updates the screen, and renders the clock and tabs.

        This loop continuously listens for user input, updates the display, and calls the necessary
        methods to render the UI elements and handle user interactions.
        """
        run = True
        while run:
            # Ensures no screen overlap
            self.screen.fill("black")

            # Builds Calendar Tab
            self.calendar_tab.render()

            # Checks If Alarm Is Ready
            self.alarm_clock_tab.check_alarm()

            # Builds Bottom Bracket And Ensures Any Pre-Reqs for Alarm
            self.alarm_clock_tab.build_bottom_bracket()

            # Builds Tabs
            self.draw_tabs()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button click
                        if self.alarm_clock_tab.alarm_triggered_flag:  # Ensures Alarm is active to avoid error
                            self.alarm_clock_tab.snooze()  # Snoozes Alarm
                elif event.type == pygame.MOUSEWHEEL:
                    self.alarm_tab()  # Changes to Different Tab

            # Update display
            pygame.display.flip()

            # Adds CRT Filter
            crt_shader.Graphic_engine.__call__(self.crt_shader)
            pygame.time.delay(60)  # Small delay to reduce CPU usage

        pygame.quit()


if __name__ == "__main__":
    app = MainApp()
    app.home()
