import pygame
import random
import copy
pygame.init()
pygame.display.set_caption('Chess')
Screen = pygame.display.set_mode((850, 600))
Screen.fill((100,100,100))
Game_Variables = {
        'Turn':"W", 
        'Object_Focus':None,
        'Running_State':True,
        'Possible_Moves':None,
        "counter":0
    }
#old me reversed the indexes on accident and realised It far too late, current me also realised It far too late
Pieces_Positions = [
    ["R",0,0,"B"],["H",1,0,"B"],["B",2,0,"B"],["Q",3,0,"B"],["K",4,0,"B"],["B",5,0,"B"],["H",6,0,"B"],["R",7,0,"B"],
    ["P",0,1,"B"],["P",1,1,"B"],["P",2,1,"B"],["P",3,1,"B"],["P",4,1,"B"],["P",5,1,"B"],["P",6,1,"B"],["P",7,1,"B"],
    ["",0,2,""],["",1,2,""],["",2,2,""],["",3,2,""],["",4,2,""],["",5,2,""],["",6,2,""],["",7,2,""],
    ["",0,3,""],["",1,3,""],["",2,3,""],["",3,3,""],["",4,3,""],["",5,3,""],["",6,3,""],["",7,3,""],
    ["",0,4,""],["",1,4,""],["",2,4,""],["",3,4,""],["",4,4,""],["",5,4,""],["",6,4,""],["",7,4,""],
    ["",0,5,""],["",1,5,""],["",2,5,""],["",3,5,""],["",4,5,""],["",5,5,""],["",6,5,""],["",7,5,""],
    ["P",0,6,"W"],["P",1,6,"W"],["P",2,6,"W"],["P",3,6,"W"],["P",4,6,"W"],["P",5,6,"W"],["P",6,6,"W"],["P",7,6,"W"],
    ["R",0,7,"W"],["H",1,7,"W"],["B",2,7,"W"],["Q",3,7,"W"],["K",4,7,"W"],["B",5,7,"W"],["H",6,7,"W"],["R",7,7,"W"]
]
Castling_Bools = {
    "W":{
        "L":True,
        "R":True
    },
    "B":{
        "L":True,
        "R":True
    }
}
Piece_Movesets = {
    "H":[[[-1,-2],[1,-2],[2,-1],[2,1],[1,2],[-1,2],[-2,1],[-2,-1]],False], # table of moves' offsets by x,y , bool deciding whether It's 1x or infinite range
    "B":[[[-1,-1],[1,-1],[-1,1],[1,1]],True],
    "R":[[[-1,0],[0,-1],[1,0],[0,1]],True],
    "Q":[[[-1,-1],[1,-1],[-1,1],[1,1],[-1,0],[0,-1],[1,0],[0,1]],True],
    "K":[[[-1,-1],[1,-1],[-1,1],[1,1],[-1,0],[0,-1],[1,0],[0,1]],False],
    "P":{
        "W":[[-1,-1],[1,-1],[0,-1],[0,-2]],
        "B":[[-1,1],[1,1],[0,1],[0,2]]
    }
}
Piece_Worthiness = {
    "P":1,
    "H":3,
    "B":3,
    "R":5,
    "Q":9,
    "K":10,
    '':0,
    "E":0
}
# For En_passant so I don't need to add a whooping 1 IF 
En_Path = {
    "B":1,
    "W":-1
}
Double_Move_Position = {
    "W":6,
    "B":1
}