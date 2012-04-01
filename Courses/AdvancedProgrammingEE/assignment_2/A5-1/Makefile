# Makefile for  in assignment_02
# Course Name : EE 717 - Advanced Computing for Electrical Engineers
# ABOUT : Implementation of A5/1.
# Dilawar, dilawar@ee.iitb.ac.in
# Created on : Aug 14, 2010
# Modification logs : 
CC = g++
CFLAGS = -c -g -Wall 
MACRO =  -D DEBUG_NOTHING # change to DEBUG if you want to see all the crap.
VPATH = 
OBJECTS = main.o linear_feedback_shift_register.o
INCFLAGS = -I include 
LDFLAGS = -Wl,-rpath,/usr/local/lib
LIBS = 

all: lfsr

lfsr: $(OBJECTS)
	$(CC) -o lfsr $(OBJECTS) $(LDFLAGS) $(LIBS)

main.o : main.cc
	$(CC)  $(CFLAGS) $(MACRO) $(INCFLAGS)$< -o $@

linear_feedback_shift_register.o : linear_feedback_shift_register.cc
	$(CC) $(CFLAGS) $(MACRO) $(INCFLAGS)$< -o $@


.SUFFIXES:
.SUFFIXES:	.c .cc .C .cpp .o

.c.o :
	$(CC) -o $@ -c $(CFLAGS) $< $(INCFLAGS)

count:
	wc *.c *.cc *.C *.cpp *.h *.hpp

clean:
	rm -f *.o

.PHONY: all
.PHONY: count
.PHONY: clean
