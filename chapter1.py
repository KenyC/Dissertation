# %%
"""
Chapter 1
====================================
In this computation, I use "a or b" as a proxy for an existential with sub-domain alternatives.

Some global preliminaries

"""
# Imports 
from exh                  import *
from exh.exts.gq          import *
from exh.exts.subdomain   import *
from exh.model     import options
import exh.options as     options_alts

options.dom_quant     = 4      # Setting a large-ish domain of quantification
options.latex_display = False  # disabling LateX display ; you can enable if you're using Jupyter Notebook (as opposed to IPython) 
display = jprint if options.latex_display else print
options_alts.scales = ListScales([
	SimpleScales([{Existential, Universal}, {Existential, Most}]),  # Remove "or"/"and" scale; we'll be using disjunction to model existentials without universal alternatives
	sub_scale # sub-domain alternatives
])

# %%
"""
Defining predicates and quantifiers that match the name in the text:
"""

# Match names in text
Anut  = A("nut")
Enut  = E("nut")
Esquirrel = Ec_("squirrel", domain = D3) # An existential with subdomain alternatives over a domain of size 3
Asquirrel = A("squirrel", domain = D3)   # The corresponding universal for good measure
cracked = Pred(name = "cracked", depends = ["squirrel", "nut"], domains = (D3, default_domain))
# scrat = Pred(name = "scrat", depends = "nut")
# acorn = Pred(name = "acorn", depends = "nut")
# waggs = Pred(name = "waggs", depends = "nut")

Aamb  = A("amb")
Eamb  = E("amb")
arabic   = Pred(name = "arabic",   depends = "amb")
english  = Pred(name = "english",  depends = "amb")
mandarin = Pred(name = "mandarin", depends = "amb")

Edancer = Ec_("dancer", domain = Domain(5)) 
Adancer = A("dancer", domain = Domain(5))
smiled  = Pred(name = "smiled", depends = "dancer", domains = [Domain(5)])

# %%
"""
<span id="noncumulative"></span>
# Exhaustive participation inferences in non-cumulative sentences: recursive Exh 
*The dancers smiled*
"""


prejacent = Edancer > smiled # there is a dancer that smiled
universe = Universe(f = prejacent) # Universe objects contain all logical possibilities ; we can use them to check for equivalences
sentence  = Exh(Exh(prejacent))
# The combination of dots and circles on the quantifier represent the domain of the existential quantifier: dots are individuals outside the domain, circle individuals inside
print("Assumed LF:", sentence)
sentence.diagnose(display)
print(
	"Equivalent to universal:", 
	universe.equivalent(sentence, Adancer > smiled)
)
# Printing excluded alternatives

# %%
"""
<span id="noncumulative_ii"></span>
# Exhaustive participation inferences in non-cumulative sentences: innocent inclusion Exh 
*The dancers smiled*
"""


prejacent = Edancer > smiled # there is a dancer that smiled
universe = Universe(f = prejacent) # Universe objects contain all logical possibilities ; we can use them to check for equivalences
sentence  = Exh(prejacent, ii = True)
print("Assumed sentence:", sentence)
sentence.diagnose(display)
print(
	"Equivalent to universal:", 
	universe.equivalent(sentence, Adancer > smiled)
)
# Printing excluded alternatives

# %%
"""
<span id="cumulative_every_naive"></span>
# Cumulative reading of every/distributive implicatures : non-recursive exhaustification without some/all scale
*Every ambassador speaks Arabic, French or Mandarin*  
*The three squirrels cracked every nut*

Note how we perform the exhaustification, ignoring that "every" has "some" as an alternative. As pointed out by Chemla & Spector (2011), the "some" alternative block the distributive implicature, a testament to the inadequacy of the standard derivation.
"""



prejacent  = Aamb > arabic | english | mandarin
universe   = Universe(f = prejacent)
sentence   = Exh(prejacent, scales = []) # we must ignore the "some/all" scales. 

print("Assumed LF:", sentence)

sentence.diagnose(display)
print(
	"There is an ambassador that only speaks English:", 
	universe.entails(sentence, Eamb > english & ~arabic & ~mandarin)
)

dist = (Eamb > english) & (Eamb > arabic) & (Eamb > mandarin)
print(
	"Equivalent to reported distributive implicature:", 
	universe.equivalent(
		sentence, 
		prejacent & dist
	)
)

# %%
"""
<span id="ii_with_some"></span>
# Cumulative reading of every/distributive implicatures : non-recursive exhaustification with some/all scale
*Every ambassador speaks Arabic, French or Mandarin*  
*The three squirrels cracked every nut*

Here, we allow "some" as an alternative to "every". We don't generate problematic distributive implicature because we don't generate any implicature at all!
"""

prejacent  = Aamb > arabic | english | mandarin
universe   = Universe(f = prejacent)
sentence   = Exh(prejacent, scales = [{Existential, Universal}]) # we must ignore the "some/all" scales. 

print("Assumed LF:", sentence)

sentence.diagnose(display)
print(
	"There is an ambassador that only speaks English:", 
	universe.entails(sentence, Eamb > english & ~arabic & ~mandarin)
)

dist = (Eamb > english) & (Eamb > arabic) & (Eamb > mandarin)
print(
	"Equivalent to prejacent:", 
	universe.equivalent(
		sentence,
		prejacent
	)
)


# %%
"""
<span id="dist_ii"></span>
# Distributive implicature/cumulative readings of "every" : innocent exclusion exhaustification
*Every ambassador speaks Arabic, French or Mandarin*  
*The three squirrels cracked every nut*

Note how we perform the exhaustification, ignoring that "every" has "some" as an alternative. As pointed out by Chemla & Spector (2011), the "some" alternative block the distributive implicature, a testament to the inadequacy of the standard derivation.
Because II exhaustification embeds IE exhaustification, the results are the same.
"""


prejacent  = Aamb > arabic | english | mandarin
universe   = Universe(f = prejacent)
sentence   = Exh(prejacent, scales = [], ii = True) # here too, we must ignore the "some/all" scales. As p

print("Assumed LF:", sentence)

# Since exclusion happens first, the derived result is the same as above
sentence.diagnose(display)
print(
	"There is an ambassador that only speaks English:", 
	universe.entails(sentence, Eamb > english & ~arabic & ~mandarin)
)

dist = (Eamb > english) & (Eamb > arabic) & (Eamb > mandarin)
print(
	"Equivalent to reported distributive implicature:", 
	universe.equivalent(
		sentence, 
		prejacent & dist
	)
)
print()

# %%
"""
What if we allowed the "some" alternative to "all"? The reading is equivalent to the following conjuntive statement:  
*Every ambassador speaks Arabic, English and Mandarin.*
"""

sentence = Exh(prejacent, 
               scales = [{Existential, Universal}],
               ii     = True)
sentence.diagnose(display) 
# The reading is way too strong!
print(
	"All ambassador speak all languages:", 
	universe.equivalent(
		sentence, 
		Aamb > arabic & english & mandarin
	)
)


# %%
"""
<span id="dist_ii_conj"></span>
What if we allowed both "some/all" and "or/and"?
Here, we generated an embedded implicature that "every ambassador speaks only one of the three languages" and no distributive implicature.
Note that pruning alternatives here (if we follow Bar-Lev (2018)) since pruning in his system only makes statements weaker.
Since the fully exhuastified statement does not entail the dist. implicature, the pruned statement won't either.
"""

sentence = Exh(prejacent, 
               scales = [{Existential, Universal},  {Or, And}],
               ii     = True)
sentence.diagnose(display) 
# The reading has an embedded implicature
print(
	"Equivalent to an embedded implicature:", 
	universe.equivalent(
		sentence, 
		Aamb > (arabic & ~english & ~mandarin) | (~arabic & english & ~mandarin) | (~arabic & ~english & mandarin)
	)
)

print(
	"Has distributive implicature:", 
	universe.equivalent(
		sentence, 
		Eamb > arabic
	)
)



# %%
"""
<span id="dist_recursive"></span>
# Distributive implicatures with recursive exhaustification 
"""

prejacent  = Aamb > arabic | english | mandarin
universe = Universe(f = prejacent)
sentence   = Exh(Exh(prejacent))

print("Assumed LF:", sentence)

sentence.diagnose(display)

dist = (Eamb > english) & (Eamb > arabic) & (Eamb > mandarin)
print("Target Distributive Implicatures:", dist)
print(
	"Equivalent to conjunction of prejacent and dist implicature:", 
	universe.equivalent(
		sentence, 
		prejacent & dist
	)
)

# %%
"""
<span id="cumulative_every"></span>
# Cumulative reading of every 

This is exactly the same as above with disjunction replaced with sub-domain existentials
"""



prejacent  = Anut > Esquirrel > cracked
universe   = Universe(f = prejacent)
sentence   = Exh(Exh(prejacent))

print("Assumed LF:", sentence)

sentence.diagnose(display)
cumulative_reading = (Anut > Esquirrel > cracked) & (Asquirrel > Enut > cracked)
print("Cumulative reading:", cumulative_reading)
print(
	"Equivalent to cumulative reading:", 
	universe.equivalent(
		sentence, 
		cumulative_reading
	)
)

# %%
"""
<span id="cumulative_every_ii"></span>
# Cumulative reading of every: the innocent inclusion approach 
"""

prejacent  = Anut > Esquirrel > cracked
sentence   = Exh(prejacent, ii = True)
universe = Universe(f = prejacent)

print("Assumed LF:", sentence)

sentence.diagnose(display)
cumulative_reading = (Anut > Esquirrel > cracked) & (Asquirrel > Enut > cracked)
print("Cumulative reading:", cumulative_reading)
print(
	"Equivalent to cumulative reading:", 
	universe.equivalent(
		sentence, 
		cumulative_reading
	)
)
doubly_distributive = Asquirrel > Anut > cracked
print("Doubly distributive reading:", doubly_distributive)
print(
	"Equivalent to doubly-distributive reading: ", 
	universe.equivalent(sentence, doubly_distributive)
)

# %%
"""
<span id="cumulative_most"></span>
# Cumulative reading of most 
"""
prejacent  = M("nut") > Esquirrel > cracked
universe = Universe(f = prejacent)
lf = Exh(Exh(prejacent))


print("Assumed LF:", lf)

lf.diagnose(display)
print("Equivalent to cumulative reading:", universe.equivalent(lf, prejacent & (Asquirrel > Enut > cracked)))


# %%
"""
<span id="cumulative_most_impl"></span>
# Cumulative reading of most : with all alternative
"""
prejacent  = M("nut") > Esquirrel > cracked
universe = Universe(f = prejacent)
scales = ListScales([
	SimpleScales([{Existential, Most, Universal}]),
	sub_scale
])
lf = Exh(Exh(prejacent, scales = scales), scales = scales)


print("Assumed LF:", lf)

lf.diagnose(display)
cumul_impl = prejacent & (Asquirrel > Enut > cracked) & ~(Anut > Esquirrel > cracked)

print(
	"Equivalent to cumulative reading + implicature:", 
	universe.equivalent(
		lf, 
		cumul_impl
	)
)
print("Cumulative reading + implicature :=")
print(cumul_impl)


# %%
"""
<span id="schein"></span>
# Schein's video-game example
*The video-games taught every quarterback two new plays.*

Here, we will work on small domains to avoid blowing up the computer
"""

# Defining the quantifiers of the sentence
D2 = Domain(2)
Evideo       = Ec_("vg",  domain = D2) # An existential with sub-domain alternatives
Avideo       = A("vg",    domain = D2)
Aquarterback = A("qb",    domain = D2) # ... every quarterback ...
Equarterback = E("qb",    domain = D2)
two_plays    = M("play",  domain = D3) # using most which is equivalent to two on a domain of cardinality 3
Eplay        = E("play",  domain = D3) 
taught       = Pred(name = "taught", depends = ["vg", "qb", "play"], domains = [D2, D2, D3])

prejacent = Aquarterback > two_plays > (Evideo > taught) # Little problem with C constructor requires parenthesis to parse
print(prejacent)
lf = Exh(Exh(prejacent))
universe = Universe(f = lf)

lf.diagnose(display)

cumulative_reading = prejacent & (Avideo > Equarterback > (Eplay > taught))
print("Equivalent to cumulative reading:", universe.equivalent(lf, cumulative_reading))


# %%
"""
<span id="asymmetries"></span>
# Asymmetries in cumulative readings 
Non-cumulative reading of every.
"""
lf         = Exh(Exh(Anut > Exh(Exh(Esquirrel > cracked))))
universe = Universe(f = lf)
print("Assumed LF:", lf)



lf.diagnose(display)
cumulative_reading = 
print("Equivalent to cumulative reading:", universe.equivalent(lf, (Ax > a | b) & (Ex > a) & (Ex > b)))
print("Equivalent to doubly-dist reading:", universe.equivalent(lf, Ax > a & b))

# %%
"""
<span id="asymmetries"></span>
# Asymmetries in cumulative readings 
*Every nut appealed to the squirrels*

With 4 Exh, the computations get a bit slow. It takes 3-5s on my computer.
"""

scales     = [{Existential, Universal}] # our "disjunction", which models the existential with subdomain alternates, should not have a conjunctive alternative
lf         = Exh(Exh(Anut > Exh(Exh(Esquirrel > cracked))))
universe = Universe(f = lf)


print("Assumed LF:", lf)
lf.diagnose(display)

cumulative_reading = (Anut > Esquirrel > cracked) & (Asquirrel > Enut > cracked)
print("Equivalent to cumulative reading:", universe.equivalent(lf, cumulative_reading))
doubly_distributive = Asquirrel > Anut > cracked
print("Equivalent to doubly-dist reading:", universe.equivalent(lf, doubly_distributive))


# %%
"""
<span id="ordinary"></span>
# Ordinary cumulative sentences 
Ordinary cumulative sentences  
*The squirrels cracked the nuts*

**Caution:** The last two cells are the most computation-greedy cells of the notebook. Takes 5-10s to run to run on my (old) computer.

Here, to be faithful to what happens at the actual LF, we must first compute recursive strengthening on alternatives where the domain of the squirrels exsitential is fixed.
To do so, I manually generate alternatives for a sentence where Esquirrel is replaced with an existential without subdomain alternatives.
"""
from exh.alternatives import alt
Dsquirrel = Domain(3)
Dnut      = Domain(3)

Enut = Ec_("nut", domain = Dnut)   
Anut = A("nut",   domain = Dnut)   
Esquirrel = Ec_("squirrel", domain = Dsquirrel) 
Asquirrel = A("squirrel",   domain = Dsquirrel)   
cracked = Pred(name = "cracked", depends = ["squirrel", "nut"], domains = (Dsquirrel, Dnut))
universe = Universe(f = cracked)

alts_to_nut = alt(
	E("squirrel", domain = Dsquirrel) > Enut > cracked, 
	scales = sub_scale, 
	subst  = options_alts.sub
) 
first_strengthening =  Exh(Exh(Esquirrel > Enut > cracked, alts = alts_to_nut))
print("First strengthening", first_strengthening)
first_strengthening.diagnose(display)
print('Equivalent to "{}" :'.format(Anut > Esquirrel > cracked),
	universe.equivalent(first_strengthening, Anut > Esquirrel > cracked)
)
print("###############################")

# %%
"""
The second strengthening consider alternatives to Esquirrel quantifiers. We generate them manually as before.

"""

alts_to_squirrel = alt(
	# Enut > Esquirrel > cracked, 
	E("nut", domain = Dnut) > Esquirrel > cracked, 
	scales = sub_scale, 
	subst  = options_alts.sub
) 
second_strengthening = Exh(Exh(first_strengthening, extra_alts = alts_to_squirrel))

print("Second strengthening", first_strengthening)
second_strengthening.diagnose(display)
print("Equivalent to cumulative reading:",
	universe.equivalent(
		second_strengthening, 
		(Anut > Esquirrel > cracked) & (Asquirrel > Enut > cracked)
))


# %%