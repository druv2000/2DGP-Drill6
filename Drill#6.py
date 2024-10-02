from pico2d import *
import random

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

Background = load_image('TUK_GROUND.png')
Character = load_image('george.png')
Goal = load_image('hand_arrow.png')

def handle_events():
    global is_program_running
    events = get_events()
    for event in events:
        # esc키를 누르거나, 윈도우를 닫으면 종료
        if event.type == SDL_QUIT:
            is_program_running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            is_program_running = False
    pass

def set_goal():
    global character_x, character_y, goal_x, goal_y

    # 캐릭터가 목표에 도착했을때 무작위 위치로 목표 재설정
    if character_x == goal_x and character_y == goal_y:
        new_x = random.randint(0, TUK_WIDTH)
        new_y = random.randint(0, TUK_HEIGHT)
        goal_x, goal_y = new_x, new_y
    pass

def chase_goal():
    global character_x, character_y, goal_x, goal_y, dir

    # 출발점 및 목표점 설정
    x1, y1 = character_x, character_y
    x2, y2 = goal_x, goal_y

    # 캐릭터의 이동 속도 및 거리 설정
    speed = 5
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    # 이동
    if distance > speed:
        # 등속 이동
        character_x += ((x2 - x1) / distance) * speed
        character_y += ((y2 - y1) / distance) * speed

        # 목표 방향으로 바라보는 방향 수정
        if abs(x2 - x1) > abs(y2 - y1):
            if x2 > x1:
                dir = RIGHT
            else:
                dir = LEFT
        else:
            if y2 > y1:
                dir = UP
            else:
                dir = DOWN
    else:
        # 남은 거리가 일정 수준 미만이면 즉시 목표로 이동
        character_x, character_y = x2, y2

#========= main ===========

# 캐릭터 시작점, 목표의 위치 등 초기화
character_x = TUK_WIDTH / 2; character_y = TUK_HEIGHT / 2
goal_x = random.randint(0, TUK_WIDTH); goal_y = random.randint(0, TUK_HEIGHT)
animation_speed = 10
frame = 0; count = 0

# 방향 설정(george.png의 형식대로 나타냄) 초기 상태 : DOWN
UP = 2; DOWN = 0; LEFT = 1; RIGHT = 3
dir = DOWN

is_program_running = True
while(is_program_running):
    # 각종 함수 실행
    set_goal()
    chase_goal()
    handle_events()

    # 배경, 오브젝트 그리기
    clear_canvas()
    Background.draw(TUK_WIDTH / 2, TUK_HEIGHT / 2)
    Character.clip_draw(48*dir, 48*frame, 48, 48, character_x, character_y, 100, 100)
    Goal.draw(goal_x, goal_y)
    update_canvas()

    # 설정한 속도로 애니메이션 프레임 재생
    count += 1
    if count % animation_speed == 0:
        frame = (frame + 1) % 4
    delay(0.01)
    pass