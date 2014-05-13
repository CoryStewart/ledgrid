#!/usr/bin/env python
''' TextBuilder.py - Class for building text images & scrolling them on the Ledgrid.'''

import sys
from Ledgrid import *
from PIL import Image
from random import randrange

# ================================================================================
class TextBuilder(SpriteSheet):
    color = "random"
    letter_coords = {
        'frogger_F'     : (16, 368),
        'frogger_R'     : (40, 368),
        'frogger_O'     : (64, 368),
        'frogger_G'     : (88, 368),
        'frogger_E'     : (112, 368),
        'frogger_ '     : (136, 368), # space

        '0'         : (204,  28), 
        '1'         : (220,  28),
        '2'         : (236,  28),
        '3'         : (252,  28),
        '4'         : (268,  28),
        '5'         : (284,  28),
        '6'         : (300,  28),
        '7'         : (316,  28),
        '8'         : (332,  28),
        '9'         : (348,  28),

        'A'         : (204,  44), 
        'B'         : (220,  44),
        'C'         : (236,  44),
        'D'         : (252,  44),
        'E'         : (268,  44),
        'F'         : (284,  44),
        'G'         : (300,  44),
        'H'         : (316,  44),
        'I'         : (332,  44),
        'J'         : (348,  44),

        'K'         : (204,  60),
        'L'         : (220,  60),
        'M'         : (236,  60),
        'N'         : (252,  60),
        'O'         : (268,  60),
        'P'         : (284,  60),
        'Q'         : (300,  60),
        'R'         : (316,  60),
        'S'         : (332,  60),
        'T'         : (348,  60),

        'U'         : (204,  76), 
        'V'         : (220,  76),
        'W'         : (236,  76),
        'X'         : (252,  76),
        'Y'         : (268,  76),
        'Z'         : (284,  76),
        '-'         : (300,  76),
        ' '         : (316,  76),
        'Copyright' : (332,  76),
        'Box'       : (348,  76),
    }

    def __init__( self ):
        h = SpriteSheet.__init__( self, 'sprite_sheets/Frogger.png', stepx=16, stepy=16, offsetx=32, offsety=32 ) 
        return( h )

    def setColor( self, newcolor ):
        self.color = newcolor

    def createStringImage( self, mystr, printinfo=True ):
        sizex = 8
        sizey = 16
        space_sizex = 4  # make space characters smaller
        img1 = Image.open( "./sprite_sheets/frogger.png" )
        ni_size_x = (len(mystr)*sizex) - (mystr.count(' ') * (8-space_sizex)) # make new image size take into account the smaller size of spaces
        ni = Image.new( 'RGB', (ni_size_x, sizey) )

        paste_loc_x = 0
        paste_loc_y = 0
        space_letter_coords = self.letter_coords.get(' ')
        for idx, character in enumerate( mystr ):
            key = character
            (x1, y1) = self.letter_coords.get( key, space_letter_coords ) # get the coords asked for if they exist, else return coords for a space
            if( self.color == 'white' ):
                pass
            elif( self.color == 'yellow' ):
                y1 += 1 * 64
            elif( self.color == 'red' ):
                y1 += 2 * 64
            elif( self.color == 'cyan' ):
                y1 += 3 * 64
            elif( self.color == 'purple' ):
                y1 += 4 * 64
            elif( self.color == 'random' ):
                y1 += randrange(5) * 64
            if printinfo:
                    print '%d : character = "%s", %s, %d, (%d,%d)' % (idx, character, key, ord( character ), x1, y1)

            if( character == ' ' ):
                sizex = space_sizex # make spaces smaller
            else:
                sizex = 8
            crop_box = (x1+4,y1,x1+4+sizex,y1+sizey)
            letter_img = img1.crop( crop_box )
            ni.paste( letter_img, (paste_loc_x, 0, paste_loc_x+sizex, sizey) )
            paste_loc_x += sizex
        return( ni )

    def createFroggerStringImage( self, mystr, printinfo=True ):
        sizex = 16
        sizey = 16
        space_sizex = 4  # make space characters smaller
        img1 = Image.open( "./sprite_sheets/frogger.png" )
        ni_size_x = (len(mystr)*sizex) - (mystr.count(' ') * (sizex-space_sizex)) # make new image size take into account the smaller size of spaces
        ni = Image.new( 'RGB', (ni_size_x, sizey) )

        paste_loc_x = 0
        paste_loc_y = 0
        space_letter_coords = self.letter_coords.get('frogger_ ')
        for idx, character in enumerate( mystr ):
            key = 'frogger_' + character
            (x1, y1) = self.letter_coords.get( key, space_letter_coords ) # get the coords asked for if they exist, else return coords for a space
            if printinfo:
                    print '%d : character = "%s", %s, %d, (%d,%d)' % (idx, character, key, ord( character ), x1, y1)

            if( character == ' ' ):
                sizex = space_sizex # make spaces smaller
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

    if False:
        debug = True
        tb = TextBuilder();
        string_image = tb.createStringImage( "CORY STEWART", debug );
        grid = Ledgrid()
        grid.showWideImage( string_image, duration_ms=6, printinfo=debug )
        grid.clear()
        grid.close()
        sys.exit(0)
    if True:
        debug = False
        tb = TextBuilder();
        string_image = tb.createFroggerStringImage( "   F R O G G E R ", debug );
        grid = Ledgrid()
        grid.showWideImage( string_image, duration_ms=0, printinfo=debug )
        grid.clear()
        grid.close()
        sys.exit(0)
