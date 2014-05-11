#!/usr/bin/env python
''' ledgrid.py - test script for writing to PRU 0 mem using PyPRUSS library & driving ledgrid.'''

#import os
import sys
import pypruss                              # The Programmable Realtime Unit Library
import numpy as np                          # Needed for braiding the pins with the delays
import curses
from time import sleep
from PIL import Image

# ================================================================================
class AnimationSequence():
    sequence = []

    # ----
    def __init__( self ):
        pass

    # ----
    def addFrame( self, sprite, duration_ms=100):
        self.sequence.append( (sprite, duration_ms) )

# ================================================================================
class SpriteSheet():
    "SpriteSheet: Class to represent a sprite sheet image file."
    filename = ''
    offsetx = 0
    offsety = 0
    stepx = 0
    stepy = 0
    sprites = {}

    # ----
    def __init__( self, filename, stepx=16, stepy=16, offsetx=0, offsety=0 ):
        self.filename = filename
        self.stepx = stepx
        self.stepy = stepy
        self.offsetx = offsetx
        self.offsety = offsety

    # ----
    def defineSprite( self, sprite_name, x1, y1 ):
        if( self.sprites.has_key(sprite_name) == 0 ):
            self.sprites[sprite_name] = (x1, y1)
        else:
            print "Sprite", sprite_name, " was already added with defineSprite()."
            raise Exception()

    # ----
    def getSprite( self, sprite_name ):
        if( self.sprites.has_key(sprite_name) ):
            (x, y) = self.sprites[sprite_name]
            return( (self.filename, x, y) )
        else:
            print "Sprite", sprite_name, " does not exist."
            raise Exception()
        return

# ================================================================================
class Ledgrid():
    """Ledgrid class: Provides methods for displaying and animating sprites on 
    the 16x16 RGB Grid."""

    clear_leds_at_end = True

    # scaling factors to conserve power & correct color
    RedBrightnessPct = 0.43
    GrnBrightnessPct = 0.68
    BluBrightnessPct = 0.73

    # ----
    def showSequence( self ):
        pass

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
        pypruss.exec_program(0, "./ledgriddrvr.bin")    # Load firmware on PRU 0
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
        red = int( tup3val[0] * RedBrightnessPct ) 
        grn = int( tup3val[1] * GrnBrightnessPct )
        blu = int( tup3val[2] * BluBrightnessPct )
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
    def dummy( self ):
        sheet = Image.open( 'frogger.png' )
        print sheet.format, sheet.size, sheet.mode

        # Index over all the sprites in the PNG file.  It's a 24 x 20 array of 16x16 pixel sprites.
        sprite_idx_arr = []
        for iy in xrange( 15 ):
            for ix in xrange( 6 ):
                sprite_idx_arr.append( (ix, iy) )

        #sprite_idx_arr = [ (7, 0), (8, 0), (9, 0), (11, 0), (12, 0), (13, 0), (15, 0), (12, 1), (14, 1), (13, 3) ]
        # for (ix, iy) in sprite_idx_arr:
        stdscr.addstr(0,0,"Hit 'q' to quit...")
        stdscr.refresh()
        ix = iy = 0
        x1 = (ix-1)*stepx+offsetx
        y1 = (iy-1)*stepy+offsety
        while key != ord('q'):
            stdscr.addstr( 3,0, "(%d, %d)                " % (x1, y1) )
            stdscr.addstr( 4,0, "Stepsize: %d, %d" % (stepx, stepy) )
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_RIGHT:
                x1 += stepx
            elif (key == curses.KEY_LEFT) and ( x1 > 0 ):
                    x1 -= stepx
            elif (key == curses.KEY_UP) and ( y1 > 0 ):
                    y1 -= stepy
            elif key == curses.KEY_DOWN:
                y1 += stepy
            elif key == ord('x'):
                stepx -= 1
            elif key == ord('X'):
                stepx += 1
            elif key == ord('y'):
                stepy -= 1
            elif key == ord('Y'):
                stepy += 1
            x2 = x1 + sizex
            y2 = y1 + sizey
            box = (x1, y1, x2, y2)
            region = sheet.crop( box )

            ni = Image.new('RGB', (sizex, sizey) )
            ni.paste( region, (0, 0, sizex, sizey) )
            newimgname = "img_%d_%d.png" % (ix, iy)
            #print "Writing %s" % newimgname
            #ni.save( newimgname )
            data = self._get_img_array( ni )
            self._sendPixels( data )

# ================================================================================
def mymain( stdscr ):
    #stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)
    key = ''

    stdscr.addstr( 0,0, "Hi" )
    stdscr.refresh()

    frogger = SpriteSheet( 'frogger.png', stepx=24, stepy=24, offsetx=32, offsety=32 )
    frogger.defineSprite( 'explode1', 48, 112 )

    seq1 = AnimationSequence()
    seq1.addFrame( frogger.getSprite('explode'), duration_ms=60 )

    grid = Ledgrid()
    #grid.dummy()

    grid.showSequence( seq1 )
    grid.clear()
    grid.close()

    ###curses.endwin()
    sys.exit(0)

# --------------------------------------------------------------------------------
if __name__ == '__main__':
    curses.wrapper( mymain )
