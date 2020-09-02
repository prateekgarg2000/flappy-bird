from classes import *

def main(genomes,config):
    birds=[]
    nets=[]
    gens=[]
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230,350))
        gens.append(genome)

    base=Base(630)
    run =True
    pipes=[Pipe(700)]
    clock=pygame.time.Clock()
    win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    score=0
    draw_window(win,birds,pipes,base,score,0)
    pygame.time.wait(1000)
    while run:
        if len(birds) <=0 or gens[0].fitness>1500:
            run=False
            break



        # clock.tick(30)
        key_states = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.quit()
                quit()
        if key_states[pygame.K_ESCAPE]:
            run=False
            pygame.quit()
            quit()
        pipe_index=0
        if len(birds)>0 and len(pipes)>1 and birds[0].x > pipes[0].x + pipes[0].PIPE_BOTTOM.get_width():
            pipe_index=1
        for x,bird in enumerate(birds):
            bird.move()
            gens[x].fitness +=0.1
            output = nets[x].activate((bird.y,abs(bird.y-pipes[pipe_index].height),abs(bird.y-pipes[pipe_index].bottom)))
            if output[0]>0.5:
                bird.jump()
        # if key_states[32]==1:
        #     bird.jump()
            # key_states[32]=0
        rem=[]
        for pipe in pipes:
            for x,bird in enumerate(birds):
                if pipe.collide(bird) or bird.y+bird.img.get_height()>630 or bird.y<0:
                    gens[x].fitness-=2
                    birds.pop(x)
                    nets.pop(x)
                    gens.pop(x)


            if(pipe.x +pipe.PIPE_BOTTOM.get_width()<0):
                rem.append(pipe)
            add_pipe=False
            if (not pipe.passed) and len(birds)>0 and  pipe.x + pipe.PIPE_BOTTOM.get_width() < birds[0].x:
                pipe.passed=True
                add_pipe=True
                gens[x].fitness+=3

            pipe.move()
            if add_pipe:
                score+=1
                pipes.append(Pipe(600))

            for r in rem:
                pipes.remove(r)
        base.move()
        draw_window(win,birds,pipes,base,score,0,gens)
    pygame.time.wait(1000)

def run(config_path):
    config=neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats=neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main,10)
    with open("trained_bird.h5","wb") as f:
        pickle.dump(winner,f)
    


if __name__ =="__main__":
    config_path=os.path.join(os.getcwd(),"config-feedforward.txt")
    run(config_path)
