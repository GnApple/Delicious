from config import *
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, flyImages_paths: tuple, dropImages_paths: tuple):
        super().__init__()
        # 图像地址
        self.flyImages = [pygame.image.load(eachPath).convert_alpha() for eachPath in flyImages_paths]
        self.dropImages = [pygame.image.load(eachPath).convert_alpha() for eachPath in dropImages_paths]
        self.flyMode = 0
        self.image = self.flyImages[self.flyMode]

        # 属性
        self.isAlive = True
        self.movable = True
        self.moveSpeed = 1
        self.health = 0

        # 动画属性
        self.flyMode = 0
        self.dropMode = 0
        self.defaultPlayGap = PLAY_GAP
        self.playGap = self.defaultPlayGap

        # 音效
        self.downSound = sounds_dict["me_down"]

        # 图像尺寸
        self.rect = self.image.get_rect()

    def changeFlyMode(self):
        if len(self.flyImages) == 1:
            return
        if self.flyMode + 1 < len(self.flyImages):
            self.flyMode += 1
        else:
            self.flyMode = 0

    def flyPlay(self):
        # 播放飞行时的动画
        if self.playGap > 0:
            self.playGap -= 1
        else:
            self.changeFlyMode()
            self.image = self.flyImages[self.flyMode]
            self.playGap = self.defaultPlayGap

    def dropPlay(self):
        self.isAlive = False
        if self.dropMode < len(self.dropImages):
            if self.playGap != 0:
                self.playGap -= 1
            elif self.playGap == 0:
                self.image = self.dropImages[self.dropMode]
                self.dropMode += 1
                self.playGap = self.defaultPlayGap
        else:
            self.kill()

    def move(self, flag: int):
        if self.isAlive and self.movable:
            if flag == MOVE_LEFT:
                self.rect.x -= self.moveSpeed
            elif flag == MOVE_RIGHT:
                self.rect.x += self.moveSpeed
            elif flag == MOVE_UP:
                self.rect.y -= self.moveSpeed
            elif flag == MOVE_DOWN:
                self.rect.y += self.moveSpeed

    def update(self):
        super().update()
        self.move(MOVE_DOWN)
        if self.health < 0:
            if self.isAlive:
                self.downSound.play()
            self.isAlive = False
        if self.isAlive:
            self.flyPlay()
        else:
            self.dropPlay()
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


class Enemy1(Enemy):
    def __init__(self):
        super().__init__(flyImages_paths=enemy1FlyImages_paths, dropImages_paths=enemy1DropImages_paths)
        self.rect.x, self.rect.y = random.randint(0, SCREEN_WIDTH - self.rect.width), 0 - 10 * self.rect.height
        self.moveSpeed = 3
        self.scores = 100
        self.downSound = sounds_dict["enemy1_down"]


class Enemy2(Enemy):
    def __init__(self):
        super().__init__(flyImages_paths=enemy2FlyImages_paths, dropImages_paths=enemy2DropImages_paths)
        self.rect.x, self.rect.y = random.randint(0, SCREEN_WIDTH - self.rect.width), 0 - 10 * self.rect.height
        self.moveSpeed = 2
        self.health = 30
        self.scores = 300
        self.downSound = sounds_dict["enemy2_down"]


class Enemy3(Enemy):
    def __init__(self):
        super().__init__(flyImages_paths=enemy3FlyImages_paths, dropImages_paths=enemy3DropImages_paths)
        self.rect.x, self.rect.y = random.randint(0, SCREEN_WIDTH - self.rect.width), 0 - 10 * self.rect.height
        self.moveSpeed = 1
        self.health = 100
        self.scores = 1000
        self.downSound = sounds_dict["enemy3_down"]
        sounds_dict["enemy3_flying"].set_volume(0.1)
        sounds_dict["enemy3_flying"].play()
