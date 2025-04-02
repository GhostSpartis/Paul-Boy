import pygame
from google.oauth2 import service_account
from googleapiclient.discovery import build


class YoutubeTablet:
    """
    A class representing a YouTube statistics display module for a Pygame-based application.

    Attributes:
        PIP_COLOUR (tuple): RGB color for bright green.
        MID_PIP_COLOUR (tuple): RGB color for medium green.
        DARK_PIP_COLOUR (tuple): RGB color for dark green.
        RED (tuple): RGB color for red.
        screen (pygame.Surface): The Pygame screen surface.
        font (pygame.font.Font): The font used for rendering text.
        SERVICE_ACCOUNT_FILE (str): Path to the service account JSON file.
        SCOPES (list): List of scopes for YouTube API access.
        credentials (Credentials): Authentication credentials for YouTube API.
        youtube (Resource): YouTube API client instance.
        CHANNEL_ID (str): The YouTube channel ID to fetch statistics for.
        subs (int): Number of subscribers.
        views (int): Number of views.
        videos (int): Number of videos.
        channel_name (str): The name of the YouTube channel.
    """

    PIP_COLOUR = (5, 250, 5)
    MID_PIP_COLOUR = (1, 150, 9)
    DARK_PIP_COLOUR = (1, 50, 9)
    RED = (255, 0, 0)

    def __init__(self, screen):
        """
        Initializes the YouTubeTablet with a given Pygame screen.

        Args:
            screen (pygame.Surface): The Pygame screen where stats will be displayed.
        """
        self.screen = screen
        self.font = pygame.font.Font("media/monofonto rg.otf", 30)
        self.SERVICE_ACCOUNT_FILE = 'media/APIUSER.json'
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
        self.credentials = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        self.youtube = build('youtube', 'v3', credentials=self.credentials)
        self.CHANNEL_ID = 'PUT CHANNEL ID'
        self.subs = 0
        self.views = 0
        self.videos = 0
        self.channel_name = "john"

    def draw_youtube_frame(self):
        """Draws the decorative frame around the YouTube stats section."""
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(3, 40, 2, 8))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(3, 40, 78, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(170, 40, 305, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(80, 20, 2, 22))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(80, 20, 5, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(170, 20, 2, 22))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(167, 20, 5, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(170, 40, 45, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(475, 40, 2, 8))

    def draw_image(self, emblem, x, y):
        """
        Loads and draws an image onto the screen.

        Args:
            emblem (str): Path to the image file.
            x (int): X-coordinate of the image.
            y (int): Y-coordinate of the image.
        """
        img = pygame.image.load(emblem)
        img = pygame.transform.scale(img, (30, 30))
        img = pygame.transform.flip(img, True, False)
        self.screen.blit(img, (x, y))

    def get_youtube_stats(self):
        """Fetches YouTube statistics for the specified channel using the YouTube API."""
        request = self.youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=self.CHANNEL_ID
        )
        response = request.execute()
        channel_info = response['items'][0]
        stats = channel_info['statistics']
        snippet = channel_info['snippet']
        self.channel_name = snippet['title']
        self.subs = stats['subscriberCount'] + " Subs"
        self.views = stats['viewCount'] + " Views"
        self.videos = stats['videoCount'] + " Videos"

    def draw_stat(self, stat, x, y):
        """
        Draws a statistic on the screen.

        Args:
            stat : The string or integer representing the statistic.
            x (int): X-coordinate of the text.
            y (int): Y-coordinate of the text.
        """
        stat_name = self.font.render(stat, True, self.PIP_COLOUR)
        self.screen.blit(stat_name, (x, y))

    def draw_stat_frame(self, x, y, length, width):
        """
        Draws a rectangular frame around a statistic.

        Args:
            x (int): X-coordinate of the rectangle.
            y (int): Y-coordinate of the rectangle.
            length (int): Width of the rectangle.
            width (int): Height of the rectangle.
        """
        pygame.draw.rect(self.screen, self.PIP_COLOUR, pygame.Rect(x, y, length, width))

    def render(self):
        """Renders the YouTube statistics on the screen."""
        self.get_youtube_stats()
        self.draw_youtube_frame()
        habit_tab = self.font.render("HABIT", True, self.MID_PIP_COLOUR, None)
        self.screen.blit(habit_tab, (110, 40))
        youtube_tab = self.font.render("YOUTUBE", True, self.PIP_COLOUR, None)
        self.screen.blit(youtube_tab, (200, 40))
        pygame.draw.rect(self.screen, self.DARK_PIP_COLOUR, pygame.Rect(40, 122, 410, 130))
        goal = self.font.render("      1,000 Subs", True, self.RED, None)
        self.screen.blit(goal, (200, 200))
        self.draw_image("media/TrophyGoal.png", 250, 205)
        self.draw_stat_frame(40, 82, 410, 30)
        channel_name = self.font.render(self.channel_name, True, self.DARK_PIP_COLOUR)
        self.screen.blit(channel_name, (100, 80))
        self.draw_stat(self.videos, 300, 140)
        self.draw_image("media/CabinetVideos.png", 265, 145)
        self.draw_stat(self.views, 70, 140)
        self.draw_image("media/EyeViews.png", 40, 145)
        self.draw_stat(self.subs, 70, 200)
        self.draw_image("media/Social.png", 40, 205)
