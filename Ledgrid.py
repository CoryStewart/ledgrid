#!/usr/bin/env python
''' Ledgrid.py - Module for sending SpriteSheet images and animations to the Ledgrid Hardware.'''

#import os
import sys
import pypruss                              # The Programmable Realtime Unit Library
import numpy as np                          # Needed for braiding the pins with the delays
from time import sleep
from PIL import Image

# ================================================================================
class AnimationSequence( ):

    # ----
    def __init__( self, seqname ):
        self._sequence = []
        self.name = seqname

    # ----
    def addFrame( self, spritesheet, imgname, duration_ms=100 ):
        self._sequence.append( (spritesheet, imgname, duration_ms) )
    # ----
    def __getitem__( self, i ):
        return( self._sequence[i] )
    # ----
    def getFrame( self, i ):
        return( self._sequence[i] )
    # ----
    def getFrameCnt( self ):
        return( len(self._sequence) )
    # ----
    def __str__( self ):
        return( "AnimationSequence( %s )" % (self.name) )

# ================================================================================
class Sprite():
    x1 = y1 = 0
    x2 = y2 = 0
    sizex = sizey = 0
    name = ''

    def __init__( self, name, x1, y1, sizex=16, sizey=16 ):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1 + sizex
        self.y2 = y1 + sizey
        self.sizex = sizex
        self.sizey = sizey

# ================================================================================
class SpriteSheet():
    "SpriteSheet: Class to represent a sprite sheet image file."
    filename = ''
    offsetx = 0
    offsety = 0
    stepx = 0
    stepy = 0
    sizex = 16  # x size of the images within the sheet
    sizey = 16  # y size of the images within the sheet
    maxx = 0    # max x coord of the whole sheet
    maxy = 0    # max y coord of the whole sheet

    sprites = {}

    # ----
    def __init__( self, filename, stepx=16, stepy=16, offsetx=0, offsety=0, maxx=0, maxy=0 ):
        self.filename = filename
        self.stepx = stepx
        self.stepy = stepy
        self.offsetx = offsetx
        self.offsety = offsety

    # ----
    def defineSprite( self, sprite_name, x1, y1, sizex=16, sizey=16 ):
        if( self.sprites.has_key(sprite_name) == 0 ):
            s = Sprite( sprite_name, x1, y1, sizex, sizey )
            self.sprites[sprite_name] = s
        else:
            print "Sprite", sprite_name, " was already added with defineSprite()."
            raise Exception()

    # ----
    def getSprite( self, sprite_name ):
        if( self.sprites.has_key(sprite_name) ):
            return( self.sprites[sprite_name] )
        else:
            print "Sprite", sprite_name, " does not exist."
            raise Exception()
        return

# ================================================================================
class FroggerSheet(SpriteSheet):
    def __init__( self ):
        h = SpriteSheet.__init__( self, 'sprite_sheets/frogger.png', stepx=16, stepy=16, offsetx=32, offsety=32 ) 

        self.defineSprite( 'explode1', 48, 112 )
        self.defineSprite( 'explode2', 72, 112 )
        self.defineSprite( 'explode3', 96, 112 )
        self.defineSprite( 'skull1', 16, 112  )
        self.defineSprite( 'skull2', 128, 112 )
        self.defineSprite( 'skull3', 152, 112 )
        self.defineSprite( 'skull4', 176, 112 )
        self.defineSprite( 'snake1', 16, 272 ) # 2 wide
        self.defineSprite( 'snake2', 16, 304 ) # 2 wide
        self.defineSprite( 'snake3', 56, 272 ) # 2 wide
        self.defineSprite( 'snake4', 56, 304 ) # 2 wide
        self.defineSprite( 'snake5', 96, 272 ) # 2 wide
        self.defineSprite( 'log', 112, 304 ) # 3 wide
        self.defineSprite( 'racecar1', 16, 336 )
        self.defineSprite( 'bulldozer', 40, 336 )
        self.defineSprite( 'truck', 64, 336 ) # 2 wide
        self.defineSprite( 'compactcar', 104, 336 )
        self.defineSprite( 'racecar2', 128, 336 )
        self.defineSprite( 'frogger_F', 16, 368 )
        self.defineSprite( 'frogger_R', 40, 368 )
        self.defineSprite( 'frogger_O', 64, 368 )
        self.defineSprite( 'frogger_G', 88, 368 )
        self.defineSprite( 'frogger_E', 112, 368 )
        self.defineSprite( 'alligator_headopen', 120, 208 )
        self.defineSprite( 'FrogStanding1', 128, 176 )
        self.defineSprite( 'FrogStanding2', 104, 176 )
        self.defineSprite( 'SwimmingTurtle1', 48, 144 )
        self.defineSprite( 'SwimmingTurtle2', 72, 144 )
        self.defineSprite( 'SwimmingTurtle3', 96, 144 )
        self.defineSprite( 'FrogSplat1', 128, 144 )
        self.defineSprite( 'FrogSplat2', 152, 144 )
        self.defineSprite( '100pts', 16, 176 )
        self.defineSprite( '200pts', 40, 176 )
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
class MarioSheet(SpriteSheet):
    def __init__( self ):
        h = SpriteSheet.__init__( self, 'sprite_sheets/mario_sheet.png', stepx=16, stepy=16, offsetx=0, offsety=0 ) 

        self.defineSprite( 'mario1', 0, 0 )
        self.defineSprite( 'mario2', 16, 0 )
        self.defineSprite( 'mario3', 32, 0 )
        return( h )

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
class Ledgrid():
    """Ledgrid class: Provides methods for displaying and animating sprites on 
    the 16x16 RGB Grid."""

    clear_leds_at_end = True
    prucode_file = "./pru_code/ledgriddrvr.bin"

    # scaling factors to conserve power & correct color
    RedBrightnessPct = 0.43
    GrnBrightnessPct = 0.68
    BluBrightnessPct = 0.73

    # ----
    def close( self ):
        if( self.clear_leds_at_end ):
            self.clear()
        pypruss.exit()

    # ----
    def __init__( self ):
        pypruss.modprobe()                          # This only has to be called once per boot
        pypruss.init()                              # Init the PRU
        pypruss.open(0)                             # Open PRU event 0 which is PRU0_ARM_INTERRUPT
        pypruss.pruintc_init()                      # Init the interrupt controller

    # ----
    def _sendPixels( self, data ):
        pypruss.pru_write_memory(0, 0, data)    # Load the data in the PRU ram
        pypruss.exec_program(0, self.prucode_file )    # Load firmware on PRU 0
        pypruss.wait_for_event(0)               # Wait for event 0 which is connected to PRU0_ARM_INTERRUPT
        pypruss.clear_event(0)                  # Clear the event
        #sleep( 0.500 )                          # sleep 1s

    # ----
    def clear( self ):
        'Clear the ledgrid (write black to all pixels)'
        empty_data = [256] + [0]*256            # 1st index is #_of_pixels, then 256 pixel values of 0 follow it
        self._sendPixels( empty_data )

    # ----
    def sendImage( self ):
        pass

    # ----
    def _reversebits( self, val ):
        newval = int('{:08b}'.format(val)[::-1], 2)
        return( newval )

    # ----
    def _tuple3_to_hex( self, tup3val ):
        # Takes a tuple of 3 color values & formats it as a single 32bit integer with 
        # GRB (grn red blu) 8 bit intensity values.
        red = int( tup3val[0] * self.RedBrightnessPct ) 
        grn = int( tup3val[1] * self.GrnBrightnessPct )
        blu = int( tup3val[2] * self.BluBrightnessPct )
        red = self._reversebits( red )
        grn = self._reversebits( grn )
        blu = self._reversebits( blu )
        val = (blu << 16) + (red << 8) + (grn)
        return( val )

    # ----
    def _get_img_array( self, image ):
        if image.mode != 'RGB':
            image = image.convert( 'RGB' ) # change to RGB if you don't care about alpha

        pixels = image.load( )
        data = []

        width, height = image.size
        #print "Image size: (%d, %d)." % (width, height)
        for idx in xrange( 0, (height * width) + 2 ):
            data.append( 0 )

        idx = 0
        data[idx] = height * width # First index contains Number of Pixels
        idx += 1
        for h in range( 0, height ):
            if( h % 2 == 0 ):
                for w in range( 0, width ):
                    color = pixels[w,h]
                    data[idx] = self._tuple3_to_hex( color )
                    idx += 1
            else:
                for w in range( width-1, -1, -1 ):
                    color = pixels[w,h]
                    data[idx] = self._tuple3_to_hex( color )
                    idx += 1
        return( data )

    # ----
    def showSequence( self, seq, printinfo=True ):
        if printinfo:
            print "showSequence( %s ):" % (seq)
        for i in range( seq.getFrameCnt() ):
            (ss, imgname, duration_ms) = seq[i] # ss is the spritesheet object handle
            s = ss.sprites[imgname]             # s is the sprite object handle
            if printinfo:
                print "i=%d : ss.filename=%s, " % (i, ss.filename),
                print "imgname=%s, duration_ms=%d, x1=%d, y1=%d, x2=%d, y2=%d, sizex=%d, sizey=%d" % (imgname, duration_ms, s.x1, s.y1, s.x2, s.y2, s.sizex, s.sizey)
            sheet = Image.open( ss.filename )
            #print 'Sheet info: format=%s, size=%s, mode=%s' % (sheet.format, sheet.size, sheet.mode)

            box = (s.x1, s.y1, s.x2, s.y2)
            region = sheet.crop( box )

            ni = Image.new('RGB', (s.sizex, s.sizey) )
            ni.paste( region, (0, 0, s.sizex, s.sizey) )
            data = self._get_img_array( ni )
            self._sendPixels( data )
            sleep( 0.001 * duration_ms  )

    # ----
    def exploreSheet( self, ss ):
        """exploreSheet: Takes a reference to a SpriteSheet object, displays a 16x16 pixel window of the sheet and
        the coordinates of the window.  It takes keypresses to allow you to pan the window around to find images
        within the sheet and determine the coordinates of each image.  Keys:
            k, j, h, l : move the window in stepsize increments: up, down, left, right.
            x, X       : decrease or increase (respectively) the x-axis stepsize
            y, Y       : decrease or increase (respectively) the y-axis stepsize
            q          : quit
        """
        print "exploreSheet( %s ):" % (ss)
        x1 = y1 = 0
        sizex = ss.sizex
        sizey = ss.sizey
        x2 = sizex
        y2 = sizey
        stepx = ss.stepx
        stepy = ss.stepy
        maxx = ss.maxx
        maxy = ss.maxy
        key = ''
        while key != 'q':
            print "Position = (%d, %d).  Stepsize = %d, %d" % (x1, y1, stepx, stepy)
            if key == 'k' and (y1 > 0):   # up
                print "Up"
                y1 -= stepy
            #elif key == ord( 'j' ) and ((y1 < maxy) or (maxy == 0)): # down
            elif key == 'j' and ((y1 < maxy) or (maxy == 0)): # down
                print "Down"
                y1 += stepy
            elif key == 'h' and (x1 > 0): # left
                print "Left"
                x1 -= stepx
            elif key == 'l' and ((x1 < maxx) or (maxx == 0)): # right
                print "Right"
                x1 += stepx
            elif key == 'x':
                print "Decrease StepX"
                stepx -= 1
            elif key == 'X':
                print "Increase StepX"
                stepx += 1
            elif key == 'y':
                print "Decrease StepY"
                stepy -= 1
            elif key == 'Y':
                print "Increase StepY"
                stepy += 1

            x2 = x1 + sizex
            y2 = y1 + sizey
            box = (x1, y1, x2, y2)
            sheet = Image.open( ss.filename )
            if( maxx == 0 or maxy == 0 ):
                maxx, maxy = sheet.size
            #print 'Sheet info: format=%s, size=%s, mode=%s' % (sheet.format, sheet.size, sheet.mode)
            region = sheet.crop( box )
            ni = Image.new( "RGB", (ss.sizex, ss.sizey) )
            ni.paste( region, (0, 0, ss.sizex, ss.sizey) )
            data = self._get_img_array( ni )
            self._sendPixels( data )
            while True:
                print "waiting for key"
                key = sys.stdin.read(1)
                key = key.rstrip()
                if key != ord( '\n' ) and key != ord( '\r' ):
                    print "Pressed key '%s'" % (key)
                    break

# ================================================================================
if __name__ == '__main__':
    frogger = FroggerSheet( )
    mario = MarioSheet( )
    minecraft = MinecraftSheet();

    # Use the SpriteSheet.exploresheet() method to display the sprites & determine their coords:
    if False:
        mrspacman = SpriteSheet( 'sprite_sheets/mrs_pacman_16x16.png', stepx=16, stepy=16, offsetx=0, offsety=0 )
        grid = Ledgrid()
        grid.exploreSheet( mrspacman )
        grid.clear()
        grid.close()
        sys.exit(0)
        
    # Use the AnimationSequence.addFrame() method to define a sequences of images for an animation:
    if True:        
        seq3 = AnimationSequence("seq3")
        seq3.addFrame( mario, 'mario1', duration_ms=1000 )

        seq1 = AnimationSequence("seq1")

        seq1.addFrame( minecraft, 'wheat1', duration_ms=100 )
        seq1.addFrame( minecraft, 'wheat2', duration_ms=100 )
        seq1.addFrame( minecraft, 'wheat3', duration_ms=100 )
        seq1.addFrame( minecraft, 'wheat4', duration_ms=100 )
        seq1.addFrame( minecraft, 'wheat5', duration_ms=100 )
        seq1.addFrame( minecraft, 'wheat6', duration_ms=100 )
        seq1.addFrame( minecraft, 'wheat7', duration_ms=100 )
        seq1.addFrame( minecraft, 'wheat8', duration_ms=100 )
        seq1.addFrame( minecraft, 'glass', duration_ms=150 )
        seq1.addFrame( minecraft, 'lava', duration_ms=150 )
        seq1.addFrame( minecraft, 'tracks_redstone_on', duration_ms=250 )
        seq1.addFrame( minecraft, 'tracks_redstone_off', duration_ms=250 )
        seq1.addFrame( minecraft, 'yel_tracks_redstone_on', duration_ms=250 )
        seq1.addFrame( minecraft, 'yel_tracks_redstone_off', duration_ms=250 )
        seq1.addFrame( minecraft, 'grass1', duration_ms=150 )
        seq1.addFrame( minecraft, 'grass2', duration_ms=150 )
        seq1.addFrame( minecraft, 'grass3', duration_ms=150 )
        seq1.addFrame( minecraft, 'grass4', duration_ms=150 )
        seq1.addFrame( minecraft, 'torch_on', duration_ms=250 )
        seq1.addFrame( minecraft, 'torch_off', duration_ms=250 )
        seq1.addFrame( minecraft, 'ladder', duration_ms=350 )

        seq1.addFrame( frogger, 'explode1', duration_ms=150 )
        seq1.addFrame( frogger, 'explode2', duration_ms=150 )
        seq1.addFrame( frogger, 'explode3', duration_ms=150 )
        seq1.addFrame( frogger, 'explode1', duration_ms=150 )
        seq1.addFrame( frogger, 'explode2', duration_ms=150 )
        seq1.addFrame( frogger, 'explode3', duration_ms=150 )
        seq1.addFrame( frogger, 'explode1', duration_ms=150 )
        seq1.addFrame( frogger, 'explode2', duration_ms=150 )
        seq1.addFrame( frogger, 'explode3', duration_ms=150 )
        seq1.addFrame( frogger, 'skull1', duration_ms=150 )
        seq1.addFrame( frogger, 'skull2', duration_ms=150 )
        seq1.addFrame( frogger, 'skull3', duration_ms=150 )
        seq1.addFrame( frogger, 'skull4', duration_ms=150 )
        seq1.addFrame( frogger, 'racecar1', duration_ms=150 )
        seq1.addFrame( frogger, 'racecar2', duration_ms=150 )
        seq1.addFrame( frogger, 'alligator_headopen', duration_ms=150 )
        seq1.addFrame( frogger, 'FrogStanding1', duration_ms=150 )
        seq1.addFrame( frogger, 'FrogStanding2', duration_ms=150 )
        seq1.addFrame( frogger, 'FrogStanding1', duration_ms=150 )
        seq1.addFrame( frogger, 'FrogStanding2', duration_ms=150 )
        seq1.addFrame( frogger, 'FrogStanding1', duration_ms=150 )
        seq1.addFrame( frogger, 'FrogStanding2', duration_ms=150 )
        seq1.addFrame( frogger, 'SwimmingTurtle1', duration_ms=150 )
        seq1.addFrame( frogger, 'SwimmingTurtle2', duration_ms=150 )
        seq1.addFrame( frogger, 'SwimmingTurtle3', duration_ms=150 )
        seq1.addFrame( frogger, 'SwimmingTurtle2', duration_ms=150 )
        seq1.addFrame( frogger, 'SwimmingTurtle1', duration_ms=150 )
        seq1.addFrame( frogger, 'SwimmingTurtle2', duration_ms=150 )
        seq1.addFrame( frogger, 'SwimmingTurtle3', duration_ms=150 )
        seq1.addFrame( frogger, 'SwimmingTurtle2', duration_ms=150 )
        seq1.addFrame( frogger, 'SwimmingTurtle1', duration_ms=150 )
        seq1.addFrame( frogger, 'SwimmingTurtle2', duration_ms=150 )
        seq1.addFrame( frogger, 'SwimmingTurtle3', duration_ms=150 )
        seq1.addFrame( frogger, 'FrogSplat1', duration_ms=150 )
        seq1.addFrame( frogger, 'FrogSplat2', duration_ms=150 )
        seq1.addFrame( frogger, '100pts', duration_ms=150 )
        seq1.addFrame( frogger, '200pts', duration_ms=150 )

        seq2 = AnimationSequence("seq2")
        seq2.addFrame( mario, 'mario1', duration_ms=60 )
        seq2.addFrame( mario, 'mario2', duration_ms=60 )
        seq2.addFrame( mario, 'mario3', duration_ms=60 )
        seq2.addFrame( mario, 'mario2', duration_ms=60 )
        seq2.addFrame( mario, 'mario1', duration_ms=60 )
        seq2.addFrame( mario, 'mario2', duration_ms=60 )
        seq2.addFrame( mario, 'mario3', duration_ms=60 )
        seq2.addFrame( mario, 'mario2', duration_ms=60 )
        seq2.addFrame( mario, 'mario1', duration_ms=60 )
        seq2.addFrame( mario, 'mario2', duration_ms=60 )
        seq2.addFrame( mario, 'mario3', duration_ms=60 )
        seq2.addFrame( mario, 'mario2', duration_ms=60 )
        seq2.addFrame( mario, 'mario1', duration_ms=60 )
        seq2.addFrame( mario, 'mario2', duration_ms=60 )
        seq2.addFrame( mario, 'mario3', duration_ms=60 )
        seq2.addFrame( mario, 'mario2', duration_ms=60 )
        seq2.addFrame( mario, 'mario1', duration_ms=60 )
        seq2.addFrame( mario, 'mario2', duration_ms=60 )
        seq2.addFrame( mario, 'mario3', duration_ms=60 )
        seq2.addFrame( mario, 'mario2', duration_ms=60 )
        seq2.addFrame( mario, 'mario1', duration_ms=60 )
        seq2.addFrame( mario, 'mario2', duration_ms=60 )
        seq2.addFrame( mario, 'mario3', duration_ms=60 )
        seq2.addFrame( mario, 'mario2', duration_ms=60 )

    grid = Ledgrid()
    grid.showSequence( seq3, printinfo=False )
    grid.showSequence( seq2, printinfo=False )
    grid.showSequence( seq1, printinfo=False )
    grid.clear()
    grid.close()
    sys.exit(0)
