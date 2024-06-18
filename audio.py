import pygame
import time
import os
import asyncio
import soundfile as sf
from mutagen.mp3 import MP3

class AudioManager:

    def __init__(self):
        # Use higher frequency to prevent audio glitching noises
        pygame.mixer.init(frequency=48000, buffer=1024) 

    def playAudio(self, file_path, sleep_during_playback=True, delete_file=False, play_using_music=True):
        print(f"Playing file: {file_path}")
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=48000, buffer=1024) 

        if play_using_music:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

        else:
            pygame_sound = pygame.mixer.Sound(file_path) 
            pygame_sound.play()

        if sleep_during_playback:
            _, ext = os.path.splitext(file_path)

            if ext.lower() == '.wav':
                wav_file = sf.SoundFile(file_path)
                file_length = wav_file.frames / wav_file.samplerate
                wav_file.close()

            elif ext.lower() == '.mp3':
                mp3_file = MP3(file_path)
                file_length = mp3_file.info.length

            else:
                print("Unknown file type")
                return

            time.sleep(file_length)

            if delete_file:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                try:  
                    os.remove(file_path)
                    print("Deleted the audio file.")
                except PermissionError:
                    print("Couldn't remove {file_path} because it is being used by another process.")

    async def audioAsync(self, file_path):
        print("Playing file: {file_path}")
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=48000, buffer=1024) 
        pygame_sound = pygame.mixer.Sound(file_path) 
        pygame_sound.play()

        _, ext = os.path.splitext(file_path)
        if ext.lower() == '.wav':
            wav_file = sf.SoundFile(file_path)
            file_length = wav_file.frames / wav_file.samplerate
            wav_file.close()
        elif ext.lower() == '.mp3':
            mp3_file = MP3(file_path)
            file_length = mp3_file.info.length
        else:
            print("Unknown file type")
            return

        await asyncio.sleep(file_length)
