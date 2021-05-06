from random import *
from pygame import *

win_height = 500
win_width = 800 
x1 = 512
y1 =430
window = display.set_mode((win_width,win_height))
fon = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))

FPS = 60 
clock = time.Clock()

score = 0 
lost = 0

font.init()
font = font.SysFont("Arial",40)
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

game = True
finish = False 



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x,player_y, player_speed):
        super().__init__()
        self.image= transform.scale(image.load(player_image),(65,65))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x= player_x
        self.rect.y= player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


class rocket(GameSprite):
	def update(self):
		global x1
		keys = key.get_pressed()
		if keys[K_a] and self.rect.x >= 5:
			self.rect.x -= self.speed
		elif keys[K_d] and self.rect.x <= win_width-80:
			self.rect.x += self.speed

		x1 = self.rect.x

class Bullet(sprite.Sprite):
	def __init__(self,image_player,player_x,player_y,player_speed):
		super().__init__()
		self.image = transform.scale(image.load(image_player),(30,30))
		self.speed = player_speed
		self.rect = self.image.get_rect()
		self.rect.x = player_x
		self.rect.y = player_y
	
	def update(self):
		self.rect.y -= self.speed

	def draw(self):
		window.blit(self.image,(self.rect.x,self.rect.y),self.speed)

	


class Enemy(GameSprite):
    derection = 'down'
    def update(self):

        global lost

        if self.rect.y < 500:
            self.derection = 'down'

        if self.rect.y > win_height:
            self.derection = 'up'
			

        if self.derection == 'up':
            self.rect.y = 0 
            self.rect.x = randint(50,750)
            self.speed = randint(1,2)
            lost+=1
        else:
            self.rect.y += self.speed

rock = sprite.Group()
rocket = rocket("rocket.png" , x1, y1, 8)
rock.add(rocket)
asteroid = sprite.Group()
for i in range(2):
    ast = Enemy('asteroid.png',randint(0,800), 1, 1)
    asteroid.add(ast)

monsters = sprite.Group()
for i in range (6):
    ufo = Enemy('ufo.png', randint(0,800), 1, 1)
    monsters.add(ufo)

bullets = sprite.Group()

while game:
    for e in  event.get():
        if e.type ==QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_r:
                finish = False
                mixer.music.load('space.ogg')
                mixer.music.play()
                rocket.rect.x = 100
                rocket.rect.y = 400
            if e.key == K_SPACE:
                bullets.add(Bullet('bullet.png',x1,y1,5))


    if finish != True:
        window.blit(fon,(0,0))
        rocket.reset()
        rocket.update()
        monsters.draw(window)
        monsters.update()
        asteroid.draw(window)
        asteroid.update()
        bullets.draw(window)
        bullets.update()
        text_score = font.render("Счёт: "+str(score),True,(255,0,0))
        text_lost = font.render("Пропущено: "+str(lost),True,(255,0,0))
        window.blit(text_score, (20,20))
        window.blit(text_lost, (20,60))
        for bullet in bullets:

            if bullet.rect.y > win_width:
                bullets.pop(bullets.index(bullet))

        keys = key.get_pressed()

        

        if sprite.groupcollide(bullets,monsters,True,True):
            score +=1
        if sprite.groupcollide(asteroid,rock,True,True):
            finish = True
            end1 = font.render("Вы проиграли,нажмите R,что-бы начать завново",True,(200,0,0))
            window.blit(end1,(250,300))

        if len(monsters) < 6:
            ufo = Enemy('ufo.png', randint(0,750), 1, 1)
            monsters.add(ufo)

        if len(asteroid) < 1:
            ast = Enemy('asteroid.png', randint(0,750), 1, 2)
            asteroid.add(ast)

    

    


    if score >= 31:
        win = font.render("Ты победил",True,(255,0,0))
        window.blit(win, [250,300])
        finish = True
        
			
			


    if lost >= 10:
        win = font.render("Вы проиграли,нажмите R,что-бы начать завново",True,(255,0,0))
        window.blit(win, [250,300])
        finish = True
    clock.tick(FPS)
    display.update()

