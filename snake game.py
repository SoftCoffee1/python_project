"""
pygame을 활용하여 snake game 만들기!

<Steps>
1. 그리드가 있는 surface 생성해주기.
2. snake와 food객체 생성해주기.
2-1. snake 객체가 갖고 있어야할 매서드들
    - __init__ : 총 4가지 요소를 초기화 --> 처음길이, 위치, 색깔 3가지 요소는 fixed하게 정해주고 이동 방향은 랜덤하게 설정.
    - move : 현재 이동방향으로 한칸 이동하도록 구현 (deque 사용하면 시간효율적일듯)
    ---------------> get_head_positions : 머리의 위치를 알아야 그 다음 위치로 이동 가능
    - turn : 방향키를 누르면 이동방향이 바뀌도록 구현.

2-2. food 객체가 갖고 있어야할 매서드들
    - __init__ : 총 2가지 요소를 초기화 --> 색깔 fixed, 위치 랜덤하게 설정.

3. while loop를 구성
 --> step1. FPS 설정
 --> step2. 뱡힝키 대기
 --> step3. surface 그리기
 --> step4. 뱀 움직이게 하기
 --> step5. 뱀과 음식 그려넣기
 --> step6. surface 및 display 업데이트 하기!

 ###### clock.tick(10) --> 1초에 while loop 10번 돌리는 것이므로, 만약 1/10초안에 방향키 두번이상을 누르는 경우는
 ######                    방향전환이 제대로 이루어지지 않을 수도 있다는 문제점이 있다.
"""

import pygame
import sys
import random
from collections import deque


class Snake:

    def __init__(self):
        self.length = 1
        self.positions = deque()
        self.positions.append(((SCREEN_HEIGHT // 2), (SCREEN_WIDTH // 2)))
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = SNAKE_COLOR
    
    ## move매서드를 위해서는 뱀의 머리를 알아야하므로, 머리좌표를 구하는 매서드
    def get_head_position(self):
        return self.positions[0]

    
    ## 자기자신에게 부딪힐 경우 게임이 종료되어, 다시 초기화해주는 매서드
    def reset(self):
        self.length = 1
        self.positions = deque()
        self.positions.append(((SCREEN_HEIGHT // 2), (SCREEN_WIDTH // 2)))
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        

    ## 뱀의 움직임에 관여하는 매서드
    def move(self):
        cur = self.get_head_position()
        x, y = self.direction

        new_x = (cur[0] + x*GRIDSIZE) % SCREEN_HEIGHT
        new_y = (cur[1] + y*GRIDSIZE) % SCREEN_WIDTH

        
        ## 자기자신에게 부딪히는 경우에는 초기화하기!
        ## 자기자신에게 부딪히려면 길이가 3보다 커야한다!
        if self.length > 3 and (new_x, new_y) in self.positions:
            self.reset()

            ## 여기서 함수 종료하지 않으면, 길이 1짜리가 부딪힌 그 자리에서 다시 시작함!
            return

        self.positions.appendleft((new_x, new_y))

        ## 실제 길이보다 하나가 더 긴경우는 가장 꼬리를 빼준다
        if len(self.positions) > self.length:
            self.positions.pop()

    
    ## 뱀 회전 매서드
    def turn(self, direction):
        
        ## 길이가 1보다 크면서, 정반대방향으로 가려고 하는 경우는 불가능하다.
        if self.length > 1 and (direction[0]*-1, direction[1]*-1) == self.direction:
            return

        ## 나머지 경우는 회전 가능!
        self.direction = direction

    ## 방향키 누르는 것을 제어하는 매서드
    def handle_keys(self):
        for event in pygame.event.get():
            
            ## 종료버튼 누르는 경우, 파이게임 종료하고, while loop 종료하기!
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

    ## 움직인 뱀을 실제 surface에 그리기
    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))

            ## 뱀 그리기
            pygame.draw.rect(surface, SNAKE_COLOR, r)
            
            ## 뱀을 구성하는 정사각형의 가장자리를 빈칸느낌으로 디자인하기
            pygame.draw.rect(surface, BRIGHTER_GRID_COLOR, r, 1)




class Food:

    def __init__(self):
        self.color = FOOD_COLOR
        self.position = (0,0)
        self.randomize_position()

    ## food의 위치를 랜덤하게 배정해주는 매서드
    def randomize_position(self):
        self.position = random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE, random.randint(0, GRID_WIDTH - 1) * GRIDSIZE

    
    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))

        ## 음식을 그리기
        pygame.draw.rect(surface, FOOD_COLOR, r)

        ## 음식을 구성하는 정사각형의 가장자리를 빈칸으로 디자인하기
        pygame.draw.rect(surface, BRIGHTER_GRID_COLOR, r, 1)



## 전체적인 그리드 생성
def drawGrid(surface):
    for x in range(GRID_HEIGHT):
        for y in range(GRID_WIDTH):

            if (x+y)%2 == 0:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, BRIGHTER_GRID_COLOR, r)

            else:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, DARKER_GRID_COLOR, r)







## 게임화면의 높이와 너비
SCREEN_HEIGHT = 480
SCREEN_WIDTH = 480

## 게임면 내의 그리드 크기와
## 세로 그리드, 가로 그리드 개수를 담기
GRIDSIZE = 20
GRID_HEIGHT = SCREEN_HEIGHT // GRIDSIZE
GRID_WIDTH = SCREEN_WIDTH // GRIDSIZE

## 방향 벡터
UP    = (0,-1)
DOWN  = (0, 1)
LEFT  = (-1,0)
RIGHT = (1, 0)


## 색깔
SNAKE_COLOR = (17, 24, 47)
BRIGHTER_GRID_COLOR = (93,216,228)
DARKER_GRID_COLOR = (84,194,205)
FOOD_COLOR = (23, 163, 49)


def main():
    
    ## pygame 기본 구조 : 
    ### --> pygame 초기화
    ### --> FPS설정을 위한 clock변수 
    ### --> 기본적인 screen 뼈대 만들기 
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)


    ## 인스턴스 생성
    snake = Snake()
    food = Food()

    while True:

        ## FPS(초당 프레임)이 10임을 의미함
        clock.tick(10)
        
        ## 방향키중 어떤것을 누르는 지 체크하는 메서드
        snake.handle_keys()

        ## 매번 새로운 빈 그리드를 그려주어야 뱀이 이동하는 것처럼 보인다.
        ## 이 과정 생략하면 의도하지 않았지만 뱀의 자취가 그대로 남는 형태로 그려진다.
        drawGrid(surface)

        ## while 한번 돌때마다 한칸씩 움직이는 과정
        snake.move()

        ## 새롭게 이동한 머리가 food의 위치와 같다면
        ## 뱀의 길이가 길어지고, food를 랜덤한 위치에 다시 뿌려놓는다.
        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()


        ## 뱀과 음식을 surface에 그려넣는 과정
        ## move 메서드에 의해 뱀이 성장했을 수도, 그대로일수도 있다.
        snake.draw(surface)
        food.draw(surface)

        
        ## surface를 (0,0)을 시작으로 그리기!
        screen.blit(surface, (0,0))

        ## 마지막에는 항상 넣어줘야 그림이 그려진다고 함!
        pygame.display.update()


main()
