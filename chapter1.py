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
print("Assumed sentence:", sentence)
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
# Cumulative reading of every/distributive implicatures : non-recursive exhaustification
*Every ambassador speaks Arabic, French or Mandarin*  
*The three squirrels cracked every nut*

Note how we perform the exhaustification, ignoring that "every" has "some" as an alternative. As pointed out by Chemla & Spector (2011), the "some" alternative block the distributive implicature, a testament to the inadequacy of the standard derivation.
"""



prejacent  = Aamb > arabic | english | mandarin
universe   = Universe(f = prejacent)
sentence   = Exh(prejacent, scales = []) # we must ignore the "some/all" scales. As p

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
<span id="schein"></span>
*The video-games taught every quarterback two new plays.*

Here, we will work on small domains to avoid blowing up the computer
"""

D2 = Domain(2)
Evideo       = Ec_("vg",  domain = D2)
Avideo       = A("vg",    domain = D2)
Aquarterback = A("qb",    domain = D2)
Equarterback = E("qb",    domain = D2)
two_plays    = M("play",  domain = D3) # using most which is equivalent to two on that domain
Eplay        = E("play",  domain = D3) # using most which is equivalent to two on that domain
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
<span id="ordinary"></span>
# Ordinary cumulative sentences 
Ordinary cumulative sentences  
*The squirrels cracked the nuts*

**Caution:** This is by far the most computation-greedy cells of the notebook. Takes 30s to 1min to run on my (old) computer.
"""

# We need to redefine the quantifier 
Enut = Ec_("nut", domain = D3)   
Anut = A("nut",   domain = D3)   
Esquirrel = Ec_("squirrel", domain = D3) 
Asquirrel = A("squirrel",   domain = D3)   
cracked = Pred(name = "cracked", depends = ["squirrel", "nut"], domains = (D3, D3))
lf      = Exh(Exh(Exh(Exh(Enut > Esquirrel > cracked))))
universe = Universe(f = lf)



print("Assumed LF:", lf)
lf.diagnose(display)

cumulative_reading = (Anut > Esquirrel > cracked) & (Asquirrel > Enut > cracked)
print("Equivalent to cumulative reading:", universe.equivalent(lf, cumulative_reading))
doubly_distributive = Asquirrel > Anut > cracked
print("Equivalent to doubly-dist reading:", universe.equivalent(lf, doubly_distributive))

# %%
"""
Does it not work? Well, notice how none of the alterantives considered by *Exh* have any of the *Exh* stripped away.
The package implements this behavior by default. If we allow the prejacent of Exh to be an alternative to Exh, the account of Free choice is lost!
"""

options_alts.prejacent_alternative_to_exh = True
free_choice = Exh(Exh(a | b))
universe = Universe(f = free_choice)
options_alts.prejacent_alternative_to_exh = False

free_choice.diagnose(display)
print("No strengthening:", universe.equivalent(free_choice, a | b))

# %%
"""
Is that an issue? Maybe we need to consider recursive *Exh* (i.e. *Exh Exh*) as a unit. As a unit, *Exh Exh* does not have *Exh* as an alternative, but it does have its prejacent as an alternative.
"""

Enut = Ec_("nut", domain = D3)   
Anut = A("nut",   domain = D3)   
Esquirrel = Ec_("squirrel", domain = D3) 
Asquirrel = A("squirrel",   domain = D3)   
cracked = Pred(name = "cracked", depends = ["squirrel", "nut"], domains = (D3, D3))
lf      = Exh(Exh(
	Enut > Exh(Exh(Esquirrel > cracked)),
	extra_alts = Exh(Enut > Esquirrel > cracked).alts
))
universe = Universe(f = lf)



print("Assumed LF:", lf)
lf.diagnose(display)

cumulative_reading = (Anut > Esquirrel > cracked) & (Asquirrel > Enut > cracked)
print("Equivalent to cumulative reading:", universe.equivalent(lf, cumulative_reading))
doubly_distributive = Asquirrel > Anut > cracked
print("Equivalent to doubly-dist reading:", universe.equivalent(lf, doubly_distributive))


# print("Equivalent to doubly-dist reading:", universe.equivalent(lf, Ax > a & b))


# %%