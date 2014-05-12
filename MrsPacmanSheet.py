#!/usr/bin/env python
''' MrsPacmanSheet.py - Class for defining the MrsPacman SpriteSheet class and all of the img frames within the sheet.'''

import sys
from Ledgrid import *

# ================================================================================
class MrsPacmanSheet(SpriteSheet):
    def __init__( self ):
        h = SpriteSheet.__init__( self, 'sprite_sheets/mrs_pacman_16x16.png', stepx=16, stepy=16, offsetx=0, offsety=0 ) 

        self.defineSprite( 'pacman_up_open1',                     0,   0 )
        self.defineSprite( 'pacman_up_open2',                    16,   0 )
        self.defineSprite( 'pacman_up_closed',                   32,   0 )
        self.defineSprite( 'pacman_down_open1',                  48,   0 )
        self.defineSprite( 'pacman_down_open2',                  64,   0 )
        self.defineSprite( 'pacman_down_closed',                 80,   0 )
        self.defineSprite( 'pacman_left_open1',                  96,   0 )
        self.defineSprite( 'pacman_left_open2',                 112,   0 )

        self.defineSprite( 'pacman_left_closed',                  0,  16 )
        self.defineSprite( 'pacman_right_open1',                 16,  16 )
        self.defineSprite( 'pacman_right_open2',                 32,  16 )
        self.defineSprite( 'pacman_right_closed',                48,  16 )
        self.defineSprite( 'ghost_vulnerable1',                  64,  16 )
        self.defineSprite( 'ghost_vulnerable2',                  80,  16 )
        self.defineSprite( 'ghost_vulnerable3',                  96,  16 )
        self.defineSprite( 'ghost_vulnerable4',                 112,  16 )

        self.defineSprite( 'ghost_red_eyes_up1',                  0,  32 )
        self.defineSprite( 'ghost_red_eyes_up2',                 16,  32 )
        self.defineSprite( 'ghost_red_eyes_down1',               32,  32 )
        self.defineSprite( 'ghost_red_eyes_down2',               48,  32 )
        self.defineSprite( 'ghost_red_eyes_left1',               64,  32 )
        self.defineSprite( 'ghost_red_eyes_left2',               80,  32 )
        self.defineSprite( 'ghost_red_eyes_right1',              96,  32 )
        self.defineSprite( 'ghost_red_eyes_right2',             112,  32 )

        self.defineSprite( 'ghost_pink_eyes_up1',                 0,  48 )
        self.defineSprite( 'ghost_pink_eyes_up2',                16,  48 )
        self.defineSprite( 'ghost_pink_eyes_down1',              32,  48 )
        self.defineSprite( 'ghost_pink_eyes_down2',              48,  48 )
        self.defineSprite( 'ghost_pink_eyes_left1',              64,  48 )
        self.defineSprite( 'ghost_pink_eyes_left2',              80,  48 )
        self.defineSprite( 'ghost_pink_eyes_right1',             96,  48 )
        self.defineSprite( 'ghost_pink_eyes_right2',            112,  48 )

        self.defineSprite( 'ghost_cyan_eyes_up1',                 0,  64 )
        self.defineSprite( 'ghost_cyan_eyes_up2',                16,  64 )
        self.defineSprite( 'ghost_cyan_eyes_down1',              32,  64 )
        self.defineSprite( 'ghost_cyan_eyes_down2',              48,  64 )
        self.defineSprite( 'ghost_cyan_eyes_left1',              64,  64 )
        self.defineSprite( 'ghost_cyan_eyes_left2',              80,  64 )
        self.defineSprite( 'ghost_cyan_eyes_right1',             96,  64 )
        self.defineSprite( 'ghost_cyan_eyes_right2',            112,  64 )

        self.defineSprite( 'ghost_orange_eyes_up1',               0,  80 )
        self.defineSprite( 'ghost_orange_eyes_up2',              16,  80 )
        self.defineSprite( 'ghost_orange_eyes_down1',            32,  80 )
        self.defineSprite( 'ghost_orange_eyes_down2',            48,  80 )
        self.defineSprite( 'ghost_orange_eyes_left1',            64,  80 )
        self.defineSprite( 'ghost_orange_eyes_left2',            80,  80 )
        self.defineSprite( 'ghost_orange_eyes_right1',           96,  80 )
        self.defineSprite( 'ghost_orange_eyes_right2',          112,  80 )

        self.defineSprite( 'cherry',                              0,  96 )
        self.defineSprite( 'strawberry',                         16,  96 )
        self.defineSprite( 'orange',                             32,  96 )
        self.defineSprite( 'pretzel',                            48,  96 )
        self.defineSprite( 'apple',                              64,  96 )
        self.defineSprite( 'pear',                               80,  96 )
        self.defineSprite( 'bannana',                            96,  96 )
        self.defineSprite( '500pts',                            112,  96 )

# cory: There's a bug in my SpriteSheet class definition where '200pts' from the frogger sheet is sharing the same
#       namespace as this one from the mrs_pacman SpriteSheet.  It should be separate namespaces so need to figure this
#       out.  But temporarily commenting this one out.
#        self.defineSprite( '200pts',                              0, 112 )
        self.defineSprite( '400pts',                             16, 112 )
        self.defineSprite( '800pts',                             32, 112 )
        self.defineSprite( '1600pts',                            48, 112 )
        self.defineSprite( 'ghost_invisible_eyes_up',            64, 112 )
        self.defineSprite( 'ghost_invisible_eyes_down',          80, 112 )
        self.defineSprite( 'ghost_invisible_eyes_left',          96, 112 )
        self.defineSprite( 'ghost_invisible_eyes_right',        112, 112 )
        return( h )

# ================================================================================
if __name__ == '__main__':
    # Use the SpriteSheet.exploresheet() method to display the sprites & determine their coords:
    if False:
        ss = SpriteSheet( 'sprite_sheets/mrs_pacman_16x16.png', stepx=16, stepy=16, offsetx=0, offsety=0 )
        grid = Ledgrid()
        grid.exploreSheet( ss )
        grid.clear()
        grid.close()
        sys.exit(0)
        
    # Use the AnimationSequence.addFrame() method to define a sequences of images for an animation:
    if True:        
        mrspacman_ss = MrsPacmanSheet( )

        seq1 = AnimationSequence("seq1")
        dur = 200
        seq1.addFrame( mrspacman_ss, 'pacman_right_open1', duration_ms=dur )
        seq1.addFrame( mrspacman_ss, 'pacman_right_open2', duration_ms=dur )
        seq1.addFrame( mrspacman_ss, 'pacman_right_closed', duration_ms=dur )

        seq2 = AnimationSequence("seq2")
        dur = 250
        seq2.addFrame( mrspacman_ss, 'ghost_vulnerable1', duration_ms=dur )
        seq2.addFrame( mrspacman_ss, 'ghost_vulnerable2', duration_ms=dur )
        seq2.addFrame( mrspacman_ss, 'ghost_vulnerable3', duration_ms=dur )
        seq2.addFrame( mrspacman_ss, 'ghost_vulnerable4', duration_ms=dur )

        seq3 = AnimationSequence("seq3")
        dur = 150
        seq3.addFrame( mrspacman_ss, 'ghost_red_eyes_up1', duration_ms=dur )
        seq3.addFrame( mrspacman_ss, 'ghost_red_eyes_up2', duration_ms=dur )
        seq3.addFrame( mrspacman_ss, 'ghost_red_eyes_down1', duration_ms=dur )
        seq3.addFrame( mrspacman_ss, 'ghost_red_eyes_down2', duration_ms=dur )
        seq3.addFrame( mrspacman_ss, 'ghost_red_eyes_left1', duration_ms=dur )
        seq3.addFrame( mrspacman_ss, 'ghost_red_eyes_left2', duration_ms=dur )
        seq3.addFrame( mrspacman_ss, 'ghost_red_eyes_right1', duration_ms=dur )
        seq3.addFrame( mrspacman_ss, 'ghost_red_eyes_right2', duration_ms=dur )

        seq4 = AnimationSequence("seq4")
        dur = 350
        seq4.addFrame( mrspacman_ss, 'cherry',        duration_ms=dur )
        seq4.addFrame( mrspacman_ss, 'strawberry',    duration_ms=dur )
        seq4.addFrame( mrspacman_ss, 'orange',        duration_ms=dur )
        seq4.addFrame( mrspacman_ss, 'pretzel',       duration_ms=dur )
        seq4.addFrame( mrspacman_ss, 'apple',         duration_ms=dur )
        seq4.addFrame( mrspacman_ss, 'pear',          duration_ms=dur )
        seq4.addFrame( mrspacman_ss, 'bannana',       duration_ms=dur )
        seq4.addFrame( mrspacman_ss, '500pts',        duration_ms=dur )


        seq5 = AnimationSequence("seq5")
        dur = 250
        seq5.addFrame( mrspacman_ss, '200pts',                      duration_ms=dur )
        seq5.addFrame( mrspacman_ss, '400pts',                      duration_ms=dur )
        seq5.addFrame( mrspacman_ss, '800pts',                      duration_ms=dur )
        seq5.addFrame( mrspacman_ss, '1600pts',                     duration_ms=dur )

        seq6 = AnimationSequence("seq6")
        dur = 150
        seq6.addFrame( mrspacman_ss, 'ghost_invisible_eyes_up',     duration_ms=dur )
        seq6.addFrame( mrspacman_ss, 'ghost_invisible_eyes_down',   duration_ms=dur )
        seq6.addFrame( mrspacman_ss, 'ghost_invisible_eyes_left',   duration_ms=dur )
        seq6.addFrame( mrspacman_ss, 'ghost_invisible_eyes_right',  duration_ms=dur )

        grid = Ledgrid()
        for i in range(4):
            grid.showSequence( seq1, printinfo=False )
        for i in range(2):
            grid.showSequence( seq2, printinfo=False )
        for i in range(1):
            grid.showSequence( seq3, printinfo=False )
        for i in range(1):
            grid.showSequence( seq4, printinfo=False )
        for i in range(1):
            grid.showSequence( seq5, printinfo=False )
        for i in range(3):
            grid.showSequence( seq6, printinfo=False )
        grid.clear()
        grid.close()
        sys.exit(0)
