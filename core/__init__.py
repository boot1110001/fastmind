#core.__init__
#by boot1110001

### IMPORTS ####################################################################
import sys, os, re
import getopt
from optparse import OptionParser
# To not show the default message of pygame import
import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import core
from core import key
from core import log
from core import cfunc as cf

import graphic
from graphic import color
from graphic import displays

import languages
from languages import *

### EDITABLE VARIABLES #########################################################
lang = en.EN
verbose = True

menu_color_scheme = color.Scheme2
level_color_scheme = color.Scheme2
game_color_scheme = color.Scheme2

stdsize = 40 # 10/15/40...
cellscope = 15 # ODD NUMBER def=15

### AUTOMATIC VARIABLES ########################################################
pxscope = cellscope * stdsize
cellcenter = int((cellscope / 2) + 0.5)
pxcenter = (pxscope / 2) - (stdsize / 2)

# --- Game Keys
game_key_mode = 1
def_in_game_key_delay = 4
in_game_key_delay = def_in_game_key_delay


psv = python_short_version = re.compile(r'([0-9]\.[0-9])\.[0-9] ').match(sys.version).group(1)

### NON EDITABLE VARIABLES #####################################################
# --- Files and folders
main_pkg = 'core'
version_file = 'version.txt'
icon_file = 'media/icon.ico'
# icon_file = 'media/icon.png'
font_file = 'media/node.ttf'
lvls_folder = 'lvls'

### FUNCTIONS ##################################################################


### MAIN #######################################################################
def main():
    # --- GLOBAL VARIABLES -----------------------------------------------------
    global verbose, lang, version_file, icon_file, font_file, lvls_folder, game_key_mode, def_in_game_key_delay, in_game_key_delay

    # --- MAIN VARIABLES -------------------------------------------------------
    width, height = pxscope, pxscope # window size

    mselect = 0
    mmaxselect = 4
    lselect = 0
    lmaxselect = 0

    # --- file variables
    rootpath = os.path.dirname(os.path.abspath(__file__)).replace(main_pkg,'')
    version_file = rootpath+version_file
    icon_file = rootpath+icon_file
    font_file = rootpath+font_file
    lvls_folder = rootpath+lvls_folder

    # --- game variables
    map = 0
    old_time = 0
    victory = False

    # --- level_list variables
    lvlist = cf.get_lvls(lvls_folder)
    lmaxselect = len(lvlist) - 1
    lvname = '1.lv'

    # --- state control
    # 0 - menu
    # 1 - game
    # 2 - level menu
    # 3 - credits
    display_state = 0

    # --- version variables
    version = ""
    shortversion = ""
    try:
        version = open(version_file, 'r').read().replace('\n','')
        patron = re.compile(r'(.*\..*\..*)\.')
        shortversion = patron.search(version).group(1)
    except:
        log.p.warning(lang.version_warning)

    # --- CMD INIT -------------------------------------------------------------
    log.p.init(lang.wellcome_msg+version+")")
    log.p.info(lang.wellcome_info+pygame.version.ver+")")

    # --- Parameters -----------------------------------------------------------
    parser = OptionParser()
    parser.add_option(
        "-v", "--verbose", dest="verbose",
        action="store_true", default=False,
        help="print status messages to stdout.")
    parser.add_option(
        "-l", "--lang", dest="lang",
        help="changes the default language."
    )
    parser.add_option(
        "-p", "--play", dest="lvshortname",
        help="play the LEVEL instantly.", metavar="LEVEL"
    )
    parser.add_option(
        "-s", "--show", dest="show_level_list",
        action="store_true", default=False,
        help="show the available levels.")

    (options, args) = parser.parse_args()

    # --- Verbose
    verbose = options.verbose

    # --- Language
    if options.lang:
        lang = languages.set_lang(options.lang)

    # --- Play instantly
    if options.lvshortname:
        lvname = options.lvshortname+".lv"
        display_state = 1
        if not (lvname in lvlist):
            # print(lang.select_level_fail)
            log.p.fail(lang.select_level_fail)
            cf.print_level_list(lvlist)
            sys.exit()
        plout = cf.play_level(lvname, width, height, lang, stdsize, cellcenter, game_color_scheme, lvls_folder)
        map = plout[0]
        old_time = plout[1]
        victory = plout[2]

    # --- Show level-list
    if  options.show_level_list:
        # print(lang.level_list_msg)
        log.p.info(lang.level_list_msg)
        cf.print_level_list(lvlist)
        sys.exit()

    # --- Post-options parameters ----------------------------------------------
    if verbose: cf.print_file_vars(version_file, icon_file, font_file, lvls_folder)

    # --- PYGAME INIT ----------------------------------------------------------
    pygame.init()
    # Set the height and width of the screen
    size = [width, height]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("FASTMIND " + shortversion)
    logo = pygame.image.load(icon_file)
    pygame.display.set_icon(logo)
    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------------------------------------------
    while not done:
        # --- Event Processing & logic
        for event in pygame.event.get():

            # ESTO HAY QUE MODULARLO
            if event.type == pygame.QUIT:
                done = True

            elif (display_state == 0): # on menu
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE):
                        # print('[ESCP] '+lang.exiting)
                        log.p.escp(lang.exiting)
                        done = True
                    elif (event.key == pygame.K_RETURN):
                        if (mselect == 0):
                            # print('[ENTR] '+lang.play_level)
                            log.p.entr(lang.play_level)
                            display_state = 1
                            plout = cf.play_level(lvname, width, height, lang, stdsize, cellcenter, game_color_scheme, lvls_folder)
                            map = plout[0]
                            old_time = plout[1]
                            victory = plout[2]
                        elif (mselect == 1):
                            # print('[ENTR] '+lang.select_level)
                            log.p.entr(lang.select_level)
                            display_state = 2
                        elif (mselect == 2):
                            # print('[ENTR] '+lang.credits)
                            # print('[FAIL] '+lang.not_implemented)
                            log.p.entr(lang.credits)
                            log.p.fail(lang.not_implemented)
                        elif (mselect == 3):
                            # print('[ENTR] '+lang.config)
                            # print('[FAIL] '+lang.not_implemented)
                            log.p.entr(lang.config)
                            log.p.fail(lang.not_implemented)
                        elif (mselect == 4):
                            # print('[ENTR] '+lang.exiting)
                            log.p.entr(lang.exiting)
                            done = True
                        else:
                            # print('[ENTR] '+lang.nothing)
                            log.p.entr(lang.nothing)
                            pass
                    else:
                        mselect = key.onmenukey(event, mselect, mmaxselect, verbose)

            elif ((display_state == 1) and (game_key_mode == 0)): # on game (game_key_mode: 0)
                if not victory:
                    if event.type == pygame.KEYDOWN:
                        pressed_keys = pygame.key.get_pressed()
                        if (pressed_keys[pygame.K_ESCAPE]):
                            # print('[ESCP] '+lang.return_to_menu)
                            log.p.escp(lang.return_to_menu)
                            display_state = 0
                        else:
                            key.ongamekey(pressed_keys, map, lang, verbose)
                else:
                    if (event.type == pygame.KEYDOWN):
                        if not (event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]):
                            # print('[INFO] '+lang.key_pressed_return_to_menu)
                            log.p.info(lang.key_pressed_return_to_menu)
                            display_state = 0

            elif (display_state == 2): # on menu level
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE):
                        # print('[ESCP] '+lang.return_to_menu)
                        log.p.escp(lang.return_to_menu)
                        display_state = 0
                    elif (event.key == pygame.K_RETURN):
                        # print('[ENTR] '+lang.play_level)
                        log.p.entr(lang.play_level)
                        display_state = 1
                        lvname = str(lselect)+'.lv'
                        plout = cf.play_level(lvname, width, height, lang, stdsize, cellcenter, game_color_scheme, lvls_folder)
                        map = plout[0]
                        old_time = plout[1]
                        victory = plout[2]
                    else:
                        lselect = key.onlevelkey(event, lselect, lmaxselect, verbose)

        if ((display_state == 1) and (game_key_mode == 1)): # on game (game_key_mode: 1)
            if not victory:
                if event.type == pygame.KEYDOWN:
                    pressed_keys = pygame.key.get_pressed()
                    if (pressed_keys[pygame.K_ESCAPE]):
                        # print('[ESCP] '+lang.return_to_menu)
                        log.p.escp(lang.return_to_menu)
                        display_state = 0
                    else:
                        if (in_game_key_delay == 0):
                            key.ongamekey(pressed_keys, map, lang, verbose)
                            in_game_key_delay = def_in_game_key_delay
                        else:
                            if (in_game_key_delay > 0): in_game_key_delay-=1
            else:
                if (event.type == pygame.KEYDOWN):
                    if not (event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]):
                        # print('[INFO] '+lang.key_pressed_return_to_menu)
                        log.p.info(lang.key_pressed_return_to_menu)
                        display_state = 0

        # --- Drawing
        if (display_state == 0):
            displays.displaymenu(
                screen, width, stdsize, pxcenter, mselect, font_file,
                menu_color_scheme.MENU1,
                menu_color_scheme.MENU2,
                menu_color_scheme.BG_MENU,
                [   lang.menu_play,
                    lang.menu_levels,
                    lang.menu_credits,
                    lang.menu_config,
                    lang.menu_exit
                ]
            )

        elif (display_state == 1):
            if not victory: victory, lvl_time = map.checkvictory(victory, old_time, lang)
            displays.displaygame(
                screen, map, victory,
                stdsize, width, height, lvl_time, font_file,
                game_color_scheme.RESULT1,
                game_color_scheme.RESULT2,
                game_color_scheme.BG,
                [lang.result_txt, lang.result_seconds]
            )

        elif (display_state == 2):
            displays.displaylevel(
                screen, lvlist, lselect, stdsize, cellscope,
                level_color_scheme.LEVEL1,
                level_color_scheme.LEVEL2,
                level_color_scheme.BG_LEVEL
            )

        # --- Wrap-up
        clock.tick(60) # Limit to 60 frames per second

        pygame.display.flip()

    # Close everything down
    pygame.quit()
