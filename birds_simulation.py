import math, random
import pygame.locals
import numpy as np

pygame.init()

width = 1500
height = 1000
size = [width, height]
screen = pygame.display.set_mode(size)
# Make the mouse pointer invisible one the screen
pygame.mouse.set_visible(0)

center_x = width / 2
center_y = height / 2

barriers = [[500, 160], [500, 180], [500, 200], [640, 360], [640, 380], [640, 400], [800, 640], [800, 660], [800, 680]]
barrier_radius = 15

no_of_birds = 60
no_of_birds2 = 20
speed_spread = 2
max_speed = 6
max_speed2 = 10

border = 100
leader_border = 200
border_speed_change = 0.2
border2 = 100
leader_border2 = 200
border_speed_change2 = 0.2

min_dist_between_species = 30.0
min_dist = 15.0
neighbourhood_area = 70.0
min_dist2 = 15.0
naighbourhood_area2 = 70.0

leader_random_speed_change = 0.2
leader_max_speed = 6.0
leader_random_speed_change2 = 0.2
leader_max_speed2 = 10.0

birdlist = []
birdlist2 = []
food = None
predator = None

# Generate leader bird
leaderbirdx = 800.0
leaderbirdy = 300.0
leaderbirdvx = 4.0
leaderbirdvy = 4.0
leaderbirdx2 = 600.0
leaderbirdy2 = 600.0
leaderbirdvx2 = -4.0
leaderbirdvy2 = 0.0

# Generate birds
i = 0
k = 0
food_closest = None
predator_farthest = None
food_closest2 = None

while (i < no_of_birds):
    x = random.uniform(center_x, width)
    y = random.uniform(0, height)
    vx = random.uniform(-speed_spread, speed_spread)
    vy = random.uniform(-speed_spread, speed_spread)
    added_bird = [x, y, vx, vy]
    birdlist.append(added_bird)
    i += 1
while (k < no_of_birds2):
    x2 = random.uniform(0, center_x)
    y2 = random.uniform(0, height)
    vx2 = random.uniform(-speed_spread, speed_spread)
    vy2 = random.uniform(-speed_spread, speed_spread)
    added_bird2 = [x2, y2, vx2, vy2]
    birdlist2.append(added_bird2)
    k += 1

quit_pressed = False
iterator = 0
while not quit_pressed:
    # Set screen background
    screen.fill((102, 153, 255))
    iterator += 1

# -------------------------------------------------------------------------------------------
# Birds reproduction section
# -------------------------------------------------------------------------------------------
    # Breed new bird
    if iterator%500 == 0:
        x_new_bird = leaderbirdx
        y_new_bird = leaderbirdy
        vx_new_bird = random.uniform(-speed_spread, speed_spread)
        vy_new_bird = random.uniform(-speed_spread, speed_spread)
        newbirdn = [x_new_bird, y_new_bird, vx_new_bird, vy_new_bird]
        birdlist.append(newbirdn)

# -------------------------------------------------------------------------------------------
# Food section
# -------------------------------------------------------------------------------------------
    # Randomly place food on the screen
    if food is not None:
        pygame.draw.circle(screen, (0, 100, 0), food, 12)
        if min_food_dist < 10.0 or min_food_dist2 < 20.0:
            food = None

# -------------------------------------------------------------------------------------------
# Predator section
# -------------------------------------------------------------------------------------------
    # Randomly place predator on the screen and manage its velocity
    if predator is not None:
        # Update predator position and speed
        if (predator[0] < leader_border):
            predator[2] += border_speed_change
        if (predator[1] < leader_border):
            predator[3] += border_speed_change
        if (predator[0] > width - leader_border):
            predator[2] -= border_speed_change
        if (predator[1] > height - leader_border):
            predator[3] -= border_speed_change
        predator[2] += random.uniform(-leader_random_speed_change, leader_random_speed_change)
        predator[3] += random.uniform(-leader_random_speed_change, leader_random_speed_change)
        # Cap maximum speed of predator
        speed = math.sqrt(math.pow(predator[2], 2) + math.pow(predator[3], 2))
        if (speed > leader_max_speed):
            predator[2] = leaderbirdvx * leader_max_speed / speed
            predator[3] = leaderbirdvy * leader_max_speed / speed
        predator[0] += predator[2]
        predator[1] += predator[3]
        # Draw predator
        pygame.draw.circle(screen, (204, 0, 0), [np.int64(predator[0]), np.int64(predator[1])], 15)

# -------------------------------------------------------------------------------------------
# Birds section
# -------------------------------------------------------------------------------------------
    # Set leader bird to bird that has biggest distance to predator
    if predator_farthest is not None and predator is not None:
        leaderbirdx = birdlist[predator_farthest][0]
        leaderbirdy = birdlist[predator_farthest][1]
        leaderbirdvx = birdlist[predator_farthest][2]
        leaderbirdvy = birdlist[predator_farthest][3]

    # Set leader bird to bird that has smallest distance to food
    # (it counts when there's no predator, running away from predator has higher priority
    if food_closest is not None and predator is None:
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
    leaderbirdvx += random.uniform(-leader_random_speed_change, leader_random_speed_change)
    leaderbirdvy += random.uniform(-leader_random_speed_change, leader_random_speed_change)
    # Cap maximum speed of leader bird
    speed = math.sqrt(leaderbirdvx*leaderbirdvx + leaderbirdvy*leaderbirdvy)
    if (speed > leader_max_speed):
        leaderbirdvx = leaderbirdvx * leader_max_speed / speed
        leaderbirdvy = leaderbirdvy * leader_max_speed / speed
    leaderbirdx += leaderbirdvx
    leaderbirdy += leaderbirdvy

    # Draw birds, positions and speeds
    i = 0
    min_food_dist = 1500
    max_predator_dist = 0
    while (i < len(birdlist)):
        # Make copies for clarity
        x = birdlist[i][0]
        y = birdlist[i][1]
        vx = birdlist[i][2]
        vy = birdlist[i][3]
        # Set colors of birds
        colr = 0.0
        colg = 0.0
        colb = 0.0
        # Draw birds
        pygame.draw.circle(screen, (colr, colg, colb), (np.int64(x), np.int64(y)), 4, 0)

        # Birds move towards leader bird
        leaderdiffx = leaderbirdx - x
        leaderdiffy = leaderbirdy - y
        vx += 0.007 * leaderdiffx
        vy += 0.007 * leaderdiffy

        # Birds calculate distance to food
        if food is not None and predator is None:
            food_dist = math.sqrt(math.pow(x - food[0], 2) + math.pow(y - food[1], 2))
            if food_dist < min_food_dist:
                min_food_dist = food_dist
                food_closest = i
        # Birds calculate distance from predator
        if predator is not None:
            predator_dist = math.sqrt(math.pow(x - predator[0], 2) + math.pow(y - predator[1], 2))
            if predator_dist > max_predator_dist:
                max_predator_dist = predator_dist
                predator_farthest = i

        # Calculate average velocity of other birds
        # Bird moves away from neighbours that are too close
        j = 0
        avxtotal = 0
        avytotal = 0
        avcount = 0
        while (j < no_of_birds):
            if (j != i):
                dx = birdlist[j][0] - x  # x-distance between current i-th bird and j-th bird
                dy = birdlist[j][1] - y  # y-distance between current i-th bird and j-th bird
                dist = math.sqrt(dx * dx + dy * dy)  # euclidean distance
                # if distance is smaller than minimum distance birds move away from each other
                if (dist < min_dist):
                    vx -= dx * 0.3
                    vy -= dy * 0.3
                # sum up velocities of nearby birds and counts them
                if (dist < neighbourhood_area):
                    avxtotal += birdlist[j][2]
                    avytotal += birdlist[j][3]
                    avcount += 1
            j += 1
        # Match to average velocity of nearby birds
        if (avcount != 0):
            avx = avxtotal / avcount
            avy = avytotal / avcount
            vx = 0.9 * vx + 0.1 * avx # Add x average velocity component to x-velocity
            vy = 0.9 * vy + 0.1 * avy # Add y average velocity component to y-velocity

        # Birds bounce off obstacles and slow down
        for barrier in barriers:
            dx = barrier[0] - x
            dy = barrier[1] - y
            dist = math.sqrt(dx*dx + dy*dy)
            if (dist < barrier_radius + 15):
                vx -= dx * 0.1
                vx *= 0.6 # Slow down
                vy -= dy * 0.1
                vy *= 0.6 # Slow down
        # Birds avoid birds of other species
        for one in range(len(birdlist)):
            for two in range(len(birdlist2)):
                dx2_dx1 = birdlist2[two][0] - birdlist[one][0]  # x-distance between current i-th bird and j-th bird
                dy2_dy1 = birdlist2[two][1] - birdlist[one][1]  # y-distance between current i-th bird and j-th bird
                dist2_1 = math.sqrt(dx2_dx1 * dx2_dx1 + dy2_dy1 * dy2_dy1)  # euclidean distance
                # if distance is smaller than minimum distance birds move away from each other
                if (dist2_1 < min_dist_between_species):
                    vx -= dx * 0.8
                    vx *= 10.0
                    vy -= dy * 0.8
                    vy *= 10.0

        # Birds bound off bounds of screen window
        if x >= width + 100:
            vx -= x * 0.1
            vx *= 0.6  # Slow down
            vy -= y * 0.1
            vy *= 0.6  # Slow down
        if y >= height + 100:
            vx -= x * 0.1
            vx *= 0.6  # Slow down
            vy -= y * 0.1
            vy *= 0.6  # Slow down
        if x < -100:
            vx -= x * 0.1
            vx *= 0.6  # Slow down
            vy -= y * 0.1
            vy *= 0.6  # Slow down
        if y < -100:
            vx -= x * 0.1
            vx *= 0.6  # Slow down
            vy -= y * 0.1
            vy *= 0.6  # Slow down

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

# -------------------------------------------------------------------------------------------
# Birds2 section
# -------------------------------------------------------------------------------------------
    # Set leader bird to bird that has smallest distance to food
    if food_closest2 is not None:
        leaderbirdx2 = birdlist2[food_closest2][0]
        leaderbirdy2 = birdlist2[food_closest2][1]
        leaderbirdvx2 = birdlist2[food_closest2][2]
        leaderbirdvy2 = birdlist2[food_closest2][3]

    # Update leader bird position and speed
    if (leaderbirdx2 < leader_border2):
        leaderbirdvx2 += border_speed_change2
    if (leaderbirdy2 < leader_border2):
        leaderbirdvy2 += border_speed_change2
    if (leaderbirdx2 > width - leader_border2):
        leaderbirdvx2 -= border_speed_change2
    if (leaderbirdy2 > height - leader_border2):
        leaderbirdvy2 -= border_speed_change2

    # Draw leaderbird and update
    leaderbirdvx2 += random.uniform(-leader_random_speed_change2, leader_random_speed_change2)
    leaderbirdvy2 += random.uniform(-leader_random_speed_change2, leader_random_speed_change2)
    # Cap maximum speed of leader bird
    speed2 = math.sqrt(leaderbirdvx2*leaderbirdvx2 + leaderbirdvy2*leaderbirdvy2)
    if (speed2 > leader_max_speed2):
        leaderbirdvx2 = leaderbirdvx2 * leader_max_speed2 / speed2
        leaderbirdvy2 = leaderbirdvy2 * leader_max_speed2 / speed2
    leaderbirdx2 += leaderbirdvx2
    leaderbirdy2 += leaderbirdvy2
    k = 0
    min_food_dist2 = 1500
    while (k < len(birdlist2)):
        # Make copies for clarity
        x2 = birdlist2[k][0]
        y2 = birdlist2[k][1]
        vx2 = birdlist2[k][2]
        vy2 = birdlist2[k][3]
        # Set colors of birds
        colr2 = 0
        colg2 = 255
        colb2 = 255
        # Draw birds
        pygame.draw.circle(screen, (colr2, colg2, colb2), (np.int64(x2), np.int64(y2)), 6, 0)

        # Birds move towards leader bird
        leaderdiffx2 = leaderbirdx2 - x2
        leaderdiffy2 = leaderbirdy2 - y2
        vx2 += 0.008 * leaderdiffx2
        vy2 += 0.008* leaderdiffy2

        # Birds calculate distance to food
        if food is not None:
            food_dist2 = math.sqrt(math.pow(x2 - food[0], 2) + math.pow(y2 - food[1], 2))
            if food_dist2 < min_food_dist2:
                min_food_dist2 = food_dist2
                food_closest2 = k
        # Calculate average velocity of other birds
        # Bird moves away from neighbours that are too close
        j = 0
        avxtotal2 = 0
        avytotal2 = 0
        avcount2 = 0
        while (j < no_of_birds2):
            if (j != k):
                dx2 = birdlist2[j][0] - x2  # x-distance between current i-th bird and j-th bird
                dy2 = birdlist2[j][1] - y2  # y-distance between current i-th bird and j-th bird
                dist2 = math.sqrt(dx2 * dx2 + dy2 * dy2)  # euclidean distance
                # if distance is smaller than minimum distance birds move away from each other
                if (dist2 < min_dist2):
                    vx2 -= dx2 * 0.3
                    vy2 -= dy2 * 0.3
                # sum up velocities of nearby birds and counts them
                if (dist2 < naighbourhood_area2):
                    avxtotal2 += birdlist2[j][2]
                    avytotal2 += birdlist2[j][3]
                    avcount2 += 1
            j += 1
        # Match to average velocity of nearby birds
        if (avcount2 != 0):
            avx2 = avxtotal2 / avcount2
            avy2 = avytotal2 / avcount2
            vx2 = 0.9 * vx2 + 0.1 * avx2  # Add x average velocity component to x-velocity
            vy2 = 0.9 * vy2 + 0.1 * avy2  # Add y average velocity component to y-velocity

        # Birds bounce off obstacles and slow down
        for barrier in barriers:
            dx2 = barrier[0] - x2
            dy2 = barrier[1] - y2
            dist2 = math.sqrt(dx2*dx2 + dy2*dy2)
            if (dist2 < barrier_radius + 15):
                vx2 -= dx2 * 0.1
                vx2 *= 0.6 # Slow down
                vy2 -= dy2 * 0.1
                vy2 *= 0.6 # Slow down

        # Birds bound off bounds of screen window
        if x2 >= width + 100:
            vx2 -= x2 * 0.1
            vx2 *= 0.6  # Slow down
            vy2 -= y2 * 0.1
            vy2 *= 0.6  # Slow down
        if y2 >= height + 100:
            vx2 -= x2 * 0.1
            vx2 *= 0.6  # Slow down
            vy2 -= y2 * 0.1
            vy *= 0.6  # Slow down
        if x2 < -100:
            vx2 -= x2 * 0.1
            vx2 *= 0.6  # Slow down
            vy2 -= y2 * 0.1
            vy2 *= 0.6  # Slow down
        if y2 < -100:
            vx2 -= x2 * 0.1
            vx2 *= 0.6  # Slow down
            vy2 -= y2 * 0.1
            vy2 *= 0.6  # Slow down

        # Cap maximum speed
        speed2 = math.sqrt(vx2*vx2 + vy2*vy2)
        if (speed2 > max_speed2):
            vx2 = vx2 * max_speed2 / speed2
            vy2 = vy2 * max_speed2 / speed2

        # Update positions according to speeds
        birdlist2[k][0] += vx2
        birdlist2[k][1] += vy2
        birdlist2[k][2] = vx2
        birdlist2[k][3] = vy2
        k += 1

# -------------------------------------------------------------------------------------------
# App functionalities
# -------------------------------------------------------------------------------------------
    for barrier in barriers:
        pygame.draw.circle(screen, (150,100,0), (np.int64(barrier[0]), np.int64(barrier[1])), barrier_radius, 0)

    pygame.display.flip()
    i += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_pressed = True
        if event.type == pygame.KEYUP and event.key == pygame.K_p:
            px = random.uniform(0, width)
            py = random.uniform(0, height)
            pvx = random.uniform(-speed_spread, speed_spread)
            pvy = random.uniform(-speed_spread, speed_spread)
            predator = [px, py, pvx, pvy]
            pygame.draw.circle(screen, (255, 0, 0), [np.int64(px), np.int64(py)], 10)
        if event.type == pygame.KEYUP and event.key == pygame.K_k and predator is not None:
            predator = None
        if event.type == pygame.KEYUP and event.key == pygame.K_f:
            collide = [True]
            while True in collide:
                fx = random.uniform(0, width)
                fy = random.uniform(0, height)
                collide = [True for x, y in barriers if math.fabs(x - fx) < 15 and math.fabs(y - fy) < 15]
                food = [np.int64(fx), np.int64(fy)]
                pygame.draw.circle(screen, (100, 200, 100), food, 7)