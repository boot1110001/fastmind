#core.cfunc
#by boot1110001

### IMPORTS ####################################################################
from os import listdir
from os.path import isfile, join

### FUNCTIONS ##################################################################
def get_lvls(dir):
    onlyfiles = [f for f in listdir(dir) if isfile(join('lvls', f))]
    return onlyfiles

def print_list(string,list):
    for i in list: print(string+str(i))

def print_level_list(lvlist):
    _lvlist=[]
    for lv in lvlist:
        _lvlist.append(lv.replace('.lv',''))
    print_list(' > ',_lvlist)

def draw_map(womap, screen):
    for o in womap: o.draw(screen)

def print_file_vars(version_file, icon_file, font_file, lvls_folder):
    print("[INFO] version_file = '"+version_file+"'")
    print("[INFO] icon_file = '"+icon_file+"'")
    print("[INFO] font_file = '"+font_file+"'")
    print("[INFO] lvls_folder = '"+lvls_folder+"'")