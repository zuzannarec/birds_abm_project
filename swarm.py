import pygame, os, math, time, random
import pygame.locals

pygame.init()

# set the width and height of the screen
width = 1000
height = 1000

center_x = width / 2
center_y = height / 2

no_of_birds = 60

position_spread = 10000
speed_spread = 3
max_speed = 5

border = 100
leader_border = 200
border_speed_change = 0.2

min_dist = 10.0
match_speed_window = 40.0

leader_random_speed_change = 0.2
leader_max_speed = 5.0

barriers = [[450,500],[475,500],[500,500],[525,500],[625,500],[650,500],[675,500],[700,500],[400,500],[425,500],[400,525],[400,550],[400,650],[400,675],[400,700],[375,700],[350,700],[325,700],[300,700],[275,700],[250,700],[800,200],[250,700],[100,100]]
barrier_radius = 15

size = [width, height]
screen = pygame.display.set_mode(size)

# This makes the normal mouse pointer invisible in graphics window
pygame.mouse.set_visible(0)

birdlist = []
food = None

# Generate leader bird
leaderbirdx = 300.0
leaderbirdy = 300.0
leaderbirdvx = 4.0
leaderbirdvy = 0.0

# Generate birds
i = 0
food_closest = None
while (i < no_of_birds):
    x = random.uniform(center_x - position_spread, center_x + position_spread)
    y = random.uniform(center_y - position_spread, center_y + position_spread)
    vx = random.uniform(-speed_spread, speed_spread)
    vy = random.uniform(-speed_spread, speed_spread)
    
    newbird = [x, y, vx, vy]

    birdlist.append(newbird)
    i += 1

quit_pressed = False

while not quit_pressed:

    screen.fill((0,0,0))
    # Randomly place food on a screen

    if food is None:
        if random.uniform(0,1) < 0.01:
            fx = random.uniform(0,1000)
            fy = random.uniform(0,1000)
            food = [int(fx), int(fy)]
            pygame.draw.circle(screen, (100, 200, 100), food, 7)
    else:
        pygame.draw.circle(screen, (100, 200, 100), food, 7)
        if min_food_dist < 10.0:
            food = None

    if food_closest is not None:
        leaderbirdx = birdlist[food_closest][0]
        leaderbirdy = birdlist[food_closest][1]
        leaderbirdvx = birdlist[food_closest][2]
        leaderbirdvy = birdlist[food_closest][3]


    # Update leader bird position and speed
    if (leaderbirdx < leader_border):
        leaderbirdvx += border_speed_change
    if (leaderbirdy < leader_border):
        leaderbirdvy += border_speed_change
    if (leaderbirdx > width - leader_border):
        leaderbirdvx -= border_speed_change
    if (leaderbirdy > height - leader_border):
        leaderbirdvy -= border_speed_change


    # Draw leaderbird and update
    # pygame.draw.circle(screen, (255,0,255), (int(leaderbirdx), int(leaderbirdy)), 5, 0)
    leaderbirdvx += random.uniform(-leader_random_speed_change, leader_random_speed_change)
    leaderbirdvy += random.uniform(-leader_random_speed_change, leader_random_speed_change)


    # Cap maximum speed
    speed = math.sqrt(leaderbirdvx*leaderbirdvx + leaderbirdvy*leaderbirdvy)
    if (speed > leader_max_speed):
        leaderbirdvx = leaderbirdvx * leader_max_speed / speed
        leaderbirdvy = leaderbirdvy * leader_max_speed / speed


    leaderbirdx += leaderbirdvx
    leaderbirdy += leaderbirdvy

    # Draw birds, positions and speeds
    i = 0
    min_food_dist = 2000
    while (i < no_of_birds):

        # Make copies for clarity
        x = birdlist[i][0]
        y = birdlist[i][1]
        vx = birdlist[i][2]
        vy = birdlist[i][3]

        colr = int(float(i) * 255.0 / no_of_birds)
        colg = int((no_of_birds - float(i)) * 255.0 / no_of_birds)
        colb = 255
        
        pygame.draw.circle(screen, (colr,colg,colb), (int(x), int(y)), 2, 0)

        # Birds move away from border
        if (x < border):
            vx += border_speed_change
        if (y < border):
            vy += border_speed_change
        if (x > width - border):
            vx -= border_speed_change
        if (y > height - border):
            vy -= border_speed_change

        # Birds move towards leader bird
        leaderdiffx = leaderbirdx - x
        leaderdiffy = leaderbirdy - y
        vx += 0.007 * leaderdiffx
        vy += 0.007 * leaderdiffy

        # Birds calculate distance to food
        if food is not None:
            food_dist = math.sqrt(math.pow(x - food[0], 2) + math.pow(y - food[1], 2))
            if food_dist < min_food_dist:
                min_food_dist = food_dist
                food_closest = i

        # Move away from other nearby birds
        # Also calculate average velocity of birds in larger window
        j = 0
        # For calculating average velocity of other birds
        avxtotal = 0
        avytotal = 0
        avcount = 0
        while (j < no_of_birds):
            if (j != i):
                dx = birdlist[j][0] - x
                dy = birdlist[j][1] - y
                dist = math.sqrt(dx*dx + dy*dy)
                if (dist < min_dist):
                    vx -= dx * 0.2
                    vy -= dy * 0.2
                if (dist < match_speed_window):
                    avxtotal += birdlist[j][2]
                    avytotal += birdlist[j][3]
                    avcount += 1
            j += 1
        # Match to average velocity of nearby birds
        if (avcount != 0):
            avx = avxtotal / avcount
            avy = avytotal / avcount
            vx = 0.9 * vx + 0.1 * avx
            vy = 0.9 * vy + 0.1 * avy

        # Bounce off obstacles and slow down
        for barrier in barriers:
            dx = barrier[0] - x
            dy = barrier[1] - y
            dist = math.sqrt(dx*dx + dy*dy)
            if (dist < barrier_radius + 15):
                vx -= dx * 0.1
                vx *= 0.6
                vy -= dy * 0.1
                vy *= 0.6
                
        # Cap maximum speed
        speed = math.sqrt(vx*vx + vy*vy)
        if (speed > max_speed):
            vx = vx * max_speed / speed
            vy = vy * max_speed / speed

        # Update positions according to speeds
        birdlist[i][0] += vx
        birdlist[i][1] += vy
        birdlist[i][2] = vx
        birdlist[i][3] = vy
        i += 1

    for barrier in barriers:
        pygame.draw.circle(screen, (0,100,255), (int(barrier[0]), int(barrier[1])), barrier_radius, 0)

    #time.sleep(0.1)
    pygame.display.flip()
    i += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_pressed = True
