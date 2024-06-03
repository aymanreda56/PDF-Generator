

with open('config.txt', 'r') as f:
    config_text = f.read()

if(config_text[0] == '1'):
    CHOSEN_PRESET = 1
elif(config_text[0] == '0'):
    CHOSEN_PRESET = 0
else:
    CHOSEN_PRESET = 0

FONTS = ['Arial', 'Dubai', 'Dubai Light',
         'Dubai Medium', 'Tahoma', 'Times New Roman', 'Calibri', 'Calibri Light', 
         'Courier', 'Courier New CE', 'Segoe UI', 'Segoe UI Semibold', 'Segoe UI Light', 'Segoe UI Semilight', 
         'Arabic Transparent', 'Arabic Typesetting',
         'Deco Type Naskh', 'Deco Type Extensions', 'Deco Type Special', 'Deco Type Swashes', 
         'Deco Type Variants', 'Deco Type Thuluth' , 'Farsi Simple Bold', 'Microsoft Sans Serif', 
         'Sakkal Majalla',
         'Simplified Arabic', 'Aldhabi', 'Andalus']




BUTTON_COLOR = '#03051E'
BUTTON_LIGHT_COLOR = "#070b3d"
WARNING_COLOR = '#F1D00A'
ACCEPT_COLOR = '#0B8457'
BG_COLOR1 = '#EAE1E1'
FM_COLOR = '#F0E3E3'



BUTTON_TEXT_COLOR = '#F0E3E3'
REMOVE_BUTTON_COLOR = '#B80000'


FG_COLOR1 = BG_COLOR1
FG_COLOR2 = '#F6E9B2'

FG_COLOR = FG_COLOR2 if CHOSEN_PRESET else FG_COLOR1
BG_COLOR = FG_COLOR2 if CHOSEN_PRESET else BG_COLOR1
# BG_COLOR = FG_COLOR
TEXT_COLOR = BUTTON_COLOR



TEXT_BOX_FG_COLOR = '#D8E3E7'


DROPDOWN_FG_COLOR = '#D8E3E7'
DROPDOWN_BG_COLOR = '#126E82'
DROPDOWN_TEXT_COLOR = '#132C33'
DROPDOWN_HOVER_COLOR = '#0A043C'



WHITE_TEXT_COLOR = '#FFFFFF'



FRAME_LIGHT_COLOR = '#0A043C'
FRAME_DARK_COLOR = '#C7C8CC'

ENTRY_FG_COLOR = FM_COLOR



CALENDAR_BG = '#EEEEEE'
CALENDAR_FG = '#068FFF'
# CALENDAR_TXT_COLOR = 



SCROLL_COLOR = BUTTON_COLOR
SCROLL_HOVER_COLOR = '#4F709C'



EMPTY_IMAGE_PLACEHOLDER = '#D8E3E7'











GRASS1 = '../data/grass6.png'
GRASS2 = '../data/grass5.png'

PROJ_LOGO1 = '../data/logo_dark.png'
PROJ_LOGO2 = '../data/logo_dark_prev.png'

BG_LOGO1 = '../data/BG_logo.png'
BG_LOGO2 = '../data/BG_logo_prev.png'

WHEAT_LEAVES1 = '../data/wheat_leaves2.png'
WHEAT_LEAVES2 = '../data/wheat_leaves.png'


GRASS = GRASS1 if CHOSEN_PRESET else GRASS2
BG_LOGO = BG_LOGO1 if CHOSEN_PRESET else BG_LOGO2
PROJ_LOGO = PROJ_LOGO1 if CHOSEN_PRESET else PROJ_LOGO2
WHEAT_LEAVES = WHEAT_LEAVES1 if CHOSEN_PRESET else WHEAT_LEAVES2


