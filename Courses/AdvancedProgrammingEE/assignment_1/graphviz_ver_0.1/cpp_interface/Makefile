# Makefile for problem_2 in assignment_01 
# Course Name : EE 717 - Advanced Computing for Electrical Engineers
# ABOUT :See README file. 
# Dilawar, dilawar@ee.iitb.ac.in
# Created on : July Aug 8, 2010
# Modification logs : 
CC = g++
CFLAGS = -c -g -Wall 
MACRO =  -D DEBUG 
VPATH = src:../include include
OBJECTS = main.o\
				 	read_file.o\
				 	generate_file.o
INCFLAGS = -I include 
LDFLAGS = -Wl,-rpath,/usr/local/lib
LIBS = 

all: gv-interface

gv-interface: $(OBJECTS)
	$(CC) -o gv-interface $(OBJECTS) $(LDFLAGS) $(LIBS)

main.o : main.cc
	$(CC)  $(CFLAGS) $(MACRO) $(INCFLAGS)$< -o $@

read_file.o : read_file.cc
	$(CC) $(CFLAGS) $(MACRO) $(INCFLAGS)$< -o $@

generate_file.o : generate_file.cc
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
