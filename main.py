import pygame
import math
import random


width,height = 800,600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.init()

class Mass(pygame.sprite.Sprite):

    def __init__(self,group, x, y, radius, mass, sun = False, initial_speed = True):

        pygame.sprite.Sprite.__init__(self)

        self.sun = sun
        self.radius = radius
        self.pos = pygame.Vector2(x,y)
        self.group:pygame.sprite.Group = group
        self.vel = pygame.Vector2(0,0)
        self.mass = mass
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.line_points = [(self.pos.x, self.pos.y), (self.pos.x, self.pos.y)]
        self.thrust_power = 0.1
        self.dead = False

        # find the perpidicular vector to the sun object
        if not sun and initial_speed:
            self.perp = pygame.Vector2(self.pos.x - width/2, self.pos.y - height/2)
            self.perp.rotate_ip(90)
            self.perp.scale_to_length(1)
            self.init_vel = random.random() * 10
            self.vel += self.perp * 7

    def draw(self):
        
        # if(len(self.line_points) > 500): self.line_points.pop(0)
        if(self.dead): return

        pygame.draw.circle(screen, self.color, (self.pos.x, self.pos.y), self.radius)
        pygame.draw.lines(screen, self.color, False, self.line_points, 1)

        #write the mass of the ball in the center of the ball
        font = pygame.font.SysFont('Arial', self.radius)
        text = font.render(str(self.mass), True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (self.pos.x, self.pos.y)
        screen.blit(text, textRect)


    def update(self):

        if(self.dead): return

        self.apply_gravity()

        if(self.vel.x != 0 or self.vel.y != 0):
            self.line_points.append((self.pos.x, self.pos.y))
        
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y


        self.check_out_of_universe()


    def apply_gravity(self):

        for other in self.group:

            if(other == self): continue

            distance = self.pos.distance_to(other.pos)

            if(distance <= (self.radius + other.radius)/20):
                merged_mass = Mass(self.group, self.pos.x, self.pos.y, self.radius, self.mass + other.mass, sun = False, initial_speed = False)
                merged_mass.vel = ((self.vel * self.mass) + (other.vel * other.mass)) / (self.mass + other.mass)
                merged_mass.line_points = self.line_points + other.line_points
                other.dead = True
                self.dead = True
                self.kill()
                other.kill()
                self.group.add(merged_mass)
                break
            else:
                accel = (other.mass / (distance ** 2)) * 0.01

                angle = math.atan2(other.pos.y - self.pos.y, other.pos.x - self.pos.x)

                self.vel.x += math.cos(angle) * accel
                self.vel.y += math.sin(angle) * accel

    def check_out_of_universe(self):

        if(self.pos.distance_to(pygame.Vector2(width/2, height/2)) > 1500):
            self.kill()


mass_group = pygame.sprite.Group()

# sun = Mass(mass_group, width/2, height/2, 50, 1e6, sun = True)
# mass_group.add(sun)

# for i in range(10):

#     distance_from_sun = 150 + i*25

#     angle = random.randrange(0, 6)

#     x = width/2 + distance_from_sun * math.cos(angle)
#     y = height/2 + distance_from_sun * math.sin(angle)

#     mass = Mass(mass_group, x, y, random.randint(5,15), random.randrange(10,150), initial_speed=True)
#     mass_group.add(mass)


mass1 = Mass(mass_group, width/3, height/2, 50, 4.25e4, sun = False, initial_speed = False)
mass2 = Mass(mass_group, 2*width/3, height/2, 50, 4.25e4, sun = False, initial_speed = False)

mass1.vel = pygame.Vector2(1,0)
mass2.vel = pygame.Vector2(-1,0)
mass1.vel.rotate_ip(45)
mass2.vel.rotate_ip(45)

mass_group.add(mass1)
mass_group.add(mass2)

def watermark():
    
    font = pygame.font.SysFont('Arial', 20)
    text_1 = font.render('Mohamad Chahadeh, 2023', True, (0,0,0))
    text_2 = font.render('https://mochahadeh.com/', True, (0,0,0))
    textRect_1 = text_1.get_rect()
    textRect_2 = text_2.get_rect()
    textRect_2.bottomleft = (10, height-10)
    textRect_1.bottomleft = (10, height-30)
    screen.blit(text_1, textRect_1)
    screen.blit(text_2, textRect_2)


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                THRUST_APPLIED = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                THRUST_APPLIED = False

    screen.fill((150,150,150))

    mass_group.update()
    for mass in mass_group:
        mass.draw()

    watermark()

    pygame.display.update()
    clock.tick(60)