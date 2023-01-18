import math  # 큐브 제작 시 사용되는 수학 함수
import random
import pygame  # pygame 툴 사용
import random
import time

# 사용할 색상 초기화
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)

pygame.init() #pygame 모듈 초기화
myFont = pygame.font.SysFont(None, 50) #(글자체, 글자크기) None=기본글자체

# 게임판 넓이 설정
width = 500  # 화면 높이
height = 500

cols = 25
rows = 20  # 행의 갯수


pygame.init()
pygame.display.set_caption("snake game")  # 게임 이름 설정
# GAMEOVER 창 화면 설정
size = [400,400]
screen = pygame.display.set_mode(size)

class cube():
    rows = 20
    w = 500  # 큐브 크기

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny  # "L", "R", "U", "D"
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)  # 사용자의 위치 변경

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows  # 각 큐브의 넓이, 높이
        i = self.pos[0]  # 행
        j = self.pos[1]  # 열

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        # 큐브의 행과 열 값에 각 큐브의 너비와 높이를 곱하여 그릴 위치를 결정할 수 있음
        if eyes:  # 스네이크 눈 그리기
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


# 스네이크 개체 생성
class snake():
    body = []  # 스네이크 몸
    turns = {}

    # Snake 클래스를 시작하기 위해 클래스 변수 추가
    def __init__(self, color, pos):
        # pos is given as coordinates on the grid ex (1,5)
        # pos는 격자선(그리드)에서 좌표로 제공(1,5)
        self.color = color
        self.head = cube(pos)  # 스네이크의 머리 부분
        self.body.append(self.head)  # 머리 추가 (큐브 형태)
        # 여기까지가 몸을 만드는 부분

        # 여기는 스네이크가 움직이는 방향을 나타냄
        self.dirnx = 0
        self.dirny = 1

    # 움직임
    def move(self):
        for event in pygame.event.get(): # 이벤트의 발생 여부에 따른 반복문 -> 중간에 발생한 이벤트를 확인하고 검사
            if event.type == pygame.QUIT:  # 게임 종료 ; 사용자가 빨간색 큐브와 닿을 경우
                pygame.quit()

            keys = pygame.key.get_pressed()  # 어떤 키를 누르고 있는지 확인

            for key in keys:  # 키 방향 조작
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):  # 스네이크 몸체의 전체 큐브 순환
            p = c.pos[:]  # 게임판에 큐브 위치를 저장
            if p in self.turns:  # 큐브의 현재 위치가 회전한 위치일 경우
                turn = self.turns[p]  # 돌아가야 할 방향을 잡는다
                c.move(turn[0], turn[1])  # 큐브를 해당 방향으로 이동
                if i == len(self.body) - 1:  # 만약 큐브가 모두 소멸 시에 턴 종료
                    self.turns.pop(p)
            else:  # 스네이크를 조정하지 않을 경우, 가장자리에 스네이크가 도달하게 되고 다시 가운데에 나타나게 된다
                c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    # 스네이크 만들기
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


# 빨간색 사각형
def redrawWindow():
    global win  # win - rows,width, s
    win.fill((0, 0, 0))  # 빈 화면을 검은색으로 채움
    drawGrid(width, rows, win)  # 격자선 그리기
    s.draw(win)
    snack.draw(win)
    pygame.display.update()  # 화면 업데이트
    pass


def drawGrid(w, rows, surface):  # 격자선을 그리는 함수
    sizeBtwn = w // rows  # 선과 선 사이의 거리 제공

    x = 0  # x축
    y = 0  # y축
    for l in range(rows):  # 각 루프에 수직선과 수평선을 그림
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


# 스네이크 게임의 '간식'을 추가하는 부분 ; 몸을 늘리는 '큐브'
def randomSnack(rows, item):
    positions = item.body  # 스네이크에 있는 모든 큐브의 위치를 가져옴

    while True:  # 유효한 위치를 얻을 때까지 임의의 위치를 계속 생성한다
        x = random.randrange(1, rows - 1)
        y = random.randrange(1, rows - 1)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            # 생성된 간식을 스네이크가 먹었는지 확인
            continue
        else:
            break

    return (x, y)





def main():
    global s, snack, win
    win = pygame.display.set_mode((width, height))  # 화면 개체 생성
    s = snake((255, 0, 0), (10, 10))  # 스네이크 개체 생성
    s.addCube()
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))  # 랜덤 스낵 생성
    flag = True
    clock = pygame.time.Clock()  # 프레임 개체 생성

    # 메인 루프 시작
    while flag:
        pygame.time.delay(50)  # 게임이 너무 빨리 실행되지 않도록 지연
        clock.tick(10)  # 10FPS로 실행되도록
        s.move()  # 스네이크를 움직이게 한다.

        headPos = s.head.pos
        if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0:
            print("Score:", len(s.body))
            s.reset((10, 10))

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print("Score:", len(s.body))
                while(True):
                    time.sleep(0.5)
                    screen.fill(RED)
                    myText = myFont.render("GAME OVER ", True, BLACK)
                    screen.blit(myText, (90, 100))  # (글자변수, 위치)
                    myText = myFont.render("SCORE : " + str(len(s.body)), True, BLACK)
                    screen.blit(myText, (90, 150))  # (글자변수, 위치)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:  # 창을 닫으면
                            pygame.quit()   # 게임 종료
                    pygame.display.update()
                break




        redrawWindow()  # 화면 새로고침 - def redrawWindow

main()






    
