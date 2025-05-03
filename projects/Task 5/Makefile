################################################################################
# Project configuration

BIN = fft

# Note: by default, we fetch all source code in the current directory

SOURCES  := $(wildcard *.c)
INCLUDES := $(wildcard *.h)
OBJECTS  := $(SOURCES:%.c=%.o)

################################################################################
# Toolchain configuraiton

# Compiler
CC	= gcc

# IF you are using OS X, use the following CFLAGS
CFLAGS  = -g -Wall -std=c99 -D_XOPEN_SOURCE
LDFLAGS = -lpthread

#If you are using Linux, uncomment the following lines
#CFLAGS  = -g -Wall -std=c99 -D_POSIX_SOURCE -D_GNU_SOURCE
#LDFLAGS = -lpthread -lrt -lm

# Indent
INDENT_FLAGS = -i2 -nip -di0 -br -lp -nfbs -pcs -npsl

################################################################################
# Generic Makefile rules

all: $(BIN)

clean:
	-rm -rf *.o *~ *.BAK *.gch

distclean: clean
	-rm -rf $(BIN) *.dSYM

fft: $(OBJECTS)
	$(CC) -o fft $(OBJECTS) $(CFLAGS) $(LDFLAGS)


$(OBJECTS): %.o : %.c
	$(CC) $(CFLAGS) -c $< -o $@

indent:
	@for file in $(SOURCES) $(INCLUDES); do \
		indent $(INDENT_FLAGS) $$file; \
	done
