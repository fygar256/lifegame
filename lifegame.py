#!/usr/bin/python3
from pygame.locals import *
from scipy import signal
import pygame
import sys
import numpy as np
import os

scale=5
height=100
width=100

pygame.init()    # Pygameを初期化
screen = pygame.display.set_mode((scale*width,scale*height))    # 画面を作成
pygame.display.set_caption("lifegame")    # タイトルを作成

def draw_grid():
  screen.fill((0,0,0))
  for i in range(0,width):
    pygame.draw.line(screen,(0,255,0),(0,i*scale),(scale*width,i*scale),1)
  for j in range(0,height):
    pygame.draw.line(screen,(0,255,0),(j*scale,0),(j*scale,scale*height),1)

def set(cx,cy,c):
  screen.fill((c*255,c*255,c*255),(cx*scale+1,cy*scale+1,scale-1,scale-1))

def rev(F,cx,cy):
  F[cy][cx]=int(F[cy][cx])^1
  return(F)

def put(F):
  for i in range(len(F)):
    for j in range(len(F[1])):
       set(j,i,F[i][j])

def clear():
    return(list(np.zeros((height,width))))

def initrnd():
    N = width*height
    v = np.array(np.random.rand(N) + 0.1, dtype=int)
    return v.reshape(height, width)

def count_neighbor(F):
    return signal.correlate2d(F, mask, mode="same", boundary="wrap")

def nextgen(F):
    N = count_neighbor(F)
    G = (N == 3) + F * (N == 4)
    return G

run='e'
draw_grid()
F=clear()
put(F)
mask = np.ones((3, 3), dtype=int)
while run!='q':
    for event in pygame.event.get():
        if event.type == QUIT:
            run='q'
        if event.type == KEYDOWN:  # キーを押したとき
            k=pygame.key.name(event.key)
            if k== 'q':
                run='q'
            if k=='r':
                F = initrnd()
                put(F)
            if k=='l':
              if os.path.exists("save.txt"):
                F = np.loadtxt("save.txt")
              put(F)
            if k=='w':
                np.savetxt("save.txt", F, "%d")
            if k=='e':
                run='e'
                put(F)
            if k=='g':
                run='g'
            if k=='c':
                F=clear()
                put(F)
        elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                F=rev(F,x//scale,y//scale)
                put(F)
                run='e'
        elif event.type == MOUSEMOTION:
                x, y = event.pos
    if run=='g':
      F=nextgen(F)
      put(F)
    pygame.display.update()
pygame.quit()
sys.exit()

