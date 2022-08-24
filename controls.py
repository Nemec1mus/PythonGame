import  pygame, sys
from bullet import Bullet
from zombie import Zombie
import time

def events(screen, gun, bullets):
    #Кнопки

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                gun.mright = True
            elif event.key == pygame.K_LEFT:
                gun.mleft = True
            elif event.key ==pygame.K_SPACE:
                new_bullet = Bullet(screen, gun)
                bullets.add(new_bullet)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                gun.mright = False
            elif event.key == pygame.K_LEFT:
                gun.mleft = False

def update(bg_color, screen, stats, sc, gun, zombies, bullets):
    screen.fill(bg_color)
    sc.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    gun.output()
    zombies.draw(screen)
    pygame.display.flip()

def update_bullets(screen, stats, sc,  zombies, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, zombies, True, True)
    if collisions:
        for zombies in collisions.values():
            stats.score += 10 * len(zombies)
        sc.image_score()
        check_high_score(stats, sc)
        sc.image_guns()
    if len(zombies) == 0:
        bullets.empty()
        create_army(screen,zombies)

def gun_dead(stats, screen, sc, gun, zombies, bullets):

    if stats.guns_left > 0:
        stats.guns_left -= 1
        sc.image_guns()
        zombies.empty()
        bullets.empty()
        create_army(screen, zombies)
        gun.create_gun()
        time.sleep(5)
    else:
        stats.run_game = False
        sys.exit()

def update_zombies(stats, screen, sc, gun, zombies, bullets):
    zombies.update()
    if pygame.sprite.spritecollideany(gun, zombies):
        gun_dead(stats, screen, sc, gun, zombies, bullets)
    zombies_check(stats, screen, sc, gun, zombies, bullets)

def zombies_check(stats, screen, sc, gun, zombies, bullets):
    screen_rect = screen.get_rect()
    for zombie in zombies.sprites():
        if zombie.rect.bottom >= screen_rect.bottom:
            gun_dead(stats, screen, sc, gun, zombies, bullets)
            break


def create_army(screen,zombies):
    zombie = Zombie(screen)
    zombie_width = zombie.rect.width
    number_zombie_x = int((700 - 2 * zombie_width) / zombie_width)
    zombie_height = zombie.rect.height
    number_zombie_y = int((800 - 100 - 2 * zombie_height) / zombie_height)

    for row_number in range(number_zombie_y - 6 ):
        for zombie_number in range(number_zombie_x):
            zombie = Zombie(screen)
            zombie.x = zombie_width + zombie_width * zombie_number
            zombie.y = zombie_height + zombie_height * row_number
            zombie.rect.x = zombie.x
            zombie.rect.y = zombie.rect.height + zombie.rect.height * row_number
            zombies.add(zombie)

def check_high_score(stats, sc):
    #Делаем проверку новых рекордов
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sc.image_high_score()
        with open('highscore.txt', 'w') as f:
            f.write(str(stats.high_score))

