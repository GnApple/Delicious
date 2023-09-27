# -*- coding: UTF-8 -*-
import random
import enemy
import hero
import bullets
import supply
from config import *


# 初始化窗口大小 标题
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# 全局变量
CV = ChangeableValue()
# 敌人密集程度
enemy_concentration = 2.0  # 1.0表示每秒钟随机生成1只
# 敌人速度倍率
enemySpeedRate = 1

# 读取最高分
with open(r"data/scores.txt", "r") as f:
    highestScore = int(f.read())

# 字体
font = pygame.font.Font(r"font/font.ttf", FONT_SIZE)
score_surface = font.render(f"Scores: {CV.scores}", True, (0, 0, 0), None)
highestScore_surface = font.render(f"Highest Score: {highestScore}", True, (0, 0, 0), None)

# 程序条件
done = False  # 程序本体
isGameRunning = True  # 是否正在进行
isPause = False  # 是否暂停

# 加载背景
backgroundImage = pygame.image.load(r"images\background.png").convert_alpha()

# 加载Sprite
heroPlane = hero.HeroPlane()
againImage = GameAgainImage()
gameoverImage = GameoverImage()
pauseImage = PauseOrConsumeImage()

# 加载SpriteGroup
bulletGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
scoreGroup = pygame.sprite.Group()
supplyGroup = pygame.sprite.Group()
tipGroup = pygame.sprite.Group()  # 提示组

US = upgrade_sound()


# 保存最高分
def save_scores(scores):
    global highestScore
    if scores > highestScore:
        highestScore = scores
        global highestScore_surface
        highestScore_surface = font.render(f"Highest Score: {highestScore}", True, (0, 0, 0), None)
        with open(r"data/scores.txt", "w") as g:
            g.write(str(scores))


def again_game():
    global isPause
    isPause = False
    pauseImage.image = pauseImage.images[PAUSE_NOR_MODE]
    CV.scores = 0
    CV.bomb_supply_count = DEFAULT_BOMB_SUPPLY_COUNT
    CV.heroPlane_life_count = DEFAULT_HERO_PLANE_LIFE_COUNT + 1
    CV.spawn_supply_countdown = DEFAULT_SPAWN_SUPPLY_COUNTDOWN
    global enemy_concentration
    enemy_concentration = 2.0
    enemyGroup.empty()
    bulletGroup.empty()
    supplyGroup.empty()
    global isGameRunning
    if not isGameRunning:
        heroPlane.bullet_mode = NORMAL_BULLET
        isGameRunning = True
    BGM.stop()
    BGM.play(-1)


def resetTipDisplay():
    tipGroup.empty()
    # 生成分数显示
    global score_surface
    score_surface = font.render(f"Scores: {CV.scores}", True, (0, 0, 0), None)
    # 生成bomb炸弹数量显示
    # 炸弹数量提示的y坐标
    bomb_y = score_surface.get_height() + highestScore_surface.get_height()
    if CV.bomb_supply_count > 0:
        for i in range(CV.bomb_supply_count):
            bomb_pos = SCREEN_WIDTH - (i + 1) * supply.Bomb_count((0, 0), bombSupplyCountImage_path).rect.width, \
                bomb_y
            bomb_count = supply.Bomb_count(bomb_pos, bombSupplyCountImage_path)
            tipGroup.add(bomb_count)
    # 生成残机数量显示
    if CV.heroPlane_life_count > 0:
        for j in range(CV.heroPlane_life_count):
            plane_pos = SCREEN_WIDTH - (j + 1) * supply.PlaneLife_count((0, 0), planeLifeImage_path).rect.width, \
                        bomb_y + supply.PlaneLife_count((0, 0), planeLifeImage_path).rect.height
            planeLife_count = supply.PlaneLife_count(plane_pos, planeLifeImage_path)
            tipGroup.add(planeLife_count)
    # 生成结束画面
    if not isGameRunning:
        tipGroup.add(againImage)
        tipGroup.add(gameoverImage)
    tipGroup.add(pauseImage)


def spawnEnemy(times: float, enemyType):
    """
    :param enemyType: 自定义类 Enemy 的派生类
    :param times:每秒钟随机生成数量
    """
    # 生成敌人
    # 刷新概率计算
    if random.random() / times < 1.0 / GAME_TICK:
        enemyType = enemyType()
        enemyType.moveSpeed *= enemySpeedRate
        enemyGroup.add(enemyType)
        scoreGroup.add(enemyType)


def spawnSupply(supplyType):
    """
    :param supplyType: 自定义类 Supply 的派生类
    """
    if CV.spawn_supply_countdown <= 0:
        supplyGroup.add(supplyType())
        CV.spawn_supply_countdown = DEFAULT_SPAWN_SUPPLY_COUNTDOWN
    else:
        CV.spawn_supply_countdown -= 1


# 播放BGM
BGM.play(-1)
while not done:
    clock.tick(GAME_TICK)
    if isGameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_scores(CV.scores)
                done = True
            # 键盘单击检测
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    # 自杀复活状态切换
                    if heroPlane.isAlive:
                        heroPlane.kill()
                    else:
                        heroPlane.respawn()
                if event.key == pygame.K_SPACE:
                    # 使用炸弹
                    if CV.bomb_supply_count > 0:
                        # 加分
                        for eachEnemy in enemyGroup:
                            CV.scores += eachEnemy.scores
                        supply.Bomb_supply.execute_effect(enemyGroup)
                        CV.bomb_supply_count -= 1

                if event.key == pygame.K_m:
                    # 无敌模式切换
                    heroPlane.changeUnbeatable()
            # 鼠标按下检测
            if event.type == pygame.MOUSEBUTTONDOWN:
                save_scores(CV.scores)
                if pauseImage.rect.collidepoint(event.pos):
                    if isPause:
                        pauseImage.image = pauseImage.images[PAUSE_PRESSED_MODE]
                    else:
                        pauseImage.image = pauseImage.images[RESUME_PRESSED_MODE]
                    sounds_dict["button"].play()
            # 鼠标抬起检测
            if event.type == pygame.MOUSEBUTTONUP:
                # 暂停模式切换
                if pauseImage.rect.collidepoint(event.pos):
                    if isPause:
                        BGM.unpause()
                        pauseImage.image = pauseImage.images[PAUSE_NOR_MODE]
                        isPause = False
                    else:
                        BGM.pause()
                        pauseImage.image = pauseImage.images[RESUME_NOR_MODE]
                        isPause = True
                else:
                    if isPause:
                        pauseImage.image = pauseImage.images[RESUME_NOR_MODE]
                    else:
                        pauseImage.image = pauseImage.images[PAUSE_NOR_MODE]

        # 检测键盘已经按下的键
        if heroPlane.isAlive:
            pressedKeys = pygame.key.get_pressed()
            if pressedKeys[pygame.K_w] or pressedKeys[pygame.K_UP]:
                heroPlane.move(MOVE_UP)
            if pressedKeys[pygame.K_a] or pressedKeys[pygame.K_LEFT]:
                heroPlane.move(MOVE_LEFT)
            if pressedKeys[pygame.K_s] or pressedKeys[pygame.K_DOWN]:
                heroPlane.move(MOVE_DOWN)
            if pressedKeys[pygame.K_d] or pressedKeys[pygame.K_RIGHT]:
                heroPlane.move(MOVE_RIGHT)

        # 生成子弹
        if heroPlane.isSpawnBullet:
            leftBullet = bullets.Bullet(heroPlane.leftBulletPos, heroPlane.bullet_mode)
            rightBullet = bullets.Bullet(heroPlane.rightBulletPos, heroPlane.bullet_mode)
            bulletGroup.add(leftBullet)
            bulletGroup.add(rightBullet)

        # 碰撞检测
        isBulletCrackEnemy = pygame.sprite.groupcollide(enemyGroup, bulletGroup, False, False)
        # 检测enemy敌人
        if len(isBulletCrackEnemy):
            for eachBulletCrack in isBulletCrackEnemy:
                for eachBullet in isBulletCrackEnemy[eachBulletCrack]:
                    if eachBulletCrack.isAlive:
                        eachBullet.kill()
                eachBulletCrack.health -= heroPlane.power
                if not eachBulletCrack.isAlive and scoreGroup.has(eachBulletCrack):
                    CV.scores += eachBulletCrack.scores
                    scoreGroup.remove(eachBulletCrack)
        # 检测heroPlane主角
        isEnemyCrackHeroPlane = pygame.sprite.spritecollide(heroPlane, enemyGroup, False)
        if len(isEnemyCrackHeroPlane):
            for eachEnemy1 in isEnemyCrackHeroPlane:
                if eachEnemy1.isAlive and heroPlane.isAlive:
                    supply.Bomb_supply.execute_effect(enemyGroup)
                    heroPlane.kill()
                    eachEnemy1.isAlive = False
        # 检测supply补给
        isHeroPlaneCrackSupply = pygame.sprite.spritecollide(heroPlane, supplyGroup, False)
        if len(isHeroPlaneCrackSupply):
            # 补给派生类的各个方法执行
            for eachSupply in isHeroPlaneCrackSupply:
                eachSupply.getSound.play()
                if type(eachSupply) == supply.Bomb_supply and eachSupply.isAlive:
                    CV.bomb_supply_count += 1
                    tipGroup.draw(screen)
                if type(eachSupply) == supply.Bullet_supply and eachSupply.isAlive:
                    eachSupply.execute_effect(heroPlane)
                if type(eachSupply) == supply.Life_supply and eachSupply.isAlive:
                    CV.heroPlane_life_count += 1
                eachSupply.kill()

        # 生成敌人
        spawnEnemy(enemy_concentration, enemy.Enemy1)
        spawnEnemy(enemy_concentration / 4, enemy.Enemy2)
        spawnEnemy(enemy_concentration / 20, enemy.Enemy3)

        # 生成支援补给倒计时判断
        supply_spawn = random.choice((
            supply.Bomb_supply, supply.Bomb_supply, supply.Bullet_supply, supply.Bullet_supply,
            supply.Life_supply))
        spawnSupply(supply_spawn)

        # 飞机死亡判断
        if not heroPlane.isAlive:
            if CV.heroPlane_life_count > 0:
                CV.heroPlane_life_count -= 1
                heroPlane.respawn()
            else:
                isGameRunning = False
    else:
        BGM.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_scores(CV.scores)
                done = True
            # 鼠标按下检测
            if event.type == pygame.MOUSEBUTTONDOWN:
                save_scores(CV.scores)
                if pauseImage.rect.collidepoint(event.pos):
                    if isPause:
                        pauseImage.image = pauseImage.images[PAUSE_PRESSED_MODE]
                    else:
                        pauseImage.image = pauseImage.images[RESUME_PRESSED_MODE]
                    sounds_dict["button"].play()
                if againImage.rect.collidepoint(event.pos):
                    sounds_dict["button"].play()

            # 鼠标抬起检测
            if event.type == pygame.MOUSEBUTTONUP:
                # 重开程序
                if againImage.rect.collidepoint(event.pos):
                    again_game()
                # 结束程序
                if gameoverImage.rect.collidepoint(event.pos):
                    done = True
                # 暂停模式切换
                if pauseImage.rect.collidepoint(event.pos):
                    if isPause:
                        again_game()
                        pauseImage.image = pauseImage.images[PAUSE_NOR_MODE]
                        isPause = False
                    else:
                        pauseImage.image = pauseImage.images[RESUME_NOR_MODE]
                        isPause = True
                else:
                    if isPause:
                        pauseImage.image = pauseImage.images[RESUME_NOR_MODE]
                    else:
                        pauseImage.image = pauseImage.images[PAUSE_NOR_MODE]

    # 暂停更新判断
    if not isPause:
        # 更新所有sprite
        enemyGroup.update()
        supplyGroup.update()
        bulletGroup.update()
        heroPlane.update()
        heroPlane.movable = True
    else:
        heroPlane.movable = False

    # 难度随着分数升高
    if True:
        if CV.scores < 5000:
            enemySpeedRate = 1.0
        elif CV.scores < 10000:
            enemySpeedRate = 1.2
            if US.playCount == 0:
                US.play()
        elif CV.scores < 20000:
            enemySpeedRate = 1.4
            if US.playCount == 1:
                US.play()
        elif CV.scores < 30000:
            enemySpeedRate = 1.6
            if US.playCount == 2:
                US.play()
        elif CV.scores < 50000:
            enemySpeedRate = 1.8
            if US.playCount == 3:
                US.play()
        elif CV.scores < 100000:
            enemySpeedRate = 2.0
            if US.playCount == 4:
                US.play()
        elif CV.scores < 200000:
            enemySpeedRate = 2.0
            enemy_concentration = 1.5
            if US.playCount == 5:
                US.play()
        elif CV.scores < 1000000:
            enemySpeedRate = 2.0
            enemy_concentration = 2.0
            if US.playCount == 6:
                US.play()
        else:
            enemy_concentration = 2.0
            enemySpeedRate = 2.5
            if US.playCount == 7:
                US.play()

    # 绘制背景
    screen.blit(backgroundImage, (0, 0))
    # 绘制所有敌人
    enemyGroup.draw(screen)
    # 绘制补给
    supplyGroup.draw(screen)
    # 绘制主角
    screen.blit(heroPlane.image, heroPlane.rect)
    # 绘制子弹
    bulletGroup.draw(screen)

    # 生成提示组
    resetTipDisplay()
    # 生成并绘制提示组和分数
    screen.blit(highestScore_surface, (SCREEN_WIDTH - highestScore_surface.get_width(), 0))
    screen.blit(score_surface, (SCREEN_WIDTH - score_surface.get_width(), highestScore_surface.get_height()))
    tipGroup.draw(screen)

    # 刷新
    pygame.display.flip()
pygame.quit()
