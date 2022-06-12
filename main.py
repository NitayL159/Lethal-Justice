from screen import gui
from sprites import sprites
from weapon import weapons
import pygame
from client import ClientGame
import random, time
background = pygame.image.load('sprites/BG.jpg')
window = pygame.image.load('sprites/WINDOW.jpg')
my_font = pygame.font.SysFont('Comic Sans MS', 40)

def blit_background(screen):
    for i in range(0, 4):
        for j in range(0, 3):
            screen.screen.blit(background, (i * 225, j * 225))


def get_name(screen):
    global running, game_start
    user_text = ""
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                run = False
                game_start = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
                if event.key == pygame.K_RETURN:
                    name = user_text[:-1]
                    return name
        user_print = f"Enter your name: {user_text}"
        text_surface = my_font.render(user_print, False, (255, 255, 255))
        screen.screen.blit(window, (0, 0))
        screen.screen.blit(text_surface, (50, 300))
        screen.updatescreen()

def wait_for_host(screen, client):
    game_start = False
    global running
    while not game_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.close_client()
                running = False
                game_start = True
        if client.start:
            game_start = True
        user_print = "Waiting for host to start the game..."
        text_surface = my_font.render(user_print, False, (255, 255, 255))
        screen.screen.blit(window, (0, 0))
        screen.screen.blit(text_surface, (100, 300))
        screen.updatescreen()



def main():
    screen = gui()
    running = True
    name = get_name(screen)
    client = ClientGame(screen)
    ak = weapons(10, client.id)
    rand_x = random.randint(1, 700)
    rand_y = random.randint(1, 500)
    shootloop = 0
    timer = 5
    player1 = sprites(rand_x, rand_y,  ak, client.id, name)
    screen.addsprite(player1)
    screen.addgun(ak)
    client.send_message(player1)
    wait_for_host(screen, client)
    start_ticks = pygame.time.get_ticks()
    while running:
        old_hp = player1.hp
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                player1.disconnected = True
                client.send_message(player1)
                client.close_client()
        screen.updatescreen()
        blit_background(screen)
        text_seconds = f"Time left: {int(30 - seconds)}"
        text_surface = my_font.render(text_seconds, False, (255, 255, 255))
        screen.screen.blit(text_surface, (550, 5))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if player1.calculateAngle(mouse_x, mouse_y):
            client.send_message(player1)
        screen.blitsprite(player1)
        hit_id = ak.check_hit(screen.sprites)
        if hit_id:
            for sprite in screen.sprites:
                if sprite.id == hit_id:
                    if sprite.hp - 10 == 0:
                        player1.score += 1
                        print(player1.score)
            client.send_message(int(hit_id))

        screen.blitProjectile()
        client.send_message(ak)
        if player1.hp != old_hp:
            old_hp = player1.hp
            client.send_message(player1)

        if player1.hp == 0:
            old_hp = 100
            player1.hp = 100
            rand_x = random.randint(1, 700)
            rand_y = random.randint(1, 500)
            player1.x, player1.y = rand_x, rand_y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            client.send_message(player1)
            player1.right()
        if keys[pygame.K_a]:
            client.send_message(player1)
            player1.left()
        if keys[pygame.K_w]:
            client.send_message(player1)
            player1.up()
        if keys[pygame.K_s]:
            client.send_message(player1)
            player1.down()

        if shootloop > 0:
            shootloop -= 1

        if keys[pygame.K_r] and player1.reloaded == False:
            player1.reload()
            client.send_message(player1)

        if keys[pygame.K_SPACE] and shootloop == 0:
            player1.addBullet()
            shootloop = 250

        if seconds > 30:
            running = False
            check_win(screen, player1)

    client.close_client()

def check_win(screen, player1):
    max = screen.sprites[0].score
    for sprite in screen.sprites:
        if sprite.score > max:
            max = sprite.score
    if max == player1.score:
        blit_win(screen, player1, player1.name)
    else:
        blit_lose(screen, player1, player1.name)

def blit_win(screen, player1, name):
    blit_run = True
    while blit_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                blit_run = False
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_RETURN:
                    blit_run = False
        screen.screen.blit(window, (0, 0))
        text = f"Congratulations!, {name} you won with {player1.score} points"
        text_surface = my_font.render(text, False, (255, 255, 255))
        screen.screen.blit(text_surface, (50, 300))
        text = f"Press enter to close the game!!"
        text_surface = my_font.render(text, False, (255, 255, 255))
        screen.screen.blit(text_surface, (50, 340))
        screen.updatescreen()

def blit_lose(screen, player1, name):
    blit_run = True
    while blit_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                blit_run = False
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_RETURN:
                    blit_run = False
        screen.screen.blit(window, (0, 0))
        text = f"You lost, {name} with {player1.score} points :("
        text_surface = my_font.render(text, False, (255, 255, 255))
        screen.screen.blit(text_surface, (50, 300))
        text = f"Press enter to close the game!!"
        text_surface = my_font.render(text, False, (255, 255, 255))
        screen.screen.blit(text_surface, (50, 340))
        screen.updatescreen()


if __name__ == '__main__':
    main()