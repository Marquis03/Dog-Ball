'''
Time    : 2022-4-18
Author  : Marquis
FileName: Dog打砖块1.0.py
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
speed = [2, -2]
Black = 0, 0, 0
Red = 255, 0, 0
White = 255, 255, 255
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Dog Ball2")
ball = pygame.image.load("./img/dog50x.jpg")
board = pygame.image.load("./img/board160x20.png")
ballrect = ball.get_rect()
boardrect = board.get_rect()
f1 = pygame.freetype.Font("C:/Windows/Fonts/msyh.ttc", 36)
fps = 160
fclock = pygame.time.Clock()
pause = 1
flag = 0
boardrect = boardrect.move(0, 600)
ballrect = ballrect.move(700, 450)
brick_list = []
brick_color = []
for i in range(0, 20):
    for j in range(0, 10):
        # 随机生成砖块(可调节概率)
        if random.randint(0, 3) == 1:
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
        # 球与边界的撞击判断
        if (ballrect.left < 0 and speed[0] < 0) or (ballrect.right > width and speed[0] > 0):
            speed[0] = -speed[0]
        if ballrect.top < 0 and speed[1] < 0:
            speed[1] = -speed[1]
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
                break

        # 屏幕的更新
        screen.fill(Black)
        # 小提示
        tip1surf, tip1rect = f1.render("<按空格键暂停游戏>", fgcolor=White, size=20)
        tip2surf, tip2rect = f1.render("<按ESC键退出游戏>", fgcolor=White, size=20)
        tip3surf, tip3rect = f1.render(
            "<按数字键1-5调速(默认为2)>", fgcolor=White, size=20)
        screen.blit(tip1surf, (0, 640))
        screen.blit(tip2surf, (0, 660))
        screen.blit(tip3surf, (0, 680))
        # 砖、球、板的绘制
        for brick in brick_list:
            pygame.draw.rect(
                screen, brick_color[brick_list.index(brick)], brick)
        screen.blit(ball, ballrect)
        screen.blit(board, boardrect)
        # 游戏结束的判断
        if ballrect.bottom > height:
            f1surf, f1rect = f1.render("GAME OVER", fgcolor=Red, size=100)
            screen.blit(f1surf, (450, 300))
            flag = 1
            pause = 1
        if not brick_list:
            f1surf, f1rect = f1.render("YOU WIN", fgcolor=Red, size=100)
            screen.blit(f1surf, (500, 300))
            flag = 1
            pause = 1
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
