
all: $(wildcard *.py)
	@echo "Converting all notebooks"

%_: %.html
	firefox $<

%.html: %.ipynb
	/home/keny/anaconda3/envs/exh_test/bin/jupyter nbconvert $< --to html

%.ipynb: %.py
	py2jp   $<
