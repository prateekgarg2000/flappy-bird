import pygame
import neat
import os
import time
import random
import pickle

pygame.font.init()

WIN_HEIGHT=700
WIN_WIDTH=500
BIRD_IMAGES=[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png")))]
PIPE_IMAGE=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMAGE=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMAGE=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
STAT_FONT=pygame.font.SysFont("comicsans",50)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

class Bird:
    IMAGES=BIRD_IMAGES
    MAX_ROTATION=25
    ROT_VEL=20
    ANIMATION_TIME=5

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=0
        self.tick_count=0
        self.vel=0
        self.height=self.y
        self.img_count=0
        self.img=self.IMAGES[0]

    def jump(self):
        self.vel=-20
        self.tilt=30
        self.tick_count=0
        self.height=self.y

    def move(self):
        self.tick_count+=1
        d=self.vel  + 1.2
        self.vel=self.vel+2.4
        if(d>16):
            d=16
        self.y = self.y + d

        if d<0 :
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
                if self.tilt > -90:
                    self.tilt -= self.ROT_VEL


    def draw(self,win):
        self.img = self.IMAGES[self.img_count//self.ANIMATION_TIME]
        self.img_count+=1
        if(self.img_count==4*self.ANIMATION_TIME):
            self.img_count=0
        if self.tilt <= -80:
            self.img=self.IMAGES[1]
            self.img_count=self.ANIMATION_TIME
        rotated_image = pygame.transform.rotate(self.img,self.tilt)
        new_rect= rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)


    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP=200
    VEL=5

    def __init__(self,x):
        self.x=x
        self.height=0
        self.top=0
        self.bottom=0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE,False,True)
        self.PIPE_BOTTOM =PIPE_IMAGE
        self.passed=False
        self.set_height()

    def set_height(self):
        self.height=random.randrange(50,450)
        self.top=self.height-self.PIPE_TOP.get_height()
        self.bottom=self.height+self.GAP

    def move(self):
        self.x-=self.VEL

    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))

    def collide(self,bird):
        bird_mask=bird.get_mask()
        top_mask=pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask=pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x-bird.x,self.top-round(bird.y))
        bottom_offset = (self.x-bird.x,self.bottom-round(bird.y))
        b_point=bird_mask.overlap(bottom_mask,bottom_offset)
        t_point=bird_mask.overlap(top_mask,top_offset)
        if(b_point or t_point):
            return True

        return False

class Base:
    VEL=5
    WIDTH=BASE_IMAGE.get_width()
    IMG=BASE_IMAGE

    def __init__(self,y):
        self.y = y
        self.x1=0
        self.x2=self.WIDTH

    def move(self):
        self.x1-= self.VEL
        self.x2-= self.VEL

        if self.x1 + self.WIDTH <0:
            self.x1=self.x2+self.WIDTH

        if self.x2 + self.WIDTH <0:
            self.x2=self.x1+self.WIDTH

    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))

def draw_window(win,birds,pipes,base,score,is_human,gens=None):
    win.blit(BG_IMAGE,(0,-100))
    text=STAT_FONT.render("score: "+str(score),1,(255,255,255))
    win.blit(text,(WIN_WIDTH -10 -text.get_width(),10))
    if gens:
        text=STAT_FONT.render("fitness: "+str(round(gens[0].fitness,2)),1,(255,255,255))
        win.blit(text,(10,10))

    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    if is_human:
        birds.draw(win)
    else:
        for bird in birds:
            bird.draw(win)
    pygame.display.update()
