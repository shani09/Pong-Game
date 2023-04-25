# Implementation of classic arcade game Pong

import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]

paddle1_pos = 0
paddle2_pos = 0
paddle1_vel = 0
paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    
    ball_vel[0] = random.randrange(100, 200)/50
    ball_vel[1] = random.randrange(100, 300)/50
    
    if direction == RIGHT:
        ball_vel[0] =  ball_vel[0] * -1
        ball_vel[1] =  ball_vel[1] * -1

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if (ball_pos[1] - BALL_RADIUS) < 0:
        ball_vel[1] = -1 * ball_vel[1]
    if (ball_pos[1] + BALL_RADIUS) > HEIGHT:
        ball_vel[1] = -1 * ball_vel[1]    
        
    # draw ball
    canvas.draw_circle([ball_pos[0], ball_pos[1]], 17, 3, "White", "Blue")
    
    # update paddle's vertical position, keep paddle on the screen
    if (HEIGHT/-2 + HALF_PAD_HEIGHT) <= (paddle1_pos + paddle1_vel) <= (HEIGHT/2 - HALF_PAD_HEIGHT + 2):
        paddle1_pos += paddle1_vel
    if (HEIGHT/-2 + HALF_PAD_HEIGHT) <= (paddle2_pos + paddle2_vel) <= (HEIGHT/2 - HALF_PAD_HEIGHT + 2):
        paddle2_pos += paddle2_vel
     
    # draw paddles
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT + paddle1_pos], [WIDTH - HALF_PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT + paddle1_pos], PAD_WIDTH, "Yellow") 
    canvas.draw_line([HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT + paddle2_pos], [HALF_PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT + paddle2_pos], PAD_WIDTH, "Lime") 
    
    # determine whether paddle and ball collide or gutters
    x_condition_p1 = [float(ball_pos[0] + BALL_RADIUS), float(WIDTH - PAD_WIDTH)] 
    y_condition_p1 = [float(ball_pos[1]), float(HEIGHT/2 - HALF_PAD_HEIGHT + paddle1_pos), float(HEIGHT/2 + HALF_PAD_HEIGHT + paddle1_pos)]
    
    x_condition_p2 = [float(ball_pos[0] - BALL_RADIUS), float(PAD_WIDTH)] 
    y_condition_p2 = [float(ball_pos[1]), float(HEIGHT/2 - HALF_PAD_HEIGHT + paddle2_pos), float(HEIGHT/2 + HALF_PAD_HEIGHT + paddle2_pos)]
    
    if (x_condition_p1[0] > x_condition_p1[1]) and (y_condition_p1[1] < y_condition_p1[0] < y_condition_p1[2]):
        ball_vel[0] = -1.1 * ball_vel[0]
        ball_vel[1] = 1.1 * ball_vel[1]      
    elif (x_condition_p2[0] < x_condition_p2[1]) and (y_condition_p2[1] < y_condition_p2[0] < y_condition_p2[2]):
        ball_vel[0] = -1.1 * ball_vel[0]
        ball_vel[1] = 1.1 * ball_vel[1]       
    elif x_condition_p1[0] > (WIDTH - PAD_WIDTH):
        score1 += 1
        spawn_ball(RIGHT)
    elif x_condition_p2[0] < 0:
        score2 += 1
        spawn_ball(LEFT)
    
    # draw scores
    canvas.draw_text(str(score2), (WIDTH - PAD_WIDTH - WIDTH/4 , 60) , 36 , "White", "sans-serif")
    canvas.draw_text(str(score1), (WIDTH/2 - PAD_WIDTH - WIDTH/4, 60), 36 , "White", "sans-serif")
    
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle1_vel += 4
    elif key == simplegui.KEY_MAP["up"]:
        paddle1_vel -= 4
    
    if key == simplegui.KEY_MAP["s"]:
        paddle2_vel += 4
    elif key == simplegui.KEY_MAP["w"]:
        paddle2_vel -= 4
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle1_vel -= 4
    elif key == simplegui.KEY_MAP["up"]:
        paddle1_vel += 4
    
    if key == simplegui.KEY_MAP["s"]:
        paddle2_vel -= 4
    elif key == simplegui.KEY_MAP["w"]:
        paddle2_vel += 4

# reset button
def reset_game():
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    score1 = 0
    score2 = 0
    paddle1_pos = 0
    paddle2_pos = 0	
    paddle1_vel = 0
    paddle2_vel = 0
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart game', reset_game, 100)

# start frame
new_game()
frame.start()

