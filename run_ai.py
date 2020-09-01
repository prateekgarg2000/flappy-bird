from classes import *

def ai_play():

    config_path=os.path.join(os.getcwd(),"config-feedforward.txt")
    config=neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
    with open("trained_bird.h5","rb") as f:
        genome=pickle.load(f)
    network = neat.nn.FeedForwardNetwork.create(genome, config)

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
        if key_states[pygame.K_ESCAPE]:
            run=False
        pipe_index=0
        if len(pipes)>1 and bird.x > pipes[0].x + pipes[0].PIPE_BOTTOM.get_width():
            pipe_index=1
        output = network.activate((bird.y,abs(bird.y-pipes[pipe_index].height),abs(bird.y-pipes[pipe_index].bottom)))
        if output[0]>0.5:
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
    ai_play()
