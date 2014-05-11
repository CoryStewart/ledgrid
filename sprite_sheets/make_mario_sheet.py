#!/usr/bin/env python
''' mk_mario_sheet.py - combines three separate .png files into one sprite sheet.'''

import numpy as np                          # Needed for braiding the pins with the delays
from PIL import Image

# ================================================================================

if __name__ == '__main__':
    image1 = Image.open( "../pil/mario/marioWalk_1.png" )
    image2 = Image.open( "../pil/mario/marioWalk_2.png" )
    image3 = Image.open( "../pil/mario/marioWalk_3.png" )

    sizex, sizey = image1.size
    box = (0, 0, sizex, sizey)
    region1 = image1.crop( box )
    region2 = image2.crop( box )
    region3 = image3.crop( box )
    ni = Image.new( 'RGB', (3*sizex, sizey) )
    ni.paste( region1, (0*sizex, 0, 1*sizex, sizey) )
    ni.paste( region2, (1*sizex, 0, 2*sizex, sizey) )
    ni.paste( region3, (2*sizex, 0, 3*sizex, sizey) )
    ni.save( "mario_sheet.png" );

