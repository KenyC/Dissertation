FILES   := $(wildcard *.py)
TARGETS := $(FILES:.py=_)
HTML    := $(FILES:.py=.html)
NBS     := $(FILES:.py=.ipynb)

all: $(HTML)
	@echo "Converting all notebooks"
	
display: $(TARGETS)
	@echo "All notebooks converted and displayed"

clean:
	@echo "Removing notebooks and html files"
	rm -f $(HTML)
	rm -f $(NBS)

rebuild: clean all

.PRECIOUS: %.html %.ipynb # Apparently "make" deletes intermediate files!

%_: %.html
	firefox $<

%.html: %.ipynb
	jupyter nbconvert $< --to html

%.ipynb: %.py
	py2jp   $<
# 	jupyter nbconvert $@ --to notebook --execute --inplace
