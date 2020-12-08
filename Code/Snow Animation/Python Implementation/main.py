#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pygame
from random import randint,random

class Renderer:
    def __init__(self,resolution=(1000,600),fps=60):
        self.screen_size = resolution
        self.fps = fps
        
        self.n_flakes = 3000
        self.flakes = self.gen_flakes()
        
        # Initialise the vector field
        self.vf = VectorField(self.screen_size)
                
        # Initalise visualiser
        pygame.init()        

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.main_loop()
    
    def gen_flakes(self):
        flakes = []
        for i in range(self.n_flakes):
            tmp_pos = [randint(0,self.screen_size[0]),randint(0,self.screen_size[1])]
            tmp_vec = [0,randint(-1,1)*0.5+random()*0.5]
            col = randint(0,255)
            col = [col,col,col]
            flakes.append(Flake(i,tmp_pos,radius=randint(2,4),
                                vec=tmp_vec,
                                colour=col))
            flakes[i].screen_size = self.screen_size
        return flakes
            
    def draw_flakes(self):
        # Draw flakes on screen surface
        for f in self.flakes:
            pygame.draw.ellipse(self.screen,f.colour,[f.pos[0],f.pos[1],f.radius,f.radius])
    
    def move_flake(self,flake):
        flake.update_pos()
    
    def physics(self):
        # Update the velocity based on the vector field
        for f in self.flakes:
            #f.add_force([randint(-1,1),randint(-1,1)])
            tmp_vec = [
                self.vf.u[self.screen_size[0] - int(f.pos[0])-1][self.screen_size[1] - int(f.pos[1])-1],
                self.vf.v[self.screen_size[0] - int(f.pos[0])-1][self.screen_size[1] - int(f.pos[1])-1]
                ]

            f.set_force(tmp_vec)
            #f.add_force([random()*0.5,random()*0.5])
            self.move_flake(f)
        
    def main_loop(self):
        # Close the program if the user clicks the close button
        done = False

        while not done:
            self.physics()
            self.screen.fill(pygame.Color('black'))
            self.draw_flakes()

            for event in pygame.event.get():   
                if event.type == pygame.QUIT:  
                    done = True   

            # Update the screen 
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        
class VectorField:
    def __init__(self,resolution,v_type='default',field_range=[-1,1,-1,1]):
        self.resolution = resolution
        self.field_range = field_range
        self.x,self.y,self.u,self.v = self.gen_field(v_type)
    def gen_field(self,v_type = 'default'):
        x_space = np.linspace(self.field_range[0],
                              self.field_range[1],
                              max(self.resolution))
        y_space = np.linspace(self.field_range[2],
                              self.field_range[3],
                              max(self.resolution))
        x,y = np.meshgrid(x_space,y_space)
        
        if v_type == 'default':
            u = -np.sin(x**2)
            v = [[1 for i in range(max(self.resolution))] for j in range(max(self.resolution))]
            return x,y,u,v
        if v_type == 'wind':
            u = -x
            v = [[random() for i in range(self.resolution[1])] for j in range(self.resolution[0])]
            return x,y,u,v
    def plot_field(self):
        plt.quiver(self.x,self.y,self.u,self.v)
        plt.show()

class Flake:
    def __init__(self,f_id,pos,radius=1,vec=[5,1],colour=[0,0,0]):
        self.id = f_id
        self.pos = pos
        self.radius = radius
        self.vec = vec[:]
        self.init_vec = self.vec[:]
        self.screen_size = None
        self.colour = colour
    
    def add_force(self,vec):
        self.vec[0] += vec[0]
        self.vec[1] += vec[1]
    
    def set_force(self,vec):
        self.vec[0] = vec[0] + self.init_vec[0]
        self.vec[1] = vec[1] + self.init_vec[1]
        
    def update_pos(self):
        self.pos[0] += 0.5*self.vec[0]
        self.pos[1] += 0.5*self.vec[1]
        wall_bounce = False
        # Screen wrapping
        # x
        if wall_bounce:
            # Alternatively can bounce from the walls
            if self.pos[0] > self.screen_size[0]:
                self.pos[0] = self.screen_size[0]
                #self.vec = self.init_vec[:]
                self.vec[0] *= -1
            if self.pos[0] < 0:
                self.pos[0] = 0
                #self.vec = self.init_vec[:]
                self.vec[0] *= -1
        else:
            if self.pos[0] > self.screen_size[0]:
                self.pos[0] = 0
                self.vec = self.init_vec[:]
            if self.pos[0] < 0:
                self.vec = self.init_vec[:]
                self.pos[0] = self.screen_size[0]
        # y
        if self.pos[1] > self.screen_size[1]:
            self.pos[1] = 0
            self.vec = self.init_vec[:]
        if self.pos[1] < 0:
            self.pos[1] = self.screen_size[1]
            self.vec = self.init_vec[:]

R = Renderer()

