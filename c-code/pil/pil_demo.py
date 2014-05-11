# Decent tutorial: http://www.nerdparadise.com/tech/python/pil/pixelcrashcourse/
#import HYP_Utils
import sys

from PIL import Image

PIL_Version = Image.VERSION
img_filename = "./mario/marioWalk_1.png"
image = Image.open( img_filename )


#if image.mode != 'RGBA':
#    image = image.convert( 'RGBA' ) # change to RGB if you don't care about alpha
if image.mode != 'RGB':
    image = image.convert( 'RGB' ) # change to RGB if you don't care about alpha

pixels = image.load( )
color = pixels[4, 5] # x=4, y=5 (0 indexed)
print color

width = image.size[0]
height = image.size[1]
for w in range( 0, width ):
    for h in range( 0, height ):
        color = pixels[w,h]
        print 'w=%d h=%d color=%s' % (w, h, color)



