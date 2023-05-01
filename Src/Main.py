import pygame
import pygame.gfxdraw
import random
from scipy.spatial import Delaunay
import numpy as np

# initialize Pygame
pygame.init()

# set screen dimensions
screen_width = 1200
screen_height = 1000

# create Pygame screen
screen = pygame.display.set_mode((screen_width, screen_height))


# set up clock for controlling FPS
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# set up colors
white = (255, 255, 255)
BackGroundColour = (27, 30, 43)
pointColour = (0, 0, 0)
lineColour = (255,255,255)
delta_time = 1

zoom = 1


def addFpsCounter():
    fps = str(int(clock.get_fps()))
    fps_text = font.render("FPS: " + fps, True, (0, 255, 0))
    # draw FPS text to top left corner of screen
    screen.blit(fps_text, (10, 10))
    
def addPointMarker(point,text=" <--",):
    markerText = font.render(text, True, (255, 0, 0))
    # draw FPS text to top left corner of screen
    screen.blit(markerText, point)
    
def createPoints(num_points = 3):
    # set up random points
    points = []
    for i in range(num_points):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        point = [x, y]
        points.append(point)
    return points

def AddInitialVelocities(num_points):
    velocities = []
    for i in range(num_points):
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)
        velocity = [dx, dy]
        velocities.append(velocity)
    return velocities

def CreatePointSizes(num_points, avarageSize= 8, maxSize = 1):
    PointSizes = []
    for i in range(num_points):
        PointSizes.append(random.normalvariate(avarageSize,maxSize))
    return PointSizes

def DrawPoints(points, num_points, pointColour,pointSizes,zoom =1):
    for i in range(num_points):
        pygame.gfxdraw.filled_circle(screen, int(points[i][0]), int(points[i][1]), int(pointSizes[i]),pointColour)
        pygame.gfxdraw.aacircle(screen, int(points[i][0]), int(points[i][1]), int(pointSizes[i]),pointColour)
        #pygame.draw.circle(screen, pointColour, (int(points[i][0]), int(points[i][1])), int(pointSizes[i]))
        
def update_points(points, velocities, dt, screen_width, screen_height, point_radius):
    for i in range(len(points)):
        # Update position based on velocity
        points[i][0] += velocities[i][0] * dt
        points[i][1] += velocities[i][1] * dt

        # Check for collision with screen edges
        if points[i][0] - point_radius < 0:
            points[i][0] = point_radius
            velocities[i][0] = abs(velocities[i][0])
        elif points[i][0] + point_radius > screen_width:
            points[i][0] = screen_width - point_radius
            velocities[i][0] = -abs(velocities[i][0])

        if points[i][1] - point_radius < 0:
            points[i][1] = point_radius
            velocities[i][1] = abs(velocities[i][1])
        elif points[i][1] + point_radius > screen_height:
            points[i][1] = screen_height - point_radius
            velocities[i][1] = -abs(velocities[i][1])


PointLocations = createPoints(100)
num_points = len(PointLocations)
PointVelocities = AddInitialVelocities(num_points)
pointSizes = CreatePointSizes(num_points)

# set up initial velocities for points

# set up main game loop
running = True
while running:

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill screen with white
    screen.fill(BackGroundColour)
    

    
    # update point positions

    update_points(PointLocations,PointVelocities,delta_time,screen_width,screen_height,8)

    # draw Delaunay triangulation of points
    tri = Delaunay(PointLocations)
    
    
        
    for simplex in tri.simplices:
        poly = [PointLocations[simplex[0]],PointLocations[simplex[1]],PointLocations[simplex[1]],PointLocations[simplex[2]],PointLocations[simplex[2]],PointLocations[simplex[0]]]
        avarageY = (PointLocations[simplex[0]][1] + PointLocations[simplex[1]][1] + PointLocations[simplex[2]][1]) / 3
        
        lineColour = (255-int(255*avarageY/screen_height),int(255*avarageY/screen_height),0)
        pygame.gfxdraw.filled_polygon(screen,poly,lineColour)

    # draw points as small circles
    DrawPoints(PointLocations,num_points,pointColour,pointSizes)
    
    addPointMarker(PointLocations[0])
    addFpsCounter()

    # update screen
    pygame.display.update()

    # control FPS
    delta_time = (clock.tick(100000) / 30)

# quit Pygame
pygame.quit()
