#!/usr/bin/env python
''' TextBuilder.py - Class for building text images & scrolling them on the Ledgrid.'''

import sys
from Ledgrid import *
from PIL import Image

# ================================================================================
class TextBuilder(SpriteSheet):
    letter_coords = {
        'frogger_F' : (16, 368),
        'frogger_R' : (40, 368),
        'frogger_O' : (64, 368),
        'frogger_G' : (88, 368),
        'frogger_E' : (112, 368),
        'frogger_ ' : (136, 368), # space
    }

    def __init__( self ):
        h = SpriteSheet.__init__( self, 'sprite_sheets/Frogger.png', stepx=16, stepy=16, offsetx=32, offsety=32 ) 
        return( h )

    def createFroggerStringImage( self, mystr, printinfo=True ):
        sizex = 16
        sizey = 16
        img1 = Image.open( "./sprite_sheets/frogger.png" )
        ni = Image.new( 'RGB', (len(mystr)*sizex, sizey) )

        paste_loc_x = 0
        paste_loc_y = 0
        space_letter_coords = self.letter_coords.get('frogger_ ')
        for idx, character in enumerate( mystr ):
            key = 'frogger_' + character
            (x1, y1) = self.letter_coords.get( key, space_letter_coords ) # get the coords asked for if they exist, else return coords for a space
            #(x1, y1) = self.letter_coords[key]
            if printinfo:
                    print '%d : character = "%s", %s, %d, (%d,%d)' % (idx, character, key, ord( character ), x1, y1)

            if( character == ' ' ):
                sizex = 4 # make spaces smaller
            else:
                sizex = 16
            crop_box = (x1,y1,x1+sizex,y1+sizey)
            letter_img = img1.crop( crop_box )
            #ni.paste( letter_img, (idx*sizex, 0, (idx+1)*sizex, sizey) )
            ni.paste( letter_img, (paste_loc_x, 0, paste_loc_x+sizex, sizey) )
            paste_loc_x += sizex
        return( ni )


# ================================================================================
if __name__ == '__main__':
        debug = False
        tb = TextBuilder();
        string_image = tb.createFroggerStringImage( "   F R O G G E R ", debug );
        grid = Ledgrid()
        #grid.showSequence( seq1, printinfo=False )
        grid.showWideImage( string_image, duration_ms=0, printinfo=debug )
        grid.clear()
        grid.close()
        sys.exit(0)
