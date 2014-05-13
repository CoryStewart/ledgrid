#!/usr/bin/env python
''' FroggerSheet.py - Class for defining the Frogger SpriteSheet class and all of the img frames within the sheet.'''

import sys
from Ledgrid import *

# ================================================================================
class FroggerSheet(SpriteSheet):
    def __init__( self ):
        h = SpriteSheet.__init__( self, 'sprite_sheets/frogger.png', stepx=16, stepy=16, offsetx=32, offsety=32 ) 

        self.defineSprite( 'null', 160, 16 )

        self.defineSprite( 'frog_green_up1', 16, 16 )  # frog at rest
        self.defineSprite( 'frog_green_up2', 40, 16 )  # frog pushing off from a jump
        self.defineSprite( 'frog_green_up3', 64, 16 )  # frog in the air
        self.defineSprite( 'frog_green_left1', 88, 16 )
        self.defineSprite( 'frog_green_left2', 112, 16 )
        self.defineSprite( 'frog_green_left3', 136, 16 )

        self.defineSprite( 'frog_blue_up1', 16, 48 )  # frog at rest
        self.defineSprite( 'frog_blue_up2', 40, 48 )  # frog pushing off from a jump
        self.defineSprite( 'frog_blue_up3', 64, 48 )  # frog in the air
        self.defineSprite( 'frog_blue_left1', 88, 48 )
        self.defineSprite( 'frog_blue_left2', 112, 48 )
        self.defineSprite( 'frog_blue_left3', 136, 48 )

        self.defineSprite( 'frog_yellow_up1', 16, 80 )  # frog at rest
        self.defineSprite( 'frog_yellow_up2', 40, 80 )  # frog pushing off from a jump
        self.defineSprite( 'frog_yellow_up3', 64, 80 )  # frog in the air
        self.defineSprite( 'frog_yellow_left1', 88, 80 )
        self.defineSprite( 'frog_yellow_left2', 112, 80 )
        self.defineSprite( 'frog_yellow_left3', 136, 80 )

        self.defineSprite( 'skull1', 16, 112  )
        self.defineSprite( 'explode1', 48, 112 )
        self.defineSprite( 'explode2', 72, 112 )
        self.defineSprite( 'explode3', 96, 112 )
        self.defineSprite( 'skull2', 128, 112 )
        self.defineSprite( 'skull3', 152, 112 )
        self.defineSprite( 'skull4', 176, 112 )

        self.defineSprite( 'island_bog', 16, 144 )
        self.defineSprite( 'SwimmingTurtle1', 48, 144 )
        self.defineSprite( 'SwimmingTurtle2', 72, 144 )
        self.defineSprite( 'SwimmingTurtle3', 96, 144 )
        self.defineSprite( 'Turtle_Sinking1', 128, 144 )
        self.defineSprite( 'Turtle_Sinking2', 152, 144 )
        self.defineSprite( 'Turtle_Sinking3', 176, 144 )

        self.defineSprite( '100pts', 16, 176 )
        self.defineSprite( '200pts', 40, 176 )
        self.defineSprite( 'bee', 80, 176 )
        self.defineSprite( 'FrogStanding1', 128, 176 )
        self.defineSprite( 'FrogStanding2', 104, 176 )
        self.defineSprite( 'alligator_red_headopening1', 152, 176 )
        self.defineSprite( 'alligator_red_headopening2', 176, 176 )

        self.defineSprite( 'cove_NE', 16, 208 ) # halfsize (8x8)
        self.defineSprite( 'cove_NW', 32, 208 ) # halfsize (8x8)
        self.defineSprite( 'cove_N', 16, 208 ) # halfsize (8x8)
        self.defineSprite( 'alligator_orange_body', 80, 208 ) # 2 wide

        self.defineSprite( 'alligator_orange_headopen1', 120, 208 )
        self.defineSprite( 'alligator_orange_headopen2', 144, 208 )

        self.defineSprite( 'cove_E', 16, 224 ) # halfsize (8x8)
        self.defineSprite( 'cove', 32, 224 ) # halfsize (8x8)
        self.defineSprite( 'cove_W', 48, 224 ) # halfsize (8x8)

        self.defineSprite( 'cove_SW', 16, 240 ) # halfsize (8x8)
        self.defineSprite( 'cove_SE', 48, 240 ) # halfsize (8x8)
        self.defineSprite( 'seamonster1', 80, 240 )
        self.defineSprite( 'seamonster2', 104, 240 )

        self.defineSprite( 'snake1', 16, 272 ) # 2 wide
        self.defineSprite( 'snake2', 16, 304 ) # 2 wide
        self.defineSprite( 'snake3', 56, 272 ) # 2 wide
        self.defineSprite( 'snake4', 56, 304 ) # 2 wide
        self.defineSprite( 'snake5', 96, 272 ) # 2 wide
        self.defineSprite( 'log', 112, 304 ) # 3 wide
        self.defineSprite( 'racecar1', 16, 336 )
        self.defineSprite( 'bulldozer', 40, 336 )
        self.defineSprite( 'truck', 64, 336 ) # 2 wide
        self.defineSprite( 'compact_car', 104, 336 )
        self.defineSprite( 'racecar2', 128, 336 )
        self.defineSprite( 'frogger_F', 16, 368 )
        self.defineSprite( 'frogger_R', 40, 368 )
        self.defineSprite( 'frogger_O', 64, 368 )
        self.defineSprite( 'frogger_G', 88, 368 )
        self.defineSprite( 'frogger_E', 112, 368 )
        self.defineSprite( 'frogger_ ', 136, 368 ) # space
        self.defineSprite( 'FrogSplat1', 128, 144 )
        self.defineSprite( 'FrogSplat2', 152, 144 )
        step = 16
        x = 188
        x += step; self.defineSprite( 'A_yel', x, 108 )
        x += step; self.defineSprite( 'B_yel', x, 108 )
        x += step; self.defineSprite( 'C_yel', x, 108 )
        x += step; self.defineSprite( 'D_yel', x, 108 )
        x += step; self.defineSprite( 'E_yel', x, 108 )
        x += step; self.defineSprite( 'F_yel', x, 108 )
        x += step; self.defineSprite( 'G_yel', x, 108 )
        x += step; self.defineSprite( 'H_yel', x, 108 )
        x += step; self.defineSprite( 'I_yel', x, 108 )
        x += step; self.defineSprite( 'J_yel', x, 108 )
        x = 188
        x += step; self.defineSprite( 'K_yel', x, 124 )
        x += step; self.defineSprite( 'L_yel', x, 124 )
        x += step; self.defineSprite( 'M_yel', x, 124 )
        x += step; self.defineSprite( 'N_yel', x, 124 )
        x += step; self.defineSprite( 'O_yel', x, 124 )
        x += step; self.defineSprite( 'P_yel', x, 124 )
        x += step; self.defineSprite( 'Q_yel', x, 124 )
        x += step; self.defineSprite( 'R_yel', x, 124 )
        x += step; self.defineSprite( 'S_yel', x, 124 )
        x += step; self.defineSprite( 'T_yel', x, 124 )
        x = 188
        x += step; self.defineSprite( 'U_yel', x, 140 )
        x += step; self.defineSprite( 'V_yel', x, 140 )
        x += step; self.defineSprite( 'W_yel', x, 140 )
        x += step; self.defineSprite( 'X_yel', x, 140 )
        x += step; self.defineSprite( 'Y_yel', x, 140 )
        x += step; self.defineSprite( 'Z_yel', x, 140 )
        x += step; self.defineSprite( 'dash_yel', x, 140 )
        x += step; self.defineSprite( 'space', x, 140 )
        self.defineSprite( 'Box_yel', 348, 140 )
        self.defineSprite( 'Copyright_yel', 332, 140 )

        # Red:
        #     0 = 204,156
        #     1 = 220,156
        #     ... 9 = 348,156
        # 
        # Blue:
        #     0 = 204, 220
        #     1 = 220, 220
        #     9 = 348, 220
        # Purple:
        #     9 = 348, 284
        return( h )

# ================================================================================
if __name__ == '__main__':
    # Use the SpriteSheet.exploresheet() method to display the sprites & determine their coords:
    if False:
        ss = SpriteSheet( 'sprite_sheets/frogger.png', stepx=16, stepy=16, offsetx=0, offsety=0 )
        grid = Ledgrid()
        grid.exploreSheet( ss )
        grid.clear()
        grid.close()
        sys.exit(0)
        
    # Use the AnimationSequence.addFrame() method to define a sequences of images for an animation:
    if True:        
        frogger_ss = FroggerSheet( )
        dur = 150

        seq1 = AnimationSequence("seq1")
        seq1.addFrame( frogger_ss, 'SwimmingTurtle1', duration_ms=dur )
        seq1.addFrame( frogger_ss, 'SwimmingTurtle2', duration_ms=dur )
        seq1.addFrame( frogger_ss, 'SwimmingTurtle3', duration_ms=dur )
        seq1.addFrame( frogger_ss, 'SwimmingTurtle2', duration_ms=dur )

        seq2 = AnimationSequence("seq2")
        seq2.addFrame( frogger_ss, 'explode1', duration_ms=dur )
        seq2.addFrame( frogger_ss, 'explode2', duration_ms=dur )
        seq2.addFrame( frogger_ss, 'explode3', duration_ms=dur )
        seq2.addFrame( frogger_ss, 'explode1', duration_ms=dur )
        seq2.addFrame( frogger_ss, 'explode2', duration_ms=dur )
        seq2.addFrame( frogger_ss, 'explode3', duration_ms=dur )
        seq2.addFrame( frogger_ss, 'explode1', duration_ms=dur )
        seq2.addFrame( frogger_ss, 'explode2', duration_ms=dur )
        seq2.addFrame( frogger_ss, 'explode3', duration_ms=dur )

        seq3 = AnimationSequence("seq3")
        seq3.addFrame( frogger_ss, 'skull1', duration_ms=dur )
        seq3.addFrame( frogger_ss, 'skull2', duration_ms=dur )
        seq3.addFrame( frogger_ss, 'skull3', duration_ms=dur )
        seq3.addFrame( frogger_ss, 'skull4', duration_ms=dur )
        seq3.addFrame( frogger_ss, 'racecar1', duration_ms=dur )
        seq3.addFrame( frogger_ss, 'racecar2', duration_ms=dur )
        seq3.addFrame( frogger_ss, 'alligator_orange_headopen1', duration_ms=dur )
        seq3.addFrame( frogger_ss, 'alligator_orange_headopen2', duration_ms=dur )
        seq3.addFrame( frogger_ss, 'FrogStanding1', duration_ms=dur )
        seq3.addFrame( frogger_ss, 'FrogStanding2', duration_ms=dur )
        seq3.addFrame( frogger_ss, 'FrogStanding1', duration_ms=dur )
        seq3.addFrame( frogger_ss, 'FrogStanding2', duration_ms=dur )
        seq3.addFrame( frogger_ss, 'FrogStanding1', duration_ms=dur )
        seq3.addFrame( frogger_ss, 'FrogStanding2', duration_ms=dur )
        seq3.addFrame( frogger_ss, '100pts', duration_ms=dur )
        seq3.addFrame( frogger_ss, '200pts', duration_ms=dur )

        grid = Ledgrid()
        grid.showSequence( seq1, printinfo=True )
        grid.showSequence( seq1, printinfo=True )
        grid.showSequence( seq1, printinfo=True )
        grid.showSequence( seq2, printinfo=True )
        grid.showSequence( seq3, printinfo=True )
        grid.clear()
        grid.close()
        sys.exit(0)
