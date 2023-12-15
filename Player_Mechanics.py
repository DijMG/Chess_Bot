from Creation import *
def Castling_Shanenigans(result): #fourth parameter doesn't wanna cooperate when It's a purely simulated move without player_legal_move..? Im just gonna code It raw
    if(Game_Variables["Turn"] == "W"):
        Simulate_Move(Pieces_Positions,result[1][0],result[1][1],[4,7]) # king move
        if result[0][0] == 63:
            Simulate_Move(Pieces_Positions,result[0][0],result[0][1],[7,7]) # rook move
            Pieces_Positions[62][1] = 6
            Pieces_Positions[62][2] = 7
            Pieces_Positions[61][1] = 5
            Pieces_Positions[61][2] = 7
        else:
            Simulate_Move(Pieces_Positions,result[0][0],result[0][1],[0,7]) # rook move
            Pieces_Positions[59][1] = 3
            Pieces_Positions[59][2] = 7
            Pieces_Positions[58][1] = 2
            Pieces_Positions[58][2] = 7
            Pieces_Positions[57][1] = 1
            Pieces_Positions[57][2] = 7
    else:
        Simulate_Move(Pieces_Positions,result[1][0],result[1][1],[4,0]) # king move
        if result[0][0] == 0:
            Simulate_Move(Pieces_Positions,result[0][0],result[0][1],[0,0]) # rook move
            Pieces_Positions[1][1] = 1
            Pieces_Positions[1][2] = 0
            Pieces_Positions[2][1] = 2
            Pieces_Positions[2][2] = 0
            Pieces_Positions[3][1] = 3
            Pieces_Positions[3][2] = 0
        else:
            Simulate_Move(Pieces_Positions,result[0][0],result[0][1],[7,0]) # rook move
            Pieces_Positions[5][1] = 5
            Pieces_Positions[5][2] = 0
            Pieces_Positions[6][1] = 6
            Pieces_Positions[6][2] = 0
def King_Danger(Chess_Map):
    King_Figure = None
    for Figure in Chess_Map:
        if Figure[0] == "K" and Figure[3] == Game_Variables["Turn"]:
            King_Figure = Figure
            break
    Reverse_Colour = None
    if Game_Variables["Turn"] == "W":Reverse_Colour = "B"
    else:Reverse_Colour = "W"
    All_Enemy_Attack_Moves = Move_Collection(copy.deepcopy(Chess_Map),Reverse_Colour,["All"])
    Filtered_Moves = []
    for Bracket in All_Enemy_Attack_Moves:
        Filtered_Moves.append(Bracket["Move"])
        #print(Bracket)
    if [King_Figure[1],King_Figure[2]] in Filtered_Moves:
        return True
    else:
        return False
def Simulate_Move(Chess_Map,old_index,new_index,old_position):
    figure_copy = copy.deepcopy(Chess_Map[old_index])
    if(figure_copy[0] == "P"):
        if(Game_Variables["Turn"] == "W"):
            if(new_index >= 0 and new_index <= 7):
                figure_copy[0] = "Q"
        else:
            if(new_index >= 55 and new_index <= 63):
                figure_copy[0] = "Q"
    #En-Passant removal
    if(Chess_Map[new_index][0] == "E"):
        Chess_Map[new_index-(En_Path[Game_Variables["Turn"]])*8][0] = ""
        Chess_Map[new_index-(En_Path[Game_Variables["Turn"]])*8][3] = ""
    
    Chess_Map[new_index] = figure_copy
    Chess_Map[new_index][1] = round(Chess_Map[new_index][1])
    Chess_Map[new_index][2] = round(Chess_Map[new_index][2])
    #switch up ^ v
    Chess_Map[old_index] = ['',old_position[0],old_position[1],'']
    Chess_Map[old_index][1] = old_position[0]
    Chess_Map[old_index][2] = old_position[1]
    #Info = [former move, used figure, index of the supposed move]
def Player_Legal_Move(Chess_Map,Info): # for simulating player moves and giving true/false feedback
    current_move = Info[0]
    current_figure = Info[1]
    Supposed_Move = [round(Chess_Map[Info[2]][1]),round(Chess_Map[Info[2]][2])]
    Current_Moveset = Piece_Movesets[current_figure[0]]
    Appropriate_Move = False
    #castling conditions
    castling_info = {
        "W":{
            "07":["L",[56,57,58],[[56,59],[57,58]]], # first for association, second are the requirements, given indexes must be empty for successful castling
            "77":["R",[61,62],[[63,61],[60,62]]],   # third being positions rook & king going from & to
        },
        "B":{
            "00":["R",[1,2,3],[[0,3],[4,2]]],
            "70":["L",[5,6],[[7,5],[4,6]]]
        }
    }
    if(current_figure[0] == "K"):
        #if move Is directed on one of the rooks
        castle_move = False
        try:
            castling_info[Game_Variables["Turn"]][str(Supposed_Move[0])+str(Supposed_Move[1])]
            castle_move = True
        except:castle_move = False # just so there's something there
        if castle_move == True:
            if(castling_info[Game_Variables["Turn"]][str(Supposed_Move[0])+str(Supposed_Move[1])][0] in ["R","L"]):
                can_castle = castling_info[Game_Variables["Turn"]][str(Supposed_Move[0])+str(Supposed_Move[1])][2]
                for hopefully_empty_index in castling_info[Game_Variables["Turn"]][str(Supposed_Move[0])+str(Supposed_Move[1])][1]:
                    if Chess_Map[hopefully_empty_index][0] != "":
                        can_castle = False
                return can_castle
    #if target Is an ally
    if(Chess_Map[Supposed_Move[1]*8+Supposed_Move[0]][3] == Game_Variables["Turn"]):
        return Appropriate_Move
    Move_Direction = Set_Direction(Supposed_Move)
    if(current_figure[0] == "P"):
        Current_Moveset = copy.deepcopy(Current_Moveset[Game_Variables["Turn"]])
        #going back/sideways DECLINED
        if(current_figure[1] == "W" and Move_Direction[1] >= 0 or
           current_figure[1] == "B" and Move_Direction[1] <= 0):
            return Appropriate_Move
        #double move insert
        if((current_figure[1] == "W" and current_move[1] == 6) or (current_figure[1] == "B" and current_move[1] == 1) ):
            if  Chess_Map[(current_move[1] + Move_Direction[1])*8+(current_move[0] + Move_Direction[0])][3] == "":
                Current_Moveset.insert(0,[0,Current_Moveset[2][1]*2])

        for Move in Current_Moveset:
            if (current_move[0] + Move[0] == Supposed_Move[0] and current_move[1] + Move[1] == Supposed_Move[1]):
                #if(Chess_Map[(current_move[1] + Move_Direction[1])*8+(current_move[0] + Move_Direction[0])][0] == "E"):
                if(Move_Direction[0] != 0):
                    if(Chess_Map[(current_move[1] + Move_Direction[1])*8+(current_move[0] + Move_Direction[0])][3] in {"",Game_Variables["Turn"]}
                       and Chess_Map[(current_move[1] + Move_Direction[1])*8+(current_move[0] + Move_Direction[0])][0] != "E"
                       ):
                        return False
                    else:
                
                        Appropriate_Move = True
                        return Appropriate_Move
                else:
                    #single forward
                    if(Move[1] == 1 or Move[1] == -1):
                        if(Chess_Map[(current_move[1] + Move[1])*8+(current_move[0] + Move[0])][3] != ""):
                            return False
                    else:
                        #double forward
                        #En-Passant insert, a half-object (has a figure name but doesn't have a colour, which makes It attackable by the enemy yet doesn't act 
                        # as a physical figure that would block some attacks)
                        if(Chess_Map[(current_move[1] + round(Move[1]/2))*8+(current_move[0] + Move[0])][3] == ""
                           and current_move[1] == Double_Move_Position[Game_Variables["Turn"]]):
                                Chess_Map[(current_move[1] + Move_Direction[1])*8+(current_move[0] + Move_Direction[0])][0] = "E"
                        else:
                            return False
                Appropriate_Move = True
                return Appropriate_Move
    elif(current_figure[0] == "H"):
        for Move in Current_Moveset[0]:
            if (current_move[0] + Move[0] == Supposed_Move[0] and current_move[1] + Move[1] == Supposed_Move[1]):
                Appropriate_Move = True
                break
    else:
        if Current_Moveset[1] == False:
            if (current_move[0] + Move_Direction[0] == Supposed_Move[0] and current_move[1] + Move_Direction[1] == Supposed_Move[1]):
                Appropriate_Move = True
                return Appropriate_Move
        else:
            #keeps going the direction of the move until the move Is reached, pretty cool
            while(True):
                # If something Is In path
                if(Move_Direction[0] > 0 or Move_Direction[0] < 0 or Move_Direction[1] > 0 or Move_Direction[1] < 0):
                    if (Chess_Map[(current_move[1] + Move_Direction[1])*8+current_move[0] + Move_Direction[0]][0] != ""
                        and Chess_Map[(current_move[1] + Move_Direction[1])*8+current_move[0] + Move_Direction[0]][0] != "E"
                        and (current_move[0] + Move_Direction[0] != Supposed_Move[0] or current_move[1] + Move_Direction[1] != Supposed_Move[1])):
                        return False
                #out of range
                if((current_move[0] + Move_Direction[0] < 0 or current_move[0] + Move_Direction[0] > 7 or current_move[1] + Move_Direction[1] < 0 or current_move[1] + Move_Direction[1] > 7)):
                    return Appropriate_Move
                #movement 
                if (current_move[0] + Move_Direction[0] == Supposed_Move[0] 
                    and current_move[1] + Move_Direction[1] == Supposed_Move[1]
                    and Normalize_Direction(Move_Direction) in Current_Moveset[0]
                    ):
                    Appropriate_Move = True
                    return Appropriate_Move
                if(Move_Direction[0] < 0):Move_Direction[0] -= 1
                elif(Move_Direction[0] > 0):Move_Direction[0] += 1
                if(Move_Direction[1] < 0):Move_Direction[1] -= 1
                elif(Move_Direction[1] > 0):Move_Direction[1] += 1
    return Appropriate_Move
def Player_Mechanics(Pieces_Positions):
    global Redo
    Redo = False
    global old_chess_map
    #if(Game_Variables["counter"] == 0):
        #Game_Variables["counter"] += 1
        #searches for a missed en-passant to remove
    for Individual_Figure in Pieces_Positions:
        if Individual_Figure[0] == "E":
            if Pieces_Positions[(Individual_Figure[2]+En_Path[Game_Variables["Turn"]])*8+Individual_Figure[1]][3] == Game_Variables["Turn"]:
                print("removed en-passant")
                Individual_Figure[0] = ""
                break
    #close
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:
            Game_Variables["Running_State"] = False
        #full process of legalizing/unleashing/reverting moves, kinda messy
        if event.type == pygame.MOUSEBUTTONUP:
            Game_Variables["Possible_Moves"] = None
            if(Game_Variables["Object_Focus"] != None):
                old_index = Game_Variables["Object_Focus"]["Index"]
                Piece_Move_Info = [Game_Variables["Object_Focus"]["Position"],Game_Variables["Object_Focus"]["Figure"],Game_Variables["Object_Focus"]["Index"]]
                result = Player_Legal_Move(Pieces_Positions,Piece_Move_Info)
                if(result == True):
                    new_index = round(Pieces_Positions[Game_Variables["Object_Focus"]["Index"]][2])*8 + round(Pieces_Positions[Game_Variables["Object_Focus"]["Index"]][1])
                    #print(old_index,new_index,Game_Variables["Object_Focus"]["Position"])
                    Simulate_Move(Pieces_Positions,old_index,new_index,Game_Variables["Object_Focus"]["Position"])
                    #check whether own king Is under attack afterwards, revert the state If so
                    if King_Danger(Pieces_Positions) == True:
                        #if(Pieces_Positions == old_chess_map):
                            #print("we are not so different, spiderman")
                        Pieces_Positions = old_chess_map
                        #print("KING UNDER ATTACK")
                        Redo = True
                    else:
                        #disable castlings
                        Castling_Switch = [
                            [["R",0,0,"B"],["B","R"]],
                            [["R",7,0,"B"],["B","L"]],
                            [["R",0,7,"W"],["W","L"]],
                            [["R",7,7,"W"],["W","R"]],
                        ]
                        for castling in Castling_Switch:
                            if ([Game_Variables["Object_Focus"]["Figure"][0],Game_Variables["Object_Focus"]["Position"][0],
                                Game_Variables["Object_Focus"]["Position"][1],Game_Variables["Object_Focus"]["Figure"][1]] == castling[0]):
                                Castling_Bools[castling[1][0]][castling[1][1]] = False
                        if([Game_Variables["Object_Focus"]["Figure"][0],Game_Variables["Object_Focus"]["Position"][0],
                            Game_Variables["Object_Focus"]["Position"][1],Game_Variables["Object_Focus"]["Figure"][1]] == ["K",4,0,"B"]):
                            Castling_Bools["B"]["L"] = False
                            Castling_Bools["B"]["R"] = False
                        elif([Game_Variables["Object_Focus"]["Figure"][0],Game_Variables["Object_Focus"]["Position"][0],
                            Game_Variables["Object_Focus"]["Position"][1],Game_Variables["Object_Focus"]["Figure"][1]] == ["K",4,7,"W"]):
                            Castling_Bools["W"]["L"] = False
                            Castling_Bools["W"]["R"] = False
                        #switch turn   
                        if Game_Variables["Turn"] == "W":Game_Variables["Turn"] = "B"
                        else:Game_Variables["Turn"] = "W"
                        Game_Variables["counter"] = 0
                elif result == False:
                    Pieces_Positions[old_index][1] = Game_Variables["Object_Focus"]["Position"][0] # Game_Variables["Object_Focus"]["Position"] being old position
                    Pieces_Positions[old_index][2] = Game_Variables["Object_Focus"]["Position"][1]
                #castling scenario
                else:
                    Castling_Shanenigans(result)
                    if King_Danger(Pieces_Positions) == True:
                        Pieces_Positions = old_chess_map
                        Redo = True
                    else:
                        Castling_Bools[Game_Variables["Turn"]]["L"] = False
                        Castling_Bools[Game_Variables["Turn"]]["R"] = False
                        if Game_Variables["Turn"] == "W":Game_Variables["Turn"] = "B"
                        else:Game_Variables["Turn"] = "W"
            Game_Variables["Object_Focus"] = None
        #set the target piece
        if event.type == pygame.MOUSEBUTTONDOWN:
            Coordinate_X,Coordinate_Y = event.pos
            Coordinate_X = Coordinate_X/75
            Coordinate_Y = Coordinate_Y/75
            Fixed_Coordinate_X = Coordinate_X - Coordinate_X % 1
            Fixed_Coordinate_Y = Coordinate_Y - Coordinate_Y % 1
            for Individual_Figure in Pieces_Positions:
                if([Individual_Figure[1],Individual_Figure[2]] == [Fixed_Coordinate_X,Fixed_Coordinate_Y] and Game_Variables["Turn"] == Individual_Figure[3]):
                    old_chess_map = copy.deepcopy(Pieces_Positions)
                    Game_Variables["Object_Focus"] = {
                        "Figure":[Individual_Figure[0],Individual_Figure[3]],
                        "Position":[copy.copy(Individual_Figure[1]),copy.copy(Individual_Figure[2])],
                        "Index":Individual_Figure[2]*8 + Individual_Figure[1] 
                    }
                    break
        #move around the target piece
        if event.type == pygame.MOUSEMOTION and Game_Variables["Object_Focus"] != None:
            #show ALL available moves for the controlled figure
            Available_Moves = Move_Collection(copy.deepcopy(Pieces_Positions),Game_Variables["Turn"],["Specific",[{
                    #Ughh
                    "Piece_Type":Game_Variables["Object_Focus"]["Figure"][0],
                    "Piece_Position":[Game_Variables["Object_Focus"]["Position"][0],Game_Variables["Object_Focus"]["Position"][1]],
                    "Piece_Colour":Game_Variables["Object_Focus"]["Figure"][1]
                }]])
            #simulate and filter every move whether It's actually viable
            Saved_Real_Figure_Info = copy.deepcopy(Game_Variables["Object_Focus"])
            To_Remove_Moves = []
            for Viable_Move in Available_Moves:
                Simulated_Chess_Map = copy.deepcopy(Pieces_Positions)
                Piece_Move_Info = [
                    Viable_Move["Owner"]["Piece_Position"],
                    [Viable_Move["Owner"]["Piece_Type"],Viable_Move["Owner"]["Piece_Colour"]],
                    Viable_Move["Move"][1]*8+Viable_Move["Move"][0]
                    ]
                if(Player_Legal_Move(Simulated_Chess_Map,Piece_Move_Info) == True):
                    old_index = Viable_Move["Owner"]["Piece_Position"][1]*8+Viable_Move["Owner"]["Piece_Position"][0]
                    new_index = Viable_Move["Move"][1]*8+Viable_Move["Move"][0]
                    Simulate_Move(Simulated_Chess_Map,old_index,new_index,Viable_Move["Owner"]["Piece_Position"])
                    if King_Danger(Simulated_Chess_Map) == True:
                        To_Remove_Moves.insert(0,Viable_Move)
            Game_Variables["Object_Focus"] = Saved_Real_Figure_Info
            Available_Moves = [move for move in Available_Moves if move not in To_Remove_Moves]
            Game_Variables["Possible_Moves"] = Available_Moves
            Pieces_Positions[Game_Variables["Object_Focus"]["Index"]][1] += event.rel[0]/75
            Pieces_Positions[Game_Variables["Object_Focus"]["Index"]][2] += event.rel[1]/75
    if Redo == True:
        Game_Variables["Object_Focus"] = None
        Game_Variables["counter"] = 0
        Game_Variables["Possible_Moves"] = None
    return Pieces_Positions