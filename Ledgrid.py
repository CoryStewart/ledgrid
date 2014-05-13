#!/usr/bin/env python
''' Ledgrid.py - Module for sending SpriteSheet images and animations to the Ledgrid Hardware.'''

import sys
import pypruss                              # The Programmable Realtime Unit Library
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
        if( sprite_name == '' ):
            pass    # do nothing when called with empty sprite_name
        elif( self.sprites.has_key(sprite_name) == 0 ):
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
        sleep( 0.003 )                          # Allow pru to complete
        pypruss.clear_event(0)                  # Clear the event

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
    def showWideImage( self, im, duration_ms, printinfo=False ):
        if printinfo:
            print "showWideImage():"
        sizex, sizey = im.size
        if printinfo:
            print "Image size: %d, %d" % (sizex, sizey)
        for xoffset in range( sizex-16 ):
            #print "%d / %d" % (xoffset, sizex-16-1)
            crop_box = (xoffset, 0, xoffset+16, 16)
            region = im.crop( crop_box )
            ni = Image.new( 'RGB', (16, 16) )
            ni.paste( region, (0, 0, 16, 16) )
            data = self._get_img_array( ni )
            self._sendPixels( data )
            if( xoffset < sizex-16-1 ):
                sleep( 0.001 * duration_ms )
            else:
                sleep( 0.020 ) # allow longer delay on last _sendPixels (linux seems to kill pru process & leave half drawn screen on the ledgrid otherwise)

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
    import MrsPacmanSheet, MinecraftSheet, MarioSheet, FroggerSheet
    import TextBuilder

    textbuilder_h = TextBuilder.TextBuilder();
    frogger_ss = FroggerSheet.FroggerSheet( )
    mario_ss = MarioSheet.MarioSheet( )
    minecraft_ss = MinecraftSheet.MinecraftSheet();
    mrspacman_ss = MrsPacmanSheet.MrsPacmanSheet();

    # Use the SpriteSheet.exploresheet() method to display the sprites & determine their coords:
    if False:
        ss = SpriteSheet( 'sprite_sheets/mrs_pacman_16x16.png', stepx=16, stepy=16, offsetx=0, offsety=0 )
        grid = Ledgrid()
        grid.exploreSheet( ss )
        grid.clear()
        grid.close()
        sys.exit(0)
        
    # Use the AnimationSequence.addFrame() method to define a sequences of images for an animation:
    if True:        
        mario_seq1 = AnimationSequence("mario_seq1")
        mario_seq1.addFrame( mario_ss, 'mario1', duration_ms=1000 )

        minecraft_seq1 = AnimationSequence("minecraft_seq1")

        dur = 75
        minecraft_seq1.addFrame( minecraft_ss, 'wheat1', duration_ms=dur )
        minecraft_seq1.addFrame( minecraft_ss, 'wheat2', duration_ms=dur )
        minecraft_seq1.addFrame( minecraft_ss, 'wheat3', duration_ms=dur )
        minecraft_seq1.addFrame( minecraft_ss, 'wheat4', duration_ms=dur )
        minecraft_seq1.addFrame( minecraft_ss, 'wheat5', duration_ms=dur )
        minecraft_seq1.addFrame( minecraft_ss, 'wheat6', duration_ms=dur )
        minecraft_seq1.addFrame( minecraft_ss, 'wheat7', duration_ms=dur )
        minecraft_seq1.addFrame( minecraft_ss, 'wheat8', duration_ms=dur )
        minecraft_seq1.addFrame( minecraft_ss, 'player_head', duration_ms=550 )
        minecraft_seq1.addFrame( minecraft_ss, 'zombie_head', duration_ms=550 )
        minecraft_seq1.addFrame( minecraft_ss, 'creeper_head', duration_ms=550 )
        minecraft_seq1.addFrame( minecraft_ss, 'skeleton_head', duration_ms=550 )
        minecraft_seq1.addFrame( minecraft_ss, 'wither_skeleton_head', duration_ms=550 )
        minecraft_seq1.addFrame( minecraft_ss, 'multi_heads', duration_ms=650 )
        minecraft_seq1.addFrame( minecraft_ss, 'glass', duration_ms=550 )
        minecraft_seq1.addFrame( minecraft_ss, 'lava', duration_ms=450 )
        minecraft_seq1.addFrame( minecraft_ss, 'cobweb', duration_ms=350 )
        minecraft_seq1.addFrame( minecraft_ss, 'tracks_redstone_on', duration_ms=250 )
        minecraft_seq1.addFrame( minecraft_ss, 'tracks_redstone_off', duration_ms=250 )
        minecraft_seq1.addFrame( minecraft_ss, 'tracks_redstone_on', duration_ms=250 )
        minecraft_seq1.addFrame( minecraft_ss, 'tracks_redstone_off', duration_ms=250 )
        minecraft_seq1.addFrame( minecraft_ss, 'yel_tracks_redstone_on', duration_ms=250 )
        minecraft_seq1.addFrame( minecraft_ss, 'yel_tracks_redstone_off', duration_ms=250 )
        minecraft_seq1.addFrame( minecraft_ss, 'yel_tracks_redstone_on', duration_ms=250 )
        minecraft_seq1.addFrame( minecraft_ss, 'yel_tracks_redstone_off', duration_ms=250 )
        minecraft_seq1.addFrame( minecraft_ss, 'grass1', duration_ms=150 )
        minecraft_seq1.addFrame( minecraft_ss, 'grass2', duration_ms=150 )
        minecraft_seq1.addFrame( minecraft_ss, 'grass3', duration_ms=150 )
        minecraft_seq1.addFrame( minecraft_ss, 'grass4', duration_ms=250 )
        minecraft_seq1.addFrame( minecraft_ss, 'rose', duration_ms=250 )
        minecraft_seq1.addFrame( minecraft_ss, 'dandelion', duration_ms=250 )
        minecraft_seq1.addFrame( minecraft_ss, 'red_mushroom', duration_ms=250 )
        minecraft_seq1.addFrame( minecraft_ss, 'mushroom', duration_ms=250 )
        minecraft_seq1.addFrame( minecraft_ss, 'cake', duration_ms=450 )
        minecraft_seq1.addFrame( minecraft_ss, 'furnace_lit', duration_ms=550 )
        minecraft_seq1.addFrame( minecraft_ss, 'redstone_torch_lit', duration_ms=100 )
        minecraft_seq1.addFrame( minecraft_ss, 'redstone_torch_unlit', duration_ms=100 )
        minecraft_seq1.addFrame( minecraft_ss, 'redstone_torch_lit', duration_ms=100 )
        minecraft_seq1.addFrame( minecraft_ss, 'redstone_torch_unlit', duration_ms=100 )
        minecraft_seq1.addFrame( minecraft_ss, 'redstone_torch_lit', duration_ms=100 )
        minecraft_seq1.addFrame( minecraft_ss, 'redstone_torch_unlit', duration_ms=100 )
        minecraft_seq1.addFrame( minecraft_ss, 'redstone_torch_lit', duration_ms=100 )
        minecraft_seq1.addFrame( minecraft_ss, 'redstone_torch_unlit', duration_ms=100 )
        minecraft_seq1.addFrame( minecraft_ss, 'ladder', duration_ms=550 )

        frogger_seq1 = AnimationSequence("frogger_seq1")

        frogger_seq1.addFrame( frogger_ss, 'frog_green_up1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'frog_green_up2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'frog_green_up3', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'frog_blue_up1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'frog_blue_up2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'frog_blue_up3', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'frog_yellow_up1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'frog_yellow_up2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'frog_yellow_up3', duration_ms=150 )

        frogger_seq1.addFrame( frogger_ss, 'skull1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'explode1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'explode2', duration_ms=125 )
        frogger_seq1.addFrame( frogger_ss, 'explode3', duration_ms=100 )
        frogger_seq1.addFrame( frogger_ss, 'explode1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'explode2', duration_ms=125 )
        frogger_seq1.addFrame( frogger_ss, 'explode3', duration_ms=100 )
        frogger_seq1.addFrame( frogger_ss, 'explode1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'explode2', duration_ms=125 )
        frogger_seq1.addFrame( frogger_ss, 'explode3', duration_ms=100 )
        frogger_seq1.addFrame( frogger_ss, 'skull1', duration_ms=150 )
        #frogger_seq1.addFrame( frogger_ss, 'skull2', duration_ms=150 )
        #frogger_seq1.addFrame( frogger_ss, 'skull3', duration_ms=150 )
        #frogger_seq1.addFrame( frogger_ss, 'skull4', duration_ms=350 )
        frogger_seq1.addFrame( frogger_ss, 'racecar1', duration_ms=250 )
        frogger_seq1.addFrame( frogger_ss, 'racecar2', duration_ms=250 )
        frogger_seq1.addFrame( frogger_ss, 'alligator_orange_headopen1', duration_ms=650 )
        frogger_seq1.addFrame( frogger_ss, 'alligator_orange_headopen2', duration_ms=250 )
        frogger_seq1.addFrame( frogger_ss, 'FrogStanding1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'FrogStanding2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'FrogStanding1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'FrogStanding2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'FrogStanding1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'FrogStanding2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle3', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle3', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle3', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'Turtle_Sinking1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'Turtle_Sinking2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'Turtle_Sinking3', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'Turtle_Sinking2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'Turtle_Sinking1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle3', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle3', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle1', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle2', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, 'SwimmingTurtle3', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, '100pts', duration_ms=150 )
        frogger_seq1.addFrame( frogger_ss, '200pts', duration_ms=150 )

        mario_seq2 = AnimationSequence("mario_seq2")
        mario_seq2.addFrame( mario_ss, 'mario1', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario2', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario3', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario2', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario1', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario2', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario3', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario2', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario1', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario2', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario3', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario2', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario1', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario2', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario3', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario2', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario1', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario2', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario3', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario2', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario1', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario2', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario3', duration_ms=60 )
        mario_seq2.addFrame( mario_ss, 'mario2', duration_ms=60 )

        mrspacman_seq1a = AnimationSequence("mrspacman_seq1a")
        dur = 40
        mrspacman_seq1a.addFrame( mrspacman_ss, 'pacman_right_open1', duration_ms=dur )
        mrspacman_seq1a.addFrame( mrspacman_ss, 'pacman_right_open2', duration_ms=dur )
        mrspacman_seq1a.addFrame( mrspacman_ss, 'pacman_right_closed', duration_ms=dur )

        mrspacman_seq1b = AnimationSequence("mrspacman_seq1b")
        dur = 250
        mrspacman_seq1b.addFrame( mrspacman_ss, 'ghost_vulnerable1', duration_ms=dur )
        mrspacman_seq1b.addFrame( mrspacman_ss, 'ghost_vulnerable2', duration_ms=dur )
        mrspacman_seq1b.addFrame( mrspacman_ss, 'ghost_vulnerable3', duration_ms=dur )
        mrspacman_seq1b.addFrame( mrspacman_ss, 'ghost_vulnerable4', duration_ms=dur )

        mrspacman_seq1c = AnimationSequence("mrspacman_seq1c")
        dur = 150
        mrspacman_seq1c.addFrame( mrspacman_ss, 'ghost_red_eyes_up1', duration_ms=dur )
        mrspacman_seq1c.addFrame( mrspacman_ss, 'ghost_red_eyes_up2', duration_ms=dur )
        mrspacman_seq1c.addFrame( mrspacman_ss, 'ghost_red_eyes_down1', duration_ms=dur )
        mrspacman_seq1c.addFrame( mrspacman_ss, 'ghost_red_eyes_down2', duration_ms=dur )
        mrspacman_seq1c.addFrame( mrspacman_ss, 'ghost_red_eyes_left1', duration_ms=dur )
        mrspacman_seq1c.addFrame( mrspacman_ss, 'ghost_red_eyes_left2', duration_ms=dur )
        mrspacman_seq1c.addFrame( mrspacman_ss, 'ghost_red_eyes_right1', duration_ms=dur )
        mrspacman_seq1c.addFrame( mrspacman_ss, 'ghost_red_eyes_right2', duration_ms=dur )

        mrspacman_seq1f = AnimationSequence("mrspacman_seq1f")
        dur = 50
        mrspacman_seq1f.addFrame( mrspacman_ss, 'ghost_invisible_eyes_up',     duration_ms=dur )
        mrspacman_seq1f.addFrame( mrspacman_ss, 'ghost_invisible_eyes_right',  duration_ms=dur )
        mrspacman_seq1f.addFrame( mrspacman_ss, 'ghost_invisible_eyes_down',   duration_ms=dur )
        mrspacman_seq1f.addFrame( mrspacman_ss, 'ghost_invisible_eyes_left',   duration_ms=dur )
        mrspacman_seq1f.addFrame( mrspacman_ss, 'ghost_invisible_eyes_up',     duration_ms=dur )
        mrspacman_seq1f.addFrame( mrspacman_ss, 'ghost_invisible_eyes_right',  duration_ms=dur )
        mrspacman_seq1f.addFrame( mrspacman_ss, 'ghost_invisible_eyes_down',   duration_ms=dur )
        mrspacman_seq1f.addFrame( mrspacman_ss, 'ghost_invisible_eyes_left',   duration_ms=dur )

        mrspacman_seq1d = AnimationSequence("mrspacman_seq1d")
        dur = 350
        mrspacman_seq1d.addFrame( mrspacman_ss, 'cherry',        duration_ms=dur )
        mrspacman_seq1d.addFrame( mrspacman_ss, 'strawberry',    duration_ms=dur )
        mrspacman_seq1d.addFrame( mrspacman_ss, 'orange',        duration_ms=dur )
        mrspacman_seq1d.addFrame( mrspacman_ss, 'pretzel',       duration_ms=dur )
        mrspacman_seq1d.addFrame( mrspacman_ss, 'apple',         duration_ms=dur )
        mrspacman_seq1d.addFrame( mrspacman_ss, 'pear',          duration_ms=dur )
        mrspacman_seq1d.addFrame( mrspacman_ss, 'bannana',       duration_ms=dur )
        mrspacman_seq1d.addFrame( mrspacman_ss, '500pts',        duration_ms=dur )


        mrspacman_seq1e = AnimationSequence("mrspacman_seq1e")
        dur = 250
        mrspacman_seq1e.addFrame( mrspacman_ss, '200pts',                      duration_ms=dur )
        mrspacman_seq1e.addFrame( mrspacman_ss, '400pts',                      duration_ms=dur )
        mrspacman_seq1e.addFrame( mrspacman_ss, '800pts',                      duration_ms=dur )
        mrspacman_seq1e.addFrame( mrspacman_ss, '1600pts',                     duration_ms=dur )

        # ----

        grid = Ledgrid()

        for i in range( 5 ):

            # --- Mario ---

            textbuilder_h.setColor( "random" );
            string_image = textbuilder_h.createStringImage( " - MARIO -  ", False );
            grid.showWideImage( string_image, duration_ms=4 );
            #grid.showSequence( mario_seq1, printinfo=False )
            grid.showSequence( mario_seq2, printinfo=False )

            # --- Minecraft ---

            textbuilder_h.setColor( "cyan" );
            string_image = textbuilder_h.createStringImage( " - MINECRAFT -  ", False );
            grid.showWideImage( string_image, duration_ms=4 );
            grid.showSequence( minecraft_seq1, printinfo=False )

            # --- Frogger ---

            string_image = textbuilder_h.createFroggerStringImage( "  F R O G G E R", False );
            grid.showWideImage( string_image, duration_ms=0 );
            grid.showSequence( frogger_seq1, printinfo=False )

            # --- Mrs Pacman ---

            textbuilder_h.setColor( "red" );
            string_image = textbuilder_h.createStringImage( " - MRS PACMAN -  ", False );
            grid.showWideImage( string_image, duration_ms=4 );

            for i in range(4):
                grid.showSequence( mrspacman_seq1a, printinfo=False )
            for i in range(2):
                grid.showSequence( mrspacman_seq1b, printinfo=False )
            for i in range(1):
                grid.showSequence( mrspacman_seq1c, printinfo=False )
            for i in range(2):
                grid.showSequence( mrspacman_seq1f, printinfo=False )
            for i in range(1):
                grid.showSequence( mrspacman_seq1d, printinfo=False )
            for i in range(1):
                grid.showSequence( mrspacman_seq1e, printinfo=False )

        grid.clear()
        grid.close()
        sys.exit(0)
