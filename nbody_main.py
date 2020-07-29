# 필요한 라이브러리 임포트
import numpy as np
import math
from random import uniform

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from numba import cuda
from numba import *


# 거리의 최소값
min_distance = 0.1

# 중력상수
G = 0.1

# step size
delta_T = 1

# 물체 개수
particles = 100000
# 최대 반지름 거리
radius = 1000

PAUSE = False


last_pos_x = 0
last_pos_y = 0
zoom_scale = 1.0
dataL = 0
x_rot = 0
y_rot = 0
z_rot = 0


# 프리먼 법칙
''' 원반은하 중심에서 표면밝기는 같음'''
def FreemanLaw(r):
    # 0.35는
    return math.exp(-r / 0.35)


# RK4에서의 cuda 가속 적용
@cuda.jit
def velocityCalculation(A, V, B):
    row, col = cuda.grid(2)

    # cuda 메모리 초과하지 않도록 지정
    if row < A.shape[0]:
        if col < A.shape[0]:
            # 입자가 같지 않도록 제외
            if row == col:
                return

            # 거리 계산
            r_x = (A[col, 0] - A[row, 0])
            r_y = (A[col, 1] - A[row, 1])
            r_z = (A[col, 2] - A[row, 2])

            r = (r_x**2 + r_y**2 + r_z**2)**(1/2)

            # zero division error를 방지하기 위함
            r = max(r, min_distance)

            # 속도 update
            V[row, 0] += ((G * .01 * delta_T) / r)*r_x / r
            V[row, 1] += ((G * .01 * delta_T) / r)*r_y / r
            V[row, 2] += ((G * .01 * delta_T) / r)*r_z / r

        # 중력까지의 거리?
        r_x = (B[0] - A[row, 0])
        r_y = (B[1] - A[row, 1])
        r_z = (B[2] - A[row, 2])

        r = (r_x ** 2 + r_y ** 2 + r_z ** 2) ** (1 / 2)

        # zero division error를 방지하기 위함
        r = max(r, min_distance)

        # 속도 update(3은 임의의 scaling 상수)
        V[row, 0] += ((G * 3 * delta_T) / r) * r_x / r
        V[row, 1] += ((G * 3 * delta_T) / r) * r_y / r
        V[row, 2] += ((G * 3 * delta_T) / r) * r_z / r

        # 위치 업데이트
        A[row, 0] += V[row, 0]
        A[row, 1] += V[row, 1]
        A[row, 2] += V[row, 2]

# 초기설정 - number은 개수
def initialize(number, distance):
    vertices = np.zeros((number, 3), np.float)
    velocities = np.zeros((number, 3), np.float)

    for i in range(number):
        # 위치를 임의적으로 생성한 후 프리먼 법칙에 부합한지 확인
        while True:
            rand = uniform(0, 1)
            r = uniform(0, 1)

            if rand <= FreemanLaw(r): # rand 값이 0.35*r보다 작으면
                r = r * distance # r값에 distance argument를 곱하여 반환
                break
            else:
                continue # 크면 그대로 반환

        # 위치 설정
        # 난수로 theta값을 설정
        theta = uniform(0, 2*math.pi) # 0~2pi

        x = r*math.cos(theta)
        y = r*math.sin(theta)
        # -5~5까지의 임의 uniform 난수 생성
        z = uniform(-5, 5)

        vertices[i] = [x, y, z]

        # 초기 각속도 설정
        rad_vel = (G / r**2)**(1/2)

        vx = -r*rad_vel*math.sin(theta)
        vy = r*rad_vel*math.cos(theta)
        # disk의 수직한 방향으로 섭동(perturbation) - (임의의 작은 상수 지정)
        vz = uniform(-0.0005, 0.0005)

        velocities[i] = [vx, vy, vz]

    return vertices, velocities, np.array([0, 0, 0], np.float)

def draw(vertices):
    glVertexPointerd(vertices)
    glEnable(GL_VERTEX_ARRAY)
    glDrawArrays(GL_POINTS, 0, len(vertices))

def main():
    global last_pos_x, last_pos_y, zoom_scale, x_rot, y_rot, z_rot, PAUSE, G

    A, V, B = initialize(particles, radius)

    # 블록당 쓰레드
    threads_per_block = (16, 16)
    blocks_per_grid_x = int(math.ceil(A.shape[0] / threads_per_block[0]))
    blocks_per_grid_y = int(math.ceil(A.shape[1] / threads_per_block[1]))
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    # 디스플레이 설정
    display = (1000, 1000) # 디스플레이 크기 설정
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, radius*2)
    glTranslatef(0.0, 0.0, -radius)
    glRotatef(0, 0, 20, 0.5)

    clock = pygame.time.Clock()

    while True:
        # 최대 시간
        clock.tick(90)

        pygame.display.set_caption('%s FPS: %.2f' % ('n-body simulation', clock.get_fps()))

        # 클릭 등 디스플레이 내 설정
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                glScaled(1.05, 1.05, 1.05)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                glScaled(0.95, 0.95, 0.95)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP6:
                    B[0] += 5
                elif event.key == pygame.K_KP4:
                    B[0] -= 5
                elif event.key == pygame.K_KP8:
                    B[1] += 5
                elif event.key == pygame.K_KP2:
                    B[1] -= 5
                elif event.key == pygame.K_KP9:
                    B[2] += 5
                elif event.key == pygame.K_KP3:
                    B[2] -= 5
                elif event.key == pygame.K_SPACE:
                    PAUSE = not PAUSE
                elif event.key == pygame.K_r:
                    A, V, B = initialize(particles, radius)

                elif event.key == pygame.K_s:
                    pygame.image.save()

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                dx = x - last_pos_x
                dy = y - last_pos_y

                mouseState = pygame.mouse.get_pressed()
                if mouseState[0]:
                    modelView = (GLfloat * 16)()
                    mvm = glGetFloatv(GL_MODELVIEW_MATRIX, modelView)

                    # x-y 축의 회전 결합
                    temp = (GLfloat * 3)()
                    temp[0] = modelView[0] * dy + modelView[1] * dx
                    temp[1] = modelView[4] * dy + modelView[5] * dx
                    temp[2] = modelView[8] * dy + modelView[9] * dx
                    norm_xy = math.sqrt(temp[0] * temp[0] + temp[1] * temp[1] + temp[2] * temp[2])
                    glRotatef(math.sqrt(dx * dx + dy * dy), temp[0] / norm_xy, temp[1] / norm_xy, temp[2] / norm_xy)

                last_pos_x = x
                last_pos_y = y

        # 계산
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if not PAUSE:
            velocityCalculation[blocks_per_grid, threads_per_block](A, V, B)
        draw(A)
        pygame.display.flip()

if __name__ == '__main__':
    main()
