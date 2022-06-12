import pygame
import math
from sprites import sprites
bullet_pic = pygame.image.load('sprites/bullets/bullet1.png')
bullet_pic = pygame.transform.scale(bullet_pic, (24, 9))
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)


class gui:
    def __init__(self):
        pygame.init()
        self.WIDTH = 900
        self.HEIGHT = 675
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.sprites = []
        self.guns = []
        self.score = 0

    def addsprite(self, new_sprite):
        flag = True
        for sprite in self.sprites:
            if sprite.id == new_sprite.id:
                self.sprites[self.sprites.index(sprite)] = new_sprite
                flag = False
        if flag:
            self.sprites.append(new_sprite)


    def addgun(self, new_gun):
        flag = True
        for gun in self.guns:
            if gun.id == new_gun.id:
                self.guns[self.guns.index(gun)] = new_gun
                flag = False
        if flag:
            self.guns.append(new_gun)

    def blitsprite(self, player):
        for sprite in self.sprites:
            if sprite.disconnected:
                self.sprites.pop(self.sprites.index(sprite))
                break
            sprite_images, walk_count = sprite.getimage()
            sprite_images = pygame.transform.scale(sprite_images[walk_count], (156, 100))
            text_surface = my_font.render(sprite.name, False, (255, 255, 255))
            self.blitRotate(sprite_images, (sprite.getx() + 78, sprite.gety() + 50), (78, 50), sprite.angle, True)
            self.blitRotate(text_surface, (sprite.getx() + 78 + 15, sprite.gety() + 50), (78, 50),  sprite.angle, True)
            health_bar = pygame.Rect((sprite.getx() - 10, sprite.gety()), (10, sprite.hp))
            pygame.draw.rect(self.screen, (0, 255, 0), health_bar)
            if sprite.id == player.id:
                score_text = f"score: {sprite.score}"
                ammo_text = f"ammo: {sprite.gun.ammo}"
                ammo_surface = my_font.render(ammo_text, False, (255, 255, 255))
                score_surface = my_font.render(score_text, False, (255, 255, 255))
                self.screen.blit(score_surface, (10, 10))
                self.screen.blit(ammo_surface, (10, 50))

    def blitRotate(self, image, pos, originPos, angle, blit):
        # offset from pivot to center
        image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        # roatetd image center
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
        if not blit:
            return rotated_image_rect
        self.screen.blit(rotated_image, rotated_image_rect)


    def updatescreen(self):
        pygame.display.flip()
        self.screen.fill((0,0,0))

    def blitProjectile(self):
        for gun in self.guns:
            for bullet in gun.bullets:
                if not bullet.bulletHit:
                    x, y, angle = bullet.getBulletCoordinations()
                    x = x + (gun.vel * math.cos(math.radians(angle)))
                    y = y - (gun.vel * math.sin(math.radians(angle)))
                    if x < 0 or x > 1000 or y < 0 or y > 600:
                        gun.bullets.pop(gun.bullets.index(bullet))
                    else:
                        bullet.setBulletCoordinations(x, y)
                    self.blitRotate(bullet_pic, (x + 8, y + 3), (16, 6), angle, True)
                else:
                    gun.bullets.pop(gun.bullets.index(bullet))

    def hp_down(self, id):
        for sprite in self.sprites:
            if int(sprite.id) == id:
                self.sprites[self.sprites.index(sprite)].hp -= 10


