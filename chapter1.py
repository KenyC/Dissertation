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

options.dom_quant     = 4      # Setting a large-ish domain of quantification
options.latex_display = False  # disabling LateX display ; you can enable if you're using Jupyter Notebook (as opposed to IPython) 
display = jprint if options.latex_display else print
options_alts.scales   = [{Existential, Universal}, {Existential, Most}] # Remove "or"/"and" scale; we'll be using disjunction to model existentials without universal alternatives


# %%
"""
<span id="noncumulative"></span>
# Exhaustive participation inferences in non-cumulative sentences: recursive Exh 
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
<span id="noncumulative_ii"></span>
# Exhaustive participation inferences in non-cumulative sentences: innocent inclusion Exh 
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
<span id="cumulative_every_naive"></span>
# Cumulative reading of every : non-recursive exhaustification

Note how we perform the exhaustification, ignoring that "every" has "some" as an alternative. As pointed out by Chemla & Spector (2011), the "some" alternative block the distributive implicature, a testament to the inadequacy of the standard derivation.
"""

# setting a and b to depend on x (innocuous warnings appear)
# here, we only use thee disjuncts ; the number of logical possibility can quickly explode
a("x")
b("x")
c("x")

prejacent  = Ax > a | b | c
universe   = Universe(f = prejacent)
sentence   = Exh(prejacent, scales = []) # we must ignore the "some/all" scales. As p

print("Assumed LF:", sentence)

sentence.diagnose(display)
print(
	"There is a nut that only Scrat cracked:", 
	universe.entails(sentence, Ex > a & ~b & ~c)
)
print(
	"Equivalent to cumulative reading:", 
	universe.equivalent(
		sentence, 
		prejacent & (Ex > a) & (Ex > b) & (Ex > c)
	)
)
# %%
"""
<span id="cumulative_every"></span>
# Cumulative reading of every 
"""

prejacent  = Ax > a | b | c
universe = Universe(f = prejacent)
sentence   = Exh(Exh(prejacent))

print("Assumed LF:", sentence)

sentence.diagnose(display)
print(
	"Equivalent to cumulative reading:", 
	universe.equivalent(
		sentence, 
		prejacent & (Ex > a) & (Ex > b) & (Ex > c)
	)
)

# %%
"""
<span id="cumulative_every_ii"></span>
# Cumulative reading of every: the innocent inclusion approach 
"""

prejacent  = Ax > a | b | c
sentence   = Exh(prejacent, ii = True)

print("Assumed LF:", sentence)

sentence.diagnose(display)
print("Equivalent to cumulative reading:          ", universe.equivalent(sentence, prejacent & (Ex > a) & (Ex > b) & (Ex > c)))
print("Equivalent to doubly-distributive reading: ", universe.equivalent(sentence, (Ax > a) & (Ax > b) & (Ax > c)))

# %%
"""
<span id="cumulative_most"></span>
# Cumulative reading of most 
"""
prejacent  = Mx > a | b | c
first_exh  = Exh(prejacent)
lf         = Exh(first_exh)

print("Assumed LF:", lf)

lf.diagnose(display)
print("Equivalent to cumulative reading:", universe.equivalent(lf, prejacent & (Ex > a) & (Ex > b) & (Ex > c)))





# %%
"""
<span id="asymmetries"></span>
# Asymmetries in cumulative readings 
Non-cumulative reading of every.
"""

scales     = [{Existential, Universal}] # our "disjunction", which models the existential with subdomain alternates, should not have a conjunctive alternative
lf         = Exh(Exh(Ax > Exh(Exh(a | b))))
print("Assumed LF:", lf)



lf.diagnose(display)
print("Equivalent to cumulative reading:", universe.equivalent(lf, (Ax > a | b) & (Ex > a) & (Ex > b)))
print("Equivalent to doubly-dist reading:", universe.equivalent(lf, Ax > a & b))

# %%
"""
<span id="asymmetries"></span>
# Asymmetries in cumulative readings 
Non-cumulative reading of every.
"""

scales     = [{Existential, Universal}] # our "disjunction", which models the existential with subdomain alternates, should not have a conjunctive alternative
lf         = Exh(Exh(Ax > Exh(Exh(a | b))))
print("Assumed LF:", lf)



lf.diagnose(display)
print("Equivalent to cumulative reading:", universe.equivalent(lf, (Ax > a | b) & (Ex > a) & (Ex > b)))
print("Equivalent to doubly-dist reading:", universe.equivalent(lf, Ax > a & b))

# %%
"""
<span id="ordinary"></span>
# Ordinary cumulative sentences 
Ordinary cumulative sentences  
*The squirrels cracked the nuts*
"""

s1_cracked_n1 = Pred(1, name = "s1 cracked n1")
s1_cracked_n2 = Pred(2, name = "s2 cracked n1")
s2_cracked_n1 = Pred(3, name = "s1 cracked n2")
s2_cracked_n2 = Pred(4, name = "s2 cracked n2")


sentence = Exh(Exh(s1_cracked_n1, alts = [s1_cracked_n2]))
print(sentence.alts)
# print("Equivalent to cumulative reading:", universe.equivalent(lf, (Ax > a | b) & (Ex > a) & (Ex > b)))
# print("Equivalent to doubly-dist reading:", universe.equivalent(lf, Ax > a & b))


# %%