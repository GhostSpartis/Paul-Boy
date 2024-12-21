import pygame
import calendar
from datetime import datetime
from AlarmClockTab import AlarmClockTab
from time import strftime


class CalendarTab:
    """
    A class to manage and render the calendar tab in a Pygame application.

    Attributes:
    -----------
    PIP_COLOUR : tuple
        RGB color for the main green color used in the interface.
    MID_PIP_COLOUR : tuple
        RGB color for the medium green color used in the interface.
    DARK_PIP_COLOUR : tuple
        RGB color for the dark green color used in the interface.
    screen : pygame.Surface
        The surface where the calendar tab will be rendered.
    bottom_bar_font : pygame.font.Font
        Font used for the bottom bar text.
    alarm_font : pygame.font.Font
        Font used for displaying alarm-related text.
    dial_font : pygame.font.Font
        Font used for displaying dials.
    tab_font : pygame.font.Font
        Font used for the tab labels.
    side_clock_font : pygame.font.Font
        Font used for the main clock display.
    current_date : datetime
        The current date and time.
    clock_tab : ClockTab
        An instance of the ClockTab class used for drawing and managing clock-related features.

    Methods:
    --------
    draw_calendar():
        Render the calendar for the current month, highlighting the current day.
    draw_calendar_frame():
        Draw a decorative frame around the calendar area.
    render():
        Render the complete calendar tab, including the calendar, clock, and alarm information.
    """

    PIP_COLOUR = (5, 250, 5)
    MID_PIP_COLOUR = (1, 150, 9)
    DARK_PIP_COLOUR = (1, 50, 9)

    def __init__(self, screen):
        self.screen = screen
        self.bottom_bar_font = pygame.font.Font("media/monofonto rg.otf", 25)
        self.alarm_font = pygame.font.Font("media/monofonto rg.otf", 20)
        self.dial_font = pygame.font.Font("media/monofonto rg.otf", 40)
        self.tab_font = pygame.font.Font("media/monofonto rg.otf", 30)
        self.side_clock_font = pygame.font.Font("media/monofonto rg.otf", 80)
        self.current_date = datetime.now()
        self.clock_tab = AlarmClockTab(screen)

    def draw_calendar(self):
        """
        Render the calendar for the current month, highlighting the current day.

        The calendar displays the current month's days in a grid, with the current day highlighted in red.
        """
        # Get current month and year
        year = int(strftime("%Y"))
        month = int(strftime("%m"))
        day = int(strftime("%d"))

        # Get month calendar as a matrix
        month_calendar = calendar.monthcalendar(year, month)

        # Render month name and year
        header = f"{calendar.month_name[month]} {year}"
        header_surface = self.alarm_font.render(header, True, self.PIP_COLOUR, None)
        self.screen.blit(header_surface, (280, 80))

        # Render the calendar grid
        for row, week in enumerate(month_calendar):
            for col, date in enumerate(week):
                if date != 0:
                    color = self.PIP_COLOUR if date != day else (255, 0, 0)  # Highlight today in red
                    date_surface = self.alarm_font.render(str(date), True, color, None)
                    self.screen.blit(date_surface, (260 + col * 30, 100 + row * 25))

    def draw_calendar_frame(self):
        """
        Draw the decorative frame around the Calendar.

        This method creates a visual border around the Calendar display area.
        """
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(3, 40, 2, 8))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(3, 40, 203, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(205, 20, 2, 22))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(205, 20, 5, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(295, 20, 2, 22))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(290, 20, 5, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(295, 40, 180, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(475, 40, 2, 8))

    def render(self):
        """
        Render the complete calendar tab.

        This includes drawing the calendar, clock, and alarm information, along with the decorative frame and tabs.
        """
        # Builds Frame Around Display
        self.draw_calendar_frame()

        # Builds Calendar and Side-Clock
        self.draw_calendar()
        current_time = strftime('%H:%M')
        clock_surface = self.side_clock_font.render(current_time, True, self.PIP_COLOUR, None)
        self.screen.blit(clock_surface, (20, 120))

        # Top Sub-Bar Tabs
        alarm_tab = self.tab_font.render("ALARM", True, self.MID_PIP_COLOUR, None)
        self.screen.blit(alarm_tab, (300, 40))
        date_tab = self.tab_font.render("DATE", True, self.PIP_COLOUR, None)
        self.screen.blit(date_tab, (215, 40))

        # Builds Bottom Bracket
        self.clock_tab.build_bottom_bracket()
