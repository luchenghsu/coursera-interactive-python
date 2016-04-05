import simplegui

# define global variables
t = 0
success = 0
attempts = 0
is_timer_running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    return str((t/10/10/6) % 10) + ":" + str((t/10/10) % 6) + str((t/10) % 10) +"."+str(t % 10)
    
def counter_format(success , attempts):
    return str(success) + "/" + str(attempts)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global is_timer_running
   
    if is_timer_running == False:
        timer.start()
        
    is_timer_running = True

def stop_handler():
    
    global is_timer_running
    global success 
    global attempts
       
    if is_timer_running == True:
        timer.stop()
        attempts = attempts + 1
        if t % 10 == 0:
            success = success + 1
    
    is_timer_running = False
        

def reset_handler():
    global t
    global success
    global attempts
    t = 0
    success = 0
    attempts = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global t
    t = t + 1

timer = simplegui.create_timer(100, timer_handler)


# define draw handler
def draw(canvas):
    canvas.draw_text(format(t), (35, 110), 48, 'White')
    canvas.draw_text(counter_format(success, attempts), (150, 20), 24, 'Green')
    
    
# create frame
frame = simplegui.create_frame('Stopwatch', 200, 200)
start = frame.add_button('Start', start_handler, 100)
stop = frame.add_button('Stop', stop_handler, 100)
reset = frame.add_button('Reset', reset_handler, 100)

# register event handlers
frame.set_draw_handler(draw)

# start frame
frame.start()


# Please remember to review the grading rubric
