import pygame


class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            
            pygame.mixer.init()
           
            cls._instance._init_sounds()
        return cls._instance

    def _init_sounds(self):
        self.background_music_path = "Assets/SoundsFiles/backgroundmusiclooped.mp3"
        self.sounds = {
            "explosion": pygame.mixer.Sound("Assets/SoundsFiles/explosion.wav"),
            "laser": pygame.mixer.Sound("Assets/SoundsFiles/lasershot.mp3"),
            "shield_up": pygame.mixer.Sound("Assets/SoundsFiles/shield_up.wav"),
            "alienspawn": pygame.mixer.Sound("Assets/SoundsFiles/alienspawnsound.mp3"),
        }
        self.music_volume = 0.1
        self.sound_volume = 0.5
        pygame.mixer.music.set_volume(self.music_volume)

    def play_music(self, loop=True):
        
        pygame.mixer.music.load(self.background_music_path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1 if loop else 0)

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
            print(f" Sound '{sound_name}' not found.")

    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sound_volume(self, volume):
        self.sound_volume = volume

    def fade_out_music(self, time):
        pygame.mixer.music.fadeout(time)
    
    def fade_in_music(self, music_file, loop=True, fade_time_ms=2000):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loops=-1 if loop else 0, fade_ms=fade_time_ms)

    def get_music_volume(self):
        return self.music_volume

    def get_sound_volume(self):
        return self.sound_volume

    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    def set_sound_volume(self, volume):
        self.sound_volume = volume
        for sound in self.sounds.values():
            sound.set_volume(volume)
    
    def increase_music_volume(self):
        self.music_volume = min(1.0, self.music_volume + 0.1)
        pygame.mixer.music.set_volume(self.music_volume)
        print(f"Music volume: {self.music_volume:.1f}")

    def decrease_music_volume(self):
        self.music_volume = max(0.0, self.music_volume - 0.1)
        pygame.mixer.music.set_volume(self.music_volume)
        print(f"Music volume: {self.music_volume:.1f}")

    def increase_sound_volume(self):
        self.sound_volume = min(1.0, self.sound_volume + 0.1)
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
        print(f"Sound volume: {self.sound_volume:.1f}")

    def decrease_sound_volume(self):
        self.sound_volume = max(0.0, self.sound_volume - 0.1)
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
        print(f"Sound volume: {self.sound_volume:.1f}")

