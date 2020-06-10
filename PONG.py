# Implementation of classic arcade game Pong
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 10
ANIM_BALL_RADIUS = [3,6,9,12,10] #animation steps
anim_num = 0
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH * 0.5
HALF_PAD_HEIGHT = PAD_HEIGHT * 0.5
PADDLE_INC = 4
paddle1_move = 0
paddle1_vel = 0
paddle2_move = 0
paddle2_vel = 0
move_range = HEIGHT - (2 * HALF_PAD_HEIGHT)
min_range_limit = HALF_PAD_HEIGHT
max_range_limit = HEIGHT - HALF_PAD_HEIGHT
score1= 0
score2= 0
score_limit = 3
is_game_ended = False
countdown = 4
countdown_text = ""
is_playing = False
title = "PONG"
title_size = 40
blurb = 'An "Interactive Programming With Python" Mini-Project - Rice University'
blurb_size = 15
credit = "Programmed by Brenton Wright"
credit_size = 15
delay_counter = 0 
delay_size = 1 # delay in secs
volley_counter = 0
mult = 0
paddle_extra_length = 8 # Distance added to paddle Top and Bottom, to HIT BALL when it looks like it SHOULD HIT IT
direction = "Random"

# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = [WIDTH * 0.5, HEIGHT * 0.5]
vel = [0.0, 0.0]
 
def check_if_random_direction():
    global direction
    if direction == "Random":
        #ADD random in here
        rand = random.randrange(0,2)
        if rand == 0:
            direction = "Left"
        else:
            direction = "Right"
    
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction, mult): # Mult used to increase difficulty during gameplay. See Ramp Difficulty.
    global ball_pos, vel
    if direction == "Left":
        ball_pos[0] -= vel[0] *mult # Negative VEL X pushes circle to the LEFT
        ball_pos[1] -= vel[1] *mult # Negative VEL Y MOVES UP; 
    elif direction == "Right":
        ball_pos[0] += vel[0] *mult # Positive VEL X pushes circle to the RIGHT
        ball_pos[1] -= vel[1] *mult # Negative VEL Y goes -Y MOVES UP; 

# define event handlers
def unlock_paddles():
    global is_game_ended
    is_game_ended = False #unlocks paddles - allows move
    
def play_score_delay():
    score_delay_timer.start()

def reset_countdown_timer():
    global countdown, countdown_text
    countdown = 4 #resetting countdown
    countdown_text = ""
    
def reset_ball():
    #resets ball position
    global ball_pos, vel,anim_num, volley_counter 
    ball_pos = [WIDTH* 0.5, HEIGHT * 0.5]
    vel = [0,0]
    volley_counter = 0
    #print "Resetting Volley Counter"
    anim_num = 0
    ball_anim_timer.start()
    
def reset_ball_offscreen():
    #resets ball position
    global ball_pos, vel,anim_num, BALL_RADIUS 
    ball_pos = [WIDTH* 0.5, HEIGHT * 0.5]
    BALL_RADIUS = 1
    vel = [0,0]
    anim_num = 0
    
def reset_game():
    global  paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, is_game_ended  # these are numbers
    unlock_paddles()
    # reset countdown
    countdown = 4 #resetting countdown
       
    #resets paddles to center
    paddle1_vel=0
    create_paddle1_list() 
    paddle2_vel=0
    create_paddle2_list() 
    
    #resets scores
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    reset_ball()
    
    #reset direction
    direction = "Random"
    
def play_game():
    global is_game_ended, vel
    unlock_paddles()
    vel = [2,1] # move ball
    
def new_game(): # plays next set
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, vel
    ball_pos = [WIDTH* 0.5, HEIGHT * 0.5]
    vel = [2,1]
    
def end_game():
    global is_game_ended, is_playing, vel
    is_game_ended = True # LOCKS paddles if True. Controlle in Draw(Canvas) function
    is_playing = False
    vel = [0,0] #pauses ball
    score_delay_timer.stop()

def create_paddle1_list():
    global paddle1_pos
    paddle1_pos = [0, (HEIGHT* 0.5 - HALF_PAD_HEIGHT) -paddle1_vel], [PAD_WIDTH, (HEIGHT* 0.5 - HALF_PAD_HEIGHT)-paddle1_vel], [PAD_WIDTH, (HEIGHT* 0.5 + HALF_PAD_HEIGHT)-paddle1_vel], [0, (HEIGHT* 0.5 + HALF_PAD_HEIGHT)-paddle1_vel]
    return paddle1_pos

def create_paddle2_list():
    global paddle2_pos
    paddle2_pos = [WIDTH,(HEIGHT* 0.5 - HALF_PAD_HEIGHT) -paddle2_vel],[WIDTH - PAD_WIDTH, (HEIGHT* 0.5 - HALF_PAD_HEIGHT) -paddle2_vel], [WIDTH - PAD_WIDTH, (HEIGHT* 0.5 + HALF_PAD_HEIGHT) -paddle2_vel],[WIDTH, (HEIGHT* 0.5 + HALF_PAD_HEIGHT) -paddle2_vel]
    return paddle2_pos

def draw(canvas):
    global mult, direction, paddle_extra_length, volley_counter, score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle1_move, paddle2_vel, paddle2_move, vel, is_game_ended, is_playing
    # draw mid line and gutters
    canvas.draw_line([WIDTH * 0.5, 0],[WIDTH * 0.5, HEIGHT], 4, "YellowGreen")
    canvas.draw_circle((WIDTH * 0.5, HEIGHT * 0.5), 100, 4, "YellowGreen")
    canvas.draw_line([HALF_PAD_WIDTH, 0],[HALF_PAD_WIDTH, HEIGHT], PAD_WIDTH, "DarkSlateGrey")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, 0],[WIDTH - HALF_PAD_WIDTH, HEIGHT], PAD_WIDTH, "DarkSlateGrey")
    
    #Draw Title - When not playing
    if is_playing == False:
        title_width = frame.get_canvas_textwidth(title, title_size) # gets text width to align centered below ie: (width * 0.5)
        canvas.draw_text(title, ((WIDTH * 0.5) - (title_width * 0.5), HEIGHT * 0.5 + 150), title_size, 'White', 'sans-serif')
    
        blurb_width = frame.get_canvas_textwidth(blurb, blurb_size) 
        canvas.draw_text(blurb, ((WIDTH * 0.5) - (blurb_width * 0.5), HEIGHT * 0.5 + 170), blurb_size, 'White', 'sans-serif')

        credit_width = frame.get_canvas_textwidth(credit, credit_size) 
        canvas.draw_text(credit, ((WIDTH * 0.5) - (credit_width * 0.5), HEIGHT * 0.5 + 188), credit_size, 'White', 'sans-serif')
    
    #countdown display - controlled by timer
    if countdown >=0:
        width = frame.get_canvas_textwidth(countdown_text, 100) # gets text width to align centered below ie: (width * 0.5)
        canvas.draw_text(str(countdown_text), ((WIDTH * 0.5) - (width * 0.5), HEIGHT * 0.90), 100, 'White', 'sans-serif')
    
    #prevent paddle move if ENDGAME
    if is_game_ended == True:
        paddle1_move = 0
        paddle2_move = 0
    
    # collide and reflect off of TOP of canvas
    if ball_pos[1] <= BALL_RADIUS:
        vel[1] = - vel[1]
    
    # collide and reflect off of BOTTOM of canvas
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        vel[1] = - vel[1]
        
    # collide with LEFT gutter
    if (ball_pos[0] <= 0 + PAD_WIDTH + BALL_RADIUS):
        # determine whether paddle and ball collide
        if (ball_pos[1] > (paddle1_pos[0][1] - paddle_extra_length)) and (ball_pos[1] < (paddle1_pos[3][1] + paddle_extra_length) and (is_game_ended == False)):
            vel[0] = - vel[0] #relect ball
            volley_counter +=1
        else:
            if(score2 < score_limit ): # Compare Score with ScoreLimit: if score2 is under score_limit, then
                score2 = score2 +1 #increment Player 2 Score
                direction = "Right" #As RIGHT wins, spawn next ball towards Right
                if(score2 < score_limit): #if score2 is still LESS than score_limit
                    reset_ball_offscreen() #Hack to fix ball remaining in gutter
                    score_delay_timer.start()
            else:
                end_game()
                width = frame.get_canvas_textwidth('Player 2 Wins', 50)
                canvas.draw_text('Player 2 Wins', ((WIDTH * 0.5) - (width* 0.5), HEIGHT * 0.5 + 15), 50, 'White', 'sans-serif') # NOte: 15 = Vertical Text Offset

    # collide with RIGHT gutter
    if (ball_pos[0] >= WIDTH - PAD_WIDTH - (BALL_RADIUS)):
        # determine whether paddle and ball collide
        if (ball_pos[1] > (paddle2_pos[0][1] - paddle_extra_length)) and (ball_pos[1] < (paddle2_pos[3][1] + paddle_extra_length) and (is_game_ended == False)): 
            vel[0] = - vel[0] #reflect ball
            volley_counter +=1
        else:
            if(score1 < score_limit ): # Compare Score with ScoreLimit: if score2 is under score_limit, then
                score1 = score1 +1 #increment Player 2 Score
                direction = "Left" #As LEFT wins, spawn next ball towards Left
                if(score1 < score_limit): #if score2 is still LESS than score_limit
                    reset_ball_offscreen() #Hack to fix ball remaining in gutter
                    score_delay_timer.start()
                    
            else:
                end_game()
                width = frame.get_canvas_textwidth('Player 1 Wins', 50)
                canvas.draw_text('Player 1 Wins', ((WIDTH * 0.5) - (width* 0.5), HEIGHT * 0.5 + 15), 50, 'White', 'sans-serif')
        
    #Ramp difficulty with amount of volleys
    if (volley_counter <= 4):
        if mult != 1.5:
            mult = 1.5
            #print mult
    elif (volley_counter > 4) and (volley_counter <= 8):
        if mult != 2:
            mult = 2
            #print mult
    elif (volley_counter > 8) and (volley_counter <= 12) :
        if mult != 2.5:
            mult = 2.5
            #print mult
    elif (volley_counter > 12) and (volley_counter <= 16) :
        if mult != 3:
            mult = 3
            #print mult
    elif (volley_counter > 16) and (volley_counter <= 20) :
        if mult != 3.5:
            mult = 3.5
            #print mult
    elif (volley_counter > 20) :
        if mult != 4:
            mult = 4
            #print mult
    
    check_if_random_direction()
    spawn_ball(direction, mult) # update ball using Multiple to increase speed
    
    if anim_num >0: #using a timer to control when Ball is drawn, allowing Anim-in and out
        canvas.draw_circle((ball_pos), BALL_RADIUS, 1, 'White','White') # draw ball
       
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos = create_paddle1_list()
    paddle2_pos = create_paddle2_list()  
    if(paddle1_pos[0][1] > 0) and (paddle1_pos[3][1] <= HEIGHT): #draw if button held
        paddle1_vel += paddle1_move
        
    if(paddle2_pos[0][1] > 0) and (paddle2_pos[3][1] <= HEIGHT): #draw if button held
        paddle2_vel += paddle2_move
    
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 1, 'White','White')
    canvas.draw_polygon(paddle2_pos, 1, 'White','White')
        
    # draw scores
    canvas.draw_text(str(score1), (WIDTH / 4 - 20 , HEIGHT / 4), 100, 'White', 'sans-serif')
    canvas.draw_text(str(score2), ((WIDTH / 4) * 3 -20, HEIGHT / 4), 100, 'White', 'sans-serif')

    #Change Button Text from Play to Restart, if game going.
    if is_playing == True:
        play_button.set_text("RESTART GAME") 
    else:
        play_button.set_text("PLAY GAME") 
    
def keydown(key):
    global paddle1_vel, paddle2_vel, paddle1_move, paddle2_move
    if is_game_ended == False: #if END GAME - no key input
        if key == simplegui.KEY_MAP["W"] and (paddle1_pos[0][1] > 0):
                paddle1_move = PADDLE_INC
                paddle1_vel += paddle1_move     
        if key == simplegui.KEY_MAP["S"] and (paddle1_pos[3][1] <= HEIGHT):
                paddle1_move = -PADDLE_INC
                paddle1_vel += paddle1_move
        if key == simplegui.KEY_MAP["up"] and (paddle2_pos[0][1] > 0):
                paddle2_move = PADDLE_INC
                paddle2_vel += paddle2_move     
        if key == simplegui.KEY_MAP["down"] and (paddle2_pos[3][1] <= HEIGHT):
                paddle2_move = -PADDLE_INC
                paddle2_vel += paddle2_move  

def keyup(key):
    global paddle1_vel, paddle2_vel, paddle1_move, paddle2_move
    if key == simplegui.KEY_MAP["W"]:
            paddle1_move = 0
    elif key == simplegui.KEY_MAP["S"]:
            paddle1_move = 0
    elif key == simplegui.KEY_MAP["up"]:
            paddle2_move = 0
    elif key == simplegui.KEY_MAP["down"]:
            paddle2_move = 0

def play_button_handler():
    global is_playing
    reset_game()
    countdown_timer.start()
    is_playing = True
    
def countdown_timer_handler():
    global countdown, countdown_text
    
    if countdown > 1:
        countdown -=1
        countdown_text = str(countdown)
    elif countdown == 1:
        countdown -=1
        countdown_text = "GO"
    else:
        countdown = 0
        countdown_timer.stop()
        countdown_text = ""
        if is_game_ended == True:
            play_game()
        else:
            new_game()
    
def ball_anim_timer_handler():
    global BALL_RADIUS, anim_num
    if anim_num < len(ANIM_BALL_RADIUS):
        anim_num += 1
        BALL_RADIUS = ANIM_BALL_RADIUS[anim_num - 1]
    else:
        ball_anim_timer.stop()

def score_delay_timer_handler():
    """ Runs A counter when a Score is made. Allows time to play Goal animation before New game starts"""
    global delay_counter
    if delay_counter < delay_size:
        delay_counter +=1
    else:
        delay_counter = 0 #reset
        score_delay_timer.stop()
        reset_ball()
        reset_countdown_timer()
        countdown_timer.start()
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background("ForestGreen")
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
play_button = frame.add_button('Play', play_button_handler)

#register Timer
countdown_timer = simplegui.create_timer(1000, countdown_timer_handler)
ball_anim_timer = simplegui.create_timer(15, ball_anim_timer_handler)
score_delay_timer = simplegui.create_timer(500, score_delay_timer_handler)

# start frame
is_game_ended = True #locks controls until PLAY button pressed
frame.start() 
unlock_paddles()