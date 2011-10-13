###############################################################################
# Makefile for literate python program. It creates pdf and dvi documents as
# well as generate codes for execution,
#
# USAGE : make <target> file=<filename>
# <fileaname> must be without any extension. For example, if one wants to make
# example.snw for generating a dvi file then one should use following command.
# $ make dvi file=example
#
# (c) Dilawar, 2011
# Email : dilawar@ee.iitb.ac.in
# 
# June 30, 2011
###############################################################################
SHELL = /bin/sh
NOTANGLE = notangle 
NOWEAVE = noweave -delay # it implies -n option. Automatic latex wrapper will not be includeded in out tex file.
PY = python
PYFLAGS = 
PYFLAGS2 =
file = bipartite

$(file) : $(file).snw
	$(NOTANGLE) $(file).snw > ./codes/$(file).py
	$(PY) $(PYFLAGS) -i ./codes/$(file).py


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
