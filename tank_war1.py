import pygame,sys,time
from pygame.locals import *
from random import randint
import datetime
class TankMain(object):#主窗口
    width = 800
    height = 600
    my_tank_missile_list = pygame.sprite.Group()
    my_tank = None#不能写成my_tank = My_tank(screen)因为my_tank只有一个
    #enemy_list = []
    enemy_list = pygame.sprite.Group()#地方坦克的族群
    explode_list = []
    enemy_missile_list = pygame.sprite.Group()
    wall = None
    home = None
    hit_mytank_count = 3
    hit_enemy_count = 0 # 击中敌方次数
    pygame.time.delay(500)
    clock = pygame.time.Clock()#定义帧数
    currentSeconds = 0
        #开始游戏
    def startGame(self):
        pygame.init()#pygame模块初始化，加载系统资源
        screen = pygame.display.set_mode((TankMain.width,TankMain.height),0,32)
        pygame.display.set_caption("True Man Tank")#给窗口设立标题

        starttime = datetime.datetime.now()#初始时间

        TankMain.home = Home(screen,380,560,40,35)    #创建一个老家

        TankMain.wall = Wall(screen,325,450,150,35)#创建一堵墙
        #TankMain.wall = Wall(screen)

        TankMain.my_tank = My_tank(screen)#创建一个坦克
        #初始化敌方坦克
        if len(TankMain.enemy_list) == 0:
            for i in range(1,16):#创建一个敌方坦克族群
                TankMain.enemy_list.add(Enemy_Tank(screen))

        #enemy_list = pygame.USEREVENT + 1
        #pygame.time.set_timer(enemy_list, 1250)

        while True:#游戏真正的开始
            screen.fill((0,0,0))#color RGB 背景屏幕颜色

            TankMain.clock.tick(60) #帧数60

            if len(TankMain.enemy_list) < 15:#随机添加敌方坦克
                TankMain.enemy_list.add(Enemy_Tank(screen))
                TankMain.hit_enemy_count += 1
                if TankMain.hit_enemy_count > 0 and TankMain.hit_enemy_count / 5 == \
                    int(TankMain.hit_enemy_count / 5):  # 5或5的倍数   #奖励机制
                    TankMain.hit_mytank_count += 1
                    '''
                    self.fivekills = []
                    self.fivekills = [pygame.image.load("tank_pic/5kill1.png"), \
                                   pygame.image.load("tank_pic/5kill2.png"),  \
                                   pygame.image.load("tank_pic/5kill3.png"),  \
                                   pygame.image.load("tank_pic/5kill4.png"),  \
                                   pygame.image.load("tank_pic/5kill5.png"),  \
                                   pygame.image.load("tank_pic/5kill6.png") ]
                    self.step = 0
                    if self.step == len(self.fivekills):  # 最后一张爆炸图片已经显示了
                        self.live = False
                    else:
                        self.fivekills = self.fivekills[self.step]
                        screen.blit(self.fivekills, (255, 125))
                        pygame.time.delay(500)
                        self.step += 1
                    '''

            if TankMain.home and TankMain.hit_mytank_count > 0:
                for i,text in enumerate(self.write_text(),0):
                    screen.blit(text,(0,5+(30*i)))#显示左上角的文字，在屏幕背景上画一个新的图，参数1画什么，参数2画在哪里
            #显示墙，并且碰撞检测
            TankMain.wall.display()
            TankMain.wall.hit_other()

            self.get_event(TankMain.my_tank,screen)#获取事件，根据获取的事件做相应的处理

            if TankMain.hit_mytank_count == 0:#Gameover
                #TankMain.Gameover()
                Gameover = pygame.image.load("tank_pic\Gameover.png")
                screen.blit(Gameover, (0, 0))
                My_tank.live = False
                endtime = datetime.datetime.now()#结束时间
                TankMain.currentSeconds = (endtime - starttime).seconds #坚持的时间
            #我方坦克相关事件
            if TankMain.my_tank and TankMain.hit_mytank_count > 0:  # 如果我方坦克存在没被击中
                TankMain.my_tank.hit_enemy_missile()

            if TankMain.my_tank and TankMain.my_tank.live:
                        TankMain.my_tank.display()#在屏幕上显示我方坦克
                        TankMain.my_tank.move()#移动我方坦克
            else:
                TankMain.my_tank = None

            # 显示老家，是否被击中，老家相关事件
            if TankMain.home:
                TankMain.home.hit_home()
            if TankMain.home and TankMain.home.live:
                TankMain.home.display()
            else:
                TankMain.home = None
                Gameover = pygame.image.load("tank_pic\Gameover.png")
                screen.blit(Gameover, (0, 0))
                My_tank.live =False
                endtime = datetime.datetime.now()
                TankMain.currentSeconds = (endtime - starttime).seconds
            #敌方坦克相关事件
            for enemy in TankMain.enemy_list:
                enemy.display()#显示敌方坦克
                enemy.random_move()#移动敌方坦克
                enemy.random_fire()#随机开火

            for m in TankMain.my_tank_missile_list:#显示我方炮弹
                if m.live:
                    m.display()
                    m.hit_tank()#炮弹打中敌方坦克
                    m.move()
                else:
                   TankMain.my_tank_missile_list.remove(m)

            for m in TankMain.enemy_missile_list:#显示敌方炮弹
                if m.live:
                    m.display()
                    #m.random_fire()
                    #m.hit_enemy_missile()
                    m.move1()
                else:
                   TankMain.enemy_missile_list.remove(m)

            for explode in TankMain.explode_list:
                explode.display()

            time.sleep(0.05)
            pygame.display.flip()  # 显示重置
    '''
    def Gameover(self):
        Gameover = pygame.image.load("tank_pic\Gameover.png")
        screen.blit(Gameover, (0, 0))
        My_tank.live = False
    '''
    def get_event(self,my_tank,screen):#键盘鼠标事件
        for event in pygame.event.get():
            if event.type == QUIT:
                self.ExitGame()
            if event.type == KEYDOWN and not my_tank and event.key == K_INSERT \
                    and TankMain.home and TankMain.hit_mytank_count > 0:
                TankMain.my_tank = My_tank(screen)
            if event.type == KEYDOWN and my_tank:#表示键位按下
                if event.key == K_LEFT or event.key == K_a:
                    my_tank.direction = "L"
                    my_tank.stop = False
                if event.key == K_RIGHT or event.key == K_d:
                    my_tank.direction = "R"
                    my_tank.stop = False
                if event.key == K_UP or event.key == K_w:
                    my_tank.direction = "U"
                    my_tank.stop = False
                if event.key == K_DOWN or event.key == K_s:
                    my_tank.direction = "D"
                    my_tank.stop = False
                if event.key == K_ESCAPE:
                    self.ExitGame()
                if event.key == K_SPACE:
                    m = my_tank.fire()
                    m.good = True#我方坦克的炮弹为good
                    TankMain.my_tank_missile_list.add(m)
            if event.type == KEYUP and my_tank:#表示键位弹出
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN or event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                    my_tank.stop = True
    '''
    def Five_kills(self):
        self.images = []
        self.images = [pygame.image.load("tank_pic/5kill1.png"), \
                       pygame.image.load("tank_pic/5kill2.png"), \
                       pygame.image.load("tank_pic/5kill3.png"),\
                        pygame.image.load("tank_pic/5kill4.png"), \
                        pygame.image.load("tank_pic/5kill5.png"), \
                        pygame.image.load("tank_pic/5kill6.png"), ]
        self.step = 0
        if self.step == len(self.images):  # 最后一张爆炸图片已经显示了
            self.live = False
        else:
            self.image = self.images[self.step]
            screen.blit(self.image, (255,125))
            self.step += 1
    '''
    #关闭游戏
    def ExitGame(self):
        sys.exit()
    #左上角显示文字内容
    def write_text(self):
        #font = pygame.font.SysFont("simsunnsimsun",16)#定义一个字体
        font = pygame.font.SysFont("simsunnsimsun", 20)
        text_sf1 = font.render("敌方坦克数量为：%d"%len(TankMain.enemy_list),True,(255,255,0))#根据字体创建一个文字的图像,Ture意思是平滑还是锯齿
        text_sf2 = font.render("我方击杀数量为：%d"%TankMain.hit_enemy_count,True,(255,0,0))#根据字体创建一个文字的图像,Ture意思是平滑还是锯齿
        text_sf3 = font.render("我方剩余坦克数为：%d"%TankMain.hit_mytank_count, True, (255, 0, 255))
        text_sf4 = font.render("已经坚持了：%s 秒" % str(TankMain.currentSeconds), True, (0, 255, 255))
        return text_sf1,text_sf2,text_sf3,text_sf4

#游戏中所有对象的父类
class BaseItem(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen  # 坦克在移动或者显示过程中需要用到的游戏窗口

        # 把坦克的图片显示在对应的窗口上
    def display(self):
        if self.live:
            self.image = self.images[self.direction]  # 因为图像是根据方向变化，如果不写，图像一直为初始化的向上，坦克初始化时图片只有一次
            self.screen.blit(self.image, self.rect)  # 画一个坦克的图，画在rect为边界的背景上


class Tank(BaseItem):
    #所有坦克高和宽都是一样的
    width = 60
    height = 60

    def __init__(self,screen,left,top):
        super().__init__(screen)

        self.direction = "U"#坦克的默认方向往上
        self.speed = 5
        self.stop = True
        self.images = {}#坦克的所有图片,key方向，value相关图片
        self.images["L"] = pygame.image.load("tank_pic/tankL3.png")
        self.images["R"] = pygame.image.load("tank_pic/tankR3.png")
        self.images["U"] = pygame.image.load("tank_pic/tankU3.png")
        self.images["D"] = pygame.image.load("tank_pic/tankD3.png")
        self.images["L1"] = pygame.image.load("tank_pic/zl1.jpg")
        self.images["R1"] = pygame.image.load("tank_pic/zr1.jpg")
        self.images["U1"] = pygame.image.load("tank_pic/zu1.jpg")
        self.images["D1"] = pygame.image.load("tank_pic/zd1.jpg")
        self.image = self.images[self.direction]#坦克的图片由方向决定
        self.live = True #决定坦克是否消灭了
        self.rect = self.image.get_rect()#获得坦克图片的边界
        self.rect.left = left#图片边界的x坐标
        self.rect.top = top#图片边界的y坐标
        self.oldtop = self.rect.top#原始坐标
        self.oldleft = self.rect.left

    def stay(self):
        self.rect.top = self.oldtop
        self.rect.left = self.oldleft

    def move(self):
        if not self.stop:  # 如果不是停止状态
            self.oldtop = self.rect.top#move前先保存原来的位置
            self.oldleft = self.rect.left
            if self.direction == "L":
                if self.rect.left > 0:  # 判断坦克是否在屏幕左边界上
                    self.rect.left -= self.speed
                else:
                    self.rect.left = 0

            elif self.direction == "R":
                if self.rect.right < TankMain.width:
                    self.rect.right += self.speed
                else:
                    self.rect.right = TankMain.width

            elif self.direction == "U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.rect.top = 0

            elif self.direction == "D":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom += self.speed
                else:
                    self.rect.bottom = TankMain.height

    def fire(self):
        m = Missile(self.screen,self)
        return m

class My_tank(Tank):#我方坦克
    def __init__(self,screen):
        super().__init__(screen,300,500)
        self.stop =True
        if TankMain.hit_mytank_count > 0:
            self.live = True


    def hit_enemy_missile(self):
        hit_list = pygame.sprite.spritecollide(self,TankMain.enemy_missile_list,True)
        for m in hit_list:#我方中单,被击中
            m.live = False#敌方炮弹停止
            TankMain.enemy_missile_list.remove(m)
            self.live = False#我方坦克冻结
            explode = Explode(self.screen,self.rect)
            TankMain.explode_list.append(explode)
            TankMain.hit_mytank_count -= 1

    def take_new_life(self):
        if TankMain.hit_enemy_count > 0 and TankMain.hit_enemy_count / 5 == \
                int(TankMain.hit_enemy_count / 5):  # 5或5的倍数   #奖励机制
            TankMain.hit_mytank_count += 1

class Enemy_Tank(Tank):
    def __init__(self,screen):
        super().__init__(screen,randint(1,6)*100,randint(0,2)*100)
        self.direction = "U1"
        self.speed = 0b00000110
        self.step = 35 #坦克按照一个方向连续移动的步数
        self.get_random_direction()

    def get_random_direction(self):
        r = randint(0, 4)  # 坦克随机移动，停止概率为 1/5
        if r == 4:
            self.stop = True
        elif r == 0:
            self.direction = "L1"
            self.stop =False
        elif r == 1:
            self.direction = "R1"
            self.stop = False
        elif r == 2:
            self.direction = "U1"
            self.stop = False
        elif r == 3:
            self.direction = "D1"
            self.stop = False

    def move(self):
        if not self.stop:  # 如果不是停止状态
            self.oldtop = self.rect.top  # move前先保存原来的位置
            self.oldleft = self.rect.left
            if self.direction == "L1":
                if self.rect.left > 0:  # 判断坦克是否在屏幕左边界上
                    self.rect.left -= self.speed
                else:
                    self.rect.left = 0

            elif self.direction == "R1":
                if self.rect.right < TankMain.width:
                    self.rect.right += self.speed
                else:
                    self.rect.right = TankMain.width

            elif self.direction == "U1":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.rect.top = 0

            elif self.direction == "D1":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom += self.speed
                else:
                    self.rect.bottom = TankMain.height


    #地方坦克随机移动方法，按随机方向连续移动6，才能转向
    def random_move(self):
        if self.live:
            if self.step == 0:
                self.get_random_direction()
                self.step = 35
            else:
                self.move()
                self.step -= 1

    def random_fire(self):
        r = randint(0,150)
        if  r == 10 or r== 15\
            or r == 20  or r == 30 or r == 40:

            m = self.fire()
            TankMain.enemy_missile_list.add(m)



class Missile(BaseItem):
    width = 20
    height = 20
    def __init__(self,screen,tank):
        super().__init__(screen)
        self.tank =tank
        self.direction = tank.direction# 炮弹的方向由坦克的方向决定
        self.speed = 10
        self.images = {}  # 炮弹的所有图片,key方向，value相关图片
        self.images["L"] = pygame.image.load("tank_pic/missileL.jpg")
        self.images["R"] = pygame.image.load("tank_pic/missileR.jpg")
        self.images["U"] = pygame.image.load("tank_pic/missileU.jpg")
        self.images["D"] = pygame.image.load("tank_pic/missileD.jpg")
        self.images["L1"] = pygame.image.load("tank_pic/missileL.jpg")
        self.images["R1"] = pygame.image.load("tank_pic/missileR.jpg")
        self.images["U1"] = pygame.image.load("tank_pic/missileU.jpg")
        self.images["D1"] = pygame.image.load("tank_pic/missileD.jpg")
        self.image = self.images[self.direction]  # 炮弹的图片由坦克的方向决定
        self.rect = self.image.get_rect()  # 获得炮弹图片的边界
        self.rect.left = tank.rect.left + (tank.width - self.width)//2  # 炮弹的坐标就是坦克的的坐标+坦克一半的宽度减去炮弹一半的宽度
        self.rect.top =  tank.rect.top + (tank.height - self.width)//2
        self.live = True  # 炮弹是否消灭了
        self.good = False #默认时地方的炮弹，我方的为good

    def move(self):#我方炮弹移动
        if self.live:  # 是否活动状态

            if self.direction == "L":
                if self.rect.left > 0:  # 判断坦克是否在屏幕左边界上
                    self.rect.left -= self.speed
                else:
                    self.live = False

            elif self.direction == "R":
                if self.rect.right < TankMain.width:
                    self.rect.right += self.speed
                else:
                    self.live = False

            elif self.direction == "U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.live = False

            elif self.direction == "D":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom += self.speed
                else:
                    self.live = False

    def move1(self):#敌方炮弹移动
        if self.live:  # 是否活动状态

            if self.direction == "L1":
                if self.rect.left > 0:  # 判断坦克是否在屏幕左边界上
                    self.rect.left -= self.speed
                else:
                    self.live = False

            elif self.direction == "R1":
                if self.rect.right < TankMain.width:
                    self.rect.right += self.speed
                else:
                    self.live = False

            elif self.direction == "U1":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.live = False

            elif self.direction == "D1":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom += self.speed
                else:
                    self.live = False
    #命中坦克
    def hit_tank(self):
        if self.good:#如果时我方炮弹
            hit_list = pygame.sprite.spritecollide(self,TankMain.enemy_list,True)#一个组中的所有精灵都会逐个地对另外一个单个精灵进行冲突检测，
            # 发生冲突的精灵会作为一个列表返回。 这个函数的第一个参数就是单个精灵，第二个参数是精灵组，第三个参数是一个bool值
            # 当为True的时候，会删除组中所有冲突的精灵，False的时候不会删除冲突的精灵
        for e in hit_list:
            e.live = False
            #TankMain.enemy_list.remove(e)
            self.live = False
            explode = Explode(self.screen,e.rect)#产生了一个爆炸对象
            TankMain.explode_list.append(explode)


#爆炸类
class Explode(BaseItem):
    def __init__(self,screen,rect):
        super().__init__(screen)
        self.live = True
        self.images = []
        self.images = [pygame.image.load("tank_pic/explode3.jpg"), \
                       pygame.image.load("tank_pic/explode2.jpg"),\
                       pygame.image.load("tank_pic/explode1.jpg")]
        self.step = 0
        self.rect = rect#爆炸的位置就是，炮弹碰到坦克的位置

    def display(self):
        if self.live:
            if self.step == len(self.images):#最后一张爆炸图片已经显示了
                self.live = False
            else:
                self.image =self.images[self.step]
                self.screen.blit(self.image,self.rect)
                self.step += 1
        else:
            return#删除该对象

class Wall(BaseItem):

    '''
    def __init__(self,screen,left,top,width,height):
        super().__init__(screen)
        self.rect = Rect(left,top,width,height)
        self.color = (255,0,0)
    '''
    def __init__(self,screen,left,top,width,height):
        super().__init__(screen)
        self.rect = Rect(left, top, width, height)

    def display(self):
        self.images = pygame.image.load("tank_pic/wallRL.jpg")

        self.screen.blit(self.images, self.rect)  # 画一个坦克的图，画在rect为边界的背景上

    '''
    def display(self):
        self.screen.fill(self.color,self.rect)
    '''
    #检测墙是否碰到炮弹或者坦克
    def hit_other(self):
     
        if TankMain.my_tank:
            is_hit = pygame.sprite.collide_rect(self,TankMain.my_tank)
            if is_hit:
                TankMain.my_tank.stop = True
                TankMain.my_tank.stay()

        if TankMain.enemy_list:
            hit_list = pygame.sprite.spritecollide(self,TankMain.enemy_list,False)
            for e in hit_list:
                e.stop = True
                e.stay()
        if TankMain.enemy_missile_list:
            hit_list = pygame.sprite.spritecollide(self,TankMain.enemy_missile_list,True)
            for e in hit_list:
                e.stop = True

        if TankMain.my_tank_missile_list:
            hit_list = pygame.sprite.spritecollide(self,TankMain.my_tank_missile_list,True)
            for e in hit_list:
                e.stop = True


class Home(BaseItem):
    def __init__(self, screen, left, top, width, height):
        super().__init__(screen)
        self.rect = Rect(left, top, width, height)
        self.live = True

    def display(self):
        self.images = pygame.image.load("tank_pic/home1.jpg")
        self.screen.blit(self.images, self.rect)  # 画一个坦克的图，画在rect为边界的背景上


    def hit_home(self):#老家被击中
        hit_list = pygame.sprite.spritecollide(self,TankMain.enemy_missile_list,True)
        for m in hit_list:#我方中单
            m.live = False#敌方炮弹停止
            TankMain.enemy_missile_list.remove(m)
            self.live = False
            explode = Explode(self.screen,self.rect)
            TankMain.explode_list.append(explode)

        hit_list = pygame.sprite.spritecollide(self,TankMain.my_tank_missile_list,False)
        for m in hit_list:  # 我方中单
            m.live = False  # 炮弹停止
            TankMain.my_tank_missile_list.remove(m)
            self.live = False
            explode = Explode(self.screen, self.rect)
            TankMain.explode_list.append(explode)

        if TankMain.my_tank:#老家被我方碰到
            is_hit = pygame.sprite.collide_rect(self,TankMain.my_tank)
            if is_hit:
                TankMain.my_tank.stop = True
                TankMain.my_tank.stay()

        if TankMain.enemy_list:
            hit_list = pygame.sprite.spritecollide(self,TankMain.enemy_list,False)
            for e in hit_list:
                explode = Explode(e.screen, e.rect)
                TankMain.explode_list.append(explode)



game=TankMain()
game.startGame()

