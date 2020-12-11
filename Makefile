FILES   := $(wildcard *.py)
TARGETS := $(FILES:.py=_)
HTML    := $(FILES:.py=.html)

all: $(HTML)
	@echo "Converting all notebooks"
	
display: $(TARGETS)
	@echo "All notebooks converted and displayed"


%_: %.html
	firefox $<

%.html: %.ipynb
	/home/keny/anaconda3/envs/exh_test/bin/jupyter nbconvert $< --to html

%.ipynb: %.py
	py2jp   $<
