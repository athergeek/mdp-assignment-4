import World
import threading
import time
import random
import numpy as np

discount = 0.3
actions = World.actions
states = []
Q = {}
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0.1
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp

for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)


def do_action(action):
    s = World.player
    r = -World.score
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score
    return s, action, r, s2


def max_Q(s):
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc
    # print "State::: ",s,"Action ::::",a ,"Q: ", Q[s][a]
    World.board.delete(World.txt_Ids[str(s[0])+str(s[1])+a])
    World.set_cell_score(s, a, Q[s][a])


def run():
    global discount
    exploration_rate = 1
    max_exploration_rate = 1
    min_exploration_rate = 0.01
    exploration_decay_rate = 0.001    
    time.sleep(1)
    alpha = 1
    t = 1
    episodes = 1
    while True:
        # Pick the right action
        s = World.player
        max_act, max_val = max_Q(s)

        # Exploration-exploitation trade-off
        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold > exploration_rate:
            # Exploit if threshold is greater then exploration rate
            (s, a, r, s2) = do_action(max_act)
        else:
            # Keep exploring env with random sample action
            # action = env.action_space.sample()
            index = random.randint(0, 3)
            (s, a, r, s2) = do_action(World.actions[index])            

        

        # Update Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + discount * max_val)

        # Exploration rate decay propotional to the current value
        exploration_rate = min_exploration_rate + \
            (max_exploration_rate - min_exploration_rate) * \
            np.exp(-exploration_decay_rate * episodes)        

        # Check if the game has restarted
        t += 1.0
        if World.has_restarted():
            World.restart_game()
            time.sleep(0.01)
            print "episodes::: ",episodes,"iteration ::::",t             
            episodes = episodes + 1
            t = 1.0

        # Update the learning rate
        alpha = pow(t, -0.1)
        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(0.1)


t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()
