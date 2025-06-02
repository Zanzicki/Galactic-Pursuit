import pygame


class SoundManager:
   _instance = None

   def __new__(cls):
       if cls._instance is None:
           cls._instance = super(SoundManager, cls).__new__(cls)
           pygame.mixer.init()
           cls._instance._init_sounds()  # <-- VIGTIGT: kald metoden her!
       return cls._instance

   def _init_sounds(self):

       self.background_music_path = "Assets/SoundsFiles/backgroundmusiclooped.mp3"
       self.sounds = {
           #"explosion": pygame.mixer.Sound("Assets/SoundsFiles/explosion.wav"),
           #"laser_shot": pygame.mixer.Sound("Assets/SoundsFiles/lasershot.wav"),
           #"shield_up": pygame.mixer.Sound("Assets/SoundsFiles/shield_up.wav"),

       }
       self.music_volume = 0.3
       self.sound_volume = 0.5
       pygame.mixer.music.set_volume(self.music_volume)
    
   def play_music(self, loop=True): 
        pygame.mixer.music.load(self.background_music_path)

        if loop:
            pygame.mixer.music.play(-1)  # Loop indefinitely
        else:
            pygame.mixer.music.play(0)

   def stop_music(self):
        pygame.mixer.music.stop()

   def pause_music(self):
        pygame.mixer.music.pause()

   def resume_music(self):
        pygame.mixer.music.unpause()

   def play_sound(self, sound_name):
       if sound_name in self.sounds:
           sound = self.sounds[sound_name]
           sound.set_volume(self.sound_volume)
           sound.play()
       else:
           print(f"Sound '{sound_name}' not found in SoundManager.")

   def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(self.music_volume) 

   def set_sound_volume(self, volume):
       self.sound_volume = volume