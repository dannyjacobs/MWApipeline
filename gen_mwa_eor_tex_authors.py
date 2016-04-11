#! /usr/bin/env python
import sys




#open the raw author list
lines = open('mwa_eor_collab_raw_list.txt').readlines()
affiliations = {}
hasitprintedyet = {}
names = []
inauthors = False
for line in lines:
    if line.startswith("\\"):
        affilname = line.split('{')[0]
        affiltext = line.split('{')[1][:-2]
        affiliations[affilname] = affiltext
        hasitprintedyet[affilname] = False
        #make a dict of affiliation text indexed with the affiliation variable name
for line in lines:
    if len(line)>0 and not line.startswith('#') and not line.startswith('\\'):
        names += [[line.strip(),[]]] #author line, name of affiliation
        for affilname in affiliations: #scan for affiliations!
            if affilname in line:
                names[-1][1].append(affilname)

"""
\def\Dunlap{\altaffilmark{23}}
\def\Dunlaptxt{\altaffiltext{23}{Dunlap Institute for Astronomy and Astrophysics, University of Toronto, ON M5S 3H4, Canada}}
"""
#output
outfile = open('mwa_eor_collab.tex','w')
print "writing mwa_eor_collab.tex"
count = 1
for name in names:
    for affil in name[1]:
        if not hasitprintedyet[affil]:
            outfile.write("\\def{affil}{{\\altaffilmark{{{count}}}}}\n".format(affil=affil,count=count))
            outfile.write("\\def{affil}txt{{\\altaffiltext{{{count}}}{{{txt}}}}}\n".format(
                                    count=count,
                                    affil=affil,
                                    txt=affiliations[affil]))
            outfile.write('\n')
            hasitprintedyet[affil] = True
            count += 1
#print the authors
outfile.write("\\author{\n")
for name in names:
    outfile.write(name[0]+'\n')
outfile.write("}\n")

#print the affiltexts
count = 1
for k in hasitprintedyet:
    hasitprintedyet[k] =False
for name in names:
    for affil in name[1]:
        if not hasitprintedyet[affil]:
            outfile.write("{affil}txt".format(affil=affil)+'\n')
            hasitprintedyet[affil] = True
            count += 1

