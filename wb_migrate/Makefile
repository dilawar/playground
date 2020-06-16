export PATH := "$(shell ruby -r rubygems -e 'puts Gem.user_dir')/bin:$(PATH)"
SHELL := /bin/bash
RUBY := $(shell which ruby)
GEM := $(shell which gem)

all : export_to_html
	@echo "Call `make convert` now"

convert:
	find . -name "*.html" | xargs -I file ./wphtml_to_md.py file > file.md


export_to_html : dependencies
	@echo "Assuming you have changed 'source' field in 'import.rb' file"
	$(RUBY) ./import.rb 
	

dependencies :
	@echo "Assuming ruby is installed"
	@echo "See https://import.jekyllrb.com/docs/wordpressdotcom/"
	$(GEM) install jekyll-import --user-install
	$(GEM) install hpricot --user-install || echo "Failed to install hpricot"
	$(GEM) install open_uri_redirections --user-install || echo "Failed to install open_uri_redirections"
