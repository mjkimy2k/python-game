import pygame  # pygame 모듈을 가져옴
import random  # 랜덤 모듈을 가져옴
import sys  # 시스템 모듈을 가져옴

# 게임 초기화
pygame.init()  # pygame 초기화

# 화면 설정
screen_width = 480  # 화면 너비 설정
screen_height = 600  # 화면 높이 설정
screen = pygame.display.set_mode((screen_width, screen_height))  # 화면 크기 설정
pygame.display.set_caption("Pipe Dodger")  # 창 제목 설정

# 이미지 파일 이름 및 크기 정보 리스트
images_info = [
    ('bird1.jpg', (60, 60)), 
    ('bird2.jpg', (60, 60)), 
    ('bird3.jpg', (60, 60)),
    ('chicken_leg1.jpg', (25, 25)), 
    ('chicken_leg2.jpg', (25, 25)), 
    ('chicken_leg3.jpg', (50, 50)), 
    ('chicken_leg4.jpg', (50, 50)),
    ('noon.jpg', (480, 600)), 
    ('night.jpg', (480, 600)), 
    ('pillarUp_noon.jpg', (55, 600)), 
    ('pillarDown_noon.jpg', (55, 600)),
    ('pillarUp_night.jpg', (55, 600)), 
    ('pillarDown_night.jpg', (55, 600)), 
    ('tile.jpg', (480, 80))
]

# 이미지 로드 및 크기 조정
loaded_images = [pygame.transform.scale(pygame.image.load(filename), size) for filename, size in images_info]

# 개별 변수에 이미지 할당
(bird_1, bird_2, bird_3, chicken_leg1, chicken_leg2, 
 chicken_leg3, chicken_leg4, background_noon, background_night, 
 pillar_Up_noon, pillar_Down_noon, pillar_Up_night, 
 pillar_Down_night, tile) = loaded_images

# 색상 정의
white = (255, 255, 255)  # 흰색 RGB 값
black = (0, 0, 0)  # 검은색 RGB 값

# 게임 폰트
font = pygame.font.SysFont(None, 35)  # 기본 폰트, 크기 35
big_font = pygame.font.SysFont(None, 72)  # 기본 폰트, 크기 72

# 변수 설정
picture_frequency = 20  # 새 애니메이션 프레임 교체 주기
movecount = 0  # 애니메이션 리스트의 현재 인덱스
bird_move = [bird_1, bird_2, bird_1, bird_3]  # 새 애니메이션 프레임 리스트
pipes = []  # 파이프 객체를 저장할 리스트
pipe_frequency = 80  # 파이프 생성 주기
items = []  # 아이템 객체를 저장할 리스트
item_frequency = 240  # 아이템 생성 주기
time = 0  # 게임 진행 시간
backgound_frequency = 2000  # 배경 변경 주기
score = 0  # 게임 점수
Hunger_frequency = 280  # 배고픔 감소 주기
hunger_count = 6  # 초기 배고픔 지수
chicken_leg = [chicken_leg1, chicken_leg2, chicken_leg1, chicken_leg2]  # 아이템 애니메이션 리스트
frame_count = 0  # 게임 프레임 카운트
game_over = False  # 게임 오버 상태

# 게임의 클래스 및 함수 정의

# 새 클래스 정의
class Bird:   
    def __init__(self):
        self.x = 50  # 새의 초기 X 위치
        self.y = 200  # 새의 초기 Y 위치
        self.width = 25  # 새의 너비
        self.length = 20  # 새의 길이
        self.gravity = 0.25  # 중력 값
        self.lift = -7  # 상승력 값
        self.velocity = -0.25  # 초기 속도

    def show(self):
        global frame_count, movecount
        if not game_over:
            # 현재 애니메이션 프레임을 화면에 그림
            screen.blit(bird_move[movecount], (self.x - 30, self.y - 30)) 
            # 애니메이션 프레임 업데이트
            if frame_count % picture_frequency == 0: 
                movecount += 1
                if movecount > 3:
                    movecount = 0            

    def update(self):
        # 중력 적용
        self.velocity += self.gravity
        self.y += self.velocity

        # 새가 화면을 벗어나지 않게 위치 조정
        if self.y > screen_height:
            self.y = screen_height
            self.velocity = 0
        elif self.y < 0:
            self.y = 0
            self.velocity = 0

    def up(self):
        # 새가 위로 점프하도록 속도 변경
        self.velocity += self.lift

# 파이프 클래스 정의
class Pipe:
    def __init__(self):
        self.top = random.randint(-500, -250)  # 파이프의 상단 위치 랜덤 설정
        self.bottom = self.top + 750  # 파이프의 하단 위치 설정
        self.x = screen_width  # 파이프의 초기 X 위치
        self.w = 55  # 파이프의 너비
        self.speed = 5  # 파이프의 이동 속도

    def show(self):
        # 현재 시간에 따라 낮 또는 밤 배경의 파이프를 화면에 그림
        if time % 2 == 0:
            screen.blit(pillar_Up_noon, (self.x, self.top))
            screen.blit(pillar_Down_noon, (self.x, self.bottom))
        else:
            screen.blit(pillar_Up_night, (self.x, self.top))
            screen.blit(pillar_Down_night, (self.x, self.bottom))       

    def update(self):
        # 파이프가 왼쪽으로 이동
        self.x -= self.speed

    def offscreen(self):
        # 파이프가 화면을 벗어났는지 확인
        return self.x < -self.w    

# 아이템 클래스 정의
class Item:
    def __init__(self):
        self.x = screen_width + 210  # 아이템의 초기 X 위치
        self.y = random.randint(200, 400)  # 아이템의 Y 위치 랜덤 설정
        self.size = 20  # 아이템의 크기
        self.speed = 5  # 아이템의 이동 속도
        self.color = [chicken_leg3, chicken_leg4, chicken_leg3, chicken_leg4, chicken_leg3]  # 아이템 애니메이션 리스트

    def show(self):
        global frame_count, movecount, picture_frequency
        # 현재 애니메이션 프레임을 화면에 그림
        screen.blit(self.color[movecount], (self.x - 30, self.y - 30))

    def update(self):
        # 아이템이 왼쪽으로 이동
        self.x -= self.speed

    def offscreen(self):
        # 아이템이 화면을 벗어났는지 확인
        return self.x < -self.size * 2

# 배경 함수
def background(x, time):
    # 현재 시간에 따라 낮 또는 밤 배경을 화면에 그림
    if time % 2 == 0:
        screen.blit(background_noon, (0, 0))
        screen.blit(tile, (0, x))
    else:
        screen.blit(background_night, (0, 0))
        screen.blit(tile, (0, x))

# 점수와 배고픔을 화면에 표시하는 함수
def board(x, y):
    global movecount
    score_text = font.render(f"Score: {score}", True, white)  # 점수 텍스트 생성
    hunger_text = font.render("Hunger: ", True, white)  # 배고픔 텍스트 생성
    screen.blit(score_text, (x, y))  # 점수 텍스트 화면에 그림
    screen.blit(hunger_text, (x, y + 30))  # 배고픔 텍스트 화면에 그림
    chicken = chicken_leg[movecount]  # 현재 애니메이션 프레임의 아이템
    for i in range(hunger_count):
        screen.blit(chicken, (110 + i * 22, 43))  # 배고픔 지수를 아이템으로 표시

# 새와 파이프 충돌 여부 확인 함수
def is_pipe_collision(bird, pipes):
    for pipe in pipes:
        # 새가 파이프와 충돌했는지 확인
        if bird.x + bird.width > pipe.x and bird.x - bird.width < pipe.x + pipe.w:
            if bird.y - bird.length < pipe.top + 600 or bird.y + bird.length > pipe.bottom:
                return True
    return False

# 새와 아이템 충돌 여부 확인 함수
def is_item_collision(bird, items):
    for item in items:
        # 새가 아이템과 충돌했는지 확인
        if (bird.x - item.x) ** 2 + (bird.y - item.y) ** 2 <= (bird.width + item.size)**2 + (bird.length + item.size)**2:
            return True
    return False

def render_texts(text_info_list):
    for text, font, color, pos in text_info_list:
        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=pos)
        screen.blit(rendered_text, text_rect)

def main_menu():
    menu = True
    # 텍스트 정보 리스트
    texts = [
        ("Pipe Dodger", big_font, black, (screen_width // 2, screen_height // 2 - 50)),
        ("Press SPACE to Start", font, black, (screen_width // 2, screen_height // 2 + 20))
    ]

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False  # 스페이스바를 누르면 메뉴 종료

        background(520, time)  # 배경 표시
        bird.show()  # 새 표시
        render_texts(texts)  # 텍스트 렌더링 함수 호출
        update_screen(5)  # 초당 5 프레임으로 설정

def game_over_screen():
    screen.fill(white)  # 화면을 흰색으로 채움
    # 텍스트 정보 리스트
    texts = [
        ("Game Over", big_font, black, (screen_width // 2, screen_height // 2 - 50)),
        ("Press SPACE to Restart", font, black, (screen_width // 2, screen_height // 2 + 30)),
        (f"Score: {score}", font, black, (screen_width // 2, screen_height // 2))
    ]

    background(520, time)  # 배경 표시
    render_texts(texts)  # 텍스트 렌더링 함수 호출
    update_screen(5) # 화면을 업데이트

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False  # 스페이스바를 누르면 대기 종료

def handle_events(): # 사용자 입력을 처리하는 함수
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 창을 닫으려는 경우
            pygame.quit()  # Pygame 종료
            sys.exit()  # 시스템 종료
        if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
            bird.up()  # 'u' 키를 누르면 새가 위로 점프

def update_background(): # 배경을 업데이트하는 함수
    global time
    background(520, time)  # 배경을 표시
    if frame_count % backgound_frequency == 1000:
        time += 1  # 일정 시간이 지나면 배경 시간 업데이트

def update_pipes(): # 파이프를 생성하고 업데이트하는 함수
    if frame_count % pipe_frequency == 0:
        pipes.append(Pipe())  # 파이프 생성
    for pipe in pipes:
        pipe.show()  # 파이프를 화면에 표시
        pipe.update()  # 파이프 위치를 업데이트
        if pipe.offscreen():
            pipes.remove(pipe)  # 화면을 벗어난 파이프 제거
        if pipe.x + pipe.w + bird.width == bird.x:
            global score
            score += 1  # 새가 파이프를 통과하면 점수 증가

def update_items(): # 아이템을 생성하고 업데이트하는 함수
    if frame_count % item_frequency == 0:
        items.append(Item())  # 아이템 생성
    for item in items:
        item.show()  # 아이템을 화면에 표시
        item.update()  # 아이템 위치를 업데이트
        if item.offscreen():
            items.remove(item)  # 화면을 벗어난 아이템 제거

def update_hud(): # 화면의 점수와 배고픔 지수를 업데이트하는 함수
    global hunger_count
    board(10, 10)  # 점수와 배고픔 지수를 표시
    if frame_count % Hunger_frequency == 0:
        hunger_count -= 1  # 배고픔 지수를 감소

def update_bird(): # 새의 상태를 업데이트하는 함수
    bird.show()  # 새를 화면에 표시
    bird.update()  # 새의 위치와 상태를 업데이트

def check_collisions(): # 충돌을 확인하고 처리하는 함수
    global game_over, hunger_count
    if is_pipe_collision(bird, pipes) or hunger_count == 0:
        game_over = True  # 파이프와 충돌하거나 배고픔이 0이면 게임 오버
    if is_item_collision(bird, items):
        items.clear()  # 충돌한 아이템을 제거
        hunger_count = min(hunger_count + 1, 5)  # 배고픔 지수를 증가 (최대 5)

def update_screen(tick): # 화면을 업데이트하는 함수
    pygame.display.update()  # 화면을 새로 고침
    pygame.time.Clock().tick(tick)  # 초당 60 프레임으로 설정

def reset_game(): # 게임 오버 시 게임 상태를 초기화하는 함수
    global bird, pipes, items, score, time, hunger_count, frame_count, game_over
    game_over_screen()  # 게임 오버 화면을 표시
    bird = Bird()  # 새 객체 초기화
    pipes = []  # 파이프 리스트 초기화
    items = []  # 아이템 리스트 초기화
    score = 0  # 점수 초기화
    time = 0  # 시간 초기화
    hunger_count = 6  # 배고픔 지수 초기화
    frame_count = 0  # 프레임 카운트 초기화
    game_over = False  # 게임 오버 상태 초기화

def main(): # 메인 루프 함수
    # 전역 변수를 사용함을 명시
    global score, hunger_count, game_over, frame_count, time, bird, pipes, items

    bird = Bird()  # 새 객체를 초기화
    main_menu()  # 메인 메뉴를 표시
    
    # 게임 루프: 게임 오버가 아닐 때 계속 반복
    while not game_over:
        handle_events()  # 사용자 입력을 처리
        update_background()  # 배경을 업데이트
        update_pipes()  # 파이프를 생성 및 업데이트
        update_items()  # 아이템을 생성 및 업데이트
        update_hud()  # 점수와 배고픔 지수를 화면에 표시
        update_bird()  # 새의 상태를 업데이트
        check_collisions()  # 충돌 여부를 확인
        update_screen(60)  # 화면을 업데이트

        frame_count += 1  # 프레임 카운트를 증가
        
        if game_over:
            reset_game()  # 게임 오버 시 게임을 초기화


# 게임 시작
if __name__ == "__main__":
    main()
