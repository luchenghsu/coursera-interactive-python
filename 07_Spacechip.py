# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
FONT_SIZE = 25

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def turn_counter_clockwise(self):
        self.angle_vel -= 0.1
    
    def turn_clockwise(self):
        self.angle_vel += 0.1
    
    def control_thrusters(self, thrust):
        self.thrust = thrust
       
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
        
    def shoot(self):
        global a_missile
        
        forward = angle_to_vector(self.angle)
        
        pos = [self.pos[0] + forward[0] * self.radius, 
               self.pos[1] + forward[1] * self.radius]
        
        vel = [self.vel[0] + forward[0] * 10, self.vel[1] + forward[1] * 10]
        
        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)
    
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
        if self.thrust:
            canvas.draw_image(self.image, (self.image_center[0]+90, self.image_center[1]), self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
               
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        friction = 0.02
        self.vel[0] *= (1 - friction)
        self.vel[1] *= (1 - friction)
        
        self.angle += self.angle_vel
        forward = angle_to_vector(self.angle)
        
        if self.thrust:          
            self.vel[0] += forward[0] * 0.1
            self.vel[1] += forward[1] * 0.1
     

    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
       

           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # draw lives and score
    canvas.draw_text('Lives', (FONT_SIZE*2, FONT_SIZE*2), FONT_SIZE, 'white')
    canvas.draw_text(str(lives), (FONT_SIZE*2, FONT_SIZE*3), FONT_SIZE, 'white')    
    canvas.draw_text('Score', (WIDTH-FONT_SIZE*4, FONT_SIZE*2), FONT_SIZE, 'white')
    canvas.draw_text(str(score), (WIDTH-FONT_SIZE*4, FONT_SIZE*3), FONT_SIZE, 'white')
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    random_choice = random.choice([1, -1])
    pos = (random.randrange(WIDTH), random.randrange(HEIGHT))
    vel = (random_choice, random_choice)
    ang_vel = random_choice * random.random()
    a_rock = Sprite(pos, vel, random_choice, ang_vel/10, asteroid_image, asteroid_info)
    
    

# key handlers
def keydown(key):

    if key == simplegui.KEY_MAP['left']:
        my_ship.turn_counter_clockwise()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.turn_clockwise()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.control_thrusters(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
     
def keyup(key):
    
    if key == simplegui.KEY_MAP['left']:
        my_ship.turn_clockwise()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.turn_counter_clockwise()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.control_thrusters(False)
        
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.1, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [0,0], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
