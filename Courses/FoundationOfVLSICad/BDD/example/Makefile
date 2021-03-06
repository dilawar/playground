###############################################################################
# Makefile for literate programes. It creates pdf and dvi documents as
# well as generate codes for execution.
#
# USAGE : 
# $ make  -- To execute the program.
# $ make dvi -- To make a dvi document.
# $ make pdf -- To create a pdf document.
# $ make showdvi
# $ make showpdf
#
# (c) Dilawar, 2011
# Email : dilawar@ee.iitb.ac.in
# 
# June 30, 2011
###############################################################################
SHELL = /bin/sh
NOTANGLE = notangle 
NOWEAVE = noweave #-delay it implies -n option. Automatic latex wrapper will not be includeded in out tex file.
CC = gcc 
CFLAGS = -Wall -D DEBUG
file = construct_bdd
CFLAGS2 =

$(file) : $(file).snw
	$(NOTANGLE) -RHeader $< | cpif ./codes/$(file).h
	$(NOTANGLE) $< | cpif ./codes/$(file).c
	$(CC) $(CFLAGS) ./codes/$(file).c -o mybdd


dvi : $(file).snw
	$(NOWEAVE) $< > ./docs/$(file).tex
	latex -output-directory=docs ./docs/$(file).tex 
	rm -rf *.log *.aux *.tex~

pdf : $(file).snw
	$(NOWEAVE) $< > ./docs/$(file).tex
	pdflatex -output-directory=docs ./docs/$(file).tex 
	rm -rf *.log *.aux *.tex~

showdvi : 
	if $(shell test -e ./docs/$(file).dvi) \
	then $(shell xdvi ./docs/$(file).dvi) \
	else echo 'Run make dvi file=filename.' ;\
	fi

showpdf : 
	if $(shell test -e ./docs/$(file).pdf)\
	then $(shell xpdf ./docs/$(file).pdf) \
	else echo 'Run make pdf file=filename.' ;\
	fi

purge :
	rm -rf ./docs/* ./codes/* 
