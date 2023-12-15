from __init__ import *
def Figure_Creation(Chess_Map):
    #print(Pieces_Positions)
    for Piece_Info in Chess_Map:
        if Piece_Info[0] not in ["","E"]:
            img = pygame.image.load('NeuralNetworks/AI_Projects/Images/Chess_Game/Figures/'+Piece_Info[0]+Piece_Info[3]+".png")
            Screen.blit(img,(Piece_Info[1]*75+5,Piece_Info[2]*75+5))
def Map_Creation(Possible_Moves):
        Offset_X = 0
        Offset_Y = 0
        Color = (255,244,207)
        for x in range(0,8):
            Offset_X = 0
            for y in range(0,8):
                holder = None
                if type(Possible_Moves) is list:
                    holder = Color
                    for move in Possible_Moves:
                        if move["Move"][0] == x and move["Move"][1] == y:
                            Color = (255,0,0)
                            break
                pygame.draw.rect(Screen, Color, (Offset_Y,Offset_X,75,75))
                Offset_X += 75
                if Color == (255,0,0):
                    Color = holder
                if y != 7:
                    if Color == (255,244,207):
                        Color = (100,150,100)
                    else:
                        Color = (255,244,207)
            Offset_Y += 75
def Normalize_Direction(Given_Move):
    x = 0
    y = 0
    if(Given_Move[0] > 0):
        x = 1
    elif(Given_Move[0] < 0):
        x = -1
    if(Given_Move[1] > 0):
        y = 1
    elif(Given_Move[1] < 0):
        y = -1
    return [x, y]
def Set_Direction(Supposed_Move):
    x = 0
    y = 0
    if(Game_Variables["Object_Focus"]["Position"][0] > Supposed_Move[0]):x = -1
    elif(Game_Variables["Object_Focus"]["Position"][0] < Supposed_Move[0]):x = 1
    if(Game_Variables["Object_Focus"]["Position"][1] > Supposed_Move[1]):y = -1
    elif(Game_Variables["Object_Focus"]["Position"][1] < Supposed_Move[1]):y = 1
    return [x ,y]
# for both Player_Mechanics and AI_Mechanics, collects all moves
# It passes the chess_map as an argument so you can modify a copy of It beforehand to simulate outcomes with different moves, very cool
def Move_Collection(Chess_Map,Colour_Of_Choice,Choice):
    All_Moves = []
    Figures = []
    if Choice[0] == "All":
        for Figure in Chess_Map:
            if Figure[0] not in ["","E"] and Figure[3] == Colour_Of_Choice:
                Figures.append(
                    {
                        "Piece_Type":Figure[0],
                        "Piece_Position":[Figure[1],Figure[2]],
                        "Piece_Colour":Figure[3]
                    }) 
    elif Choice[0] == "Specific":
        Figures = Choice[1]
    #print(Figures)
    for Figure in Figures:
        position = Figure["Piece_Position"]
        Current_Moveset = copy.deepcopy(Piece_Movesets[Figure["Piece_Type"]])
        if(Figure["Piece_Type"] == "P"):
            Current_Moveset = Current_Moveset[Figure["Piece_Colour"]]
            for Move in Current_Moveset:
                if(position[0]+Move[0] < 0 or position[0]+Move[0] > 7):
                    continue
                if(position[1]+Move[1] < 0 or position[1]+Move[1] > 7):
                    continue
                #If It's an attack move
                if(Move[0] != 0):
                    if(Chess_Map[ (position[1] + Move[1])*8 + (position[0]+Move[0]) ][0] != ""):
                        #if(Chess_Map[ (position[1] + Move[1])*8 + (position[0]+Move[0]) ][0] == "E"): 
                        if(Chess_Map[ (position[1] + Move[1] - En_Path[Game_Variables["Turn"]])*8 + (position[0]+Move[0]) ][0] == "P" 
                            and Chess_Map[ (position[1] + Move[1] - En_Path[Game_Variables["Turn"]])*8 + (position[0]+Move[0]) ][3] != Figure["Piece_Colour"]):
                            All_Moves.insert(0,{
                            "Owner":Figure,
                            "Move":[position[0]+Move[0],position[1]+Move[1]]
                            })
                        else:    
                            if Chess_Map[ (position[1] + Move[1])*8 + (position[0]+Move[0]) ][3] != Figure["Piece_Colour"]:
                                #print("added attack move:",Move)
                                All_Moves.insert(0,{
                                    "Owner":Figure,
                                    "Move":[position[0]+Move[0],position[1]+Move[1]]
                                })
                else:
                    if(Chess_Map[ (position[1] + Move[1])*8 + (position[0]+Move[0]) ][0] == ""):
                        if(Move[1] > 1 or Move[1] < -1):
                            if(Chess_Map[ (position[1] + round(Move[1]/2))*8 + (position[0]+Move[0]) ][0] != ""
                               or position[1] != Double_Move_Position[Figure["Piece_Colour"]]):
                                continue
                        All_Moves.insert(0,{
                            "Owner":Figure,
                            "Move":[position[0]+Move[0],position[1]+Move[1]]
                        })
        else:
            if(Current_Moveset[1] == False):
                for Move in Current_Moveset[0]:
                    #break If the move Is out of bonds
                    if(position[0]+Move[0] < 0 or position[0]+Move[0] > 7):
                        continue
                    if(position[1]+Move[1] < 0 or position[1]+Move[1] > 7):
                        continue
                    #If the move's target Isn't ally
                    if(Chess_Map[ (position[1] + Move[1])*8 + (position[0]+Move[0]) ][3] != Colour_Of_Choice):
                        All_Moves.insert(0,{
                            "Owner":Figure,
                            "Move":[position[0]+Move[0],position[1]+Move[1]]
                        })
            else:
                for Move in Current_Moveset[0]:
                    while(True):
                        #break If the move Is out of bonds
                        if(position[0]+Move[0] < 0 or position[0]+Move[0] > 7):
                            break
                        if(position[1]+Move[1] < 0 or position[1]+Move[1] > 7):
                            break
                        #appareantly this boundary test Is needed too or It's all going down, in the pawn section too..
                        if((position[1] + Move[1])*8 + (position[0]+Move[0]) < 0 or (position[1] + Move[1])*8 + (position[0]+Move[0]) > 63):
                            break
                        #If the move's target Isn't ally
                        if(Chess_Map[ (position[1] + Move[1])*8 + (position[0]+Move[0]) ][3] == ""):
                            All_Moves.insert(0,{
                                "Owner":Figure,
                                "Move":[position[0]+Move[0],position[1]+Move[1]]
                            })
                        elif(Chess_Map[ (position[1] + Move[1])*8 + (position[0]+Move[0]) ][3] != Figure["Piece_Colour"]):
                            All_Moves.insert(0,{
                                "Owner":Figure,
                                "Move":[position[0]+Move[0],position[1]+Move[1]]
                            })
                            break
                        else:
                            break
                        if(Move[0]>0):Move[0] += 1
                        elif(Move[0]<0):Move[0] -= 1
                        if(Move[1]>0):Move[1] += 1
                        elif(Move[1]<0):Move[1] -= 1   
    return All_Moves