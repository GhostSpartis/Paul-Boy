import pygame
import os
import math

class RadioTab:
    """
    A music player tab that allows the user to navigate a playlist, play, pause, stop, and visualize music.

    Attributes:
        screen (pygame.Surface): The screen surface where elements are drawn.
        font (pygame.font.Font): Font for displaying text.
        playlist (list): A list of music file paths.
        current_index (int): Index of the currently highlighted song.
        is_playing (bool): Indicates if a song is currently playing.
        wave_phase (float): Controls the oscillation movement for the visualizer.
        wave_amplitude (int): Height of the waveform oscillation.
        wave_frequency (float): Speed of the oscillation effect.
    """
    PIP_COLOUR = (5, 250, 5)
    MID_PIP_COLOUR = (1, 150, 9)
    DARK_PIP_COLOUR = (1, 50, 9)

    def __init__(self, screen, music_folder="media/music"):
        self.screen = screen
        self.font = pygame.font.Font("media/monofonto rg.otf", 20)

        # Initialize pygame mixer for music playback
        pygame.mixer.init()
        pygame.mixer.set_num_channels(1)

        self.wave_phase = 0  # Controls the oscillation movement
        self.wave_amplitude = 30  # Height of the wave
        self.wave_frequency = 0.2  # Speed of oscillation
        self.music_folder = music_folder
        self.playlist = self.create_song_playlist()
        self.current_index = 0  # Tracks which song is highlighted
        self.is_playing = False

        # Load first song if available
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_index])

    def create_song_playlist(self):
        """Loads all MP3 files from the given folder into a playlist."""
        return [os.path.join(self.music_folder, file) for file in os.listdir(self.music_folder) if file.endswith(".mp3")]

    def draw_radio_frame(self):
        """Draws the decorative frame around the music player."""
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(3, 40, 2, 8))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(3, 40, 338, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(340, 20, 2, 22))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(340, 20, 5, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(430, 20, 2, 22))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(427, 20, 5, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(430, 40, 45, 2))
        pygame.draw.rect(self.screen, self.MID_PIP_COLOUR, pygame.Rect(475, 40, 2, 8))
        pygame.draw.rect(self.screen, self.PIP_COLOUR, pygame.Rect(325, 200, 130, 2))
        pygame.draw.rect(self.screen, self.PIP_COLOUR, pygame.Rect(455, 77, 2, 125))

    def draw_selection_frame(self):
        """Draws a selection box around the currently highlighted song."""
        pygame.draw.rect(self.screen, self.PIP_COLOUR, pygame.Rect(30, 80 + self.current_index * 20, 250, 18))
        pygame.draw.rect(self.screen, self.DARK_PIP_COLOUR, pygame.Rect(35, 84 + self.current_index * 20, 10, 10))

    def draw_playlist(self):
        """Displays the list of songs with the highlighted selection frame."""
        for i, song in enumerate(self.playlist):
            song_name = os.path.basename(song)[:-4]  # Remove ".mp3" extension
            song_name = self.minimize(song_name)
            color = self.DARK_PIP_COLOUR if i == self.current_index else self.PIP_COLOUR
            song_surface = self.font.render(song_name, True, color, None)
            self.screen.blit(song_surface, (50, 77 + i * 20))

    def minimize(self, songtext):
        """Truncates the song name if it's longer than 21 characters."""
        return songtext[:19] + "..." if len(songtext) > 21 else songtext

    def play_selected_song(self):
        """Plays the currently selected song."""
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()
            self.is_playing = True

    def pause_music(self):
        """Pauses the currently playing song."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_playing = False

    def resume_music(self):
        """Resumes the paused song."""
        pygame.mixer.music.unpause()
        self.is_playing = True

    def stop_music(self):
        """Stops the currently playing song."""
        pygame.mixer.music.stop()
        self.is_playing = False

    def update_visualizer(self):
        """
        Updates the waveform visualizer by shifting the phase of the oscillating wave.
        """
        if pygame.mixer.music.get_busy():
            self.wave_phase += self.wave_frequency  # Move the wave over time

    def draw_waveform(self):
        """
        Draws an oscillating waveform across the screen.
        """

        start_x = 325
        center_y = 150
        wave_color = self.PIP_COLOUR

        for x in range(0, 125, 5):  # Draw points from left to right
            y_offset = int(self.wave_amplitude * math.sin((x * 0.05) + self.wave_phase))
            pygame.draw.circle(self.screen, wave_color, (start_x + x, center_y + y_offset), 2)


    def render(self):
        """Renders the music player interface."""
        self.screen.fill((0, 0, 0), (0, 50, 480, 200))  # Black background

        self.draw_radio_frame()
        self.draw_selection_frame()
        self.draw_playlist()
        self.update_visualizer()
        self.draw_waveform()

