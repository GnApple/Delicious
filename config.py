import pygame
import os

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 700
GAME_TICK = 90
SCREEN_TITLE = "飞机大战"

# 动画属性
PLAY_GAP = 20

# 字体大小
FONT_SIZE = 40

# 加载图像地址
# 主角所有图像
heroPlaneImages_paths = r"images\me1.png", r"images\me2.png"
heroPlaneDropImages_paths = r"images\me_destroy_1.png", r"images\me_destroy_2.png", \
    r"images\me_destroy_3.png", r"images\me_destroy_4.png"
heroPlaneImage_empty_path = r"images\me_empty.png"
# 敌人图像地址
enemy1FlyImages_paths = r"images\enemy1.png",
enemy1DropImages_paths = r"images\enemy1_down1.png", r"images\enemy1_down2.png", \
    r"images\enemy1_down3.png", r"images\enemy1_down4.png"
enemy2FlyImages_paths = r"images/enemy2.png",
enemy2DropImages_paths = r"images/enemy2_down1.png", r"images/enemy2_down2.png", \
    r"images/enemy2_down3.png", r"images/enemy2_down4.png"
enemy3FlyImages_paths = r"images/enemy3_n1.png", r"images/enemy3_n2.png"
enemy3DropImages_paths = r"images/enemy3_down1.png", r"images/enemy3_down2.png", \
    r"images/enemy3_down3.png", r"images/enemy3_down4.png", \
    r"images/enemy3_down5.png", r"images/enemy3_down6.png"
# 子弹图像
normalBulletImage_path = r"images/bullet1.png"
specialBulletImage_path = r"images/bullet2.png"
# 补给道具图像
bombSupplyImages_paths = r"images/bomb_supply.png",
bulletSupplyImages_paths = r"images/bullet_supply.png",
lifeSupplyImages_paths = r"images/life_supply.png",
# 补给道具数量显示图像
bombSupplyCountImage_path = r"images/bomb.png"
# 残机数量显示图像
planeLifeImage_path = r"images/life.png"
# 程序图像
again_image_path = r"images/again.png"
gameover_image_path = r"images/gameover.png"
pauseOrResumeImages_paths = r"images/pause_nor.png", r"images/pause_pressed.png", \
    r"images/resume_nor.png", r"images/resume_pressed.png"

# 暂停图标模式
PAUSE_NOR_MODE = 0
PAUSE_PRESSED_MODE = 1
RESUME_NOR_MODE = 2
RESUME_PRESSED_MODE = 3

# 子弹模式
NORMAL_BULLET = 0
SPECIAL_BULLET = 1

# 移动
MOVE_LEFT = 0
MOVE_RIGHT = 1
MOVE_UP = 2
MOVE_DOWN = 3

# 支援道具生成倒计时
DEFAULT_SPAWN_SUPPLY_COUNTDOWN = 15 * GAME_TICK  # 单位秒
# 默认炸弹补给数量
DEFAULT_BOMB_SUPPLY_COUNT = 3
# 默认飞机数量
DEFAULT_HERO_PLANE_LIFE_COUNT = 3


class ChangeableValue:
    def __init__(self):
        self.scores = 0  # 分数
        # 补给事项
        self.spawn_supply_countdown = DEFAULT_SPAWN_SUPPLY_COUNTDOWN  # 倒计时初始化
        self.bomb_supply_count = DEFAULT_BOMB_SUPPLY_COUNT  # 炸弹补给数量初始化
        self.heroPlane_life_count = DEFAULT_HERO_PLANE_LIFE_COUNT  # 主角飞机数量初始化


class GameAgainImage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(again_image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.rect.width) / 2
        self.rect.y = SCREEN_HEIGHT / 2 - self.rect.height / 2 - self.rect.height


class GameoverImage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(gameover_image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.rect.width) / 2
        self.rect.y = SCREEN_HEIGHT / 2 - self.rect.height / 2 + self.rect.height


class PauseOrConsumeImage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load(eachImage).convert_alpha() for eachImage in pauseOrResumeImages_paths]
        self.image = self.images[PAUSE_NOR_MODE]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0


# 背景音乐音量
BACKGROUND_MUSIC_VOLUME = 0.2
# 音效音量
EFFECT_SOUND_VOLUME = 0.2
# 音乐初始化 背景音乐 音效载入
pygame.mixer.init()
BGM = pygame.mixer.music
BGM.load(r"sound/game_music.ogg")
BGM.set_volume(BACKGROUND_MUSIC_VOLUME)
# 遍历sound文件夹下的所有wav后缀文件并且以不含后缀的文件名称字符串作为索引生成字典
# 注意文件路径中除了文件后缀前之外不能有.字符
sounds_dict = {}
sounds_source_path = r"sound/"
sound_directory = os.listdir(sounds_source_path)
for eachDirectory in sound_directory:
    if eachDirectory[-4:] == ".wav":
        effectSound = pygame.mixer.Sound(sounds_source_path + eachDirectory)
        effectSound.set_volume(EFFECT_SOUND_VOLUME)
        sounds_dict[eachDirectory[:-4]] = effectSound


# 重载难度升级音效以达成依次播放
class upgrade_sound(pygame.mixer.Sound):
    def __init__(self):
        super().__init__(file=r"sound/upgrade.wav")
        self.playCount = 0

    def play(
            self,
            loops: int = 0,
            maxtime: int = 0,
            fade_ms: int = 0,
    ) -> pygame.mixer.Channel:
        super().play()
        self.playCount += 1
