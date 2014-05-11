// ledtest.p
// based on code at: http://www.element14.com/community/community/knode/single-board_computers/next-gen_beaglebone/blog/2013/05/22/bbb--working-with-the-pru-icssprussv2 
// The GPIO pin used is GPIO1_12 and is on the BBB P8 header pin 12 and controlled by by R30_14 (...1_MI0_TXDZ/PRI_PRU0_PRU_R30_14/GPIO1_12)

.origin 0
.entrypoint START

#include "ledgriddrvr.hp"

#define GPIO1 0x4804c000
#define GPIO_CLEARDATAOUT 0x190
#define GPIO_SETDATAOUT 0x194


START:

    // Enable OCP master port
    // cory: CONST_PRUCFG is #defined as C4 in the ledgriddrvr.hp file.  C4 is the constants table entry
    //       for 'PRU-ICSS CFG (local)' {see 01-AM335x_PRU_ICSS_Overview.pdf}.
    LBCO    r0, CONST_PRUCFG, 4, 4  // r0 = *(CONST_PRUCFG + 4) # 4 bytes  ; CONST_PRUCFG is C4
    CLR     r0, r0, 4         // Clear SYSCFG[STANDBY_INIT] to enable OCP master port
    SBCO    r0, CONST_PRUCFG, 4, 4

    // Configure the programmable pointer register for PRU0 by setting c28_pointer[15:0]
    // field to 0x0120.  This will make C28 point to 0x00012000 (PRU shared RAM).
    MOV     r0, 0x00000120
    MOV     r1, CTPPR_0
    ST32    r0, r1

    // Configure the programmable pointer register for PRU0 by setting c31_pointer[15:0]
    // field to 0x0010.  This will make C31 point to 0x80001000 (DDR memory).
    MOV     r0, 0x00100000
    MOV     r1, CTPPR_1
    ST32    r0, r1

    // CORY: made my changes here
    QBA CORY    // QuickBranchAlways to CORY

//#define TESTING
CORY:
#ifdef TESTING
    MOV     r0, 0x00000001                  // number of LEDs
    MOV     r1, 0x00ff0000                  // pixel #1
    MOV     r2, 0x0000ff00                  // pixel #2
    MOV     r3, 0x000000ff                  // pixel #3
    MOV     r4, 0x00ffffff                  // pixel #4
    MOV     r5, 0x00aaaaaa                  // pixel #5
    MOV     r6, 0x00111111                  // pixel #6
    MOV     r7, 0x00ffffff                  // pixel #7
    MOV     r8, 0x10ffffff                  // pixel #8
    SBCO    r0, CONST_PRUSHAREDRAM, 0, 4*(8+1)
#endif


    LBCO    r1, CONST_PRUSHAREDRAM, 0, 4 // LoadByteBurstConstantTableOffset: r1 = *(shared_ram+0) = # of LEDS
    MOV     r3, r1          // init loop counter (r3 = r1)
    MOV     r5, 4           // r5 = byte index into shared mem for pixels:  4, 8, 12, ... (#_of_LEDS * 4)
PIXELLOOP:
    LBCO    r6, CONST_PRUSHAREDRAM, r5, 4     // Get pixel value in r6; r6 = *(r5 + 0)

    MOV     r7, 0           // initial bit index = 0
BITLOOP:
    //QBNE    IT_IS_ONE, r6, 0
    QBBS    IT_IS_ONE, r6, r7   // QuickBranchIfBitIsSet: branch if( r6 & (1 << r7) )
IT_IS_ZERO:
    CALL    OUTPUT0
    JMP     DONE_WITH_BIT
IT_IS_ONE:
    CALL    OUTPUT1

DONE_WITH_BIT:
    ADD     r7, r7, 1
    QBNE    BITLOOP, r7, (3 * 8)    // branch when we get to bit24 of the pixel value

DONE_WITH_PIXEL:
    ADD     r5, r5, 4       // Incr to next pixel
    SUB     r3, r3, 1       // r3 = r3 - 1
    QBNE    PIXELLOOP, r3, 0  // QuickBranch to PIXELLOOP if r3 != 0

    // Modify the shared mem space so the c-code can confirm the PRU has actually run (for debugging)
    MOV r0, 0xACEDACED
    MOV r1, 0xC001BABE
    MOV r2, 0xFACEFACE
    SBCO r0, CONST_PRUSHAREDRAM, 0, 12   // move 12 bytes (regs r0, r1 & r2) to shared ram

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
    MOV     r8, 34          // init delay count
DEL0_0:
    SUB     r8, r8, 1
    QBNE    DEL0_0, r8, 0

    CLR     r30.t14
    MOV     r8, 76          // init delay count
DEL1_0:
    SUB     r8, r8, 1
    QBNE    DEL1_0, r8, 0

    RET

// ---------- Subroutine OUTPUT1 ----------
OUTPUT1:
    SET     r30.t14             // Setting bit #14 of r30.  R30[14] is PRU GPO[14]
    MOV     r8, 70              // init delay count
DEL0_1:
    SUB     r8, r8, 1
    QBNE    DEL0_1, r8, 0

    CLR     r30.t14             // Clearing bit #14 of r30.  R30[14] is PRU GPO[14]
    MOV     r8, 56              // init delay count
DEL1_1:
    SUB     r8, r8, 1
    QBNE    DEL1_1, r8, 0

    RET

