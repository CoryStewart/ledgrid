#!/usr/bin/env python
#
# Copyright (C) 2012 - Cabin Programs, Ken Keller 
# Adapted to Python by Cory Stewart, 2014/3/27
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import sys      # for sys.exit
import os       # for os.system

sizeEEPROM = 244
eeprom = []

#eepromIndex = [
#    [ -1, -1, 140, 142, 132, 134, 170, 176, 172, 174, 146, 144, 118, 120,
#        150, 148, 122, 168, 116, 166, 164, 138, 136, 130, 128, 162, 202, 206,
#        204, 208, 102, 104, 100, 200, 98, 198, 194, 196, 190, 192, 186, 188,
#        182, 184, 178, 180 ],
#    [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 124, 160, 126, 156, 152, 158,
#        94, 92, 106, 108, 90, 88, 154, 112, 220, 110, 216, 214, 210, 212, 218,
#        -1, 230, -1, 234, 232, 226, 228, 222, 224, 114, 96, -1, -1, -1, -1 ] ]

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

for i in range( sizeEEPROM ):
    eeprom.append( 0 )

#eeprom = [0xaa, 0x55, 0x33, 0xee, 0x41, 0x30]
eeprom[0:6] = [0xaa, 0x55, 0x33, 0xee, 0x41, 0x30]
 

if( False ):
    ui_boardname            = raw_input( "Enter Name of Board in ASCII (max 32): " )
    ui_boardversionnum      = raw_input( "Enter HW Version of Board in ASCII (max 4): " )
    ui_mfgr                 = raw_input( "Enter Name of Manufacturer in ASCII (max 16): " )
    ui_pn                   = raw_input( "Enter Part Number in ASCII (max 16): " )
    ui_sn                   = raw_input( "Enter Serial Number in ASCII (max 16): " )
    ui_max_i_vdd3v3         = raw_input( "Enter MAX Current (mA) on VDD_3V3EXP Used by Cape (Range 0 to 250mA): " )
    ui_max_i_vdd5v          = raw_input( "Enter MAX Current (mA) on VDD_5V Used by Cape (Range 0 to 1000mA): " )
    ui_max_i_sys5v          = raw_input( "Enter MAX Current (mA) on SYS_5V Used by Cape (Range 0 to 250mA): " )
    ui_supplied_i           = raw_input( "Enter Current (mA) Supplied on VDD_5V by Cape (Range 0 to 65535mA): " )
    ui_num_pins             = raw_input( "Enter Number of Pins Used by Cape (Range 0 to 74): " )
else:
    ui_boardname            = "cory-ledgrid"
    ui_boardversionnum      = "00A0"
    ui_mfgr                 = "silicon-circuits"
    ui_pn                   = "ledgrid-cape"
    ui_sn                   = "1"
    ui_max_i_vdd3v3         = "0"
    ui_max_i_vdd5v          = "0"
    ui_max_i_sys5v          = "50" 
    ui_supplied_i           = "0"
    ui_num_pins             = "1"

pin_conn_num    = []
pin_conn_pinnum = []
pin_usage       = []
pin_type        = []
pin_slew        = []
pin_rxen        = []
pin_pupd        = []
pin_pullen      = []
pin_muxmode     = []

if( False ):
    for pin in range( int(ui_num_pins) ):
        print "Get data for pin %d" % pin
        ui_pin_conn_num     = raw_input( "PIN # %d - Enter Connector number (8 or 9): " % (pin + 1) )
        ui_pin_conn_pinnum  = raw_input( "PIN # %d - Enter connector's pin number (1 or 46): " % (pin + 1) )
        ui_pin_usage        = raw_input( "PIN # %d P%s_%s - Usage? 1=pin used, 0=unused: " % (pin + 1, ui_pin_conn_num, ui_pin_conn_pinnum) )
        ui_pin_type         = raw_input( "PIN # %d P%s_%s - Type? 1=input, 2=output, 3=bidi: " % (pin + 1, ui_pin_conn_num, ui_pin_conn_pinnum) )
        ui_pin_slew         = raw_input( "PIN # %d P%s_%s - Slew? 0=fast, 1=slow: " % (pin + 1, ui_pin_conn_num, ui_pin_conn_pinnum) )
        ui_pin_rxen         = raw_input( "PIN # %d P%s_%s - Rx Enabled? 0=disabled, 1=enabled: " % (pin + 1, ui_pin_conn_num, ui_pin_conn_pinnum) )
        ui_pin_pupd         = raw_input( "PIN # %d P%s_%s - Pullup or Pulldown? 0=pulldown, 1=pullup: " % (pin + 1, ui_pin_conn_num, ui_pin_conn_pinnum) )
        ui_pin_pullen       = raw_input( "PIN # %d P%s_%s - Pull enable? 0=enabled, 1=disabled: " % (pin + 1, ui_pin_conn_num, ui_pin_conn_pinnum) )
        ui_pin_muxmode      = raw_input( "PIN # %d P%s_%s - Pin Mux Mode? (0 through 7): " % (pin + 1, ui_pin_conn_num, ui_pin_conn_pinnum) )

        pin_conn_num.append(    ui_pin_conn_num     )
        pin_conn_pinnum.append( ui_pin_conn_pinnum  )
        pin_usage.append(       ui_pin_usage        )
        pin_type.append(        ui_pin_type         )
        pin_slew.append(        ui_pin_slew         )
        pin_rxen.append(        ui_pin_rxen         )
        pin_pupd.append(        ui_pin_pupd         )
        pin_pullen.append(      ui_pin_pullen       )
        pin_muxmode.append(     ui_pin_muxmode      )
else:
    pin_conn_num.append(    "8"     )
    pin_conn_pinnum.append( "12"    )
    pin_usage.append(       "1"     )
    pin_type.append(        "2"     )
    pin_slew.append(        "0"     )
    pin_rxen.append(        "0"     )
    pin_pupd.append(        "0"     )
    pin_pullen.append(      "1"     )
    pin_muxmode.append(     "6"     )

s = ui_boardname
size = 32
i = 0x6
for char in s:
    eeprom[i] = ord( char )
    i += 1

s = ui_boardversionnum
size = 4
i = 0x26 # 38d
for char in s:
    eeprom[i] = ord( char )
    i += 1

s = ui_mfgr
size = 16
i = 0x2A # 42d
for char in s:
    eeprom[i] = ord( char )
    i += 1

s = ui_pn
size = 16
i = 0x3A #58d
for char in s:
    eeprom[i] = ord( char )
    i += 1

s = ui_num_pins
size = 2
i = 0x4B #75d
eeprom[i] = int( s )

s = ui_sn
size = 12
i = 0x4C #76d
for char in s:
    eeprom[i] = ord( char )
    i += 1

# ---------
# print "eepromIndex[%d][%d] = \\"
# for i in range( 2 ):
#     print "" # newline
#     for j in range( 46 ):
#         #print "eepromIndex[%d][%d] = 0x%x" % (i, j, eepromIndex[i][j])
#         if( eepromIndex[i][j] == -1 ):
#             print "-1, ",
#         else:
#             print "0x%x, " % (eepromIndex[i][j]),
# print "" # newline
# sys.exit(0)


i = 88
for j in range( int(ui_num_pins) ):
    upper = ( ( int(pin_usage[j])   & 0x1 ) << 7 ) | \
            ( ( int(pin_type[j])    & 0x3 ) << 5 )
    lower = ( ( int(pin_slew[j])    & 0x1 ) << 6 ) | \
            ( ( int(pin_rxen[j])    & 0x1 ) << 5 ) | \
            ( ( int(pin_pupd[j])    & 0x1 ) << 4 ) | \
            ( ( int(pin_pullen[j])  & 0x1 ) << 3 ) | \
            ( ( int(pin_muxmode[j]) & 0x7 ) << 0 )

    eeprom_index = eepromIndex[int(pin_conn_num[j]) - 8][int(pin_conn_pinnum[j]) - 1]
    if eeprom_index == -1:
        raise Exception( 'Header pin P%d-%d cannot be changed.' % (int(pin_conn_num[j]), int(pin_conn_pinnum[j])) )
    print "For pin entry #%d : Replacing eeprom_index=0x%x values (0x%x, 0x%x) with new values (0x%x, 0x%x)" % \
        (j, eeprom_index, eeprom[eeprom_index], eeprom[eeprom_index+1], upper, lower)
    eeprom[eeprom_index]    = upper; # big endian: high_order byte in the low address
    eeprom[eeprom_index+1]  = lower; # big endian: low_order byte in the high address


# ---------

s = ui_max_i_vdd3v3
size = 2
i = 236
hi_byte = int( s ) >> 8
lo_byte = int( s ) & 0xFF
eeprom[i+0] = hi_byte
eeprom[i+1] = lo_byte

s = ui_max_i_vdd5v
size = 2
i = 238
hi_byte = int( s ) >> 8
lo_byte = int( s ) & 0xFF
eeprom[i+0] = hi_byte
eeprom[i+1] = lo_byte

s = ui_max_i_sys5v
size = 2
i = 240
hi_byte = int( s ) >> 8
lo_byte = int( s ) & 0xFF
eeprom[i+0] = hi_byte
eeprom[i+1] = lo_byte

s = ui_supplied_i
size = 2
i = 242
hi_byte = int( s ) >> 8
lo_byte = int( s ) & 0xFF
eeprom[i+0] = hi_byte
eeprom[i+1] = lo_byte

# ================================================================================
# Write the Binary File
# ================================================================================

if( False ):
    for i in range( len(eeprom) ):
        print "i=%d: %x (%s)" % (i, eeprom[i], chr( eeprom[i] ) )

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
