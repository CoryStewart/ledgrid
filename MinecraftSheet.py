#!/usr/bin/env python
''' MinecraftSheet.py - Class for defining the Minecraft SpriteSheet class and all of the img frames within the sheet.'''

import sys
from Ledgrid import *

# ================================================================================
class MinecraftSheet(SpriteSheet):
    def __init__( self ):
        h = SpriteSheet.__init__( self, 'sprite_sheets/MinecraftSheet_24x20.png', stepx=16, stepy=16, offsetx=0, offsety=0 ) 

        self.defineSprite( 'glass', 64, 272 )
        self.defineSprite( 'lava', 176, 288 )
        self.defineSprite( 'tracks_redstone_on', 144, 208 )
        self.defineSprite( 'tracks_redstone_off', 144, 224 )
        self.defineSprite( 'yel_tracks_redstone_on', 48, 176 )
        self.defineSprite( 'yel_tracks_redstone_off', 48, 160 )
        self.defineSprite( 'grass1', 128, 192 )
        self.defineSprite( 'grass2', 144, 192 )
        self.defineSprite( 'grass3', 160, 192 )
        self.defineSprite( 'grass4', 176, 192 )
        self.defineSprite( 'torch_on', 48, 96 )
        self.defineSprite( 'torch_off', 48, 112 )
        self.defineSprite( 'ladder', 48, 80 )
        self.defineSprite( 'wheat1', 128, 80 )
        self.defineSprite( 'wheat2', 144, 80 )
        self.defineSprite( 'wheat3', 160, 80 )
        self.defineSprite( 'wheat4', 176, 80 )
        self.defineSprite( 'wheat5', 192, 80 )
        self.defineSprite( 'wheat6', 208, 80 )
        self.defineSprite( 'wheat7', 224, 80 )
        self.defineSprite( 'wheat8', 240, 80 )
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
        minecraft_ss = MinecraftSheet();
        dur_short = 100
        dur_medium = 150
        dur_long = 350

        seq1 = AnimationSequence("seq1")
        seq1.addFrame( minecraft_ss, 'wheat1', duration_ms=dur_short )
        seq1.addFrame( minecraft_ss, 'wheat2', duration_ms=dur_short )
        seq1.addFrame( minecraft_ss, 'wheat3', duration_ms=dur_short )
        seq1.addFrame( minecraft_ss, 'wheat4', duration_ms=dur_short )
        seq1.addFrame( minecraft_ss, 'wheat5', duration_ms=dur_short )
        seq1.addFrame( minecraft_ss, 'wheat6', duration_ms=dur_short )
        seq1.addFrame( minecraft_ss, 'wheat7', duration_ms=dur_short )
        seq1.addFrame( minecraft_ss, 'wheat8', duration_ms=dur_short )
        seq1.addFrame( minecraft_ss, 'glass', duration_ms=dur_medium )
        seq1.addFrame( minecraft_ss, 'lava', duration_ms=dur_medium )
        seq1.addFrame( minecraft_ss, 'tracks_redstone_on', duration_ms=dur_long )
        seq1.addFrame( minecraft_ss, 'tracks_redstone_off', duration_ms=dur_long )
        seq1.addFrame( minecraft_ss, 'yel_tracks_redstone_on', duration_ms=dur_long )
        seq1.addFrame( minecraft_ss, 'yel_tracks_redstone_off', duration_ms=dur_long )
        seq1.addFrame( minecraft_ss, 'grass1', duration_ms=dur_medium )
        seq1.addFrame( minecraft_ss, 'grass2', duration_ms=dur_medium )
        seq1.addFrame( minecraft_ss, 'grass3', duration_ms=dur_medium )
        seq1.addFrame( minecraft_ss, 'grass4', duration_ms=dur_medium )
        seq1.addFrame( minecraft_ss, 'torch_on', duration_ms=dur_long )
        seq1.addFrame( minecraft_ss, 'torch_off', duration_ms=dur_long )
        seq1.addFrame( minecraft_ss, 'ladder', duration_ms=dur_long )

        grid = Ledgrid()
        grid.showSequence( seq1, printinfo=False )
        grid.clear()
        grid.close()
        sys.exit(0)
