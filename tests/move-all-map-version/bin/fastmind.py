#!/usr/bin/python3
#fastmind
#by boot1110001

### IMPORTS ####################################################################
import sys
import getopt
import pygame

from datetime import datetime

from utils import func as uf
from utils.color import Color
from core import func as cf
from core.map import Map
from graphic.rectangle import Rectangle
from graphic.wall import Wall
from graphic.goal import Goal
from graphic.player import Player

### EDITABLE VARIABLES #########################################################
stdsize = 30 # test with 10 (view with 15)
cellscope = 15 # ODD NUMBER
pxscope = cellscope*stdsize
cellcenter = int((cellscope/2)+0.5)
pxcenter = (pxscope/2)-(stdsize/2)

### NON EDITABLE VARIABLES #####################################################
window = 0 # glut window number
lvlist = [] # level file list
wmap = [] # wall list
womap = [] # wall object list
goal = 0 # goal object
player = 0 # player object
victory = False
old_time = 0
lvl_time = 0
width = 0
height = 0

hstr='''fastmind, solve mazes...
game options:
 fastmind.py -h\t\t\t--help\t\t\tShow this help.
 fastmind.py -l\t\t\t--list\t\t\tList the available levels.
 fastmind.py -p <level_name>\t--play=<level_name>\tPlay the level.
 fastmind.py -s <square_size>\t--size=<square_size>\tModify the default size (15) of the basic square.'''

### FUNCTIONS ##################################################################
def pre_draw_map(maplist,lw,lh,stdsize,startx,starty):
    global wmap, womap, goal, player

    xcellgap=cellcenter-startx
    ycellgap=cellcenter-starty
    xgap=int((xcellgap*width)/(width/stdsize))
    ygap=int((ycellgap*height)/(height/stdsize))

    maxx=stdsize*lw
    maxy=stdsize*lh
    x = y = i = 0

    while (y<maxy):
        while (x<maxx):
            xcell=int((x*(width/stdsize))/width)+1
            ycell=int((y*(height/stdsize))/height)+1
            if (maplist[i]=='#'):
                wmap.append([xcell,ycell])
                womap.append(Wall(x+xgap,y+ygap,xcell,ycell,stdsize,Color.BLUE2))
                # print('['+str(i)+'] ('+str(x)+','+str(y)+') ('+str(xcell)+','+str(ycell)+') ('+str(xcell+xcellgap)+','+str(ycell+ycellgap)+') "#"')
            elif (maplist[i]=='$'):
                goal = Goal(x+xgap,y+ygap,xcell,ycell,stdsize,Color.RED)
                # print('['+str(i)+'] ('+str(x)+','+str(y)+') ('+str(xcell)+','+str(ycell)+') "$"')
            elif (maplist[i]=='@'):
                player = Player(x+xgap,y+ygap,xcell,ycell,stdsize,Color.GREEN)
                # print('['+str(i)+'] ('+str(x)+','+str(y)+') ('+str(xcell)+','+str(ycell)+') "@"')
            else:
                # print('['+str(i)+'] ('+str(x)+','+str(y)+') ('+str(xcell)+','+str(ycell)+') " "')
                pass
            i+=1
            x+=stdsize
        x=0
        y+=stdsize

def print_result(screen):
    rectw = 14*stdsize
    recth = 4*stdsize
    rectx = (width/2)-(rectw/2)
    recty = (height/2)-(recth/2)
    borderw = stdsize*0.70
    pygame.draw.rect(screen, Color.WHITE, [rectx, recty, rectw, recth])
    pygame.draw.rect(screen, Color.BLACK, [rectx+borderw, recty+borderw, rectw-(borderw*2), recth-(borderw*2)])
    basicfont = pygame.font.SysFont('Monospace', stdsize)

    text = basicfont.render('GOAL! You pass in:', True, Color.WHITE, Color.BLACK)
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery-(stdsize/2)-2
    screen.blit(text, textrect)

    text = basicfont.render(str(lvl_time)+'s', True, Color.WHITE, Color.BLACK)
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery+(stdsize/2)+2
    screen.blit(text, textrect)

def display(screen):
    global victory, lvl_time
    # --- PREVIOUS CHECKS ------------------------------------------------------
    if (not victory and (player.x, player.y) == (goal.x, goal.y)):
        new_time = datetime.now()
        lvl_time = new_time - old_time
        print('[GOAL] You pass the level in:', lvl_time)
        victory=True
    # --- DRAWING --------------------------------------------------------------
    # Set the screen background
    screen.fill(Color.BLACK)

    cf.draw_map(womap, screen)
    goal.draw(screen)
    if not victory:
        # player.draw(screen, pxcenter, pxcenter)
        player.draw(screen)
    else:
        print_result(screen)

def checkMove(x,y):
    out=True
    if ([x,y] in wmap):
        print('[FAIL] ('+str(x)+', '+str(y)+') No move. There is a wall there.')
        out=False
    return out

def specialkey(event):
    xcell, ycell = player.xcell, player.ycell
    _xcell, _ycell = xcell, ycell
    if (event.key==pygame.K_UP):
        _ycell-=1
        if (checkMove(xcell,_ycell)):
            player.move_up()
            goal.move_down()
            cf.move_map_down(womap)
            print('[ UP ] ('+str(_xcell)+', '+str(ycell)+')')
    elif (event.key==pygame.K_DOWN):
        _ycell+=1
        if (checkMove(xcell,_ycell)):
            player.move_down()
            goal.move_up()
            cf.move_map_up(womap)
            print('[DOWN] ('+str(_xcell)+', '+str(ycell)+')')
    elif (event.key==pygame.K_LEFT):
        _xcell-=1
        if (checkMove(_xcell,ycell)):
            player.move_left()
            goal.move_right()
            cf.move_map_right(womap)
            print('[LEFT] ('+str(_xcell)+', '+str(ycell)+')')
    elif (event.key==pygame.K_RIGHT):
        _xcell+=1
        if (checkMove(_xcell,ycell)):
            player.move_right()
            goal.move_left()
            cf.move_map_left(womap)
            print('[RIGH] ('+str(_xcell)+', '+str(ycell)+')')

### MAIN #######################################################################
def main(argv):
    global stdsize, old_time, lvlist, width, height

    lvlist=cf.get_lvls()
    lvname = '1.lv'
    try:
        opts, args = getopt.getopt(argv,"hp:s:l",["help","play=","size=","list"])
    except getopt.GetoptError:
        print(hstr)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(hstr)
            sys.exit()
        elif opt in ("-p", "--play"):
            lvname = arg
        elif opt in ("-s", "--size"):
            stdsize = int(arg)
        elif opt in ("-l", "--list"):
            print('[INFO] Level list:')
            uf.print_list(' > ',lvlist)
            sys.exit()

    if not (lvname in lvlist):
        print("[FAIL] The selected level isn't in the list:")
        uf.print_list(' > ',lvlist)
        sys.exit()

    # width, height = stdsize*m.lvwidth, stdsize*m.lvheight # window size
    width, height = pxscope, pxscope # window size
    old_time = datetime.now()
    print('[INFO] Time started at:', old_time)
    m=Map(open('lvls/'+lvname, 'r').read())
    pre_draw_map(m.maplist,m.lvwidth,m.lvheight,stdsize,m.startx,m.starty)

    # --- PYGAME INIT ----------------------------------------------------------
    pygame.init()
    # Set the height and width of the screen
    size = [width, height]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("FASTMIND")
    logo = pygame.image.load('fastmind.png')
    pygame.display.set_icon(logo)
    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------------------------------------------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if not victory:
                if event.type == pygame.KEYDOWN:
                    specialkey(event)
            else:
                if event.type == pygame.KEYDOWN:
                    if (event.key==pygame.K_ESCAPE):
                        print('[ESCP] Exiting...')
                        done = True
                    elif (event.key==pygame.K_RETURN):
                        print('[ENTR] Exiting...')
                        done = True

        # --- Logic
        # --- Drawing
        display(screen)
        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(60)

        pygame.display.flip()

    # Close everything down
    pygame.quit()

### EXEC #######################################################################
if __name__ == "__main__":
    main(sys.argv[1:])
