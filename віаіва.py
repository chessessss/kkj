from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.SysFont("Modern", 70,)
win = font1.render('Ти виграв!!', True, (0, 255, 0))
lose = font1.render('Ти програв!!', True, (180, 0, 0))
font2 = font.SysFont("Modern", 32)

# фонова музика
mixer.init()
mixer.music.load('')
mixer.music.play()
fire_sound = mixer.Sound('')
 
# нам потрібні такі картинки:
img_car1 = ""  # фон гри
img_car2 = ""  # герой
img_back = ""

score = 0  # збито кораблів
life = 1
goal = 50


class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Клас гравця - автомобіль
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed


# Клас перешкоди
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            score = score + 1

    
win_width = 700
win_height = 500
display.set_caption("")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


car1 = Player(img_car1, 5, win_height - 100, 70, 100, 10)

car2 = sprite.Group()
for i in range(1, 6):
    car2 = Enemy(img_car2, randint(
        80, win_width - 80), -40, 80, 70, randint(1, 5))
    car2.add(car2)


# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False
# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна

bx = 0
while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False


    # сама гра: дії спрайтів, перевірка правил гри, перемальовка
    if not finish:
        # оновлюємо фон
        window.blit(background, (bx, 0))
        window.blit(background, (bx + 700, 0))

        # рухи спрайтів
        car1.update()
        car2.update()
        
 
        #оновлюємо їх у новому місці при кожній ітерації циклу
        car1.reset()
        car2.draw(window)
        
        bx -= 1 
        if bx == -700:
            bx = 0

        if sprite.spritecollide(car1, car2, False):
            sprite.spritecollide(car2, car1, True)
            life = life -1

        #програш
        if life == 0:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))


        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        # пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

    else:
        finish = False
        score = 0
        lost = 0
        life = 1
        for m in car2:
            m.kill()
     
        time.delay(3000)
        for i in range(1, 6):
            car2 = Enemy(img_car2, randint(80, win_width - 80), -40, 80, 70, randint(1, 5))
            car2.add(car2) 

    # цикл спрацьовує кожні 0.05 секунд
    time.delay(50)