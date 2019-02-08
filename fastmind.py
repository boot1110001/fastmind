#!/usr/bin/python3
#fastmind
#by boot1110001

### IMPORTS ####################################################################
import sys
import getopt
import pygame

from datetime import datetime

import bin
from bin.core import func as cf
from bin.core.map import Map
from bin.graphic.rectangle import Rectangle
from bin.graphic.wall import Wall
from bin.graphic.goal import Goal
from bin.graphic.player import Player
from bin.graphic import color
from bin.graphic import displays

### EDITABLE VARIABLES #########################################################
stdsize = 40 # test with 10 (view with 15)
cellscope = 15 # ODD NUMBER def=15
pxscope = cellscope*stdsize
cellcenter = int((cellscope/2)+0.5)
pxcenter = (pxscope/2)-(stdsize/2)

game_color_scheme = color.Scheme2

### NON EDITABLE VARIABLES #####################################################
# --- Level atributes
lvlist = [] # level file list
wmap = [] # wall list
womap = [] # wall object list
goal = 0 # goal object
player = 0 # player object

# --- Time control
old_time = 0
lvl_time = 0

# --- Window dimensions
width = 0
height = 0

# --- State control
onmenu = True
mselect = 0
mmaxselect = 3

onlevel = False
lselect = 0
lmaxselect = 29

ongame = False

victory = False

# --- Run options
verbose = False
hstr='''fastmind, solve mazes and measure your time...
game options:
 fastmind.py -h\t\t\t--help\t\t\tShow this help.
 fastmind.py -l\t\t\t--list\t\t\tList the available levels.
 fastmind.py -v\t\t\t--verbose\t\tEnables verbose mode.
 fastmind.py -p <level_name>\t--play=<level_name>\tPlay the level directly.'''

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
                womap.append(Wall(x+xgap,y+ygap,xcell,ycell,stdsize,game_color_scheme.WALL))
                # print('['+str(i)+'] ('+str(x)+','+str(y)+') ('+str(xcell)+','+str(ycell)+') ('+str(xcell+xcellgap)+','+str(ycell+ycellgap)+') "#"')
            elif (maplist[i]=='$'):
                goal = Goal(x+xgap,y+ygap,xcell,ycell,stdsize,game_color_scheme.GOAL)
                # print('['+str(i)+'] ('+str(x)+','+str(y)+') ('+str(xcell)+','+str(ycell)+') "$"')
            elif (maplist[i]=='@'):
                player = Player(x+xgap,y+ygap,xcell,ycell,stdsize,game_color_scheme.PLAYER1,game_color_scheme.PLAYER2)
                # print('['+str(i)+'] ('+str(x)+','+str(y)+') ('+str(xcell)+','+str(ycell)+') "@"')
            else:
                # print('['+str(i)+'] ('+str(x)+','+str(y)+') ('+str(xcell)+','+str(ycell)+') " "')
                pass
            i+=1
            x+=stdsize
        x=0
        y+=stdsize

def displaygame(screen):
    global victory, lvl_time
    # --- PREVIOUS CHECKS ------------------------------------------------------
    if (not victory and (player.x, player.y) == (goal.x, goal.y)):
        new_time = datetime.now()
        lvl_time = new_time - old_time
        print('[GOAL] You pass the level in:', lvl_time)
        victory=True
    # --- DRAWING --------------------------------------------------------------
    # Set the screen background
    screen.fill(game_color_scheme.BG)

    cf.draw_map(womap, screen)
    goal.draw(screen)
    if not victory:
        # player.draw(screen, pxcenter, pxcenter)
        player.draw(screen)
    else:
        displays.print_result(screen, stdsize, width, height, lvl_time, game_color_scheme.RESULT1, game_color_scheme.RESULT2)

def checkMove(x,y):
    out=True
    if ([x,y] in wmap):
        if verbose : print('[FAIL] ('+str(x)+', '+str(y)+') No move. There is a wall there.')
        out=False
    return out

def ongamekey(event):
    xcell, ycell = player.xcell, player.ycell
    _xcell, _ycell = xcell, ycell
    if (event.key==pygame.K_UP):
        _ycell-=1
        if (checkMove(xcell,_ycell)):
            player.move_up()
            goal.move_down()
            cf.move_map_down(womap)
            if verbose : print('[ UP ] ('+str(_xcell)+', '+str(ycell)+')')
    elif (event.key==pygame.K_DOWN):
        _ycell+=1
        if (checkMove(xcell,_ycell)):
            player.move_down()
            goal.move_up()
            cf.move_map_up(womap)
            if verbose : print('[DOWN] ('+str(_xcell)+', '+str(ycell)+')')
    elif (event.key==pygame.K_LEFT):
        _xcell-=1
        if (checkMove(_xcell,ycell)):
            player.move_left()
            goal.move_right()
            cf.move_map_right(womap)
            if verbose : print('[LEFT] ('+str(_xcell)+', '+str(ycell)+')')
    elif (event.key==pygame.K_RIGHT):
        _xcell+=1
        if (checkMove(_xcell,ycell)):
            player.move_right()
            goal.move_left()
            cf.move_map_left(womap)
            if verbose : print('[RIGH] ('+str(_xcell)+', '+str(ycell)+')')

def onmenukey(event):
    global mselect
    if (event.key==pygame.K_UP):
        mselect=mselect-1
        if mselect<0: mselect=mmaxselect
    elif (event.key==pygame.K_DOWN):
        mselect=mselect+1
        if mselect>mmaxselect: mselect=0

def onlevelkey(event):
    global lselect
    if (event.key==pygame.K_LEFT):
        lselect-=1
        if lselect<0: lselect=lmaxselect
    elif (event.key==pygame.K_RIGHT):
        lselect+=1
        if lselect>lmaxselect: lselect=0

def reset_level():
    global victory, wmap, womap, goal, player, old_time, lvl_time

    victory = False

    # --- Level atributes
    wmap = [] # wall list
    womap = [] # wall object list
    goal = 0 # goal object
    player = 0 # player object

    # --- Time control
    old_time = 0
    lvl_time = 0

def play_level(lvname):
    global old_time

    reset_level()
    old_time = datetime.now()

    m=Map(open('lvls/'+lvname, 'r').read())
    pre_draw_map(m.maplist,m.lvwidth,m.lvheight,stdsize,m.startx,m.starty)
    print('[INFO] Playing: '+m.lvrealname+' ('+lvname+')')
    print('[INFO] Time started at:', old_time)

### MAIN #######################################################################
def main(argv):
    global old_time, lvlist, width, height, verbose, ongame, onlevel, onmenu, lmaxselect, victory

    lvlist=cf.get_lvls()
    lmaxselect=len(lvlist)-1
    lvname = '1.lv'

    width, height = pxscope, pxscope # window size

    try:
        opts, args = getopt.getopt(argv,"hp:lv",["help","play=","list","verbose"])
    except getopt.GetoptError:
        print(hstr)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(hstr)
            sys.exit()
        elif opt in ("-p", "--play"):
            lvname = arg+".lv"
            onmenu = False
            ongame = True
            if not (lvname in lvlist):
                print("[FAIL] The selected level isn't in the list:")
                cf.print_level_list(lvlist)
                sys.exit()
            play_level(lvname)
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-l", "--list"):
            print('[INFO] Level list:')
            cf.print_level_list(lvlist)
            sys.exit()

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
            elif onmenu:
                if event.type == pygame.KEYDOWN:
                    if (event.key==pygame.K_ESCAPE):
                        print('[ESCP] Exiting...')
                        done = True
                    elif (event.key==pygame.K_RETURN):
                        if (mselect==0):
                            print('[ENTR] Play level')
                            onmenu = False
                            ongame = True
                            play_level(lvname)
                        elif (mselect==1):
                            print('[ENTR] Select level')
                            onmenu = False
                            onlevel = True
                        elif (mselect==2):
                            print('[ENTR] Not implemented :(')
                        elif (mselect==3):
                            print('[ENTR] Exiting...')
                            done = True
                        else:
                            print('[ENTR] None')
                            pass
                    else:
                        onmenukey(event)
            elif onlevel:
                if event.type == pygame.KEYDOWN:
                    if (event.key==pygame.K_ESCAPE):
                        print('[ESCP] Return to menu')
                        onlevel = False
                        onmenu = True
                    elif (event.key==pygame.K_RETURN):
                        print('[ENTR] Play level')
                        onlevel = False
                        ongame = True
                        lvname = str(lselect)+'.lv'
                        play_level(lvname)
                    else:
                        onlevelkey(event)
            elif ongame:
                if not victory:
                    if event.type == pygame.KEYDOWN:
                        if (event.key==pygame.K_ESCAPE):
                            print('[ESCP] Return to menu')
                            onmenu = True
                            ongame = False
                        else:
                            ongamekey(event)
                else:
                    if event.type == pygame.KEYDOWN:
                        if (event.key==pygame.K_ESCAPE):
                            print('[ESCP] Return to menu')
                            onmenu = True
                            ongame = False
                        elif (event.key==pygame.K_RETURN):
                            print('[ENTR] Return to menu')
                            onmenu = True
                            ongame = False

        # --- Logic
        # --- Drawing
        if onmenu:
            displays.displaymenu(screen, width, stdsize, pxcenter, mselect)
        elif onlevel:
            displays.displaylevel(screen, lvlist, lselect, stdsize, cellscope)
        elif ongame:
            displaygame(screen)
        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(60)

        pygame.display.flip()

    # Close everything down
    pygame.quit()

### EXEC #######################################################################
if __name__ == "__main__":
    main(sys.argv[1:])
