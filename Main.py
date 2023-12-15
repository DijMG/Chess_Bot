from Creation import *
from Player_Mechanics import *
from AI_Mechanics import *
def Game_Run(Player1,Player2):
    from Creation import Pieces_Positions 
    while Game_Variables["Running_State"]:
        Screen.fill((100,100,100))
        Map_Creation(Game_Variables["Possible_Moves"])
        Figure_Creation(Pieces_Positions)
        pygame.display.update()
        pygame.time.Clock().tick(60) 
        if Game_Variables["Turn"] == "W":
            if Player1 == "Player":
                Pieces_Positions = Player_Mechanics(Pieces_Positions)
            else:
                Pieces_Positions = AI_Mechanics(Pieces_Positions)
        else:
            if Player2 == "Player":
                Pieces_Positions = Player_Mechanics(Pieces_Positions)
            else:
                Pieces_Positions = AI_Mechanics(Pieces_Positions)
Game_Run("Player","AI")
#so It doesn't automatically turn off
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()