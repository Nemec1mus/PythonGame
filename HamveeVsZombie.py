import pygame, controls
from gun import Gun
from pygame.sprite import Group
from stats import Stats
from scores import Scores

def run():

    pygame.init()
    screen = pygame.display.set_mode((900, 1000))
    pygame.display.set_caption("Hamvee vs Zombie")
    bg_color = (244, 164, 96)
    gun = Gun(screen)
    bullets = Group()
    zombies = Group()
    controls.create_army(screen, zombies)
    stats = Stats()
    sc = Scores(screen, stats)

    while True:
        controls.events(screen, gun, bullets)
        if stats.run_game:
            gun.update_gun()
            controls.update(bg_color, screen, stats, sc, gun, zombies, bullets)
            controls.update_bullets(screen,stats, sc, zombies, bullets)
            controls.update_zombies(stats, screen, sc, gun, zombies, bullets)


run()