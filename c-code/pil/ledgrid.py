#!/usr/bin/env python
# Script to read PNG files and format the pixel data for the ledgrid.
#
# Decent tutorial for PIL: http://www.nerdparadise.com/tech/python/pil/pixelcrashcourse/

#import HYP_Utils
import sys

from PIL import Image

def reversebits( val ):
    newval = int('{:08b}'.format(val)[::-1], 2)
    return( newval )

def tuple3_to_hex( tup3val ):
    # Takes a tuple of 3 color values & formats it as a single 32bit integer with 
    # GRB (grn red blu) 8 bit intensity values.
    red = reversebits( tup3val[0] )
    grn = reversebits( tup3val[1] )
    blu = reversebits( tup3val[2] )
    #val = (grn << 16) + (red << 8) + (blu)
    val = (blu << 16) + (red << 8) + (grn)
    #print "tuple=%s, red=0x%02x, green=0x%02x, blue=0x%02x, val=0x%x" % ( tup3val, red, grn, blu, val )
    return( val )

# ================================================================================

def convert_png( img_filename, outputfile ):
    print 'Writing file: %s' % (outputfile)
    f = open( outputfile, "w" )
    image = Image.open( img_filename )

    #if image.mode != 'RGBA':
    #    image = image.convert( 'RGBA' ) # change to RGB if you don't care about alpha
    if image.mode != 'RGB':
        image = image.convert( 'RGB' ) # change to RGB if you don't care about alpha

    pixels = image.load( )

    sharedMem_int = []

    width = image.size[0]
    height = image.size[1]
    #print "Image size: (%d, %d)." % (width, height)
    for idx in range( 0, (height * width) + 1 ):
        sharedMem_int.append( 0 )

    idx = 0
    f.write( '    sharedMem_int[OFFSET_SHAREDRAM + 0] = 0x00000100; // # Number of Pixels (256)\n' )
    idx += 1
    for h in range( 0, height ):
        if( h % 2 == 0 ):
            for w in range( 0, width ):
                color = pixels[w,h]
                sharedMem_int[idx] = tuple3_to_hex( color )
                f.write( '    sharedMem_int[OFFSET_SHAREDRAM + %d] = 0x%-08x;\n' % (idx, sharedMem_int[idx]) )
                idx += 1
        else:
            for w in range( width-1, -1, -1 ):
                color = pixels[w,h]
                sharedMem_int[idx] = tuple3_to_hex( color )
                f.write( '    sharedMem_int[OFFSET_SHAREDRAM + %d] = 0x%-08x;\n' % (idx, sharedMem_int[idx]) )
                idx += 1
    f.close()

# ================================================================================

PIL_Version = Image.VERSION
convert_png( "./mario/marioWalk_1.png", "mario1_data_init.inc" )
convert_png( "./mario/marioWalk_2.png", "mario2_data_init.inc" )
convert_png( "./mario/marioWalk_3.png", "mario3_data_init.inc" )


