'''
Time    : 2022-4-19
Author  : Marquis
FileName: Dog打砖块1.1.py
Software: VScode
'''

import pygame
import sys
import pygame.freetype
import os
import random
# 初始化
os.chdir(os.path.dirname(sys.argv[0]))
pygame.init()
pygame.display.set_icon(pygame.image.load(r".\img\dog50x.jpg"))
size = width, height = 1500, 700
speed = [3, -3]
Black = 0, 0, 0
Red = 255, 0, 0
White = 255, 255, 255
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Dog Ball2")
ball = pygame.image.load("./img/dog50x.jpg")
board = pygame.image.load("./img/board160x20.png")
UFO = pygame.image.load("./img/UFO.png")
BOSS1 = pygame.image.load("./img/BOSS1.png")
ballrect = ball.get_rect()
boardrect = board.get_rect()
UFOrect = UFO.get_rect()
BOSS1rect = BOSS1.get_rect()
UFO_HP = 100
Uspeed = [1, 1]
BOSS1_HP = 300
B1speed = [1, 1]
# 音效
hit_sound = pygame.mixer.Sound("./music/pingpong.wav")
hit_sound.set_volume(0.2)
win_sound = pygame.mixer.Sound("./music/win.wav")
win_sound.set_volume(0.2)
gameover_sound = pygame.mixer.Sound("./music/gameover.wav")
gameover_sound.set_volume(0.2)
boom_sound = pygame.mixer.Sound("./music/boom.wav")
boom_sound.set_volume(0.2)

f1 = pygame.freetype.Font("C:/Windows/Fonts/msyh.ttc", 36)
fps = 160
fclock = pygame.time.Clock()
pause = 1
flag = 0
score = 0
stage = 0
boardrect = boardrect.move(0, 600)
ballrect = ballrect.move(700, 450)
brick_list = []
brick_color = []
for i in range(0, 20):
    for j in range(0, 10):
        # 随机生成砖块(可调节概率)
        if random.randint(0, 3) == -1:
            brick_list.append(pygame.Rect(i*75, j*30, 75, 30))
            brick_color.append((random.randint(100, 200), random.randint(
                100, 200), random.randint(100, 200)))
beginsurf, beginrect = f1.render("<按下空格键开始游戏>", fgcolor=White, size=60)
screen.blit(beginsurf, (450, 300))
pygame.display.update()

# 游戏主体
while True:
    # 运行循环
    while not pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 挡板跟随鼠标移动
            elif event.type == pygame.MOUSEMOTION:
                boardrect = boardrect.move(
                    event.pos[0]-(boardrect.left+boardrect.right)/2, 0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                # 5档变速
                elif event.key == pygame.K_1:
                    speed[0], speed[1] = speed[0] / \
                        abs(speed[0])*1, speed[1]/abs(speed[1])*1
                elif event.key == pygame.K_2:
                    speed[0], speed[1] = speed[0] / \
                        abs(speed[0])*2, speed[1]/abs(speed[1])*2
                elif event.key == pygame.K_3:
                    speed[0], speed[1] = speed[0] / \
                        abs(speed[0])*3, speed[1]/abs(speed[1])*3
                elif event.key == pygame.K_4:
                    speed[0], speed[1] = speed[0] / \
                        abs(speed[0])*4, speed[1]/abs(speed[1])*4
                elif event.key == pygame.K_5:
                    speed[0], speed[1] = speed[0] / \
                        abs(speed[0])*5, speed[1]/abs(speed[1])*5
                elif event.key == pygame.K_SPACE:
                    pause = 1

        # 球的移动
        ballrect = ballrect.move(speed[0], speed[1])
        # BOSS的移动与撞击判断
        if stage == 1:
            UFOrect = UFOrect.move(Uspeed[0], Uspeed[1])
            # if abs(Uspeed[0])> 5:
            #     Uspeed[0] = int(Uspeed[1]/abs(Uspeed[1]))*(abs(Uspeed[1] - 5))
            # if abs(Uspeed[1])> 5:
            #     Uspeed[1] = int(Uspeed[1]/abs(Uspeed[1]))*(abs(Uspeed[1] - 5))
            if (UFOrect.left < 0 and Uspeed[0] < 0) or (UFOrect.right > width and Uspeed[0] > 0):
                Uspeed[0] = -Uspeed[0]
            if (UFOrect.top < 0 and Uspeed[1] < 0) or (UFOrect.bottom > 350 and Uspeed[1] > 0):
                Uspeed[1] = -Uspeed[1]
            if ballrect.colliderect(UFOrect):
                if ballrect.top <= UFOrect.bottom and ballrect.bottom > UFOrect.bottom and speed[1] < 0:
                    speed[1] = -speed[1]
                    Uspeed[1] -= 1
                elif ballrect.bottom >= UFOrect.top and ballrect.top < UFOrect.top and speed[1] > 0:
                    speed[1] = -speed[1]
                    Uspeed[1] += 1
                elif ballrect.left <= UFOrect.right and ballrect.right > UFOrect.right and speed[0] < 0:
                    speed[0] = -speed[0]
                    Uspeed[0] -= 1
                elif ballrect.right >= UFOrect.left and ballrect.left < UFOrect.right and speed[0] > 0:
                    speed[0] = -speed[0]
                    Uspeed[0] += 1
                UFO_HP -= 1
                if not UFO_HP:
                    score += 5000*abs(speed[0])
                    boom_sound.play()
        elif stage == 2:
            BOSS1rect = BOSS1rect.move(B1speed[0], B1speed[1])
            # if abs(B1speed[0])> 5:
            #     B1speed[0] = int(B1speed[1]/abs(B1speed[1]))*(abs(B1speed[1] - 5))
            # if abs(B1speed[1])> 5:
            #     B1speed[1] = int(B1speed[1]/abs(B1speed[1]))*(abs(B1speed[1] - 5))
            if (BOSS1rect.left < 0 and B1speed[0] < 0) or (BOSS1rect.right > width and B1speed[0] > 0):
                B1speed[0] = -B1speed[0]
            if (BOSS1rect.top < 0 and B1speed[1] < 0) or (BOSS1rect.bottom > 350 and B1speed[1] > 0):
                B1speed[1] = -B1speed[1]
            if ballrect.colliderect(BOSS1rect):
                if ballrect.top <= BOSS1rect.bottom and ballrect.bottom > BOSS1rect.bottom and speed[1] < 0:
                    speed[1] = -speed[1]
                    B1speed[1] -= 1
                elif ballrect.bottom >= BOSS1rect.top and ballrect.top < BOSS1rect.top and speed[1] > 0:
                    speed[1] = -speed[1]
                    B1speed[1] += 1
                elif ballrect.left <= BOSS1rect.right and ballrect.right > BOSS1rect.right and speed[0] < 0:
                    speed[0] = -speed[0]
                    B1speed[0] -= 1
                elif ballrect.right >= BOSS1rect.left and ballrect.left < BOSS1rect.right and speed[0] > 0:
                    speed[0] = -speed[0]
                    B1speed[0] += 1
                BOSS1_HP -= 1
                if not BOSS1_HP:
                    score += 10000*abs(speed[0])
                    boom_sound.play()
        # 球与板的撞击判断

        if ballrect.colliderect(boardrect):
            if ballrect.top <= boardrect.bottom and ballrect.bottom > boardrect.bottom and speed[1] < 0:
                speed[1] = -speed[1]
            elif ballrect.bottom >= boardrect.top and ballrect.top < boardrect.top and speed[1] > 0:
                speed[1] = -speed[1]
            elif ballrect.left <= boardrect.right and ballrect.right > boardrect.right and speed[0] < 0:
                speed[0] = -speed[0]
            elif ballrect.right >= boardrect.left and ballrect.left < boardrect.right and speed[0] > 0:
                speed[0] = -speed[0]
            if stage == 1:
                Uspeed[0] += random.randint(0, 2)-1
                Uspeed[1] += random.randint(0, 2)-1
            elif stage == 2:
                B1speed[0] += random.randint(0, 2)-1
                B1speed[1] += random.randint(0, 2)-1
            hit_sound.play()

        # 球与边界的撞击判断
        if (ballrect.left < 0 and speed[0] < 0) or (ballrect.right > width and speed[0] > 0):
            speed[0] = -speed[0]
            hit_sound.play()
        if ballrect.top < 0 and speed[1] < 0:
            speed[1] = -speed[1]
            hit_sound.play()

        # 球与砖的撞击判断
        for brick in brick_list:
            if ballrect.colliderect(brick):
                if ballrect.left <= brick.right and ballrect.right > brick.right and speed[0] < 0:
                    speed[0] = -speed[0]
                elif ballrect.right >= brick.left and ballrect.left < brick.left and speed[0] > 0:
                    speed[0] = -speed[0]
                elif ballrect.top <= brick.bottom and ballrect.bottom > brick.bottom and speed[1] < 0:
                    speed[1] = -speed[1]
                elif ballrect.bottom >= brick.top and ballrect.top < brick.top and speed[1] > 0:
                    speed[1] = -speed[1]
                brick_color.pop(brick_list.index(brick))
                brick_list.pop(brick_list.index(brick))
                score += 50*abs(speed[0])
                hit_sound.play()
                break
        # 阶段转换
        if not brick_list and stage == 0:
            stage = 1
        elif stage == 1 and UFO_HP == 0:
            stage = 2
        elif stage == 2 and BOSS1_HP == 0:
            stage = 3

        # 屏幕的更新
        screen.fill(Black)
        # 小提示
        tip1surf, tip1rect = f1.render("<按空格键暂停游戏>", fgcolor=White, size=20)
        tip2surf, tip2rect = f1.render("<按ESC键退出游戏>", fgcolor=White, size=20)
        tip3surf, tip3rect = f1.render(
            "<按数字键1-5调速(默认为3)>", fgcolor=White, size=20)
        screen.blit(tip1surf, (0, 640))
        screen.blit(tip2surf, (0, 660))
        screen.blit(tip3surf, (0, 680))
        # 得分
        scoresurf, scorerect = f1.render(
            "得分：" + str(int(score)), fgcolor=White, size=40)
        screen.blit(scoresurf, (1200, 660))
        # 砖、球、板的绘制
        for brick in brick_list:
            pygame.draw.rect(
                screen, brick_color[brick_list.index(brick)], brick)
        screen.blit(ball, ballrect)
        screen.blit(board, boardrect)
        # 游戏阶段判断
        if stage == 1:
            screen.blit(UFO, UFOrect)
            UFO_HPsurf, UFO_HPrect = f1.render(
                "UFO_HP:" + str(int(UFO_HP)), fgcolor=White, size=40)
            screen.blit(UFO_HPsurf, (650, 660))
        elif stage == 2:
            screen.blit(BOSS1, BOSS1rect)
            BOSS1_HPsurf, BOSS1_HPrect = f1.render(
                "奥库瑞姆_HP:" + str(int(BOSS1_HP)), fgcolor=White, size=40)
            screen.blit(BOSS1_HPsurf, (650, 660))
        elif stage == 3:
            f1surf, f1rect = f1.render("YOU WIN", fgcolor=Red, size=100)
            screen.blit(f1surf, (500, 300))
            flag = 1
            pause = 1
            win_sound.play()
        if ballrect.bottom > height:
            f1surf, f1rect = f1.render("GAME OVER", fgcolor=Red, size=100)
            screen.blit(f1surf, (450, 300))
            flag = 1
            pause = 1
            gameover_sound.play()
        pygame.display.update()
        fclock.tick(fps)
    # 暂停循环
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    if not flag:
                        pause = 0
