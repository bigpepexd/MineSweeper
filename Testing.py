import pygame, sys, random, math


class Explode(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.boom = pygame.mixer.Sound('BombSound.wav')

    def left_clicked(self):
        length = 1000
        blockx = 0
        blocky = 0
        if pygame.sprite.groupcollide(cursor_group, flag_group, dokilla=False, dokillb=False):
            pass
        elif pygame.sprite.groupcollide(cursor_group, block_group, dokilla=False, dokillb=False):
            pygame.sprite.groupcollide(cursor_group, block_group, dokilla=False, dokillb=True)
        if pygame.sprite.groupcollide(cursor_group, bomb_group, dokilla=False, dokillb=False):
            for entity in block_group:
                pygame.sprite.groupcollide(bomb_group, block_group, dokilla=False, dokillb=True)
            self.boom.play()

    def right_clicked(self):
        length = 1000
        blockx = 0
        blocky = 0
        if pygame.sprite.groupcollide(flag_group, cursor_group, dokilla=False, dokillb=False):
            pygame.sprite.groupcollide(flag_group, cursor_group, dokilla=True, dokillb=False)
        elif pygame.sprite.groupcollide(cursor_group, block_group, dokilla=False, dokillb=False):
            for cursor in cursor_group:
                for block in block_group:
                    distance = math.hypot(block.rect.centerx - cursor.rect.centerx, block.rect.centery - cursor.rect.centery)
                    if distance < length:
                        length = distance
                        blockx = block.rect.centerx
                        blocky = block.rect.centery
                new_flag = Block('FlagBlock.png', blockx, blocky)
                flag_group.add(new_flag)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture_path), (26, 26))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    # try and use this for updating blocks
    def flag_update(self):
        self.image = pygame.transform.scale(pygame.image.load('FlagBlock.png'), (26, 26))


class Empty(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture_path), (32, 32))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


class Block(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture_path), (32, 32))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


class WinFlag(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture_path), (400, 400))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


class Cursor(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.image = pygame.transform.scale(pygame.image.load(picture_path), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = pygame.mouse.get_pos()
        self.rect = self.rect.inflate(-19.999, -19.999)

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()


def click_or_no_click():
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            explode.left_clicked()
        elif event.button == 3:
            explode.right_clicked()
    # elif event.type == pygame.KEYDOWN:
    #     if event.key == pygame.K_r:
    #         main()


def check_win():
    flag_nums = 0
    for bomb in bomb_group:
        for flag in flag_group:
            col = pygame.sprite.collide_rect(bomb, flag)
            if col == True:
                flag_nums += 1
    if flag_nums == num_of_bombs:
        win = WinFlag('SweeperWin.png', 420, 420)
        win_flag_group.add(win)
        win_flag_group.draw(screen)


pygame.init()
clock = pygame.time.Clock()

# creates screen with dimensions and colors
GRAY = (169, 169, 169)
screen_width = 830
screen_height = 850
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(GRAY)

# eventually will help make the bomb explosion be animated and make a sound when clicked
explode = Explode('SweeperBomb_1.png')

# creates group to add sprites to as well as useful variables for groups
win_flag_group = pygame.sprite.Group()
bomb_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
empty_group = pygame.sprite.Group()
nums_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
grid_width = 200
grid_height = 200
space_between_sprites = 30
mine_position = 0
num_of_bombs = 49
random_num = random.sample(range(256), k=num_of_bombs)

# creates block grid with random mine set underneath
for block in range(256):
    new_block = Block('SweeperBlock.png', grid_width, grid_height)
    grid_width += space_between_sprites
    block_group.add(new_block)
    if grid_width >= 200 + space_between_sprites * 16:
        grid_width = 200
        grid_height += space_between_sprites

grid_width = 200
grid_height = 200

for bomb in range(256):

    if grid_width >= 200 + space_between_sprites * 16:
        grid_width = 200
        grid_height += space_between_sprites
    mine_position += 1

    new_empty = Empty('SweeperEmpty.png', grid_width, grid_height)
    empty_group.add(new_empty)

    for i in random_num:
        if i == mine_position:
            new_mine = Bomb('SweeperBomb.png', grid_width, grid_height)
            bomb_group.add(new_mine)

    grid_width += space_between_sprites

counter = 0
grid_width = 200
grid_height = 200

# mostly works but need to make the way they spawn better
for empty in empty_group:

    if grid_width >= 200 + space_between_sprites * 16:
        grid_width = 200
        grid_height += space_between_sprites

    for bomb in bomb_group:

        distance = math.hypot(bomb.rect.centerx - empty.rect.centerx, bomb.rect.centery - empty.rect.centery)
        if 28 <= distance <= 48:
            counter += 1
    if 0 < counter <= 8:
        new_num = Empty(f'Sweeper{counter}.png', grid_width, grid_height)
        nums_group.add(new_num)
    counter = 0

    grid_width += space_between_sprites

pygame.sprite.groupcollide(nums_group, bomb_group, dokilla=True, dokillb=False)

# shovel cursor
cursor = Cursor('CursorShovel.png')
cursor_group = pygame.sprite.Group()
cursor_group.add(cursor)

pygame.mouse.set_visible(False)

background = pygame.image.load('GrayBackground.png')

# draws game board
while True:
    l_click = False
    r_click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        click_or_no_click()

        pygame.display.flip()
        screen.blit(background, (0, 0))

        empty_group.draw(screen)
        nums_group.draw(screen)
        bomb_group.draw(screen)
        block_group.draw(screen)
        flag_group.draw(screen)
        check_win()
        cursor_group.draw(screen)
        cursor_group.update()
        clock.tick(60)