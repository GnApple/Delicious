import random
import hero
from config import *


class Supply(pygame.sprite.Sprite):
    # 补给道具基类
    def __init__(self, flyImagesPaths: tuple):
        super().__init__()
        # 图像
        self.flyImages = [pygame.image.load(eachPath).convert_alpha() for eachPath in flyImagesPaths]
        self.flyMode = 0
        self.image = self.flyImages[self.flyMode]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randint(0, SCREEN_WIDTH - self.rect.width), 0 - self.rect.height
        # 属性
        self.isAlive = True
        self.moveSpeed = 2
        self.getSound = sounds_dict["get_bomb"]
        self.effectSound = sounds_dict["use_bomb"]

    def move(self, flag: int):
        if self.isAlive:
            if flag == MOVE_LEFT:
                self.rect.x -= self.moveSpeed
            elif flag == MOVE_RIGHT:
                self.rect.x += self.moveSpeed
            elif flag == MOVE_UP:
                self.rect.y -= self.moveSpeed
            elif flag == MOVE_DOWN:
                self.rect.y += self.moveSpeed

    def kill(self):
        self.isAlive = False
        super().kill()

    def update(self):
        super().update()
        self.move(MOVE_DOWN)
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


class Bomb_supply(Supply):
    def __init__(self):
        super().__init__(bombSupplyImages_paths)
        self.type = "Bomb_supply"
        self.getSound = sounds_dict["get_bomb"]
        self.effectSound = sounds_dict["use_bomb"]

    @staticmethod
    def execute_effect(enemyGroup: pygame.sprite.Group):
        sounds_dict["use_bomb"].play()
        for eachEnemy in enemyGroup:
            eachEnemy.health = -1


class Bullet_supply(Supply):
    def __init__(self):
        super().__init__(bulletSupplyImages_paths)
        self.getSound = sounds_dict["get_bullet"]

    @staticmethod
    def execute_effect(heroPlane: hero.HeroPlane):
        heroPlane.changeBulletMode()


class Life_supply(Supply):
    def __init__(self):
        super().__init__(lifeSupplyImages_paths)
        self.getSound = sounds_dict["supply"]

    @staticmethod
    def execute_effect(CV: ChangeableValue):
        pass


class Bomb_count(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class PlaneLife_count(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
