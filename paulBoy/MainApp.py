import pygame
from ClockTab import ClockTab
from time import strftime
from betterplaysound import playsound


class MainApp:
    def __init__(self):
        pygame.init()

        # Screen setup
        self.SCREEN_WIDTH = 480
        self.SCREEN_HEIGHT = 320
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("PAUL-BOY")

        # Fonts
        self.tab_font = pygame.font.Font("monofonto rg.otf", 30)

        # Colors
        self.PIP_COLOUR = (18, 220, 21)
        self.DARK_PIP_COLOUR = (1, 50, 9)

        # Background
        self.background = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.background.fill((0, 0, 0))  # Black background

        # ClockTab instance
        self.clock_tab = ClockTab(self.screen)

    def draw_tabs(self):
        """Draw the tab names at the top of the screen."""
        clock_tab_name = self.tab_font.render("CLOCK", True, self.PIP_COLOUR, None)
        calendar_tab_name = self.tab_font.render("CLNDR", True, self.PIP_COLOUR, None)
        music_tab_name = self.tab_font.render("RADIO", True, self.PIP_COLOUR, None)

        self.screen.blit(clock_tab_name, (90, 5))
        self.screen.blit(calendar_tab_name, (220, 5))
        self.screen.blit(music_tab_name, (350, 5))

    def run(self):
        """Main game loop."""
        run = True
        while run:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Clear screen
            self.screen.blit(self.background, (0, 0))

            # Draw tabs
            self.draw_tabs()

            # Render ClockTab
            self.clock_tab.render()

            # Update display
            pygame.display.flip()
            pygame.time.delay(100)  # Small delay to reduce CPU usage

        pygame.quit()


if __name__ == "__main__":
    app = MainApp()
    app.run()
