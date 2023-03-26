#Создай собственный Шутер!

from pygame import *
from random import *



speed = 5
game = True

lost = 0
score = 0

inw_back = 'galaxy.jpg'
inw_bullet = 'bullet.png'
inw_hero = 'rocket.png'
inw_enemy = 'ufo.png'
inw_asteroid = 'asteroid.png'

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

goal = 11
max_lost = 5
life_num = 5


font.init()
font2 = font.SysFont("Times New Roman", 36)


window = display.set_mode((700, 500))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(inw_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(0, win_height - 30)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
            
class Asteroids(GameSprite):
     def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(0, win_height - 30)
            self.rect.y = 0
            

win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(inw_back), (win_width, win_height))
ship = Player(inw_hero, 5, win_height-99,80,100, 10)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 6):
    monster = Enemy(inw_enemy, randint(0, win_width - 30), -40,60,60, randint(1, 3))
    monsters.add(monster)    
for i in range(1, 3):
    asteroid = Asteroids(inw_asteroid, randint(0, win_width - 30), -40, 60, 60, randint(1, 6))
    asteroids.add(asteroid)
finish = False
win = font2.render('YOU WIN!', True, (0, 255, 0))
lose = font2.render('YOU LOSE!', True, (255, 0, 0))
timer = font2.render('Подождите, идёт перезарядка...', True, (255, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #fire_sound.play()
                ship.fire()
            
    if not finish:
        window.blit(background, (0,0))
        text = font2.render("Cчёт:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(inw_enemy, randint(80, win_width - 80), -40, 60, 60, randint(1, 6))
            monsters.add(monster)
        if life_num != 0 or lost < max_lost:
            finish = False



        if  lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score == goal:
            finish = True 
            window.blit(win, (200, 200))

        if  sprite.spritecollide(ship, monsters, False) or  sprite.spritecollide(ship, asteroids, False):
            life_num = life_num - 1

        if finish == True:
            mixer.music.stop()

            
        ship.reset()
        ship.update()
        monsters.update()
        asteroids.update()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        bullets.update()
        display.update()
        

# sprites_list = sprite.spritecollide(ship, monsters, False)
# sprites_list1 = sprite.groupcolide(monsters, bullets, True, True)
    time.delay(50)
