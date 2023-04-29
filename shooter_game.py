#Создай собственный Шутер!

from pygame import*
from random import randint
font.init()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shyter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
clock = time.Clock()
fps = 90
game = True
score = 0
goal = 10
max_lost = 3
finish = False

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def  __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15,12,15)
        bullets.add(bullet)

lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(25, 675)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()


font1 = font.SysFont("Arial", 36)
text_loser = font1.render('Пропущено: ' + str(lost),1,(255,255,255))
text_chet = font1.render('Счёт: ' + str(score), 1,(255,255,255))
win = font1.render('Выигрышь', 1,(255,255,255))
lose = font1.render('Проигрышь', 1,(255,255,255))

monsters = sprite.Group()
for i in range(6):
    m = Enemy('ufo.png', randint(25,675), 0, randint(1,5), 70, 35)
    monsters.add(m)
rocket = Player('rocket.png', 350, 400, 10, 60, 90)



while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()
    if not finish:
        window.blit(background,(0,0))
        rocket.reset()
        rocket.update()
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)
        monsters.update()
        text_loser = font1.render('Пропущено: ' + str(lost),1,(255,255,255))
        window.blit(text_loser, (10,20))
        text_chet = font1.render('Счёт: ' + str(score), 1,(255,255,255))
        window.blit(text_chet, (10,50))
    collides = sprite.groupcollide(monsters,bullets,True,True)
    for c in collides:
        score = score + 1 
        monster = Enemy('ufo.png', randint(25,675), 0, randint(1,5), 70, 35)
        monsters.add(monster)

    if sprite.spritecollide(rocket,monsters,False) or lost >= max_lost:
        finish = True
        window.blit(lose,(200,200))

    if score >= goal:
        finish = True
        window.blit(win,(200,200))    


    display.update()
    clock.tick(fps)