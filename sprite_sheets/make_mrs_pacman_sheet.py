#!/usr/bin/env python
''' mk_mrspacman_sheet.py - Scales the original "mrs_pacman.gif" file down to 16x16 sprites.'''

import numpy as np                          # Needed for braiding the pins with the delays
from PIL import Image

# ================================================================================

if __name__ == '__main__':
    im = Image.open( "mrs_pacman.gif" )

    sizex, sizey = im.size
    im.thumbnail( (8*16,8*16), Image.ANTIALIAS )

    # Remove background color
    im = im.convert( "RGB" )
    orig_pixels = im.getdata()
    new_pixels = []
    first = True
    for item in orig_pixels:
        if( first ):
            print "background_color = ", item
            background_color = item
            first = False
        if( item == background_color ):
            new_pixels.append( (0,0,0) )
        else:
            new_pixels.append( item )
    im.putdata( new_pixels )

    im.save( "mrs_pacman_16x16.png", "PNG" )

