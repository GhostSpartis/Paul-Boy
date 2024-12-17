import pygame
from time import strftime
from betterplaysound import playsound
class ClockTab:

    PIP_COLOUR = (18, 220, 21)
    MID_PIP_COLOUR = (1, 150, 9)
    DARK_PIP_COLOUR = (1, 50, 9)


    def __init__(self, screen):
        self.screen = screen
        self.clock_font = pygame.font.Font("monofonto rg.otf", 130)
        self.date_font = pygame.font.Font("monofonto rg.otf", 20)
        self.button_font = pygame.font.Font("monofonto rg.otf", 20)

    def draw_clock_frame(self):
        """Draw the decorative frame around the clock."""
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(3, 40, 2, 8))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(3, 40, 77, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(80, 20, 2, 22))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(80, 20, 5, 2))

        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(170, 20, 2, 22))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(165, 20, 5, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(170, 40, 305, 2))

        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(475, 40, 2, 8))

    def draw_clock(self):
        """Render and return the clock text surface."""
        current_time = strftime('%H:%M')
        clock_surface = self.clock_font.render(current_time, True, self.PIP_COLOUR, None)
        return clock_surface

    def draw_date(self):
        """Render and return the date surface."""
        date_string = strftime("%m.%d.%Y")
        date_surface = self.date_font.render(date_string, True, self.PIP_COLOUR, None)
        return date_surface

    def draw_alarm_button(self):
        """Render and return the alarm button surface."""
        alarm_surface = self.button_font.render("Set Alarm", True, self.PIP_COLOUR, None)
        return alarm_surface

    def render(self):
        """Main method to render the entire Clock tab."""
        # Draw clock frame
        self.draw_clock_frame()

        # Clear clock area
        self.screen.fill((0, 0, 0), (80, 80, 350, 300))  # Black area for clock

        # Draw clock
        self.screen.blit(self.draw_clock(), (80, 80))

        # Draw date
        self.screen.fill(self.DARK_PIP_COLOUR, (3, 280, 157, 30))
        self.screen.blit(self.draw_date(), (5, 283))

        # Draw alarm button
        self.screen.fill(self.DARK_PIP_COLOUR, (163, 280, 130, 30))
        self.screen.blit(self.draw_alarm_button(), (165, 282))

        #draw blank edge
        self.screen.fill(self.DARK_PIP_COLOUR, (296, 280, 180, 30))

