#!/usr/bin/env python
''' MarioSheet.py - Class for defining the Mario SpriteSheet class and all of the img frames within the sheet.'''

import sys
from Ledgrid import *

# ================================================================================
class MarioSheet(SpriteSheet):
    def __init__( self ):
        h = SpriteSheet.__init__( self, 'sprite_sheets/mario_sheet.png', stepx=16, stepy=16, offsetx=0, offsety=0 ) 

        self.defineSprite( 'mario1', 0, 0 )
        self.defineSprite( 'mario2', 16, 0 )
        self.defineSprite( 'mario3', 32, 0 )
        return( h )

# ================================================================================
if __name__ == '__main__':
    # Use the SpriteSheet.exploresheet() method to display the sprites & determine their coords:
    if False:
        ss = SpriteSheet( 'sprite_sheets/mario_sheet.png', stepx=16, stepy=16, offsetx=0, offsety=0 )
        grid = Ledgrid()
        grid.exploreSheet( ss )
        grid.clear()
        grid.close()
        sys.exit(0)
        
    # Use the AnimationSequence.addFrame() method to define a sequences of images for an animation:
    if True:        
        mario_ss = MarioSheet( )
        dur = 60

        seq1 = AnimationSequence("seq1")
        seq1.addFrame( mario_ss, 'mario1', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario2', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario3', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario2', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario1', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario2', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario3', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario2', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario1', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario2', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario3', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario2', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario1', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario2', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario3', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario2', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario1', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario2', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario3', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario2', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario1', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario2', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario3', duration_ms=dur )
        seq1.addFrame( mario_ss, 'mario2', duration_ms=dur )

        grid = Ledgrid()
        grid.showSequence( seq1, printinfo=False )
        grid.clear()
        grid.close()
        sys.exit(0)
