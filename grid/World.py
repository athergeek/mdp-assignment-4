from Tkinter import *
master = Tk()

triangle_size = 0.1
cell_score_min = -0.2
cell_score_max = 0.2
Width = 100
(x, y) = (8, 8)
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*Width, height=y*Width)
player = (0, y-1)
score = 1
restart = False
walk_reward = -0.04

walls = [(1,1), (2,2), (3, 3), (4, 4), (5,5), (6,6)]
# walls = [(1, 1), (1,2), (2, 1), (2, 2)]
specials = [(7, 1, "red", -1), (7, 0, "green", 1)]
cell_scores = {}
txt_Ids = {}


def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)


def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            board.create_text(i*Width+22 ,j*Width+12,fill="darkblue",font="Times 12 italic bold",
                        text=(i,',',j), width=0)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
            # board.create_text(i*Width+52 ,j*Width+32,fill="darkblue",font="Times 10 italic bold",
            #             text=('U:' ,temp['up'] ), width=0)            
            # board.create_text(i*Width+52 ,j*Width+42,fill="darkblue",font="Times 10 italic bold",
            #             text=('D:' ,temp['down'] ), width=0)            
            # board.create_text(i*Width+52 ,j*Width+52,fill="darkblue",font="Times 10 italic bold",
            #             text=('L:' ,temp['left'] ), width=0)            
            # board.create_text(i*Width+52 ,j*Width+62,fill="darkblue",font="Times 10 italic bold",
            #             text=('R:' ,temp['right'] ), width=0)            



    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

render_grid()


def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max
    i, j = state
    if action == "up":
        txt_Ids[str(i)+str(j)+action] = board.create_text(i*Width+52 ,j*Width+32,fill="darkblue",font="Times 8 italic bold",
            text=('U:' ,format(val,'.5f') ), width=0)            
    if action == "down":
        txt_Ids[str(i)+str(j)+action] = board.create_text(i*Width+52 ,j*Width+52,fill="darkblue",font="Times 8 italic bold",
                    text=('D:' ,format(val,'.5f') ))
    if action == "left":
        txt_Ids[str(i)+str(j)+action] = board.create_text(i*Width+52 ,j*Width+72,fill="darkblue",font="Times 8 italic bold",
                    text=('L:' ,format(val,'.5f') ))
    if action == "right":
        txt_Ids[str(i)+str(j)+action] = board.create_text(i*Width+52 ,j*Width+92,fill="darkblue",font="Times 8 italic bold",
                    text=('R:' ,format(val,'.5f') ))
    


    triangle = cell_scores[state][action]
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)


def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_x, new_y)
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            if score > 0:
                print "Success! score: ", score
            else:
                print "Fail! score: ", score
            restart = True
            return
    #print "score: ", score


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player, score, me, restart
    player = (0, y-1)
    score = 1
    restart = False
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="orange", width=1, tag="me")

board.grid(row=0, column=0)


def start_game():
    master.mainloop()
