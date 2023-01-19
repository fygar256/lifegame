#!/usr/bin/python3
from pygame.locals import *
from scipy import signal
import pygame
import sys
import numpy as np
import os
import binascii



scale=5
height=100
width=100

def draw_grid(screen):
  screen.fill((0,0,0))
  for i in range(width):
    pygame.draw.line(screen,(0,255,0),(0,i*scale),(scale*width,i*scale),1)
  for j in range(height):
    pygame.draw.line(screen,(0,255,0),(j*scale,0),(j*scale,scale*height),1)

def set(screen,cx,cy,c):
  screen.fill((c*255,c*255,c*255),(cx*scale+1,cy*scale+1,scale-1,scale-1))

def put(F,screen):
  for i in range(len(F)):
    for j in range(len(F[1])):
       set(screen,j,i,F[i][j])

def rev(F,cx,cy):
  F[cy][cx]=int(F[cy][cx])^1
  return(F)

def clear():
    return(np.zeros((height,width)))

def initrandomseed():
    f=open("/dev/random",'rb') # /dev/randomを開く
    random32bitdata=f.read(4) # ４バイト読み出し
    f.close()
    randomhex=binascii.hexlify(random32bitdata) #１６進の文字列に変換
    randomint=int(randomhex,16) # 整数に変換
    np.random.seed(seed=randomint) # ランダムシードを初期化

def initrnd():
    N = width*height
    v = np.array(np.random.rand(N) + 0.1, dtype=int)
    return v.reshape(height, width)

def count_neighbor(F):
    return signal.correlate2d(F,np.ones((3, 3),dtype=int),mode="same",boundary="wrap")

def nextgen(F):
    N = count_neighbor(F)
    G = (N == 3) + F * (N == 4)
    return G

def eventloop(F,screen):
    run='e'
    while run!='q':
        for event in pygame.event.get():
            if event.type == QUIT:
                run='q'
            if event.type == KEYDOWN:  # キーを押したとき
                k=pygame.key.name(event.key)
                if k== 'q':
                    run='q'
                elif k=='e':
                    run='e'
                elif k=='g':
                    run='g'
                elif k=='r':
                    F = initrnd()
                    put(F,screen)
                elif k=='l':
                    if os.path.exists("save.txt"):
                      F = np.loadtxt("save.txt")
                    put(F,screen)
                elif k=='w':
                    np.savetxt("save.txt", F, "%d")
                elif k=='c':
                    F=clear()
                    put(F,screen)
            elif event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    F=rev(F,x//scale,y//scale)
                    put(F,screen)
                    run='e'
            elif event.type == MOUSEMOTION:
                    x, y = event.pos
        if run=='g':
          F=nextgen(F)
          put(F,screen)
        pygame.display.update()

def main():
    pygame.init()    # Pygameを初期化
    screen = pygame.display.set_mode((scale*width,scale*height))    # 画面を作成
    pygame.display.set_caption("lifegame")    # タイトルを作成
    initrandomseed()
    draw_grid(screen)
    F=clear()
    put(F,screen)
    eventloop(F,screen)
    pygame.quit()
    sys.exit()

if __name__=='__main__':
    main()
