#!/usr/bin/env python
#   Reads and decodes a BeagleBoneBlack Cape EEprom binary file.
#                                           Cory Stewart 2014-03-27

import sys      # for sys.exit
import os       # for os.system

# sizeEEPROM = 244
eeprom = []

def decode_pin_setup( pinval ):
    pinstr = "Usage=%d, "       % ( ((pinval >> 16+7) & 0x1) )
    pinstr += "Type=%d, "       % ( ((pinval >> 16+5) & 0x3) )
    pinstr += "Slew=%d, "       % ( ((pinval >>    6) & 0x1) )
    pinstr += "RxEn=%d, "       % ( ((pinval >>    5) & 0x1) )
    pinstr += "PullSel=%d, "    % ( ((pinval >>    4) & 0x1) )
    pinstr += "PullEn=%d, "     % ( ((pinval >>    3) & 0x1) )
    pinstr += "MuxMode=%d"      % ( ((pinval >>    0) & 0x7) )
    return( pinstr )

# ================================================================================

# Dump the HexDump:
cmdstr = 'hexdump -n 244 -C eeprom.bin'
print "\nCMD: ", cmdstr
res = os.system( cmdstr )

# This array specifies the index (byte offset) into the eeprom binary file for
# the big endian 16bit word that programs the pinmux for the pin.
# -1 indicates a BeagleBone header pin location that cannot be changed (power, gnd, analog, etc.).
eepromIndex = [ \
      [   -1,    -1,   # P8_1 , P8_2 
        0x8c,  0x8e,   # P8_3 , P8_4 
        0x84,  0x86,   # P8_5 , P8_6 
        0xaa,  0xb0,   # P8_7 , P8_8 
        0xac,  0xae,   # P8_9 , P8_10
        0x92,  0x90,   # P8_11, P8_12
        0x76,  0x78,   # P8_13, P8_14
        0x96,  0x94,   # P8_15, P8_16
        0x7a,  0xa8,   # P8_17, P8_18
        0x74,  0xa6,   # P8_19, P8_20
        0xa4,  0x8a,   # P8_21, P8_22
        0x88,  0x82,   # P8_23, P8_24
        0x80,  0xa2,   # P8_25, P8_26
        0xca,  0xce,   # P8_27, P8_28
        0xcc,  0xd0,   # P8_29, P8_30
        0x66,  0x68,   # P8_31, P8_32
        0x64,  0xc8,   # P8_33, P8_34
        0x62,  0xc6,   # P8_35, P8_36
        0xc2,  0xc4,   # P8_37, P8_38
        0xbe,  0xc0,   # P8_39, P8_40
        0xba,  0xbc,   # P8_41, P8_42
        0xb6,  0xb8,   # P8_43, P8_44
        0xb2,  0xb4 ], # P8_45, P8_46
      [   -1,    -1,   # P9_1 , P9_2 
          -1,    -1,   # P9_3 , P9_4 
          -1,    -1,   # P9_5 , P9_6 
          -1,    -1,   # P9_7 , P9_8 
          -1,    -1,   # P9_9 , P9_10
        0x7c,  0xa0,   # P9_11, P9_12
        0x7e,  0x9c,   # P9_13, P9_14
        0x98,  0x9e,   # P9_15, P9_16
        0x5e,  0x5c,   # P9_17, P9_18
        0x6a,  0x6c,   # P9_19, P9_20
        0x5a,  0x58,   # P9_21, P9_22
        0x9a,  0x70,   # P9_23, P9_24
        0xdc,  0x6e,   # P9_25, P9_26
        0xd8,  0xd6,   # P9_27, P9_28
        0xd2,  0xd4,   # P9_29, P9_30
        0xda,    -1,   # P9_31, P9_32
        0xe6,    -1,   # P9_33, P9_34
        0xea,  0xe8,   # P9_35, P9_36
        0xe2,  0xe4,   # P9_37, P9_38
        0xde,  0xe0,   # P9_39, P9_40
        0x72,  0x60,   # P9_41, P9_42
          -1,    -1,   # P9_43, P9_44
          -1,    -1 ] ] # P9_45, P9_46

# for i in range( sizeEEPROM ):
#     eeprom.append( 0 )

with open( 'eeprom.bin', 'rb' ) as f:
    binfiledata = f.read()

eeprom = [ord(a) for a in binfiledata]

print "\n", "=" * 70, "\n"
if( ( (eeprom[0:1])[0] == 0xaa ) and
    ( (eeprom[1:2])[0] == 0x55 ) and
    ( (eeprom[2:3])[0] == 0x33 ) and
    ( (eeprom[3:4])[0] == 0xee ) and
    ( (eeprom[4:5])[0] == 0x41 ) and
    ( (eeprom[5:6])[0] == 0x30 ) ):
    print "First five bytes are correct: %s" % ("0xaa, 0x55, 0x33, 0xee, 0x41, 0x30")
else:
    print "First five bytes are **NOT** correct: %s" % eeprom[0:6]

# for b in eeprom:
#     print "0x%x" % (b)
print "Boardname            : '%s'" % ''.join(chr(i) for i in eeprom[6:6+32])
print "Board Version        : '%s'" % ''.join(chr(i) for i in eeprom[38:38+4])
print "Manufacturer         : '%s'" % ''.join(chr(i) for i in eeprom[42:42+16])
print "Part Number          : '%s'" % ''.join(chr(i) for i in eeprom[58:58+16])
num_cape_pins = (eeprom[75:76])[0]
print "Number of Cape Pins  : '%d'" % num_cape_pins
print "Serial Number        : '%s'" % ''.join(chr(i) for i in eeprom[76:76+12])

# List Cape Pins
for con_ref in [8,9]:
    print "-" * 40
    for con_pin in range( 1, 47 ):
        index = eepromIndex[con_ref-8][con_pin-1]
        if( index == -1 ):
            print "P%d.%-2d : -Rsvd on Header-" % ( con_ref, con_pin )
        else:
            msB = (eeprom[index:index+1])[0]    # big endian: high_order byte in the low address 
            lsB = (eeprom[index+1:index+2])[0]  # big endian: low_order byte in the high address
            eeprom_pin_val = (msB << 8) + lsB
            eeprom_pin_decode = decode_pin_setup( eeprom_pin_val )
            print "P%d.%-2d : eeprom_offset=0x%-02x : eeprom_val = 0x%04x : %s" % ( con_ref, con_pin, index, eeprom_pin_val, eeprom_pin_decode )
print "-" * 40

sys.exit( res )


