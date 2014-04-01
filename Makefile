#
# Execute 'make' to create ledgrid.bin and ledgrid 
# Other options:
# make clean
# make all
# make ledgrid 
# make project
# make prucode
# make clean
#

pru = ledgriddrvr
project = ledgrid

LIB_PATH = .
LIBRARIES = pthread prussdrv
INCLUDES = -I. ${LIB_PATH}

SOURCES =  ledgrid.c

EXTRA_DEFINE = 
CCCFLAGS = $(EXTRA_DEFINE)
CC = gcc
CFLAGS = $(EXTRA_DEFINE)
PASM = pasm

all : $(pru) $(project)
pru : $(pru)
project: $(project)

$(project) : $(project:%=%.c)
	$(CC) $(CFLAGS) -c -o $@.o $@.c
	$(CC) $@.o $(LIB_PATH:%=-L%) $(LIBRARIES:%=-l%) -o $@

clean :
	rm -rf *.o *.bin $(project) core *~

$(pru) : $(pru:%=%.p)
	$(PASM) -b $@.p

.SUFFIXES: .c.d

%.d: %.c
	$(SHELL) -ec "$(CC) -M $(CPPFLAGS) $< | sed 's/$*\\.o[ :]*/$@ &/g' > $@" -include $(SOURCES:.c=.d)

