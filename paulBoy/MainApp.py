import pygame
from betterplaysound import playsound
import crt_shader
from Button import Button
from AlarmClockTablet import AlarmClockTab
from CalendarTablet import CalendarTab
from pygame.locals import *
from HabitTablet import HabitTablet
from RadioTab import RadioTab
from YoutubeTablet import YoutubeTablet
from crt_shader import Graphic_engine

class MainApp:
    """
    The main application class for PAUL-BOY, a retro-style interface application.

    This class manages the main application loop, handles user input, and coordinates
    between different tabs (alarm clock, calendar, radio, habit tracker, and YouTube player).
    It also handles the CRT shader effect for retro display aesthetics.

    Attributes:
        SCREEN_WIDTH (int): Width of the application window
        SCREEN_HEIGHT (int): Height of the application window
        SCREEN_SIZE (tuple): Tuple containing screen dimensions
        screen (pygame.Surface): Main drawing surface
        crt_shader (Graphic_engine): CRT shader effect handler
        tab_font (pygame.font.Font): Font for tab labels
        dial_font (pygame.font.Font): Font for dial displays
        alarm_font (pygame.font.Font): Font for alarm buttons
        BRIGHT_PIP_COLOUR (tuple): RGB color for bright elements
        PIP_COLOUR (tuple): RGB color for normal elements
        MID_PIP_COLOUR (tuple): RGB color for medium-brightness elements
        DARK_PIP_COLOUR (tuple): RGB color for dark elements
        background (pygame.Surface): Background surface
        alarm_clock_tab (AlarmClockTab): Alarm clock tab instance
        calendar_tab (CalendarTab): Calendar tab instance
        radio_player_tab (RadioTab): Radio player tab instance
        youtube_tablet (YoutubeTablet): YouTube player tab instance
        habit_tablet (HabitTablet): Habit tracker tab instance
        current_tab (str): Currently active tab identifier
        current_options_index (int): Index of currently selected option
    """

    def __init__(self):
        """
        Initialize the MainApp class with all necessary components.

        Sets up the pygame environment, display settings, fonts, colors,
        and initializes all tab components.
        """
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer module for sound

        self.SCREEN_WIDTH = 480
        self.SCREEN_HEIGHT = 320
        self.SCREEN_SIZE = (480, 320)
        self.screen = pygame.Surface((480, 320)).convert((255, 65282, 16711681, 0))
        pygame.display.set_caption("PAUL-BOY")
        pygame.display.set_mode(self.SCREEN_SIZE, DOUBLEBUF | OPENGL)

        self.crt_shader = Graphic_engine(self.screen)

        self.tab_font = pygame.font.Font("media/monofonto rg.otf", 30)
        self.dial_font = pygame.font.Font("media/monofonto rg.otf", 40)
        self.alarm_font = pygame.font.Font("media/monofonto rg.otf", 20)

        self.BRIGHT_PIP_COLOUR = (0, 250, 0)
        self.PIP_COLOUR = (5, 250, 5)
        self.MID_PIP_COLOUR = (1, 150, 9)
        self.DARK_PIP_COLOUR = (1, 50, 9)

        self.background = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.background.fill((0, 0, 0))

        self.alarm_clock_tab = AlarmClockTab(self.screen)
        self.calendar_tab = CalendarTab(self.screen)
        self.radio_player_tab = RadioTab(self.screen)
        self.youtube_tablet = YoutubeTablet(self.screen)
        self.habit_tablet = HabitTablet(self.screen)

        self.current_tab = "date"
        self.current_options_index = 0

        self.looping_sound = pygame.mixer.Sound("media/intro_sound.wav")
        self.looping_sound.set_volume(0.5)
        self.looping_sound.play(loops=-1)

        self.flip_sound = pygame.mixer.Sound("media/flip.wav")
        self.click_sound = pygame.mixer.Sound("media/btn_prs.wav")

    def draw_tabs(self):
        """
        Draw the tab labels at the top of the screen.

        Renders and displays the names of the available tabs (STAT, DATA, RADIO)
        using the configured tab font and colors.
        """
        clock_tab_name = self.tab_font.render("STAT", True, self.PIP_COLOUR, None)
        calendar_tab_name = self.tab_font.render("DATA", True, self.PIP_COLOUR, None)
        music_tab_name = self.tab_font.render("RADIO", True, self.PIP_COLOUR, None)
        self.screen.blit(clock_tab_name, (95, 5))
        self.screen.blit(calendar_tab_name, (220, 5))
        self.screen.blit(music_tab_name, (350, 5))

    def handle_events(self):
        """
        Handle all pygame events in the main application loop.

        Processes quit events, mouse clicks (for tab switching and controls),
        and mouse wheel events (for scrolling through options).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Right mouse button click switches tabs
                    self.looping_sound.stop()
                    self.flip_sound.play(maxtime=100)
                    pygame.time.wait(120)  # Wait for the click sound to finish
                    self.looping_sound.play(loops=-1)  # Restart the looping sound
                    self.switch_tab()
                self.handle_tab_controls(event)
            elif event.type == pygame.MOUSEWHEEL:
                self.handle_scroll(event.y)

    def switch_tab(self):
        """
        Cycle through the available tabs in a predefined order.

        The tab order is: date -> alarm -> radio -> habit -> youtube -> date...
        Updates the current_tab attribute to reflect the newly selected tab.
        """
        tab_order = ["date", "alarm", "radio", "habit", "youtube"]
        current_index = tab_order.index(self.current_tab)
        self.current_tab = tab_order[(current_index + 1) % len(tab_order)]

    def click_noise(self):
        """ Click sound for button 1 click """
        self.looping_sound.stop()
        self.click_sound.play(maxtime=100)
        pygame.time.wait(120)  # Wait for the click sound to finish
        self.looping_sound.play(loops=-1)  # Restart the looping sound

    def handle_tab_controls(self, event):
        """
        Handle control events specific to the currently active tab.

        Args:
            event (pygame.Event): The pygame event to handle
        """
        if self.current_tab == "alarm":
            if event.button == 1:
                self.click_noise()
                if self.alarm_clock_tab.alarm_triggered_flag:  # Ensures Alarm is active to avoid error
                    self.radio_player_tab.pause_music()
                    self.alarm_clock_tab.snooze()  # Snoozes Alarm
                if self.current_options_index == 1:
                    self.alarm_clock_tab.increment_dial_h()
                elif self.current_options_index == 2:
                    self.alarm_clock_tab.increment_dial_m()
                elif self.current_options_index == 3:
                    self.alarm_clock_tab.set_alarm()
                    self.current_tab = "date"
        elif self.current_tab == "radio":
            if event.button == 1:
                self.click_noise()
                if self.alarm_clock_tab.alarm_triggered_flag:  # Ensures Alarm is active to avoid error
                    self.radio_player_tab.pause_music()
                    self.alarm_clock_tab.snooze()  # Snoozes Alarm
                self.radio_player_tab.play_selected_song()
        elif self.current_tab == "habit":
            if event.button == 1:
                self.click_noise()
                if self.alarm_clock_tab.alarm_triggered_flag:  # Ensures Alarm is active to avoid error
                    self.radio_player_tab.pause_music()
                    self.alarm_clock_tab.snooze()  # Snoozes Alarm
                self.habit_tablet.increment_btn()
        elif self.current_tab == "youtube":
            if self.alarm_clock_tab.alarm_triggered_flag:  # Ensures Alarm is active to avoid error
                self.radio_player_tab.pause_music()
                self.alarm_clock_tab.snooze()  # Snoozes Alarm

    def handle_scroll(self, direction):
        """
        Handle mouse wheel scrolling events for the current tab.

        Args:
            direction (int): The direction of scrolling (positive for up, negative for down)
        """
        if self.current_tab == "alarm":
            # Define selectable options
            options = ["Blank", "HOUR DIAL", "MINUTE DIAL", "SET ALARM"]
            self.current_options_index = (self.current_options_index - direction) % len(options)
        elif self.current_tab == "radio":
            if direction > 0:
                if self.radio_player_tab.current_index > 0:
                    self.radio_player_tab.current_index = (self.radio_player_tab.current_index - 1)  # scrolls up
                else:
                    self.radio_player_tab.resume_music()  # resume music if scroll too high
                    self.radio_player_tab.current_index = -1
            elif direction < 0:
                if self.radio_player_tab.current_index >= 8:
                    self.radio_player_tab.pause_music()  # pauses music if scrolls too high
                    self.radio_player_tab.current_index = 9
                else:
                    self.radio_player_tab.current_index = (self.radio_player_tab.current_index + 1)  # scrolls down
        elif self.current_tab == "habit":
            if direction > 0 and self.habit_tablet.current_index > 0:
                self.habit_tablet.current_index -= 1
            elif direction < 0 and self.habit_tablet.current_index < 4:
                self.habit_tablet.current_index += 1

    def render(self):
        """
        Render all components of the application.

        This includes the background, tabs, and the content of the currently active tab.
        Also handles the CRT shader effect and manages the display flip.
        """
        self.screen.blit(self.background, (0, 0))
        self.draw_tabs()

        if self.current_tab == "date":
            self.calendar_tab.render()
        elif self.current_tab == "alarm":
            self.alarm_clock_tab.render()
            # Background Image for dial Buttons
            dial_img = pygame.image.load("media/black_background.png")
            dial_img = pygame.transform.scale(dial_img, (50, 35))

            # Background Image for alarm Buttons
            alarm_img = pygame.image.load("media/black_background.png")
            alarm_img = pygame.transform.scale(alarm_img, (100, 20))

            cursor_pos = pygame.mouse.get_pos()
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

        elif self.current_tab == "radio":
            self.radio_player_tab.render()
        elif self.current_tab == "habit":
            self.habit_tablet.render()
        elif self.current_tab == "youtube":
            self.youtube_tablet.render()

        self.alarm_clock_tab.check_alarm()
        self.alarm_clock_tab.build_bottom_bracket()
        pygame.display.flip()
        crt_shader.Graphic_engine.__call__(self.crt_shader)
        pygame.time.delay(60)

    def run(self):
        """
        Run the main application loop.

        Continuously processes events and renders the application until quit.
        """
        while True:
            self.handle_events()
            self.render()

if __name__ == "__main__":
    app = MainApp()
    app.run()