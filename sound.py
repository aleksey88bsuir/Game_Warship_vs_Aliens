import pygame


"""Звуки"""
pygame.mixer.init()
pygame.mixer.music.load('Music/tgfcoder-FrozenJam-SeamlessLoop.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1)
shoot_sound = pygame.mixer.Sound('Music/expl3.wav')
expl_sound = []
for snd in ['Music/expl3.wav', 'Music/expl6.wav']:
    expl_sound.append((pygame.mixer.Sound(snd)))
