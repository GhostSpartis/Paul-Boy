import multiprocessing
import pygame
from time import strftime
from betterplaysound import playsound


class AlarmClockTab:
    """
    ClockTab class manages the clock display, alarm settings, and alarm notifications.

    Attributes:
        PIP_COLOUR (tuple): The color used for clock and text.
        MID_PIP_COLOUR (tuple): The color used for the middle part of the clock frame.
        DARK_PIP_COLOUR (tuple): The color used for the darker part of the clock frame.
        screen (pygame.Surface): The screen surface where elements are drawn.
        clock_font (pygame.font.Font): Font used for displaying the time.
        bottom_bar_font (pygame.font.Font): Font used for displaying the date and other info.
        alarm_font (pygame.font.Font): Font used for the alarm notification and settings.
        dial_font (pygame.font.Font): Font used for displaying the alarm time dials.
        increment_h (int): Hour value for the alarm time.
        increment_m (int): Minute value for the alarm time.
        alarm_time (str): The formatted time string for the alarm.
        alarm_h (int): Hour value of the set alarm.
        alarm_m (int): Minute value of the set alarm.
        alarm_triggered_flag (bool): Flag indicating if the alarm has been triggered.
        snooze_check (bool): Flag indicating if snooze is active.
        stop_alarm_sound (bool): Flag for stopping the alarm sound.
        music (multiprocessing.Process): Process for playing the alarm sound.
    """

    PIP_COLOUR = (5, 250, 5)
    MID_PIP_COLOUR = (1, 150, 9)
    DARK_PIP_COLOUR = (1, 50, 9)

    def __init__(self, screen):
        """
        Initialize the ClockTab with a screen surface and default settings for the clock and alarm.

        Args:
            screen (pygame.Surface): The surface on which to draw the clock and other UI elements.
        """
        self.screen = screen
        self.clock_font = pygame.font.Font("media/monofonto rg.otf", 140)
        self.bottom_bar_font = pygame.font.Font("media/monofonto rg.otf", 25)
        self.alarm_font = pygame.font.Font("media/monofonto rg.otf", 20)
        self.dial_font = pygame.font.Font("media/monofonto rg.otf", 40)
        self.tab_font = pygame.font.Font("media/monofonto rg.otf", 30)

        self.increment_h = 0
        self.increment_m = 0
        self.alarm_time = ""
        self.alarm_h = 0
        self.alarm_m = 0

        self.alarm_triggered_flag = False
        self.snooze_check = False
        self.stop_alarm_sound = False

        self.music = multiprocessing.Process(target=playsound, args=("media/Alarm Sound.mp3",), daemon=True)

    def draw_clock_frame(self):
        """
        Draw the decorative frame around the clock for the tabs.
        """
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(3, 40, 2, 8))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(3, 40, 203, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(205, 20, 2, 22))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(205, 20, 5, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(295, 20, 2, 22))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(290, 20, 5, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(295, 40, 180, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(475, 40, 2, 8))

    def draw_clock(self):
        """
        Render and return the clock text surface.
        """
        current_time = strftime('%H:%M')
        clock_surface = self.clock_font.render(current_time, True, self.PIP_COLOUR, None)
        return clock_surface

    def draw_date(self):
        """
        Render and return the date surface.
        """
        date_string = strftime("%m.%d.%Y")
        date_surface = self.bottom_bar_font.render(date_string, True, self.PIP_COLOUR, None)
        return date_surface

    def draw_alarm_button(self):
        """
        Render and return the alarm button surface.
        """
        alarm_surface = self.alarm_font.render("Set Alarm", True, self.PIP_COLOUR, None)
        return alarm_surface

    def draw_dial(self, increment):
        """
        Render and return the alarm dial surface.

        Args:
            increment (int): The current value of the dial (hour or minute).
        """
        if increment > 9:
            dial_surface = self.dial_font.render(str(increment), True, self.PIP_COLOUR, None)
        else:
            dial_surface = self.dial_font.render("{:02d}".format(increment), True, self.PIP_COLOUR, None)
        return dial_surface

    def increment_dial_h(self):
        """
        Increment the hour dial value for setting the alarm.

        If the hour reaches 23, it wraps around to 0.
        """
        if self.increment_h >= 23:
            self.increment_h = 0
        else:
            self.increment_h += 1

    def increment_dial_m(self):
        """
        Increment the minute dial value for setting the alarm.

        If the minute reaches 59, it wraps around to 0.
        """
        if self.increment_m >= 59:
            self.increment_m = 0
        else:
            self.increment_m += 1

    def view_alarm(self):
        """
        Display an alarm icon if the alarm is set.

        This method renders an image representing the alarm when it is set.
        """
        if self.alarm_time != "":
            imp = pygame.image.load("media/VaultBoyApproved.png").convert_alpha()
            imp = pygame.transform.scale(imp, (60, 60))
            imp = pygame.transform.flip(imp, True, False)
            self.screen.blit(imp, (410, 250))

    def set_alarm(self):
        """
        Set the alarm to the current dial values.

        This method updates the alarm time using the current hour and minute values
        from the dials and resets the flags for the next alarm.
        """
        self.alarm_h = self.increment_h
        self.alarm_m = self.increment_m
        self.alarm_triggered_flag = False
        self.snooze_check = False
        self.alarm_time = "{:02d}".format(self.increment_h) + ":" + "{:02d}".format(self.increment_m)

    def check_alarm(self):
        """
        Check if the current time matches the set alarm and play a sound.

        If the time matches the alarm, it triggers the alarm sound.
        """
        current_hour = int(strftime("%H"))
        current_minute = int(strftime("%M"))

        if not self.snooze_check:
            if self.alarm_h == current_hour and self.alarm_m == current_minute:
                if not self.alarm_triggered_flag:
                    self.alarm_triggered_flag = True
                    self.music = multiprocessing.Process(
                        target=playsound, args=("media/Alarm Sound.mp3",), daemon=True)
                    self.music.start()
            else:
                self.alarm_triggered_flag = False

    def snooze(self):
        """
        Snooze the alarm for a period.

        Stops the alarm sound and sets the snooze check to true.
        """
        self.snooze_check = True
        self.alarm_triggered_flag = False
        self.music.kill()

    def alarm_notification(self):
        """
        Display the alarm notification on the screen.

        This method renders a notification on the screen when the alarm has been triggered.
        """
        if self.alarm_triggered_flag:
            # Builds Box
            self.screen.fill(self.DARK_PIP_COLOUR, (145, 90, 180, 100))
            self.screen.fill(self.PIP_COLOUR, (145, 90, 180, 2))
            self.screen.fill(self.PIP_COLOUR, (145, 190, 180, 2))
            self.screen.fill(self.PIP_COLOUR, (145, 90, 2, 100))
            self.screen.fill(self.PIP_COLOUR, (325, 90, 2, 100))

            # Builds Snooze Message
            snooze = self.alarm_font.render("WAKE UP TIME!!!", True, self.PIP_COLOUR, None)
            self.screen.blit(snooze, (165, 115))

            # Builds Ok Button
            ok = self.alarm_font.render("OK", True, self.DARK_PIP_COLOUR, None)
            self.screen.fill(self.PIP_COLOUR, (216, 150, 40, 30))
            self.screen.blit(ok, (225, 152))

    def total_sleep(self):
        """
        Calculate the total time remaining until the alarm goes off.
        """
        total_hours = self.increment_h - int(strftime('%H'))
        if total_hours < 0:
            total_hours = self.increment_h - int(strftime('%H')) + 24

        total_minutes = self.increment_m - int(strftime('%M')) + 60
        if total_minutes == 60:
            total_minutes = 0
        elif total_minutes > 60:
            total_minutes = self.increment_m - int(strftime('%M'))

        total = str(total_hours) + "Hrs " + str(total_minutes) + "M"
        return total

    def render(self):
        """
        Main method to render the entire Clock tab.

        This method handles all the drawing and rendering of elements such as the clock,
        alarm settings, buttons, date, and notification.
        """
        # Builds Clock Frame
        self.draw_clock_frame()
        self.screen.fill((0, 0, 0), (58, 50, 250, 200))  # Black area for clock

        # Builds Clock and Dials for Alarm Setting
        self.screen.blit(self.draw_clock(), (58, 50))
        self.screen.blit(self.draw_dial(self.increment_h), (175, 190))
        self.screen.blit(self.draw_dial(self.increment_m), (255, 190))
        dial_separation = self.dial_font.render(":", True, self.PIP_COLOUR, None)
        self.screen.blit(dial_separation, (225, 190))

        # Builds set alarm button
        self.screen.blit(self.draw_alarm_button(), (190, 230))

        alarm_tab = self.tab_font.render("ALARM", True, self.PIP_COLOUR, None)
        self.screen.blit(alarm_tab, (212, 40))
        date_tab = self.tab_font.render("DATE", True, self.MID_PIP_COLOUR, None)
        self.screen.blit(date_tab, (140, 40))

    def build_bottom_bracket(self):
        """ Builds the bottom bracket for the pip-boy with date, hours of sleep and alarm indicator"""
        # Builds Bottom Left Bracket
        self.screen.fill(self.DARK_PIP_COLOUR, (3, 280, 157, 30))
        self.screen.blit(self.draw_date(), (5, 282))
        self.screen.fill(self.DARK_PIP_COLOUR, (163, 280, 130, 30))

        # Builds Bottom Center Bracket
        hours_sleep = self.bottom_bar_font.render(self.total_sleep(), True, self.PIP_COLOUR, None)
        self.screen.blit(hours_sleep, (165, 282))

        # Builds Bottom Right Bracket
        self.screen.fill(self.DARK_PIP_COLOUR, (296, 280, 180, 30))
        alarm = self.bottom_bar_font.render(self.alarm_time, True, self.PIP_COLOUR, None)
        self.screen.blit(alarm, (300, 282))

        # Ensures alarm is view no matter what screen
        self.view_alarm()
        self.alarm_notification()
