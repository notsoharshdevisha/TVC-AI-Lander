import pygame
import os
import math

'''
    up: vel=neg acc=neg
    down: vel=pos acc=pos

'''


# window and refresh rate
WIDTH, HEIGHT = 900, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
#rocket initial position
ROCKET_X = 450
ROCKET_Y = 25
ROCKET_POS =(ROCKET_X, ROCKET_Y)
ROCKET_WIDTH = 50
ROCKET_HEIGHT = 90
# rocket image 
ROCKET_IMG = pygame.image.load(os.path.join('assets', 'rocket.png'))
ROCKET = pygame.transform.scale(ROCKET_IMG, (ROCKET_WIDTH, ROCKET_HEIGHT))
#window background
background = ('#9dedbf')


class Rocket:
    def __init__(self, rocket_img, pos, width, height):
        self.img = rocket_img
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
        self.rocket_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.mass = float(3000)
        self.com = (self.width/2, self.height/2)
        self.angle = float(0)
        self.v_y = float(0)
        self.v_x = float(0)
        self.thrust = float(30000)
        self.thrust_angle = float(math.radians(6))
        self.rapid_unscheduled_disassembly = False


    def position(self, time):
        self.v_y = ((-self.thrust/self.mass * math.cos(self.thrust_angle)) + 9.8) * time
        self.v_x = (-self.thrust/self.mass*math.sin(self.thrust_angle)) * time
        self.x += self.v_x * time + (1/2) * ((-self.thrust/self.mass) * math.sin(self.thrust_angle)) * time**2
        self.y += (self.v_y * time + (1/2) * ((-self.thrust/self.mass) * math.cos(self.thrust_angle) + 9.8) * time**2)
        return self.x, self.y

    def angle_pos(self, time):
        # solid cylinder: mr^2/2
        inertia = (self.mass * (self.width/2)**2)/2 
        d = self.height - self.com[1]
        torque = -(d * self.thrust * math.sin(self.thrust_angle))
        alpha = torque/inertia
        self.angle += alpha * time
        return None

def draw_window(rocket, time):
    pos_x, pos_y = rocket.position(time)
#    print(f"v_x: {rocket.v_x}, v_y: {rocket.v_y}")
#    print(f"x: {pos_x}, y: {pos_y}")
    WIN.fill(background)
    WIN.blit(rocket.img, (pos_x, pos_y))
    pygame.draw.circle(WIN, (255, 0, 0), (pos_x+rocket.com[0], pos_y+rocket.com[1]), 4)
#    print(f"com: {pos_x+rocket.com[0], pos_y+rocket.com[1]}")
    pygame.display.update()


def main():

    pygame.display.set_caption("LandAI")

    rocket = Rocket(ROCKET, ROCKET_POS, ROCKET_WIDTH, ROCKET_HEIGHT)

    clock = pygame.time.Clock()

    run = not rocket.rapid_unscheduled_disassembly

    while run:
        clock.tick(FPS)
        time = float(pygame.time.get_ticks()/1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               run = False 

        draw_window(rocket, time)

    pygame.quit()


if __name__ == "__main__":
    main()
