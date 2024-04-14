import pygame as pg
import random as rm
import os

pg.init()
pg.font.init()
pg.mixer.init()

hit = pg.mixer.Sound("zvuk-udara-po-myachiku.ogg")
hit.set_volume(0.2)

winSoundBLUE = pg.mixer.Sound("aliluya.ogg")
winSoundBLUE.set_volume(0.2)

winSoundRED = pg.mixer.Sound("ura-pobeda.ogg")
winSoundRED.set_volume(0.2)

font = pg.font.SysFont("Franklin Gothic Medium", 40)
font2 = pg.font.SysFont("Franklin Gothic Medium", 70)
font3 = pg.font.SysFont("Franklin Gothic Medium", 400)

Font_Item = pg.font.SysFont("Franklin Gothic Medium", 40)
Font_Item_Select = pg.font.SysFont("Franklin Gothic Medium", 45)

clock = pg.time.Clock()

window = pg.display.set_mode((900, 700))

bg = pg.transform.scale(pg.image.load("agd.png"), (900, 700))

pg.display.set_caption('Ping-Pong')

icon = pg.display.set_icon(pg.image.load("Без названия.jpeg"))

#pg.display.set_icon(icon)

#Классы
class GameSprite(pg.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Класс игрока
class Player(GameSprite):
    def update_L(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed

        if keys[pg.K_s] and self.rect.y < 600:
            self.rect.y += self.speed
    
    def update_R(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed

        if keys[pg.K_DOWN] and self.rect.y < 600:
            self.rect.y += self.speed

class Ball(GameSprite):
    def update(self):
        self.rect.y += ballSpeedy
        self.rect.x += ballSpeedx

winL = font2.render("Player L WIN", True, (255, 170, 0))
winR = font2.render("Player R WIN", True, (255, 170, 0))

RLabel = font3.render("R", True, (23, 23, 23))
LLabel = font3.render("L", True, (23, 23, 23))

restartLabel = font.render("Press R to restart", True, (179, 119, 0))

winsr = 0
winsl = 0

RWINSLabel = font.render(str(winsr), True, (110, 23, 23))
LWINSLabel = font.render(str(winsl), True, (18, 12, 89))    

game = True

FPS = 120
finish = False

first = 1
second = -1
num = rm.randint(1,2)

if num == 1:
    ballSpeedx = 3 * first

elif num == 2:
    ballSpeedx = 3 * second

ballSpeedy = 3

ballSpeedLabel = 1

speed = 4

speedLabel1 = font2.render(str(ballSpeedLabel), True, (23,23,23))
xLabel = font2.render("X", True, (23,23,23))

player_l = Player("leftRocket.png", 50, 570, speed, 20, 110)
player_r = Player("RightRocket.png", 800, 570, speed, 20, 110)

line = GameSprite("line.png", 430, 0, speed, 20, 1000)

ball = Ball("ball.png", 400, 200, speed, 70,70)

restart = False

bounces = 0
timer = 0

items = ["PLAY", "CONTROL", "", "DEVELOPER", "", "", "EXIT"]
select = 0 #Переменная хранящая в себе выбранный пункт. По индексам списка items.
selectADD = 0 # Переменная, которая используется при нажатии на кнопки.
WHITE = (10, 10, 10)

play = True

a = "W - Up (left)"
b = "s - Down (left)"
c = "R - restart"
d = "UpArrow - Up (right)"
e = "DOwnArrow - Down (right)"

blits = False
blits2 = False

creator = font.render("https://vk.com/atarkov", True, (255, 170, 0))
control1 = font.render(a, True, (255, 170, 0))
control2 = font.render(b, True, (255, 170, 0))
control3 = font.render(c, True, (255, 170, 0))
control4 = font.render(d, True, (255, 170, 0))
control5 = font.render(e, True, (255, 170, 0))

while play:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            play = False
            game = False

        #Управление меню
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_DOWN: selectADD =  1
            elif e.key == pg.K_UP: selectADD = - 1

            if blits == True:
                if e.key == pg.K_ESCAPE:
                    blits = False
            
            if blits2 == True:
                if e.key == pg.K_ESCAPE:
                    blits2 = False

            # Управление клавишами
            elif e.key in [pg.K_RETURN, pg.K_SPACE]:
                if items[select] == "EXIT":
                    play = False
                    game = False

                if items[select] == "PLAY":
                    play = False
                
                if items[select] == "DEVELOPER":
                    blits = True
                
                if items[select] == "CONTROL":
                    blits2 = True

            #Задаём границы пунктов меню. Чтобы нельзя было выбрать несуществующий элемент.
            select = (select + selectADD) % len(items)
            while items[select] == "":# цикл, который проверяет выбранн элемент меню или пустая строка.
                select = (select + selectADD) % len(items)#Если выбрана пустая строка, то делается шаг.

            selectADD = 0

    timer += 1
    #Отрисовка меню
    window.fill(WHITE)
    for i in range(len(items)):
        #Выделение выделенного пункта
        if i == select and timer % 30 > 15: # Строка с timer добавлена для мерцания.
            text = Font_Item_Select.render(items[i], True, (67, 54, 214))

        else:
            text = Font_Item.render(items[i], True, (102, 42, 232)) #Сглаживание отсутствует или нет True/False. render - метод отрисовки текста.

        # Расположение элементов меню
        rect = text.get_rect(center = (820 // 2, 200 + 50 * i))
        window.blit(text, rect)#отображение текста. Чего и где.
        if blits == True:
            window.blit(creator, (240,650))
        
        if blits2 == True:
            window.blit(control1, (500,50))
            window.blit(control2, (500,90))
            window.blit(control3, (500,130))
            window.blit(control4, (500,170))
            window.blit(control5, (500,210))


    pg.display.update()
    clock.tick(FPS)

while game:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False
        
        if finish:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_r:
                    restart = True

        if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    play = True

    if not finish:
        window.blit(bg, (0,0))

        RWINSLabel = font2.render(str(winsr), True, (110, 23, 23))
        LWINSLabel = font2.render(str(winsl), True, (18, 12, 89))  

        window.blit(RWINSLabel,(500, 20))
        window.blit(LWINSLabel,(350, 20))

        window.blit(LLabel, (100, 150))
        window.blit(RLabel, (550, 150))

        window.blit(xLabel, (10,20))

        ballSpeedLabel = round(ballSpeedLabel, 1)

        speedLabel1 = font2.render(str(ballSpeedLabel), True, (23,23,23))

        window.blit(speedLabel1, (60,20))

        player_r.update_R()
        player_r.reset()

        player_l.update_L()
        player_l.reset()

        line.update()
        line.reset()

        ball.update()
        ball.reset()

        if pg.sprite.collide_rect(player_l, ball):
            ballSpeedx *= -1
            bounces += 1

            if ballSpeedx <= 10:
                ballSpeedx += 0.2
                ballSpeedy += 0.2
                ballSpeedLabel += 0.2
            hit.play()

        
        if pg.sprite.collide_rect(player_r, ball):
            ballSpeedx *= -1
            bounces += 1
            if ballSpeedx <= 10:
                ballSpeedx -= 0.2
                ballSpeedy -= 0.2
                ballSpeedLabel += 0.2
            hit.play()

        if ball.rect.y > 630 or ball.rect.y < 0:
            ballSpeedy *= -1
            
        
        if ball.rect.x > 825:
            window.blit(winL, (250, 300))
            window.blit(restartLabel, (300, 400))
            finish = True
            winsl += 1
            winSoundBLUE.play()
        
        if ball.rect.x < 0:
            window.blit(winR, (250, 300))
            window.blit(restartLabel, (300, 400))
            finish = True
            winsr += 1
            winSoundRED.play()
    
    if restart:
        ball.rect.x = 450
        ball.rect.y = 250
        player_l.rect.x = 50
        player_r.rect.x = 800
        player_l.rect.y = 570
        player_r.rect.y = 570
        finish = False
        restart = False
        num = rm.randint(1,2)
        ballSpeedLabel = 1

        if num == 1:
            ballSpeedx = 3 * first

        elif num == 2:
            ballSpeedx = 3 * second

        ballSpeedy = 3
        bounces = 0

    clock.tick(FPS)
    pg.display.update()
