LED Grid on a BeagleBoneBlack
=============================
This is a project intended as a gift for my son. It's based on something similar I saw on the Tested 
show (youtube).  In that show, Jeromy Williams (jer.williams@gmail.com) showed off his 16x16 LED grid 
built with a Raspberry Pi and displayed animated video game characters on it and programmed from his
Android phone.  I decided, rather than just duplicate what he did, that I'd try to do the same thing 
with a BeagleBoneBlack.

While I totally plagiarized his idea, I've tried to research and come up with my own solution.  That's
half the fun with a project like this anyway.  My artistic skills are quite lacking though, so I 
contacted Jeromy and he graciously provided my first sprite of Mario to get started.  It's included 
in this repo.  

This project consists of:
- BeagleBoneBlack (BBB) C-code for programming the BBB PRU & running some LED driver tests.
- PRU assembly code to get the electrical timing required to drive the WS2812 LED strips.
- Python code to write a BBB cape EEPROM.
- A BBB Device Tree Overlay and compile script to configure the pin muxing on the BBB.
- Python PIL script to decode PNG files.
- To Be Added Soon:  
    - Python PYPRUSS lib use to eliminate the c-code and integrate all PIL code with PYPRUSS code.
    - Code to control the ledgrid hardware with an iPhone app.

