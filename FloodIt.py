#This is my implementation of the game Flood-It. Your goal is to make all of the colored boxes the same color using the minimum number of moves.
#You do so by building a 'cluster' starting from the upper left. Pressing a number key from 1 to 6 changes your cluster to that color and all 
#adjacent boxes of that color are then added to your cluster as well. Thus, your cluster grows over time until it encompasses the whole board.
#If this sounds confusing don't worry. Just give it a whirl -- the game is very intuitive!

import random
import numpy  #To use an array to store the boxes
import pygame #For graphics and keyboard/mouse interface

arraysize = 20  #We will display a matrixsize by matrixsize grid of boxes 
boxsize = 20    #The size of each box

colors = {1:(255,0,0),2:(0,255,0),3:(0,0,255),4:(255,128,0),5:(255,255,0),6:(0,255,255)}  #Each of the six colors are stored in a dictionary. The colors are RGB tuples.


#Screen Initialization

pygame.init()
screenwidth = max(arraysize*boxsize, 300)   #Need to ensure there is enough width to display the HUD and victory screen!
mainheight = arraysize*boxsize
HUDheight = 30                 
screenheight = mainheight + HUDheight

screen = pygame.display.set_mode((screenwidth,screenheight))
pygame.display.set_caption('FloodIt')


#Array Initialization

boxarray = numpy.zeros(arraysize**2).reshape(arraysize,arraysize)      #Array of elements with values from 1 to 6 indicating which of the six colors the boxes are.
clusterarray = numpy.zeros(arraysize**2).reshape(arraysize,arraysize)  #Array of 0s and 1s. The 1s will indicate the "cluster" as it grows.
for i in range(arraysize):                    #Initialize the random colors of boxarray
    for j in range(arraysize):
        boxarray[i][j] = random.randint(1,6)

#Variable Initialization

nummoves = 0  #Number of moves

#Define the Cluster Class

class ClusterNode:    #The cluster is a tree consisting of verticies and edges which go right or down. This tree covers the entire cluster.
    clustermembers = 0       #Number of members in the cluster
    def __init__(self,i,j):  #On initialization, check to the right and down for the same color. If found, add those to the cluster!
        if clusterarray[i,j] == 1:
            print "You somehow initialized a new node when you weren't supposed to!"
        clusterarray[i,j] = 1
        ClusterNode.clustermembers += 1
        self.i,self.j = i,j
        self.right = None
        self.down = None
        self.left = None
        self.up = None
        if j < arraysize - 1:                          #If not at right edge,
            if  boxarray[i,j] == boxarray[i,j+1]:      #And color to the right matches,
                if clusterarray[i,j+1] == 0:           #And the box to the right is not already in the cluster,
                    self.right = ClusterNode(i,j+1)    #Make the new cluster node!
        if j > 0:                                    #Ditto for left
            if  boxarray[i,j] == boxarray[i,j-1]:      
                if clusterarray[i,j-1] == 0:           
                    self.left = ClusterNode(i,j-1)    
        if i < arraysize - 1:                        #Ditto for down
            if  boxarray[i,j] == boxarray[i+1,j]:
                if clusterarray[i+1,j] == 0:  
                    self.down = ClusterNode(i+1,j)
        if i > 0:                                    #Ditto for up
            if  boxarray[i,j] == boxarray[i-1,j]:
                if clusterarray[i-1,j] == 0:  
                    self.up = ClusterNode(i-1,j)

    def propagate_color(self,color):   #Propagates the new color to every node in the cluster. Furthermore, the cluster extends to new boxes of that same color.
        boxarray[self.i,self.j] = color
        if self.right is not None:
            self.right.propagate_color(color)
        elif self.j < arraysize - 1 and boxarray[self.i,self.j+1] == color and clusterarray[self.i,self.j+1] == 0: #If the box to the right is not in the cluster and the color matches
            self.right = ClusterNode(self.i,self.j+1)                                                              #Add it to the cluster!
        if self.left is not None:
            self.left.propagate_color(color)                                                                       #Ditto for left.
        elif self.j > 0 and boxarray[self.i,self.j-1] == color and clusterarray[self.i,self.j-1] == 0:             
            self.left = ClusterNode(self.i,self.j-1)                                                              
        if self.down is not None:
            self.down.propagate_color(color)                                                                       #Ditto for down.
        elif self.i < arraysize - 1 and boxarray[self.i+1,self.j] == color and clusterarray[self.i+1,self.j] == 0:
            self.down = ClusterNode(self.i+1,self.j)
        if self.up is not None:                                                                                    
            self.up.propagate_color(color)                                                                         #Ditto for up.
        elif self.i > 0 and boxarray[self.i-1,self.j] == color and clusterarray[self.i-1,self.j] == 0:
            self.up = ClusterNode(self.i-1,self.j)
        

#Define Functions

def display():
    '''Displays the colored boxes to the screen'''
    screen.fill((0,0,0))    #clear screen first!
    for i in range(arraysize):
        for j in range(arraysize):
            rectangle = (j*boxsize,i*boxsize,boxsize,boxsize) #(upperleft_x,upperleft_y,width,height)
            color = colors[boxarray[i][j]]         
            pygame.draw.rect(screen,color,rectangle,0)

    ######This part displays the text in the HUD. This part is a bit hacky and could be refactored.
    font = pygame.font.Font(None, 36)
    text = 7*[0]
    textpos = 7*[0]
    text[0] = font.render("Moves: %d" % nummoves, 1, (255, 255, 255))
    textpos[0] = text[0].get_rect()
    textpos[0].bottomright = screen.get_rect().bottomright
    screen.blit(text[0], textpos[0])

    for color in range(1,7):
        text[color] = font.render("%d  " % color, 1, colors[color])
        textpos[color] = text[color].get_rect()
        if color == 1:
            textpos[color].bottomleft = screen.get_rect().bottomleft
        else:
            textpos[color].bottomleft = textpos[color-1].bottomright
        screen.blit(text[color],textpos[color])
    ####
    pygame.display.update()

def victory():
    '''Displays victory screen'''
    screen.fill((0,0,0))    #clear screen first!
    font = pygame.font.Font(None, 30)  # Display the victory message
    text = font.render("You flooded-it in %d moves!" % nummoves, 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    textpos.centery = screen.get_rect().centery
    screen.blit(text, textpos)

    pygame.display.update()

    displaying = 1
    while displaying == 1:             #One final loop. This keeps the screen up until the user clicks the close-window button.
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            displaying = 0
    

#Setup for Main Loop

running = 1     #Toggle to keep the main loop running. Will later be set to 0 to terminate the program
display()
root = ClusterNode(0,0)   #Create the initial cluster


#Main Loop

while running == 1:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    elif event.type == pygame.KEYDOWN:
        if event.unicode in ['1','2','3','4','5','6']:   #If you press one of the color keys
            root.propagate_color(int(event.unicode))     #Propagate that color!
            nummoves += 1
            display()
            if ClusterNode.clustermembers == arraysize ** 2:  #If the your cluster contains all the boxes 
                victory()                                     #Victory is yours!
                running = 0


    

        



