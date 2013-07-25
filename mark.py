import os
import sys
import struct
import uuid
import optparse
import codecs
import signal
import re


def aseq(n, a, b=0):
    if b == 0:
        b = a
    r = []
    for i in range(n):
        r.append(a)
        c = a
        a = a + b
        b = c
    return r

from our_leader import our_leader
from our_civ import our_civ
from histograms import histograms

# in approximate that they are built
wonders_to_watch = [
    "Great Library",
    "Temple of Artemis",
    "Stonehenge",
    "Parthenon",
    "Great Lighthouse",
    "Terracotta Army",
    "Hanging Gardens",
    "Petra",
    "Colossus",
    "Pyramids",
    "Mausoleum of Halicarnassus",
    "Statue of Zeus",
    "Chichen Itza",
    "Great Wall",
    "Oracle",
    "Machu Picchu",
    "Hagia Sophia",
    "Alhambra",
    "Borobudur",
    "Great Mosque of Djenne",
    "Notre Dame",
    "Angkor Wat",
    "Himeji Castle",
    "Globe Theatre",
    "Forbidden Palace",
    "Leaning Tower of Pisa",
    "Sistine Chapel",
    "Taj Mahal",
    "Uffizi",
    "Red Fort",
    "Porcelain Tower",
    "Louvre",
    "Brandenburg Gate",
    "Broadway",
    "Eiffel Tower",
    "Big Ben",
    "Statue of Liberty",
    "Cristo Redentor",
    "Kremlin",
    "Manhattan Project",
    "Sydney Opera House",
    "Great Firewall",
    "CN Tower",
    "Hubble Space Telescope",
    "Apollo Program",
    "Pentagon",
    "SS Engine",
    "SS Stasis Chamber",
    "SS Cockpit",
    "SS Booster",
]




# benchmark off a game file

# we can get
# city foundings
# religion pantheon + founding (but not enhanced)
# war and peace
# wonders


histogram_labels = {
    0: u'score',
    1: u'productionperturn',
    2: u'totalgold',
    3: u'goldperturn',
    4: u'citycount',
    5: u'techsknown',
    6: u'scienceperturn',
    7: u'totalculture',
    8: u'cultureperturn',
    9: u'excesshapiness',
    10: u'happiness',
    11: u'unhappiness',
    12: u'goldenageturns',
    13: u'population',
    14: u'foodperturn',
    15: u'totalland',
    16: u'gptcityconnections',
    17: u'gptinternationaltrade',
    18: u'gptdeals',
    19: u'unitmaintenance',
    20: u'buildingmaintenance',
    21: u'improvementmaintenance',
    22: u'numberofpolicies',
    23: u'numberofworkers',
    24: u'improvedtiles',
    25: u'workedtiles',
    26: u'militarymight',
}

histogram_lookup = { }

for k, v in histogram_labels.iteritems():
    histogram_lookup[v] = k
                     

def meta_info(replay, regex, label):
    p = re.compile(regex)
    m = p.findall(replay)
    print label + "\t" + m[0]
    


# return the turn at which threshold was first met
# hs = which histogram (use the name)
# t = threshold
# c = which civ (default to us)
def hist_threshold(hs, t, c=0):
    h = histogram_lookup[hs]
    for k, v in histograms[c][h].iteritems():
        if v >= t:
            return k
    return -1

def hist_events(label, hist, thresholds, c=0):
    for t in thresholds:
        print label, t, "\t", hist_threshold(hist, t, c)

def hist_when(label, hist, turns, c=0):
    h = histogram_lookup[hist]
    for t in turns:
        print label, t, "\t",
        if t in histograms[c][h]:
             print histograms[c][h][t]
        else:
            print



# block_size means it'll always be this many rows (for easier copy pasting!)
def match_events(replay, regex, event, iterate=False, block_size=6, highlight=False, extra_note=False, nln=False):
    p = re.compile(regex)
    m = p.findall(replay)

    i = -1
    for i, e in enumerate(m):
        if iterate==True and i == block_size:
            return
        elif i == block_size:
            break
        display = event
        if iterate == True:
            display += " " + str(i+1)
        display +=  "\t"
        
        if highlight == False:
            display += e[0] + "\t" # turn count
            display += e[1] # note
        else: # with highlight on we have Turn, Team, Note
            if int(e[1]) != 0: # e[1] is now player
                display += str(-int(e[0]))
            else:
                display += e[0]
            display += "\t" + e[2] # e[2] is now note

        print display

    if nln:
        print event, "\t", e[2]

    for j in range(i+1, block_size):
        display = event
        if iterate==True:
            display += " " + str(j+1)
        display += "\t \t \t"
        print display



if __name__ == "__main__":
    # set up some command line options
    op = optparse.OptionParser()
    (options, args) = op.parse_args()

    if len(args) == 0:
        print "mark.py <replay-text>"
        sys.exit(1)


    fn = args[0]
    r = file(fn, "r")
    replay = r.read()

    print "What\tWhen\tNotes"

    # city foundings
#    match_events(replay, "(\d*)\t0\t(.*) is founded.", "Founded City", block_size=10, iterate=True)

  
    meta_info(replay, "@@@ civ .*_(.*)", "Civilization")

    meta_info(replay, "@@@ diff .*_(.*)", "Difficulty")

    meta_info(replay, "@@@ speed .*_(.*)", "Speed")

    meta_info(replay, "@@@ size .*_(.*)", "Size")

    meta_info(replay, "@@@ map (.*)", "Map")
    

    # religious pantheon (for us)
    # for us
    match_events(replay, "(\d*)\t(\d*)\t(.*) .* started worshipping a pantheon of gods",
                 "Founded Pantheon", iterate=True, block_size=8, highlight=True)

    # founded religion
    match_events(replay, "(\d*)\t(\d*)\t(.*) .* founded the new",
                 "Founded Religion", iterate=True, block_size=5, highlight=True)
    
    # war and peace (on us)

    # research agreement
    match_events(replay, "(\d*)\t(\d*)\t(.*) and .*" + our_civ + " have signed a Research Agreement",
                 "RA Signed", iterate=True, block_size=15, highlight=True)
    
    # war and peace (on us)


    # wonders (maybe use negative numbers if we didn't get it?)    
    for w in wonders_to_watch:
        match_events(replay, "(\d*)\t(\d*)\t(.*) completes "+w+"!",
                     w, iterate=False, block_size=1, highlight=True)
        
    
    # city count (better, as takes into account conquest + razing)
    hist_events("Cities >= ", "citycount", range(1, 11))
    hist_events("Workers >=", "numberofworkers", range(1, 7))        
    hist_when("Score @ Turn", "score", range(30, 211, 30))
    hist_when("Food @ Turn", "foodperturn", range(30, 211, 30))
    hist_when("Production @ Turn", "productionperturn", range(30, 211, 30))
    hist_when("Gold @ Turn", "goldperturn", range(30, 211, 30))
    hist_when("Techs @ Turn", "techsknown", range(30, 211, 30))
    hist_when("Science @ Turn", "scienceperturn", range(30, 211, 30))
    hist_when("Culture @ Turn", "cultureperturn", range(30, 211, 30))
    hist_when("Policies @ Turn", "numberofpolicies", range(30, 211, 30))

    hist_when("Worked Tiles @ Turn", "workedtiles", range(30, 211, 30))
#    hist_events("Total Land @ Turn", "workedtiles", aseq(8, 2))
    hist_when("Military @ Turn", "militarymight", range(30, 211, 30))


    # offensive wars
    match_events(replay, "(\d*)\t0\t.* declares war on (.*)!",
                 "War of Aggression", iterate=True, block_size=5, extra_note=True)

    # defensive wars
    match_events(replay, "(\d*)\t(\d*)\t(.*) declares war on " + our_leader + "!",
                 "Defensive Wars", iterate=True, block_size=5, highlight=True)

    # we make peace (I think this only triggers for city states)
#    match_events(replay, "(\d*)\t0\t.* has made peace with (.*)!",
#                 "We Make Peace", iterate=True, block_size=5)
                
    # they make peace
    match_events(replay, "(\d*)\t(\d*)\t(.*) has made peace with " + our_leader + "!",
                 "They Make Peace", iterate=True, block_size=5, highlight=True)

    # victory type
    match_events(replay, "(\d*)\t(\d*)\t.* has won a (.*) Victory!!!",
                 "Victory Type", iterate=False, block_size=1, highlight=True,
                 nln=True)

    # time spent
    match_events(replay, "(\d*)\t(\d*)\tTime spent: (.*)",
                 "Time spent", iterate=False, block_size=1, highlight=True,
                 nln=True)
                 


    # can pull various stats out of our histogram as well
    # (e.g. number of techs, social policy, sci/turn)

    # probably export all histograms to "game-x-all-histograms.csv"
    # and just the ones we care about to "game-x-focus.csv" (or tsv?)
    # e.g. science at turn X, turns to social policy #Z
    # turns to # of techs... whatever else is in the histograms
    


