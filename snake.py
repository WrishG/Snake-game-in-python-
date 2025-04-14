import pygame, sys,random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/nom-nom-nom_gPJiWn4.mp3')
        self.crash = pygame.mixer.Sound('Sound/vine-boom.mp3')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index,block in enumerate(self.body):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            if index == 0:
               screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1]-block
                next_block = self.body[index-1]-block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)


    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0]+self.direction)
        self.body = body_copy[:]
    def add_block(self):
        self.new_block = True
        body_copy = self.body[:]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
    def play_crunch_sound(self):
        self.crunch_sound.play()



class FRUIT :

    def __init__(self):
        self.randomise()
    def draw_fruit(self):
        fruit_rect= pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y*cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)

    def randomise(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.apple_counter = 0
        self.high_score = 0
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()


    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_high_score()
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomise()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.apple_counter += 1
            if self.apple_counter % 10 == 0:
                pygame.time.set_timer(SCREEN_UPDATE, 120)

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomise()
        if self.apple_counter > self.high_score:
            self.high_score = self.apple_counter

    def draw_high_score(self):
        high_score_text = "High Score: " + str(self.high_score)
        high_score_surface = game_font.render(high_score_text, True, (255,255, 255))
        screen.blit(high_score_surface, (10, 10))

    def play_crash_sound(self):
        self.snake.crash.play()
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:

            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:

                self.game_over()
    def bgm(self):
        self.bgm.play()

    def game_over(self):
        self.snake.reset()



    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (0,0,0))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (0,0,0), bg_rect, 2)

    def draw_credit(self):
        cr_text = "Made by : Wrish & team"
        cr_surface = cr_font.render(cr_text,True,(255,255,255))
        cr_x = 60
        cr_y = int(cell_size * cell_number - 40)
        cr_rect = cr_surface.get_rect(bottomleft=(cr_x, cr_y))
        screen.blit(cr_surface, cr_rect)

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number*cell_size,cell_size*cell_number))
bg_img = pygame.image.load("grass (1).jpg")
bgm = pygame.mixer.Sound('Sound/videoplayback.mp3')
bgm.play(-1)

clock = pygame.time.Clock()
apple = pygame.image.load("apple2-removebg-preview_11zon (1).png").convert_alpha()
main_game = MAIN()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,200)
game_font = pygame.font.Font('joystix monospace.otf', 25)
cr_font = pygame.font.Font('Endgame DEMO.otf',15)
pygame.display.set_caption("Wrish's snake Game")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                 main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                 main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                 main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                 main_game.snake.direction = Vector2(-1,0)

    screen.blit(bg_img,(0,0))
    main_game.draw_score()
    main_game.draw_elements()
    main_game.draw_credit()
    pygame.display.update()
    clock.tick(120)
