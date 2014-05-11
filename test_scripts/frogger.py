#!/usr/bin/env python
''' ledgrid.py - test script for writing to PRU 0 mem using PyPRUSS library & driving ledgrid.'''

#import os
import sys
import pypruss                              # The Programmable Realtime Unit Library
import numpy as np                          # Needed for braiding the pins with the delays
import curses
from time import sleep
from PIL import Image

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)
key = ''

# scaling to conserve power & correct color
RedBrightnessPct = 0.35
GrnBrightnessPct = 0.60
BluBrightnessPct = 0.60

RedBrightnessPct = 0.43
GrnBrightnessPct = 0.68
BluBrightnessPct = 0.73

# ================================================================================

def reversebits( val ):
    newval = int('{:08b}'.format(val)[::-1], 2)
    return( newval )

def tuple3_to_hex( tup3val ):
    # Takes a tuple of 3 color values & formats it as a single 32bit integer with 
    # GRB (grn red blu) 8 bit intensity values.
    red = int( tup3val[0] * RedBrightnessPct ) 
    grn = int( tup3val[1] * GrnBrightnessPct )
    blu = int( tup3val[2] * BluBrightnessPct )
    red = reversebits( red )
    grn = reversebits( grn )
    blu = reversebits( blu )
    val = (blu << 16) + (red << 8) + (grn)
    return( val )

def get_img_array( image ):
    if image.mode != 'RGB':
        image = image.convert( 'RGB' ) # change to RGB if you don't care about alpha

    pixels = image.load( )
    data = []

    width, height = image.size
    #print "Image size: (%d, %d)." % (width, height)
    for idx in xrange( 0, (height * width) + 2 ):
        data.append( 0 )

    idx = 0
    data[idx] = height * width; # First index contains Number of Pixels
    idx += 1
    for h in range( 0, height ):
        if( h % 2 == 0 ):
            for w in range( 0, width ):
                color = pixels[w,h]
                data[idx] = tuple3_to_hex( color )
                idx += 1
        else:
            for w in range( width-1, -1, -1 ):
                color = pixels[w,h]
                data[idx] = tuple3_to_hex( color )
                idx += 1
    return( data )

# ================================================================================

if __name__ == '__main__':
    clear_leds_at_end = True
    sheet = Image.open( '../sprite_sheets/frogger.png' )
    print sheet.format, sheet.size, sheet.mode
    #sheet.show()
    #sys.exit(0)

    offsetx = 32 
    offsety = 32
    stepx = 12
    #stepy = 24
    stepy = 12
    sizex = 16 
    sizey = 16
    sheetx, sheety = sheet.size

    pypruss.modprobe()                          # This only has to be called once pr boot
    pypruss.init()                              # Init the PRU
    pypruss.open(0)                             # Open PRU event 0 which is PRU0_ARM_INTERRUPT
    pypruss.pruintc_init()                      # Init the interrupt controller

    # Index over all the sprites in the PNG file.  It's a 24 x 20 array of 16x16 pixel sprites.
    sprite_idx_arr = []
    for iy in xrange( 15 ):
        for ix in xrange( 6 ):
            sprite_idx_arr.append( (ix, iy) )

    #sprite_idx_arr = [
    #    (7, 0),
    #    (8, 0),
    #    (9, 0),
    #    (11, 0),
    #    (12, 0),
    #    (13, 0),
    #    (15, 0),
    #    (12, 1),
    #    (14, 1),
    #    (13, 3)
    #]
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
        key = stdscr.getch();
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
        data = get_img_array( ni )
        pypruss.pru_write_memory(0, 0, data)    # Load the data in the PRU ram
        pypruss.exec_program(0, "../pru_code/ledgriddrvr.bin")    # Load firmware on PRU 0
        pypruss.wait_for_event(0)               # Wait for event 0 which is connected to PRU0_ARM_INTERRUPT
        pypruss.clear_event(0)                  # Clear the event
        #sleep( 0.500 )                          # sleep 1s

    if( clear_leds_at_end ):
        empty_data = [256] + [0]*256            # 1st index is #_of_pixels, then 256 pixel values of 0 follow it
        pypruss.pru_write_memory(0, 0, empty_data)      # Load the data in the PRU ram
        pypruss.exec_program(0, "../pru_code/ledgriddrvr.bin")    # Load firmware on PRU 0
        pypruss.wait_for_event(0)               # Wait for event 0 which is connected to PRU0_ARM_INTERRUPT
        pypruss.clear_event(0)                  # Clear the event
        sleep( 1.000 )                          # sleep 1s

    curses.endwin()
    pypruss.exit()                              # Exit
    sys.exit(0)

