all : ./compressed_sensing.png ./magic_reconstruction.png  labnote.pdf labnote.html 
	@echo "All done"

labnote.pdf : labnote.pandoc 
	~/Scripts/pandoc2pdf.sh $<

labnote.html : labnote.pandoc
	~/Scripts/pandoc2html.py $<
