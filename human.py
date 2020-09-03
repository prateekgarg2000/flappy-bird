from classes import *

def solo_play():
    bird=Bird(230,350)
    base=Base(630)
    run =True
    pipes=[Pipe(700)]
    clock=pygame.time.Clock()
    win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    score=0
    draw_window(win,bird,pipes,base,score,1)
    pygame.time.wait(1000)
    while run:
        clock.tick(30)
        key_states = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run=False
                else:
                    bird.jump()
        rem=[]
        for pipe in pipes:
            if pipe.collide(bird):
                run=False
                break
            if(pipe.x +pipe.PIPE_BOTTOM.get_width()<0):
                rem.append(pipe)
            add_pipe=False
            if not pipe.passed and  pipe.x + pipe.PIPE_BOTTOM.get_width() < bird.x:
                pipe.passed=True
                add_pipe=True
            pipe.move()
            if add_pipe:
                score+=1
                pipes.append(Pipe(600))

            for r in rem:
                pipes.remove(r)
        base.move()
        bird.move()
        draw_window(win,bird,pipes,base,score,1)
        if bird.y+bird.img.get_height()>630 or bird.y<0:
            run=False
            break
    pygame.time.wait(1000)
    pygame.quit()
    quit()
if __name__=="__main__":
    solo_play()
