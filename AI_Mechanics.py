from Creation import *
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
    if [King_Figure[1],King_Figure[2]] in Filtered_Moves:
        return True
    else:
        return False
def Simulate_Move(Chess_Map,old_move,new_move):
    old_index = old_move[1] * 8 + old_move[0]
    new_index = new_move[1] * 8 + new_move[0]
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
    
    Chess_Map[new_index][0] = figure_copy[0]
    Chess_Map[new_index][3] = figure_copy[3]
    #switch up ^ v
    Chess_Map[old_index][0] = ''
    Chess_Map[old_index][3] = ''
def Worthiness_Depth_Reading(Move,worthiness):
    if Move["Answer"] != None:
        for x in Move["Answer"]:
            Worthiness_Depth_Reading(x,worthiness)
    else:
        worthiness += Move["Piece_Move"][1]
    return worthiness
def Depth_Expansion(Move,Multi_Dimensional_Simulated_Chess_Map):
    #very cool recursion
    if Move["Answer"] != None:
        Piece_Position = Move["Piece"]["Piece_Position"]
        Target_Position = Move["Piece_Move"][0]
        Simulate_Move(Multi_Dimensional_Simulated_Chess_Map,Piece_Position,Target_Position)
        for x in Move["Answer"]:
            Depth_Expansion(x,Multi_Dimensional_Simulated_Chess_Map)
        return
    else:
        All_Available_Branch_Moves = Move_Collection(Multi_Dimensional_Simulated_Chess_Map,Game_Variables["Turn"],["All"])
        answers = []
        for Analysed_Branch_Move in All_Available_Branch_Moves:
            Multi_Dim_Copy = copy.deepcopy(Multi_Dimensional_Simulated_Chess_Map)
            Piece_Position = Analysed_Branch_Move["Owner"]["Piece_Position"]
            Target_Position = Analysed_Branch_Move["Move"]
            Simulate_Move(Multi_Dim_Copy,Piece_Position,Target_Position)
            if King_Danger(Multi_Dim_Copy) == False:
                Multi_Dim_Copy = copy.deepcopy(Multi_Dimensional_Simulated_Chess_Map)
                Target_Location = Analysed_Branch_Move["Move"][1]*8+Analysed_Branch_Move["Move"][0]
                answers.append(
                    {
                        "Piece":Analysed_Branch_Move["Owner"],
                        "Piece_Move":[Analysed_Branch_Move["Move"],Piece_Worthiness[Multi_Dim_Copy[Target_Location][0]]],
                        "Answer":None
                    }
                )
        Move["Answer"] = answers
        return
def AI_Mechanics(Pieces_Positions):
    if(Game_Variables["counter"] == 0):
        Game_Variables["counter"] += 1
        #searches for a missed en-passant to remove
        for Individual_Figure in Pieces_Positions:
            if Individual_Figure[0] == "E":
                if Pieces_Positions[(Individual_Figure[2]+En_Path[Game_Variables["Turn"]])*8+Individual_Figure[1]][3] == Game_Variables["Turn"]:
                    Individual_Figure[0] = ""
                    break
    #create first depth of available moves
    All_Available_Moves = Move_Collection(copy.deepcopy(Pieces_Positions),Game_Variables["Turn"],["All"])
    Depth_Array = []
    for Analysed_Move in All_Available_Moves:
        Simulated_Chess_Map = copy.deepcopy(Pieces_Positions)
        Piece_Position = Analysed_Move["Owner"]["Piece_Position"]
        Target_Position = Analysed_Move["Move"]
        Simulate_Move(Simulated_Chess_Map,Piece_Position,Target_Position)
        if King_Danger(Simulated_Chess_Map) == False:
            Simulated_Chess_Map = copy.deepcopy(Pieces_Positions)
            Target_Location = Analysed_Move["Move"][1]*8+Analysed_Move["Move"][0]
            Depth_Array.append(
                {
                    "Piece":Analysed_Move["Owner"],
                    "Piece_Move":[Analysed_Move["Move"],Piece_Worthiness[Simulated_Chess_Map[Target_Location][0]]],
                    "Answer":None
                }
            )
    Multi_Dimensional_Simulated_Chess_Map = copy.deepcopy(Pieces_Positions)
    Depth = 1
    for x in range(0,Depth):
        for Move in Depth_Array:
            Depth_Expansion(Move,Multi_Dimensional_Simulated_Chess_Map)
            #print(Move)
    
    #lazy way, still thinking on how to properly modify worthiness collecting so the moves are actually weighted
    for x in range(0,len(Depth_Array)):
        Move["Piece_Move"][1] = Worthiness_Depth_Reading(Depth_Array[x],Depth_Array[x]["Piece_Move"][1])

    #find best move worthiness
    Max_Worthiness = 0
    for Option in Depth_Array:
        print(Option)
        if Option["Piece_Move"][1] > Max_Worthiness:
            Max_Worthiness = Option["Piece_Move"][1]
    #print(Max_Worthiness)
    #get all moves with equal worthiness
    Best_Moves = []
    for Option in Depth_Array:
        if Option["Piece_Move"][1] == Max_Worthiness:
            Best_Moves.append([Option["Piece"],Option["Piece_Move"][0],Max_Worthiness])
    print("le best moves")
    for x in Best_Moves:
        print(x)
    Best_Move = Best_Moves[random.randint(0,len(Best_Moves)-1)]
    print("best",Best_Move)
    Simulate_Move(Pieces_Positions,Best_Move[0]["Piece_Position"],Best_Move[1])

    if Game_Variables["Turn"] == "W":Game_Variables["Turn"] = "B"
    else:Game_Variables["Turn"] = "W"
    return Pieces_Positions
