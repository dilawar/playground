# Makefile for problem_1 in assignment_01 
# Course Name : EE 717 - Advanced Computing for Electrical Engineers
# ABOUT : Test primality of a number.
# Dilawar, dilawar@ee.iitb.ac.in
# Created on : July Aug 4, 2010
# Modification logs : 
CC = g++
CFLAGS = -c -g -Wall 
MACRO =  -D NOTHING 
VPATH = src:../include include
OBJECTS = main.o check_if_prime.o stats_algo.o
INCFLAGS = -I include 
LDFLAGS = -Wl,-rpath,/usr/local/lib
LIBS = 

all: testprime

testprime: $(OBJECTS)
	$(CC) -o testprime $(OBJECTS) $(LDFLAGS) $(LIBS)

main.o : main.cc
	$(CC)  $(CFLAGS) $(MACRO) $(INCFLAGS)$< -o $@

check_if_prime.o : check_if_prime.cc
	$(CC) $(CFLAGS) $(MACRO) $(INCFLAGS)$< -o $@

stats_algo.o : stats_algo.cc
	$(CC) $(CFLAGS) $(MACRO) $(INCFLAGS) $< -o $@

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
