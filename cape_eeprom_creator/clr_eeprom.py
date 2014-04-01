#!/usr/bin/env python

import sys      # for sys.exit
import os       # for os.system

sizeEEPROM = 244
eeprom = []


# ================================================================================
# Write the Binary File
# ================================================================================

for i in range( sizeEEPROM ):
    eeprom.append( 0 )
    #eeprom[i] = 0

print "Writing file: eeprom.bin"
with open( "eeprom.bin", 'wb' ) as f:
    #f.write( eeprom )
    f.write( str( bytearray(eeprom) ) )

# Reading:
# with open( 'eeprom.bin', 'rb' ) as f:
#     content = f.read()
#     for b in content:
#         print(b)

# hexdump -n 244 -C eeprom.bin
cmdstr = 'hexdump -n 244 -C eeprom.bin'
print "CMD: ", cmdstr
res = os.system( cmdstr )

print ""
print "*** To program the EEPROM, the cape may need a jumper on the WP to allow writing."
print "*** Then:  "
print "***      cat eeprom.bin > /sys/bus/i2c/devices/1-0057/eeprom"
print "*** to write this image to the EEPROM.  Note, 57 is the I2C cape address in this"
print "*** example.  You may need to change that to a value in the range: 54-57."
print "*** Test your I2C write (and address) with hexdump:"
print "***      hexdump -n 244 -C /sys/bus/i2c/devices/1-0057/eeprom\n"

sys.exit( res )
