#package bin.languages.english __init__
#by boot1110001

### CLASSES ####################################################################
class EN:
    # --- Graphic --------------------------------------------------------------
    menu_play =         "  PLAY  "
    menu_levels =       " LEVELS "
    menu_credits =      "  CRED  "
    menu_exit =         "  EXIT  "

    result_txt =        "GOAL!! You pass in:"
    result_seconds =    "s"

    # --- Shell ----------------------------------------------------------------
    wellcome_msg = "[INIT] Wellcome to FASTMIND ("
    wellcome_info = "[INFO] Using pygame ("

    version_warning = "[WARN] The 'version.txt' file could not be read"
    select_level_fail = "[FAIL] The selected level isn't in the list:"
    level_list_msg = "[INFO] Level list:"

    exiting = "Exiting..."
    play_level = "Play level"
    select_level = "Select level"
    credits = "Credits"
    not_implemented = "Not implemented yet :("
    none = "None"
    return_to_menu = "Return to menu"
    key_pressed_return_to_menu = "Return to menu"
    time_stopped_at = "Time stopped at:"
    you_pass_the_level_in = "You pass the level in:"
    playing = "Playing: "
    time_started_at = "Time started at:"
    no_move_wall = "No move. There is a wall there."

    help_string = '''fastmind, solve mazes and measure your time...
game options:
 fastmind.py -h\t\t\t--help\t\t\tShow this help.
 fastmind.py -l\t\t\t--list\t\t\tList the available levels.
 fastmind.py -v\t\t\t--verbose\t\tEnables verbose mode.
 fastmind.py -p <level_name>\t--play=<level_name>\tPlay the level directly.'''
