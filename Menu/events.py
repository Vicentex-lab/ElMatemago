import colisiones as colision

def eventos():
        global player_f
        global player_c
        if colision.maze[player_f][player_c] == 2:
                    if player_f==14 and player_c==0:
                        player_f=13
                        player_c=18
                        print("Matemagicamente Teletransportado")
                        
                    if player_f==13 and player_c==19:
                        player_f=14
                        player_c=1
                        print("Matemagicamente Teletransportado")