#!/usr/bin/env python
''' ledgrid.py - test script for writing to PRU 0 mem using PyPRUSS library & driving ledgrid.'''

#import HYP_Utils
import sys
import pypruss                              # The Programmable Realtime Unit Library
import numpy as np                          # Needed for braiding the pins with the delays
from time import sleep
from PIL import Image

# scaling to conserve power & correct color
RedBrightnessPct = 0.50
GrnBrightnessPct = 0.35
BluBrightnessPct = 0.90

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

def convert_png( img_filename ):
    image = Image.open( img_filename )

    if image.mode != 'RGB':
        image = image.convert( 'RGB' ) # change to RGB if you don't care about alpha

    pixels = image.load( )
    sharedMem_int = []

    width, height = image.size
    #print "Image size: (%d, %d)." % (width, height)
    for idx in xrange( 0, (height * width) + 2 ):
        sharedMem_int.append( 0 )

    idx = 0
    sharedMem_int[idx] = height * width; # First index contains Number of Pixels
    idx += 1
    for h in range( 0, height ):
        if( h % 2 == 0 ):
            for w in range( 0, width ):
                color = pixels[w,h]
                sharedMem_int[idx] = tuple3_to_hex( color )
                idx += 1
        else:
            for w in range( width-1, -1, -1 ):
                color = pixels[w,h]
                sharedMem_int[idx] = tuple3_to_hex( color )
                idx += 1
    return( sharedMem_int )

# ================================================================================

if __name__ == '__main__':
    clear_leds_at_end = True
    files = [ "../sprite_sheets/ti-icon.png" ]

    pypruss.modprobe()                          # This only has to be called once pr boot
    pypruss.init()                              # Init the PRU
    pypruss.open(0)                             # Open PRU event 0 which is PRU0_ARM_INTERRUPT
    pypruss.pruintc_init()                      # Init the interrupt controller
    for i in xrange( 2 ):
        for imgfile in files:
            data = convert_png( imgfile )
            pypruss.pru_write_memory(0, 0, data)    # Load the data in the PRU ram
            pypruss.exec_program(0, "../pru_code/ledgriddrvr.bin")    # Load firmware on PRU 0
            pypruss.wait_for_event(0)               # Wait for event 0 which is connected to PRU0_ARM_INTERRUPT
            pypruss.clear_event(0)                  # Clear the event
            sleep( 0.100 )                          # sleep 100ms

    sleep( 5.000 )                              # sleep 1s
    if( clear_leds_at_end ):
        empty_data = [256] + [0]*256            # 1st index is #_of_pixels, then 256 pixel values of 0 follow it
        pypruss.pru_write_memory(0, 0, empty_data)      # Load the data in the PRU ram
        pypruss.exec_program(0, "../pru_code/ledgriddrvr.bin")    # Load firmware on PRU 0
        pypruss.wait_for_event(0)               # Wait for event 0 which is connected to PRU0_ARM_INTERRUPT
        pypruss.clear_event(0)                  # Clear the event

    pypruss.exit()                              # Exit

