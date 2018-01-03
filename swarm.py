import pygame, os, math, time, random
pygame.init()

# set the width and height of the screen
WIDTH = 1000
HEIGHT = 1000

CENTREX = WIDTH / 2
CENTREY = HEIGHT / 2

NUMBEROFBIRDS = 200


POSITIONSPREAD = 10000
SPEEDSPREAD = 5
MAXSPEED = 10

BORDER = 100
LEADERBORDER = 200
BORDERSPEEDCHANGE = 0.2

MINDIST = 10.0
MATCHSPEEDWINDOW = 40.0

LEADERBIRDRANDOMSPEEDCHANGE = 0.2
LEADERMAXSPEED = 5.0

barriers = [[450,500],[475,500],[500,500],[525,500],[625,500],[650,500],[675,500],[700,500],[400,500],[425,500],[400,525],[400,550],[400,650],[400,675],[400,700],[375,700],[350,700],[325,700],[300,700],[275,700],[250,700],[800,200],[250,700],[100,100]]
BARRIERRADIUS = 30


size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(size)

# This makes the normal mouse pointer invisible in graphics window
pygame.mouse.set_visible(0)



birdlist = []


# Generate leader bird
leaderbirdx = 300.0
leaderbirdy = 300.0
leaderbirdvx = 5.0
leaderbirdvy = 0.0


# Generate birds
i = 0
while (i < NUMBEROFBIRDS):
    x = random.uniform(CENTREX - POSITIONSPREAD, CENTREX + POSITIONSPREAD)
    y = random.uniform(CENTREY - POSITIONSPREAD, CENTREY + POSITIONSPREAD)
    vx = random.uniform(-SPEEDSPREAD, SPEEDSPREAD)
    vy = random.uniform(-SPEEDSPREAD, SPEEDSPREAD)
    
    newbird = [x, y, vx, vy]

    birdlist.append(newbird)
    i += 1

quit_pressed = False

while not quit_pressed:

    screen.fill((0,0,0))


    # Update leader bird position and speed
    if (leaderbirdx < LEADERBORDER):
        leaderbirdvx += BORDERSPEEDCHANGE
    if (leaderbirdy < LEADERBORDER):
        leaderbirdvy += BORDERSPEEDCHANGE
    if (leaderbirdx > WIDTH - LEADERBORDER):
        leaderbirdvx -= BORDERSPEEDCHANGE
    if (leaderbirdy > HEIGHT - LEADERBORDER):
        leaderbirdvy -= BORDERSPEEDCHANGE


    # Draw leaderbird and update
    #pygame.draw.circle(screen, (255,0,255), (int(leaderbirdx), int(leaderbirdy)), 5, 0)
    leaderbirdvx += random.uniform(-LEADERBIRDRANDOMSPEEDCHANGE, LEADERBIRDRANDOMSPEEDCHANGE)
    leaderbirdvy += random.uniform(-LEADERBIRDRANDOMSPEEDCHANGE, LEADERBIRDRANDOMSPEEDCHANGE)


    # Cap maximum speed
    speed = math.sqrt(leaderbirdvx*leaderbirdvx + leaderbirdvy*leaderbirdvy)
    if (speed > LEADERMAXSPEED):
        leaderbirdvx = leaderbirdvx * LEADERMAXSPEED/speed
        leaderbirdvy = leaderbirdvy * LEADERMAXSPEED/speed


    leaderbirdx += leaderbirdvx
    leaderbirdy += leaderbirdvy


    

    # Draw birds, positions and speeds
    i = 0
    while (i < NUMBEROFBIRDS):

        # Make copies for clarity
        x = birdlist[i][0]
        y = birdlist[i][1]
        vx = birdlist[i][2]
        vy = birdlist[i][3]

        colr = int(float(i) * 255.0/NUMBEROFBIRDS)
        colg = int((NUMBEROFBIRDS-float(i)) * 255.0/NUMBEROFBIRDS)
        colb = 255
        
        pygame.draw.circle(screen, (colr,colg,colb), (int(x), int(y)), 2, 0)

        # Birds move away from border
        if (x < BORDER):
            vx += BORDERSPEEDCHANGE
        if (y < BORDER):
            vy += BORDERSPEEDCHANGE
        if (x > WIDTH - BORDER):
            vx -= BORDERSPEEDCHANGE
        if (y > HEIGHT - BORDER):
            vy -= BORDERSPEEDCHANGE

        # Birds move towards leader bird
        leaderdiffx = leaderbirdx - x
        leaderdiffy = leaderbirdy - y
        vx += 0.007 * leaderdiffx
        vy += 0.007 * leaderdiffy

        # Move away from other nearby birds
        # Also calculate average velocity of birds in larger window
        j = 0
        # For calculating average velocity of other birds
        avxtotal = 0
        avytotal = 0
        avcount = 0
        while (j < NUMBEROFBIRDS):
            if (j != i):
                dx = birdlist[j][0] - x
                dy = birdlist[j][1] - y
                dist = math.sqrt(dx*dx + dy*dy)
                if (dist < MINDIST):
                    vx -= dx * 0.2
                    vy -= dy * 0.2
                if (dist < MATCHSPEEDWINDOW):
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
            if (dist < BARRIERRADIUS + 15):
                vx -= dx * 0.1
                vx *= 0.6
                vy -= dy * 0.1
                vy *= 0.6
                
        # Cap maximum speed
        speed = math.sqrt(vx*vx + vy*vy)
        if (speed > MAXSPEED):
            vx = vx * MAXSPEED/speed
            vy = vy * MAXSPEED/speed

        # Update positions according to speeds
        birdlist[i][0] += vx
        birdlist[i][1] += vy
        birdlist[i][2] = vx
        birdlist[i][3] = vy
        i += 1

    for barrier in barriers:
        pygame.draw.circle(screen, (0,100,255), (int(barrier[0]), int(barrier[1])), BARRIERRADIUS, 0)

    #time.sleep(0.1)
    pygame.display.flip()
    i += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_pressed = True
