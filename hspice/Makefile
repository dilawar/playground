all:
	happy -gca Jeera/Par.y
	alex -g Jeera/Lex.x
	(cd Jeera/; latex Doc.tex; dvips Doc.dvi -o Doc.ps)
	ghc --make Jeera/Test.hs -o Jeera/Test
clean:
	-rm -f Jeera/*.log Jeera/*.aux Jeera/*.hi Jeera/*.o Jeera/*.dvi
	-rm -f Jeera/Doc.ps
distclean: clean
	-rm -f Jeera/Doc.* Jeera/Lex.* Jeera/Par.* Jeera/Layout.* Jeera/Skel.* Jeera/Print.* Jeera/Test.* Jeera/Abs.* Jeera/Test Jeera/ErrM.* Jeera/SharedString.* Jeera/Jeera.dtd Jeera/XML.* Makefile*
	-rmdir -p Jeera/
