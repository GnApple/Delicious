import pygame
from config import *


class HeroPlane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 主角图像加载
        self.flyImages = [pygame.image.load(image_path).convert_alpha() for image_path in heroPlaneImages_paths]
        self.dropImages = [pygame.image.load(image_path).convert_alpha() for image_path in heroPlaneDropImages_paths]
        self.emptyImage = pygame.image.load(heroPlaneImage_empty_path).convert_alpha()
        self.image = self.flyImages[0]

        # 主角图像位置尺寸加载
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.rect.width) / 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height

        # 主角状态
        self.isAlive = True
        self.isUnbeatable = False  # 无敌属性
        self.isShining = False  # 无敌闪烁判断
        self.movable = True

        # 主角属性
        self.power = 10  # 主角力量属性
        self.moveSpeed = 5
        self.flyMode = 0  # 飞行状态
        self.defaultUnbeatableGap = GAME_TICK * 2  # 两秒无敌时间间隔
        self.unbeatableGap = self.defaultUnbeatableGap
        self.constUnbeatableShiningGap = GAME_TICK / 10  # 无敌闪烁间隔

        # 子弹
        # 生成的子弹模式
        self.bullet_mode = NORMAL_BULLET
        # 子弹位置
        self.leftBulletPos = self.rect.x + self.rect.width / 4, self.rect.y
        self.rightBulletPos = (self.rect.x + self.rect.width) - self.rect.width / 4, self.rect.y
        # 子弹频率
        self.defaultBulletShootTicks = 15, 5
        self.bulletShootTick = self.defaultBulletShootTicks[self.bullet_mode]
        # 是否生成子弹
        self.isSpawnBullet = False
        # 特殊子弹持续时长倒计时
        self.default_specialBullet_countdown = 10 * GAME_TICK
        self.specialBullet_countdown = self.default_specialBullet_countdown

        # 播放动画属性
        self.defaultPlayGap = PLAY_GAP
        self.playGap = self.defaultPlayGap
        self.dropMode = 0

    def changeFlyMode(self):
        if self.flyMode + 1 < len(self.flyImages):
            self.flyMode += 1
        else:
            self.flyMode = 0

    def unbeatableChangeFlyMode(self):
        # 闪烁动画函数
        if self.unbeatableGap != 0:
            if self.unbeatableGap % self.constUnbeatableShiningGap == 0:
                if self.isShining:
                    self.image = self.emptyImage
                    self.isShining = False
                else:
                    self.isShining = True
            self.unbeatableGap -= 1
        else:
            self.isUnbeatable = False
            self.unbeatableGap = self.defaultUnbeatableGap

    def move(self, flag: int):
        if self.isAlive and self.movable:
            if flag == MOVE_LEFT and self.rect.x - self.moveSpeed > 0:
                self.rect.x -= self.moveSpeed
            elif flag == MOVE_RIGHT and self.rect.x + self.moveSpeed < SCREEN_WIDTH - self.rect.width:
                self.rect.x += self.moveSpeed
            elif flag == MOVE_UP and self.rect.y - self.moveSpeed > 0:
                self.rect.y -= self.moveSpeed
            elif flag == MOVE_DOWN and self.rect.y + self.moveSpeed < SCREEN_HEIGHT - self.rect.height:
                self.rect.y += self.moveSpeed

    def flyPlay(self):
        # 播放飞行时的动画
        if self.playGap > 0:
            self.playGap -= 1
        else:
            self.changeFlyMode()
            self.image = self.flyImages[self.flyMode]
            self.playGap = self.defaultPlayGap

        # 闪烁动画
        if self.isUnbeatable:
            self.unbeatableChangeFlyMode()

        # 子弹时长持续
        if self.bullet_mode == SPECIAL_BULLET:
            if self.specialBullet_countdown > 0:
                self.specialBullet_countdown -= 1
            else:
                self.bullet_mode = NORMAL_BULLET
                self.specialBullet_countdown = self.default_specialBullet_countdown

    def dropPlay(self):
        # 播放坠毁时的动画
        if self.dropMode < len(self.dropImages):
            if self.playGap != 0:
                self.playGap -= 1
            elif self.playGap == 0:
                self.image = self.dropImages[self.dropMode]
                self.dropMode += 1
                self.playGap = self.defaultPlayGap

    def bulletUpdate(self):
        # 子弹频率更新
        if self.bulletShootTick == 0:
            self.leftBulletPos = self.rect.x + self.rect.width / 4 - 10, self.rect.y + 20
            self.rightBulletPos = (self.rect.x + self.rect.width) - self.rect.width / 4 + 10, self.rect.y + 20
            self.isSpawnBullet = True
            self.bulletShootTick = self.defaultBulletShootTicks[self.bullet_mode]
        else:
            self.isSpawnBullet = False
            self.bulletShootTick -= 1

    def changeBulletMode(self):
        if self.bullet_mode == NORMAL_BULLET:
            self.bullet_mode = SPECIAL_BULLET
        else:
            self.bullet_mode = NORMAL_BULLET
        self.bulletShootTick = self.defaultBulletShootTicks[self.bullet_mode]

    def kill(self):
        if not self.isUnbeatable:
            self.isAlive = False
            self.isSpawnBullet = False
        sounds_dict["me_down"].play()

    def changeUnbeatable(self):
        # 无敌状态改变
        if self.isUnbeatable:
            self.isUnbeatable = False
            self.unbeatableGap = self.defaultUnbeatableGap
        else:
            self.isUnbeatable = True
            self.unbeatableGap = -1

    def respawn(self):
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.rect.width) / 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.isAlive = True
        self.isSpawnBullet = True
        self.dropMode = 0
        self.image = self.flyImages[self.flyMode]
        self.isUnbeatable = True

    def update(self):
        # 动画更新
        if self.isAlive:
            self.flyPlay()
            self.bulletUpdate()
        else:
            self.dropPlay()
