#!/usr/bin/env python
# Script to read PNG files and format the pixel data for the ledgrid.
#
# Decent tutorial for PIL: http://www.nerdparadise.com/tech/python/pil/pixelcrashcourse/

#import HYP_Utils
import sys

from PIL import Image

PIL_Version = Image.VERSION
img_filename = "./mario/marioWalk_1.png"
image = Image.open( img_filename )

def tuple3_to_hex( tup3val ):
    # Takes a tuple of 3 color values & formats it as a single 32bit integer with 
    # GRB (grn red blu) 8 bit intensity values.
    red = tup3val[2]
    grn = tup3val[1]
    blu = tup3val[0]
    return( (grn << 16) + (red << 8) + (blu) )

#if image.mode != 'RGBA':
#    image = image.convert( 'RGBA' ) # change to RGB if you don't care about alpha
if image.mode != 'RGB':
    image = image.convert( 'RGB' ) # change to RGB if you don't care about alpha

pixels = image.load( )

sharedMem_int = []

width = image.size[0]
height = image.size[1]
#print "Image size: (%d, %d)." % (width, height)
for idx in range( 0, height * width ):
    sharedMem_int.append( 0 )

idx = 0
for h in range( 0, height ):
    if( h % 2 == 0 ):
        for w in range( 0, width ):
            color = pixels[w,h]
            sharedMem_int[idx] = tuple3_to_hex( color )
            #print 'h=%2d w=%2d : RGB=%-20s  GRB[%d]=0x%x' % (h, w, color, idx, sharedMem_int[idx])
            print '    sharedMem_int[%d] = 0x%-08x;' % (idx, sharedMem_int[idx])
            idx += 1
    else:
        for w in range( width-1, -1, -1 ):
            color = pixels[w,h]
            sharedMem_int[idx] = tuple3_to_hex( color )
            #print 'h=%2d w=%2d : RGB=%-20s  GRB[%d]=0x%x' % (h, w, color, idx, sharedMem_int[idx])
            print '    sharedMem_int[%d] = 0x%-08x;' % (idx, sharedMem_int[idx])
            idx += 1



