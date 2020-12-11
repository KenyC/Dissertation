# %%
"""
Chapter 1
====================================
In this computation, I use "a or b" as a proxy for an existential with sub-domain alternatives.

Some global preliminaries

"""
# Imports 
from exh           import *
from exh.exts.gq   import *
from exh.model     import options
import exh.options as     options_alts

options.dom_quant     = 6      # Setting a large-ish domain of quantification
options.latex_display = False  # disabling LateX display ; you can enable if you're using Jupyter Notebook (as opposed to IPython) 
display = jprint if options.latex_display else print
options_alts.scales   = [{Existential, Universal}, {Existential, Most}] # Remove "or"/"and" scale; we'll be using disjunction to model existentials without universal alternatives


# %%
"""
# Exhaustive participation inferences in non-cumulative sentences: recursive Exh <span id="noncumulative"></span>
*The dancers smiled*
"""

# Here, we model the dancers as a grand disjunction
marielou = Pred(5, name = "marielou")
pierre   = Pred(6, name = "pierre")
rebecca  = Pred(7, name = "rebecca")
wilfried = Pred(8, name = "wilfried")
nazli    = Pred(9, name = "nazli")
# dancers  = [marielou, pierre, rebecca, wilfried, nazli]

prejacent = marielou | pierre | rebecca | wilfried | nazli
universe = Universe(f = prejacent) # Universe objects contain all logical possibilities ; we can use them to check for equivalences
sentence  = Exh(Exh(prejacent))
print("Assumed sentence:", sentence)
print(
	"Equivalent to universal/grand conjunction:", 
	universe.equivalent(sentence, marielou & pierre & rebecca & wilfried & nazli)
)
# Printing excluded alternatives
sentence.diagnose(display)

# %%
"""
# Exhaustive participation inferences in non-cumulative sentences: innocent inclusion Exh <span id="noncumulative_ii"></span>
*The dancers smiled*
"""


prejacent = marielou | pierre | rebecca | wilfried | nazli
universe = Universe(f = prejacent) # Universe objects contain all logical possibilities ; we can use them to check for equivalences
sentence  = Exh(prejacent, ii = True)
print("Assumed sentence:", sentence)
print(
	"Equivalent to universal/grand conjunction:", 
	universe.equivalent(sentence, marielou & pierre & rebecca & wilfried & nazli)
)
# Printing excluded alternatives
sentence.diagnose(display)

# %%
"""
# Cumulative reading of every <span id="cumulative_every"></span>
"""

# setting a and b to depend on x (innocuous warnings appear)
# here, we only use two disjuncts ; with a "large" domain of quantification (6 as set earlier), 3 disjuncts imply 200k logical possbilities
a("x")
b("x")
universe = Universe(fs = [a, b])

prejacent  = Ax > a | b
sentence   = Exh(Exh(prejacent))

print("Assumed LF:", sentence)

sentence.diagnose(display)
print("Equivalent to cumulative reading:", universe.equivalent(sentence, prejacent & (Ex > a) & (Ex > b)))

# %%
"""
# Cumulative reading of every: the innocent inclusion approach <span id="cumulative_every_ii"></span>
"""

prejacent  = Ax > a | b
sentence   = Exh(prejacent, ii = True)

print("Assumed LF:", sentence)

sentence.diagnose(display)
print("Equivalent to cumulative reading:          ", universe.equivalent(sentence, prejacent & (Ex > a) & (Ex > b)))
print("Equivalent to doubly-distributive reading: ", universe.equivalent(sentence, (Ax > a) & (Ax > b)))

# %%
"""
# Cumulative reading of most <span id="cumulative_most"></span>
"""
prejacent  = Mx > a | b
first_exh  = Exh(prejacent)
lf         = Exh(first_exh)

print("Assumed LF:", lf)

lf.diagnose(display)
print("Equivalent to cumulative reading:", universe.equivalent(lf, prejacent & (Ex > a) & (Ex > b)))





# %%
"""
# Asymmetries in cumulative readings <span id="asymmetries"></span>
Non-cumulative reading of every.
"""

scales     = [{Existential, Universal}] # our "disjunction", which models the existential with subdomain alternates, should not have a conjunctive alternative
lf         = Exh(Exh(Ax > Exh(Exh(a | b))))
print("Assumed LF:", lf)



lf.diagnose(display)
print("Equivalent to cumulative reading:", universe.equivalent(lf, (Ax > a | b) & (Ex > a) & (Ex > b)))
print("Equivalent to doubly-dist reading:", universe.equivalent(lf, Ax > a & b))


# %%