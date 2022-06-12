import math, pygame
bulletImage = pygame.image.load('sprites/bullets/bullet1.png')
bulletImage = pygame.transform.scale(bulletImage, (24, 9))


class weapons:
    def __init__(self, bullets, id):
        self.mag = bullets
        self.ammo = bullets
        self.val = 2
        self.bullets = []
        self.radius = 8
        self.vel = 2
        self.id = id
        self.ascii = 'b'

    def addbullet(self, x, y, angle):
        if self.ammo > 0:
            new_x, new_y = self.rotateBullet(bulletImage, (x - 62, y - 20), (-62, -20), angle)
            self.bullets.append(bullet(new_x, new_y, angle))
            self.ammo -= 1

    def rotateBullet(self, image, pos, originPos, angle):
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
        return rotated_image_rect[0], rotated_image_rect[1]

    def reloadAmmo(self):
        self.ammo = self.mag

    def check_hit(self, sprites):
        global client
        for sprite in sprites:
            for bullet in self.bullets:
                if self.id != sprite.id:
                    x, y, angle = bullet.getBulletCoordinations()
                    sprite_x, sprite_y = sprite.getx(),sprite.gety()
                    if sprite_x < x < sprite_x + 150 and sprite_y < y < sprite_y + 100:
                        bullet.bullet_hit()
                        return sprite.id
        return False





class bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.bulletHit = False

    def getBulletCoordinations(self):
        return self.x, self.y, self.angle

    def setBulletCoordinations(self, x, y):
        self.x, self.y = x, y

    def bullet_hit(self):
        self.bulletHit = True