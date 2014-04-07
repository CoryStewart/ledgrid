.origin 0
.entrypoint START

// Address for the Constant table Programmable Pointer Register 0(CTPPR_0)	
#define CTPPR_0         0x22028 

// Address for the Constant table Programmable Pointer Register 1(CTPPR_1)	
#define CTPPR_1         0x2202C 	

#define GPIO1           0x4804c000          // The adress of the GPIO1 
#define GPIO_DATAOUT    0x13c               // This is the register for settign data
#define LEN_ADDR        0x00000000          // Adress of the abort command          
#define PIN_OFFSET      0x00000004          // Offset for the pins (reserve the first adress for abort)
#define PRU0_ARM_INTERRUPT  19
#define CONST_PRUSHAREDDRAM C28

//.macro ST32
//.mparam src,dst
//    SBBO    src,dst,#0x00,4
//.endm

START:  
    // Enable OCP master port
    // cory: CONST_PRUCFG is #defined as C4 in the ledgriddrvr.hp file.  C4 is the constants table entry
    //       for 'PRU-ICSS CFG (local)' {see 01-AM335x_PRU_ICSS_Overview.pdf}.
    LBCO r0, C4, 4, 4                       // clear that bit
    CLR  r0, r0, 4                          // No, really, clear it!
    SBCO r0, C4, 4, 4                       // Actually i have no idea what this does

    // Configure the programmable pointer register for PRU0 by setting c28_pointer[15:0]
    // field to 0x0120.  This will make C28 point to 0x00012000 (PRU shared RAM).
    //MOV     r0, 0x00000120
    MOV     r0, 0x0
    MOV     r1, CTPPR_0
    //ST32    r0, r1
    SBBO    r0, r1, #0x0, 4

#ifdef TESTING
    MOV     r0, 0x00000008                  // number of LEDs
    MOV     r1, 0x00ff0000                  // pixel #1
    MOV     r2, 0x0000ff00                  // pixel #2
    MOV     r3, 0x000000ff                  // pixel #3
    MOV     r4, 0x00ffffff                  // pixel #4
    MOV     r5, 0x00aaaaaa                  // pixel #5
    MOV     r6, 0x00111111                  // pixel #6
    MOV     r7, 0x00ffffff                  // pixel #7
    MOV     r8, 0x10ffffff                  // pixel #8
    SBCO    r0, CONST_PRUSHAREDDRAM, 0, 4*(8+1)
#endif

    LBCO    r1, CONST_PRUSHAREDDRAM, 0, 4   // LoadByteBurstConstantTableOffset: r1 = *(shared_ram+0) = # of LEDS
    MOV     r3, r1                          // init loop counter (r3 = r1)
    MOV     r5, 4                           // r5 = byte index into shared mem for pixels:  4, 8, 12, ... (#_of_LEDS * 4)
PIXELLOOP:
    LBCO    r6, CONST_PRUSHAREDDRAM, r5, 4  // Get pixel value in r6; r6 = *(r5 + 0)

    MOV     r7, 0                           // initial bit index = 0
BITLOOP:
    QBBS    IT_IS_ONE, r6, r7               // QuickBranchIfBitIsSet: branch if( r6 & (1 << r7) )
IT_IS_ZERO:
    CALL    OUTPUT0
    JMP     DONE_WITH_BIT
IT_IS_ONE:
    CALL    OUTPUT1

DONE_WITH_BIT:
    ADD     r7, r7, 1
    QBNE    BITLOOP, r7, (3 * 8)            // branch when we get to bit24 of the pixel value

DONE_WITH_PIXEL:
    ADD     r5, r5, 4                       // Incr to next pixel
    SUB     r3, r3, 1                       // r3 = r3 - 1
    QBNE    PIXELLOOP, r3, 0                // QuickBranch to PIXELLOOP if r3 != 0

    // Modify the shared mem space so the c-code can confirm the PRU has actually run (for debugging)
    MOV r0, 0xACEDACED
    MOV r1, 0xC001BABE
    MOV r2, 0xFACEFACE
    SBCO r0, CONST_PRUSHAREDDRAM, 0, 12     // move 12 bytes (regs r0, r1 & r2) to shared ram

    // Send notification to Host for program completion
    // Writes to R31 generate PRU INTC sys_events.  
    // Sending PRU sys_event #3 (R31[3:0]=3).  
    //      PRU INTC is configured to map sys_events[30:2] -> Channel??? -> Host???
    // Host_intr 2-9 are routed to Arm & DSP INTCs.
    // The SoC INTC is configured to map:
    //      SoC INTC sys_events??? -> Channel??? -> Host???
    MOV r31.b0, PRU0_ARM_INTERRUPT+16

    // Halt the processor
    HALT

    // ---------- Subroutine OUTPUT0 ----------
OUTPUT0:
    SET     r30.t14
    MOV     r8, 34                          // init delay count
DEL0_0:
    SUB     r8, r8, 1
    QBNE    DEL0_0, r8, 0

    CLR     r30.t14
    MOV     r8, 76                          // init delay count
DEL1_0:
    SUB     r8, r8, 1
    QBNE    DEL1_0, r8, 0

    RET

    // ---------- Subroutine OUTPUT1 ----------
OUTPUT1:
    SET     r30.t14                         // Setting bit #14 of r30.  R30[14] is PRU GPO[14]
    MOV     r8, 70                          // init delay count
DEL0_1:
    SUB     r8, r8, 1
    QBNE    DEL0_1, r8, 0

    CLR     r30.t14                         // Clearing bit #14 of r30.  R30[14] is PRU GPO[14]
    MOV     r8, 56                          // init delay count
DEL1_1:
    SUB     r8, r8, 1
    QBNE    DEL1_1, r8, 0

    RET


