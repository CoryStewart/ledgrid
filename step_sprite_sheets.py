#!/usr/bin/env python
''' ledgrid_test.py - test script for writing to PRU 0 mem using PyPRUSS library & driving ledgrid.'''

import sys
from Ledgrid import *

options = ['pacman', 'frogger', 'mrs_pacman', 'mario', 'minecraft']
if sys.argv[1] not in options:
    print 'Please pass one of the following args on the cmdline: ', options
    print ' you passed: ', sys.argv[1]
    exit( -1 )
 
selected = sys.argv[1] 

if( selected == 'pacman' ):
    ss = SpriteSheet( 'sprite_sheets/pacman_spritesheet.png', stepx=16, stepy=16, offsetx=0, offsety=0 )
elif( selected == 'mrs_pacman' ):
    ss = SpriteSheet( 'sprite_sheets/mrs_pacman_16x16.png', stepx=16, stepy=16, offsetx=0, offsety=0 )
elif( selected == 'minecraft' ):
    ss = SpriteSheet( 'sprite_sheets/MinecraftSheet_24x20.png', stepx=16, stepy=16, offsetx=0, offsety=0 )
elif( selected == 'frogger' ):
    ss = SpriteSheet( 'sprite_sheets/frogger.png', stepx=16, stepy=16, offsetx=32, offsety=32 )
elif( selected == 'mario' ):
    ss = SpriteSheet( 'sprite_sheets/mario_sheet.png', stepx=16, stepy=16, offsetx=0, offsety=0 )

grid = Ledgrid()
grid.exploreSheet( ss )
grid.clear()
grid.close()
sys.exit(0)
