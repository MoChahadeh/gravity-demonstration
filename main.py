import pygame
import math
import random


width,height = 800,600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.init()

class Mass(pygame.sprite.Sprite):

    def __init__(self,group, x, y, radius, mass, sun = False):

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

        # find the perpidicular vector to the sun object
        if not sun:
            self.perp = pygame.Vector2(self.pos.x - width/2, self.pos.y - height/2)
            self.perp.rotate_ip(90)
            self.perp.scale_to_length(1)
            self.init_vel = random.random() * 10
            self.vel += self.perp * 7

    def draw(self):
        
        pygame.draw.circle(screen, self.color, (self.pos.x, self.pos.y), self.radius)
        pygame.draw.lines(screen, self.color, False, self.line_points, 1)

        #write the mass of the ball in the center of the ball
        font = pygame.font.SysFont('Arial', self.radius)
        text = font.render(str(self.mass), True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (self.pos.x, self.pos.y)
        screen.blit(text, textRect)


    def update(self):

        self.apply_gravity()
        self.draw()

        if(self.vel.x != 0 or self.vel.y != 0):
            self.line_points.append((self.pos.x, self.pos.y))
        
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y


        self.check_out_of_universe()


    def apply_gravity(self):

        for other in [x for x in self.group.sprites() if x != self]:

            distance = self.pos.distance_to(other.pos)

            accel = (other.mass / (distance ** 2)) * 0.01

            angle = math.atan2(other.pos.y - self.pos.y, other.pos.x - self.pos.x)

            self.vel.x += math.cos(angle) * accel
            self.vel.y += math.sin(angle) * accel

    def check_out_of_universe(self):

        if(self.pos.distance_to(pygame.Vector2(width/2, height/2)) > 1500):
            self.kill()


mass_group = pygame.sprite.Group()

sun = Mass(mass_group, width/2, height/2, 50, 1e6, sun = True)
mass_group.add(sun)

for i in range(8):

    distance_from_sun = 150 + i*25

    angle = random.randrange(0, 6)

    x = width/2 + distance_from_sun * math.cos(angle)
    y = height/2 + distance_from_sun * math.sin(angle)

    mass = Mass(mass_group, x, y, random.randint(5,15), random.randrange(10,100))
    mass_group.add(mass)


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

    pygame.display.update()
    clock.tick(15)