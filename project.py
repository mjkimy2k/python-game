import pygame # pygame 선언
import random
import sys

# 게임 초기화
pygame.init() # pygame 기화

# 화면 설정
screen_width = 480
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pipe Dodger")

#이미지 파일 준비
bird_1 = pygame.image.load('bird1.jpg')
bird_2 = pygame.image.load('bird2.jpg')
bird_3 = pygame.image.load('bird3.jpg')
chicken_leg1 = pygame.image.load('chicken_leg1.jpg')
chicken_leg2 = pygame.image.load('chicken_leg2.jpg')
chicken_leg3 = pygame.image.load('chicken_leg3.jpg')
chicken_leg4 = pygame.image.load('chicken_leg4.jpg')
background_noon = pygame.image.load("noon.jpg")
background_night = pygame.image.load("night.jpg")
pillar_Up_noon = pygame.image.load("pillarUp_noon.jpg")
pillar_Down_noon = pygame.image.load("pillarDown_noon.jpg")
pillar_Up_night = pygame.image.load("pillarUp_night.jpg")
pillar_Down_night = pygame.image.load("pillarDown_night.jpg")
tile = pygame.image.load("tile.jpg")

#이미지 크기 설정
bird_1 = pygame.transform.scale(bird_1,(60,60))
bird_2 = pygame.transform.scale(bird_2,(60,60))  
bird_3 = pygame.transform.scale(bird_3,(60,60))
chicken_leg1 = pygame.transform.scale(chicken_leg1,(25,25))
chicken_leg2 = pygame.transform.scale(chicken_leg2,(25,25))
chicken_leg3 = pygame.transform.scale(chicken_leg3,(50,50))
chicken_leg4 = pygame.transform.scale(chicken_leg4,(50,50))
background_noon = pygame.transform.scale(background_noon,(480,600))
background_night = pygame.transform.scale(background_night,(480,600))
pillar_Up_noon = pygame.transform.scale(pillar_Up_noon,(55,600))
pillar_Down_noon = pygame.transform.scale(pillar_Down_noon,(55,600))
pillar_Up_night = pygame.transform.scale(pillar_Up_night,(55,600))
pillar_Down_night = pygame.transform.scale(pillar_Down_night,(55,600))
tile = pygame.transform.scale(tile,(480,80))

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)

# 게임 폰트
font = pygame.font.SysFont(None, 35)
big_font = pygame.font.SysFont(None, 72)

# 변수 설정
picture_frame = 20
movecount = 0
bird_move = [bird_1, bird_2, bird_1, bird_3]
pipes = []
pipe_frequency = 80
items = []
item_frequency = 240
time = 0
backgound_frequency = 2000
score = 0
Hunger_frequency = 280
hunger_count = 6
chicken_leg = [chicken_leg1, chicken_leg2, chicken_leg1, chicken_leg2]
frame_count = 0
game_over = False

# 게임의 클래스 및 함수 정의
# 새 클래스 정의
class Bird:   
    def __init__(self):
        self.x = 50
        self.y = 200
        self.width = 25
        self.length = 20
        self.gravity = 0.25
        self.lift = -7
        self.velocity = -0.25

    def show(self):
        global frame_count, movecount
        if not game_over:
            screen.blit(bird_move[movecount],(self.x - 30, self.y - 30)) # 새 애니메이션
            if frame_count % picture_frame == 0: 
                movecount +=1
                if movecount > 3:
                    movecount = 0            

    def update(self):
        # 중력 구현
        self.velocity += self.gravity
        self.y += self.velocity

        # 새가 화면을 벗어나지 못하게 한다.
        if self.y > screen_height:
            self.y = screen_height
            self.velocity = 0
        elif self.y < 0:
            self.y = 0
            self.velocity = 0

    def up(self):
        # 새 점프 구현
        self.velocity += self.lift

# 파이프 클래스 정의
class Pipe:
    def __init__(self):
        self.top = random.randint(-500, -250)
        self.bottom = self.top + 750
        self.x = screen_width
        self.w = 55
        self.speed = 5

    def show(self):
        if time % 2 == 0:
            screen.blit(pillar_Up_noon, (self.x, self.top))
            screen.blit(pillar_Down_noon, (self.x, self.bottom))
        if time % 2 == 1:
            screen.blit(pillar_Up_night, (self.x, self.top))
            screen.blit(pillar_Down_night, (self.x, self.bottom))       

    def update(self):
        self.x -= self.speed

    def offscreen(self):
        return self.x < -self.w    

# 아이템 클래스 정의
class Item:
    def __init__(self):
        self.x = screen_width + 210
        self.y = random.randint(200, 400)
        self.size = 20
        self.speed = 5
        self.color = [chicken_leg3, chicken_leg4,chicken_leg3,chicken_leg4,chicken_leg3]

    def show(self):
        global frame_count, movecount, picture_frame
        screen.blit(self.color[movecount],(self.x - 30, self.y - 30))

    def update(self):
        self.x -= self.speed

    def offscreen(self):
        return self.x < -self.size*2

# 배경 함수
def background(x,time):
    if time % 2 == 0:
        screen.blit(background_noon, (0,0))
        screen.blit(tile, (0,x))
    if time % 2 == 1:
        screen.blit(background_night, (0,0))
        screen.blit(tile, (0,x))

# 아이콘 함수 정의
def board(x, y):
    global movecount
    score_text = font.render(f"Score: {score}", True, white)
    hunger_text = font.render("Hunger: ", True, white)
    screen.blit(score_text, (x, y))
    screen.blit(hunger_text, (x, y+30))
    chicken = chicken_leg[movecount] 
    for i in range(hunger_count):
            screen.blit(chicken, (110 + i * 22, 43))

# 충돌 함수 정의
def is_pipe_collision(bird, pipes):
    for pipe in pipes:
        if bird.x + bird.width > pipe.x and bird.x - bird.width < pipe.x + pipe.w:
            if bird.y - bird.length < pipe.top + 600 or bird.y + bird.length > pipe.bottom:
                return True
    return False

def is_item_collision(bird, items):
    for item in items:
        if (bird.x - item.x) ** 2 + (bird.y - item.y) ** 2 <= (bird.width + item.size)**2 + (bird.length + item.size)**2:
            return True
    return False

# 메인 메뉴 표시
def main_menu():
    menu = True
    title = big_font.render("Pipe Dodger", True, black)
    start_text = font.render("Press SPACE to Start", True, black)
    title_rect = title.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False        
        background(520,time)
        bird.show()
        screen.blit(title, title_rect)
        screen.blit(start_text, start_rect)
        pygame.display.update()
        pygame.time.Clock().tick(5)

# 게임 오버 화면
def game_over_screen():
    screen.fill(white)
    game_over_text = big_font.render("Game Over", True, black)
    restart_text = font.render("Press SPACE to Restart", True, black)
    score_text = font.render(f"Score: {score}", True, black)
    text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
    score_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 ))
    background(520,time)
    screen.blit(game_over_text, text_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(score_text, score_rect )   
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# 메인 게임 루프
def main(): 
    global score,hunger_count,game_over,movecount,frame_count,bird_move,time,chicken_leg,items,pipes,bird

    # Class Bird 사용을 위해 변수 지정
    bird = Bird()
    
    # 화면에 메인화면 표시
    main_menu()
        
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    bird.up()

        # 화면에 배경표시
        background(520,time)      
        if frame_count % backgound_frequency == 1000:
            time+=1
       
       # 화면에 파이브 설치 및 제거
        if frame_count % pipe_frequency == 0:
            pipes.append(Pipe())
        for pipe in pipes:
            pipe.show()
            pipe.update()
            if pipe.offscreen():
                pipes.remove(pipe)
            if pipe.x + pipe.w + bird.width == bird.x:
                score += 1

        # 화면에 아이템 설치 및 제거
        if frame_count % item_frequency == 0:
            items.append(Item())
        for item in items:
            item.show()
            item.update()
            if item.offscreen():
                items.remove(item)

        # 화면에 점수 및 배고픔 표시
        board(10, 10)
        if frame_count % Hunger_frequency == 0:
            hunger_count -= 1

        # 화면에 새 표시
        bird.show()
        bird.update()

        # 충동시 게임 오버
        if is_pipe_collision(bird, pipes) or hunger_count == 0:
                game_over = True
         
        # 아이템과 접촉시 먹은 아이템 삭제 및 배고픔 표시+1
        if is_item_collision(bird, items):
            items.clear()
            hunger_count = min(hunger_count + 1, 5)

        # 화면 업데이트 및 프레임 설정
        pygame.display.update()
        pygame.time.Clock().tick(60)
        frame_count += 1
        
        # 게임오버 초기화
        if game_over:
            game_over_screen()
            bird = Bird()
            pipes = []
            items = []
            score = 0
            time = 0
            hunger_count = 6
            frame_count = 0
            game_over = False

# 게임 시작
if __name__ == "__main__":
    main()
