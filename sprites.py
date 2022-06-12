import pygame, math
images = [pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_0.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_1.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_2.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_3.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_4.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_5.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_6.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_7.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_8.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_9.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_10.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_11.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_12.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_13.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_14.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_15.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_16.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_17.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_18.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/move/survivor-move_rifle_19.png')]
reloadImages = [pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_0.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_1.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_2.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_3.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_4.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_5.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_6.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_7.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_8.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_9.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_10.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_11.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_12.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_13.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_14.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_15.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_16.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_17.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_18.png'), pygame.image.load('sprites/Top_Down_Survivor/rifle/reload/survivor-reload_rifle_19.png')]

class sprites:
    def __init__(self, x, y, gun, id, name):
        self.x = x
        self.y = y
        self.vel = 0.4
        self.walkcount = 0
        self.tickrate = 0
        self.angle = 0
        self.gun = gun
        self.id = id
        self.reloaded = False
        self.ascii = 's'
        self.name = name
        self.hp = 100
        self.score = 0
        self.disconnected = False

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getimage(self):
        global images, reloadImages
        if self.walkcount // 20 == len(images) - 1:
            self.walkcount = 0
            if self.reloaded:
                self.reloaded = False
                self.gun.reloadAmmo()

        if not self.reloaded:
            return images, self.walkcount // 20

        else:
            self.walkcount += 1
            return reloadImages, self.walkcount // 20



    def calculateAngle(self, mouse_x, mouse_y):
        angle_x = mouse_x - (self.getx() + 76)
        angle_y = (self.gety() + 50) - mouse_y
        new_angle = math.degrees(math.atan2(angle_y, angle_x))
        if new_angle != self.angle:
            self.angle = new_angle
            return True

    def right(self):
        if self.x + self.vel < 750:
            self.x += self.vel
        if not self.reloaded:
            self.walkcount += 1


    def left(self):
        if self.x - self.vel > 0:
            self.x -= self.vel
        if not self.reloaded:
            self.walkcount += 1

    def up(self):
        if self.y - self.vel > 0:
            self.y -= self.vel
        if not self.reloaded:
            self.walkcount += 1


    def down(self):
        if self.y + self.vel < 550:
            self.y += self.vel
        if not self.reloaded:
            self.walkcount += 1


    def addBullet(self):
        self.gun.addbullet(self.x + 140, self.y + 80, self.angle)


    def reload(self):
        self.walkcount = 1
        self.reloaded = True

