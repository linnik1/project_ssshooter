import os
import pygame

pygame.init()
size = width, height = 1000, 750
screen = pygame.display.set_mode(size)

LMOVE = 'влево'
RMOVE = 'вправо'
STOP = 'стоять'
LBLAST = 'выстрел'
m_or_n = STOP
have_monsters = False
nowwindow = 'none'
mon = 0
score = 0
wx = 480
timeformon = 0
vr = 12
f = pygame.font.Font(None, 30)
txtscore = f.render('счёт:', True, (250, 250, 250))
game_go = False
game_over = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == 'yes':
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group()
one_line = pygame.sprite.Group()
just_menu = pygame.sprite.Group()
menu_staff = pygame.sprite.Group()
bullets = pygame.sprite.Group()
monsters = pygame.sprite.Group()

background = pygame.sprite.Sprite()
background.image = load_image("newbg.png")
background.rect = background.image.get_rect()
all_sprites.add(background)
background.rect.x = 0
background.rect.y = 0

theline = pygame.sprite.Sprite()
theline.image = load_image("line.png")
theline.rect = background.image.get_rect()
one_line.add(theline)
theline.rect.x = 0
theline.rect.y = 520

arr1 = pygame.sprite.Sprite()
arr1.image = load_image("arr1.png", "yes")
arr1.rect = background.image.get_rect()
arr1.rect.x = 20
arr1.rect.y = 695

arr2 = pygame.sprite.Sprite()
arr2.image = load_image("arr2.png", "yes")
arr2.rect = background.image.get_rect()
arr2.rect.x = 940
arr2.rect.y = 695

space = pygame.sprite.Sprite()
space.image = load_image("space.png")
space.rect = background.image.get_rect()
space.rect.x = 290
space.rect.y = 695

spship = pygame.sprite.Sprite()
spship.image = load_image("newspship.png", "yes")
spship.rect = background.image.get_rect()
all_sprites.add(spship)
spship.rect.x = wx
spship.rect.y = 575

menu = pygame.sprite.Sprite()
menu.image = load_image("newmen.png")
menu.rect = background.image.get_rect()
just_menu.add(menu)
menu.rect.x = 0
menu.rect.y = 0

menuwhat = pygame.sprite.Sprite()
menuwhat.image = load_image("windoo.png")
menuwhat.rect = background.image.get_rect()
menuwhat.rect.x = 260
menuwhat.rect.y = 200

menuwho = pygame.sprite.Sprite()
menuwho.image = load_image("windoo2.png")
menuwho.rect = background.image.get_rect()
menuwho.rect.x = 260
menuwho.rect.y = 200

end = pygame.sprite.Sprite()
end.image = load_image("windoo3.png")
end.rect = background.image.get_rect()
end.rect.x = 260
end.rect.y = 200


class Bullet(pygame.sprite.Sprite):
    image = load_image('dangan.png', 'yes')

    def __init__(self, group, where_sship_x):
        super().__init__(group)
        self.height = 560
        self.bullet = Bullet.image
        self.rect = self.bullet.get_rect()
        self.rect.x = where_sship_x + 30
        self.rect.y = self.height

    def update(self, vr=0):
        if self.height <= 0:
            self.kill()
        else:
            self.rect = self.rect.move(0, -vr)
            self.height -= vr


class Monster(pygame.sprite.Sprite):
    image1 = load_image('newmon1.png', 'yes')
    image2 = load_image('newmon2.png', 'yes')
    image4 = load_image('newmon4.png', 'yes')
    image5 = load_image('newmon5.png', 'yes')

    def __init__(self, group, a, b):
        super().__init__(group)
        global mon
        mon += 1
        self.phase = 1
        self.x = 100 + (a * 100)
        self.y = 10 + (b * 100)
        if b == 0:
            self.image = Monster.image5
        elif b == 1:
            self.image = Monster.image4
        elif b == 2:
            self.image = Monster.image2
        elif b == 3:
            self.image = Monster.image1
        else:
            self.image = Monster.image1
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if timeformon % 150 == 0:
            if self.phase == 1 or self.phase == 2:
                self.x += 30
            elif self.phase == 3 or self.phase == 6:
                self.y += 30
            elif self.phase == 4 or self.phase == 5:
                self.x -= 30
            self.phase += 1
            if self.phase > 6:
                self.phase -= 6
            self.rect.x = self.x
            self.rect.y = self.y
        if pygame.sprite.spritecollideany(self, bullets):
            global mon
            mon -= 1
            global score
            score += 100
            self.kill()
        if pygame.sprite.spritecollideany(self, one_line):
            global game_over
            game_over = True


clock = pygame.time.Clock()
pygame.display.set_caption('Super Space Shooter')
plus_x = pygame.USEREVENT + 25
pygame.time.set_timer(plus_x, 10)
speed = 60

running = True
while running:
    while not game_go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 95 <= x <= 494 and 435 <= y <= 509 and nowwindow == 'none':
                    game_go = True
                elif 345 <= x and 545 <= y and nowwindow == 'none':
                    nowwindow = 'menuwho'
                    menu_staff.add(menuwho)
                elif nowwindow == 'menuwho' and 695 <= x <= 759 and 200 <= y <= 264:
                    menuwho.kill()
                    nowwindow = 'none'
                elif 95 <= x <= 244 and 545 <= y <= 694 and nowwindow == 'none':
                    nowwindow = 'menuwhat'
                    menu_staff.add(menuwhat)
                elif nowwindow == 'menuwhat' and 695 <= x <= 759 and 200 <= y <= 264:
                    menuwhat.kill()
                    nowwindow = 'none'
        just_menu.draw(screen)
        if nowwindow != 'none':
            surf = pygame.Surface((1000, 750))
            surf.fill((0, 0, 0))
            surf.set_alpha(150)
            screen.blit(surf, (0, 0))
        menu_staff.draw(screen)
        pygame.display.flip()
    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 366 <= x <= 637 and 474 <= y <= 517:
                    game_go = False
                    game_over = True

        one_line.add(end)
        all_sprites.draw(screen)
        bullets.draw(screen)
        monsters.draw(screen)
        one_line.draw(screen)
        screen.blit(txtscore, (10, 8))
        txtnowscore = f.render(str(score).rjust(7, '0'), True, (250, 250, 250))
        screen.blit(txtnowscore, (10, 35))
        txtmenuscore = f.render(str(score), True, (250, 250, 250))
        screen.blit(txtmenuscore, (355, 372))

        pygame.display.flip()
    else:
        if not have_monsters:
            speed += 20
            for i in range(1, 7):
                for ii in range(4):
                    Monster(monsters, i, ii)
            have_monsters = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                lll = event.key == pygame.K_LEFT or event.key == pygame.K_a
                rrr = event.key == pygame.K_RIGHT or event.key == pygame.K_d
                if rrr and m_or_n == LMOVE or lll and m_or_n == RMOVE:
                    pass
                elif rrr or lll:
                    m_or_n = STOP
                if rrr:
                    arr2.kill()
                if lll:
                    arr1.kill()
                if event.key == pygame.K_SPACE:
                    space.kill()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    m_or_n = RMOVE
                    all_sprites.add(arr2)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    m_or_n = LMOVE
                    all_sprites.add(arr1)
                if event.key == pygame.K_SPACE:
                    Bullet(bullets, wx)
                    all_sprites.add(space)
            if m_or_n == LMOVE and wx >= 200:
                wx -= 2
                spship.rect.x = wx
            elif m_or_n == RMOVE and wx <= 760:
                wx += 2
                spship.rect.x = wx
        if mon == 0:
            have_monsters = False
        timeformon += 1
        all_sprites.draw(screen)
        one_line.draw(screen)
        monsters.update()
        monsters.draw(screen)
        bullets.update(vr)
        bullets.draw(screen)
        hits = pygame.sprite.groupcollide(monsters, bullets, True, True)
        for i in hits:
            score += 10
            mon -= 1
            speed += 4
        screen.blit(txtscore, (10, 8))
        txtnowscore = f.render(str(score).rjust(7, '0'), True, (250, 250, 250))
        screen.blit(txtnowscore, (10, 35))
        pygame.display.flip()
        clock.tick(speed)
if pygame.event.wait().type == pygame.QUIT:
    pygame.quit()
