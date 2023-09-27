from config import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, bullet_mode=NORMAL_BULLET):
        super().__init__()
        # 图像加载
        self.images = pygame.image.load(normalBulletImage_path).convert_alpha(), \
            pygame.image.load(specialBulletImage_path).convert_alpha()
        self.mode = bullet_mode
        self.image = self.images[self.mode]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        # 音效播放
        sounds_dict["bullet"].set_volume(0.1)
        sounds_dict["bullet"].play()

        # 子弹属性
        self.isAlive = True
        self.moveSpeed = 10

    def kill(self):
        self.isAlive = False
        super().kill()

    def update(self, flag: int = MOVE_UP):
        super().update()
        if self.isAlive:
            if flag == MOVE_UP:
                self.rect.y -= self.moveSpeed

        if self.rect.y < 0 - self.rect.height:
            self.kill()
