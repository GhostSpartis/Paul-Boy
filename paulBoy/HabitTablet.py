from time import strftime
import calendar
import pygame
import json
import os


class HabitTablet:
    """
        A class representing a habit tracking system within a Pygame application.

        Attributes:
            SAVE_FILE (str): The file where habit data is saved.
            PIP_COLOUR (tuple): Color for highlighting elements.
            MID_PIP_COLOUR (tuple): Medium-intensity color for UI elements.
            DARK_PIP_COLOUR (tuple): Darker color for UI elements.
            screen (pygame.Surface): The Pygame screen object.
            font (pygame.Font): Font used for rendering habit-related text.
            tab_font (pygame.Font): Font used for rendering tab labels.
            current_index (int): The currently selected habit index.
            current_day (int): The current day being tracked.
            habits (dict): Dictionary tracking different habit categories and their completion status.
        """

    SAVE_FILE = "habit_data.json"
    PIP_COLOUR = (5, 250, 5)
    MID_PIP_COLOUR = (1, 150, 9)
    DARK_PIP_COLOUR = (1, 50, 9)

    def __init__(self, screen):
        """Initializes the HabitTablet with the given screen and default habit data."""
        self.screen = screen
        self.font = pygame.font.Font("media/monofonto rg.otf", 20)
        self.current_index = 0
        self.tab_font = pygame.font.Font("media/monofonto rg.otf", 30)

        self.current_day = 0

        # Habit tracking
        self.habits = {
            "body": {"count": 0, "daily_check": False},
            "mind": {"count": 0, "daily_check": False},
            "spiritual": {"count": 0, "daily_check": False},
            "skill": {"count": 0, "daily_check": False},
            "social": {"count": 0, "daily_check": False},
        }

        self.load_progress()  # Load existing data at startup

    def draw_habit_frame(self):
        """Draws the decorative frame around the habit tracker."""
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(3, 40, 2, 8))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(3, 40, 78, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(170, 40, 305, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(80, 20, 2, 22))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(80, 20, 5, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(170, 20, 2, 22))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(167, 20, 5, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(170, 40, 45, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(475, 40, 2, 8))

    def draw_habit_image(self, emblem, x):
        """
        Loads and draws a habit-related image at the specified position.

        Args:
            emblem: string representing image location
            x (int): x location of image
        """
        img = pygame.image.load(emblem)
        img = pygame.transform.scale(img, (60, 60))
        img = pygame.transform.flip(img, True, False)
        self.screen.blit(img, (x, 70))

    def draw_habit_buttons(self):
        """Draws the buttons associated with each habit category."""
        self.draw_habit_button(50)
        self.draw_habit_button(130)
        self.draw_habit_button(210)
        self.draw_habit_button(290)
        self.draw_habit_button(370)
        self.completed_this_month(60, "body")
        self.draw_habit_image("media/Bicep.png", 50)
        self.completed_this_month(140, "mind")
        self.draw_habit_image("media/Brain.png", 130)
        self.completed_this_month(220, "spiritual")
        self.draw_habit_image("media/Cross.png", 210)
        self.completed_this_month(300, "skill")
        self.draw_habit_image("media/Skill.png", 290)
        self.completed_this_month(380, "social")
        self.draw_habit_image("media/Social.png", 370)

    def draw_habit_button(self, x):
        """
        Draws a single habit button at the specified x position.

        Args:
            x (int): position of the habit button
        """
        pygame.draw.rect(self.screen, self.PIP_COLOUR, pygame.Rect(x, 130, 2, 62))
        pygame.draw.rect(self.screen, self.PIP_COLOUR, pygame.Rect(x + 60, 130, 2, 62))
        pygame.draw.rect(self.screen, self.PIP_COLOUR, pygame.Rect(x, 130, 60, 2))
        pygame.draw.rect(self.screen, self.PIP_COLOUR, pygame.Rect(x, 190, 60, 2))
        pygame.draw.rect(self.screen, self.PIP_COLOUR, pygame.Rect(x,210, 60, 2))
        pygame.draw.rect(self.screen, self.PIP_COLOUR, pygame.Rect(x, 210, 2, 22))
        pygame.draw.rect(self.screen, self.PIP_COLOUR, pygame.Rect(x + 60, 210, 2, 22))
        pygame.draw.rect(self.screen, self.PIP_COLOUR, pygame.Rect(x, 230, 60, 2))

    def draw_selection_frame(self):
        """Draws a selection frame around the currently selected habit."""
        pygame.draw.rect(self.screen, self.PIP_COLOUR, pygame.Rect(80 * self.current_index + 50, 130, 60, 60))

    def save_progress(self):
        """Saves habit progress to a JSON file."""
        data = {
            "date": strftime("%Y-%m-%d"),
            "habits": self.habits
        }
        with open(self.SAVE_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def load_progress(self):
        """Loads habit progress from a JSON file."""
        if os.path.exists(self.SAVE_FILE):
            with open(self.SAVE_FILE, "r") as file:
                data = json.load(file)
                # If it's a new day, reset daily checks
                if data["date"] == strftime("%Y-%m-%d"):
                    self.habits = data["habits"]
                else:
                    self.reset_daily_checks()
                    self.save_progress()  # Re-save progress for today

    def reset_daily_checks(self):
        """Resets daily checks while keeping the counts."""
        for habit in self.habits.values():
            habit["daily_check"] = False

    def completed_this_month(self, x, count):
        """
        Displays the number of times a habit was completed in the current month.

        Args:
            x (int): X-coordinate of the fraction.
            count (int): amount habit was completed.
        """
        year, month = int(strftime("%Y")), int(strftime("%m"))
        days_in_month = calendar.monthrange(year, month)[1]
        progress_text = f"{self.habits[count]['count']}/{days_in_month}"  # Keep fraction format
        ttl_count = self.font.render(progress_text, True, self.PIP_COLOUR)
        self.screen.blit(ttl_count, (x, 208))

    def increment_btn(self):
        """Increments the habit count for the selected habit if it hasn't been checked today."""
        habit_names = ["body", "mind", "spiritual", "skill", "social"]
        selected_habit = habit_names[self.current_index]

        if not self.habits[selected_habit]["daily_check"]:
            self.habits[selected_habit]["count"] += 1
            self.habits[selected_habit]["daily_check"] = True
            self.save_progress()  # Save progress after increment

    def render(self):
        """Renders the habit tracker UI."""
        self.screen.fill((0, 0, 0), (0, 50, 480, 200))  # Black background
        self.draw_habit_frame()
        self.draw_selection_frame()
        self.draw_habit_buttons()

        habit_tab = self.tab_font.render("HABIT", True, self.PIP_COLOUR, None)
        self.screen.blit(habit_tab, (215, 40))
        youtube_tab = self.tab_font.render("YOUTUBE", True, self.MID_PIP_COLOUR, None)
        self.screen.blit(youtube_tab, (305, 40))

        habit_names = ["body", "mind", "spiritual", "skill", "social"]
        for i, habit in enumerate(habit_names):
            if self.habits[habit]["daily_check"]:  # Check if habit is completed
                checkmark = pygame.image.load("media/Checkmark.png")
                checkmark = pygame.transform.scale(checkmark, (60, 60))
                self.screen.blit(checkmark, (80 * i + 50, 130))
