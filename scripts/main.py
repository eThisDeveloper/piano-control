import aubio
import numpy as np
import pyaudio
import time
import keystrokes
import pygame
import sys

# initialize audio stream and pitch detection
p = pyaudio.PyAudio()

# set up audio stream from selected device
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True,
                input_device_index=0, frames_per_buffer=1024)
pitch_o = aubio.pitch("yin", 4096, 1024, 44100)

# set tolerance for pitch detection
pitch_o.set_tolerance(0.8)

# define piano note frequencies
note_freqs = {"C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13,
              "E": 329.63, "F": 349.23, "F#": 369.99, "G": 392.00,
              "G#": 415.30, "A": 440.00, "A#": 466.16, "B": 493.88}

# set threshold for input volume
volume_threshold = 0.05

# set interval for note counting
note_count_interval = 0.5  # seconds

# initialize note buffer and time buffer
note_buffer = []
time_buffer = []

# initialize Pygame
pygame.init()

# set up the window
window_width = 400
window_height = 400
window = pygame.display.set_mode((window_width, window_height))

while True:
    # read audio data from microphone
    data = stream.read(1024, exception_on_overflow=False)
    samples = np.frombuffer(data, dtype=aubio.float_type)

    # calculate pitch
    pitch = pitch_o(samples)[0]
    if pitch != 0:
        # calculate amplitude of samples
        volume = np.abs(samples).mean()

        # check if input volume is above threshold
        if volume > volume_threshold:
            # find closest piano note frequency
            closest_note = min(note_freqs, key=lambda x: abs(note_freqs[x] - pitch))
            
            # add note to buffer and update time buffer
            note_buffer.append(closest_note)
            time_buffer.append(time.time())
            
            # check if time interval has elapsed
            if time_buffer[-1] - time_buffer[0] > note_count_interval:
                # count occurrences of each note in buffer
                note_counts = {note: note_buffer.count(note) for note in set(note_buffer)}
                
                # find note with most occurrences
                most_common_note = max(note_counts, key=note_counts.get)
                
                # print most common note and clear buffers
                print("Note:", most_common_note)
                keystrokes.note(most_common_note)
                note_buffer = []
                time_buffer = []
                
                # draw the note on the window
                window.fill((255, 255, 255))
                font = pygame.font.SysFont("Arial", 48)
                text = font.render(most_common_note, True, (0, 0, 0))
                text_rect = text.get_rect(center=(window_width/2, window_height/2))
                window.blit(text, text_rect)
                pygame.display.update()
                
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()