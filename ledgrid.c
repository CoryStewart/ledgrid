/*
 * ledgrid.c
 *
 *
*/

//#define NUM_OF_PIXELS   4*60
#define NUM_OF_PIXELS   256
#define INTERSCAN_DELAY 0x0100000   // this is verified
#define BRIGHTNESS      0xFC        // 0-0xFF value for R,G, or B max value

/******************************************************************************
* Include Files                                                               *
******************************************************************************/

// Standard header files
#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <time.h>

// Driver header file
#include "prussdrv.h"
#include <pruss_intc_mapping.h>	 

/******************************************************************************
* Explicit External Declarations                                              *
******************************************************************************/

/******************************************************************************
* Local Macro Declarations                                                    *
******************************************************************************/

#define PRU_NUM 	0

#define DDR_BASEADDR        0x80000000
#define OFFSET_DDR	        0x00001000 
#define OFFSET_SHAREDRAM    2048		//equivalent with 0x00002000

#define PRUSS0_SHARED_DATARAM    4

/******************************************************************************
* Local Typedef Declarations                                                  *
******************************************************************************/


/******************************************************************************
* Local Function Declarations                                                 *
******************************************************************************/

void initPixelArr( unsigned int offset );
void initPixelArr2( unsigned int offset );
void initPixelArr3( unsigned int offset, unsigned int color );
void clearPixelArr();

/******************************************************************************
* Interrupt Service Routines                                                  *
******************************************************************************/


/******************************************************************************
* Global Variable Definitions                                                 *
******************************************************************************/

static int mem_fd;
static void *ddrMem, *sharedMem;

static unsigned int *sharedMem_int;

/******************************************************************************
* Global Function Definitions                                                 *
******************************************************************************/

int main (void) {
    unsigned int ret;
    unsigned int i, j, k;

    tpruss_intc_initdata pruss_intc_initdata = PRUSS_INTC_INITDATA;
    
    printf("\nINFO: Starting %s example.\r\n", "ledgrid");
    prussdrv_init (); // Initialize the PRU
    
    /* Open PRU Interrupt */
    ret = prussdrv_open(PRU_EVTOUT_0);
    if (ret) {
        printf("prussdrv_open open failed\n");
        return (ret);
    }
    
    /* Get the interrupt initialized */
    prussdrv_pruintc_init(&pruss_intc_initdata);

    /* Initialize example */
    printf("\tINFO: Initializing example.\r\n");
    prussdrv_map_prumem( PRUSS0_SHARED_DATARAM, &sharedMem );
    sharedMem_int = (unsigned int*) sharedMem;


    for( i=0 ; i < 3 ; i++ ) {
        //for( j=0 ; j < 3 ; j++ ) {
        for( j=1 ; j <= NUM_OF_PIXELS ; j++ ) {
            initPixelArr3( j, i % 3 );
            updatePixelStrip();
            sleep( 0.001 ); // in ms
        }
    }
    clearPixelArr();
    updatePixelStrip();
    
    // cory: Confirm PRU operation by checking that it wrote a signature into the shared ram:
    if( (sharedMem_int[OFFSET_SHAREDRAM + 0] == 0xACEDACED) &&
        (sharedMem_int[OFFSET_SHAREDRAM + 1] == 0xC001BABE) &&
        (sharedMem_int[OFFSET_SHAREDRAM + 2] == 0xFACEFACE) ) {
        printf( "PRU wrote the signature correctly... Confirmed by c-code.\n" );
    } else {
        printf( "PRU did NOT write the signature correctly...\n" );
        printf( "   sig1 = 0x%08x (expected=0x%08x)\n", sharedMem_int[OFFSET_SHAREDRAM + 0], 0xACEDACED );
        printf( "   sig2 = 0x%08x (expected=0x%08x)\n", sharedMem_int[OFFSET_SHAREDRAM + 1], 0xC001BABE );
        printf( "   sig3 = 0x%08x (expected=0x%08x)\n", sharedMem_int[OFFSET_SHAREDRAM + 2], 0xFACEFACE );
    }

    
    /* Disable PRU and close memory mapping*/
    prussdrv_pru_disable(PRU_NUM); 
    prussdrv_exit ();

    return(0);
}

/*****************************************************************************
* Local Function Definitions                                                 *
*****************************************************************************/
updatePixelStrip() {
    unsigned int k;

    /* Execute example on PRU */
    prussdrv_exec_program (PRU_NUM, "./ledgriddrvr.bin");
    /* Wait until PRU0 has finished execution */
    prussdrv_pru_wait_event (PRU_EVTOUT_0);
    prussdrv_pru_clear_event (PRU_EVTOUT_0, PRU0_ARM_INTERRUPT);
    for( k=0 ; k < INTERSCAN_DELAY ; k++ ) { ; }
} // updatePixelStrip()

// ----

void initPixelArr( unsigned int offset ) {
    int i = 0;

    sharedMem_int[OFFSET_SHAREDRAM + 0] = NUM_OF_PIXELS;      // # of Pixels
    for( i=1 ; i <= NUM_OF_PIXELS ; i++ ) {
        if( (i+offset) % 3 == 0 )
            sharedMem_int[OFFSET_SHAREDRAM + i] = BRIGHTNESS << 16; // GRB value
        else if( (i+offset) % 3 == 1 ) 
            sharedMem_int[OFFSET_SHAREDRAM + i] = BRIGHTNESS << 8; // GRB value
        else if( (i+offset) % 3 == 2 ) 
            sharedMem_int[OFFSET_SHAREDRAM + i] = BRIGHTNESS << 0; // GRB value
    }
}

void initPixelArr2( unsigned int offset ) {
    int i = 0;

    sharedMem_int[OFFSET_SHAREDRAM + 0] = NUM_OF_PIXELS;      // # of Pixels
    for( i=1 ; i <= NUM_OF_PIXELS ; i++ ) {
        if( offset == 0 )
            sharedMem_int[OFFSET_SHAREDRAM + i] = BRIGHTNESS << 16; // GRB value
        else if( offset == 1 )
            sharedMem_int[OFFSET_SHAREDRAM + i] = BRIGHTNESS << 8; // GRB value
        else if( offset == 2 )
            sharedMem_int[OFFSET_SHAREDRAM + i] = BRIGHTNESS << 0; // GRB value
    }
}

void initPixelArr3( unsigned int on_led, unsigned int color ) {
    int i;

    sharedMem_int[OFFSET_SHAREDRAM + 0] = NUM_OF_PIXELS;      // # of Pixels
    for( i=1 ; i <= NUM_OF_PIXELS ; i++ ) {
        if( i == on_led ) {
            sharedMem_int[OFFSET_SHAREDRAM + i] = 
                (color == 0) ? BRIGHTNESS << 8 :
                (color == 1) ? BRIGHTNESS << 16 :
                               BRIGHTNESS << 0; // GRB value
        } else {
            sharedMem_int[OFFSET_SHAREDRAM + i] = 0; // GRB value
        } 
    }
}

// ----

void clearPixelArr () {
    unsigned int i;

    sharedMem_int[OFFSET_SHAREDRAM + 0] = NUM_OF_PIXELS;    // # of Pixels
    for( i=1 ; i <= NUM_OF_PIXELS ; i++ ) {
        sharedMem_int[OFFSET_SHAREDRAM + i] = 0x00000000;   // GRB value
    }
}

