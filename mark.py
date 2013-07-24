import os
import sys
import struct
import uuid
import optparse
import codecs
import signal
import re


from our_leader import our_leader

# need a list of wonders that we care about
wonders_to_watch = [
    "Great Library",
    "Temple of Artemis",
    "Stonehenge",
    "Pyramids",
    "Great Lighthouse",
    "Terracotta Army",
    "Hanging Gardens",
    "Colossus",
    "Petra",
    "Parthenon",
    "Chichen Itza",
    "Mausoleum of Halicarnassus",
    "Oracle",
    "Machu Picchu",
    "Hagia Sophia",
    "Statue of Zeus",
    "Alhambra",
    "Borobudur",
    "Great Wall",
    "Notre Dame",
    "Angkor Wat",
    "Great Mosque of Djenne",
    "Himeji Castle",
    "Leaning Tower of Pisa",
    "Globe Theatre",
    "Sistine Chapel",
    "Forbidden Palace",
    "Uffizi",
    "Porcelain Tower",
    "Red Fort",
    "Taj Mahal",
    "Louvre",
    "Eiffel Tower",
    "Broadway",
    "Brandenburg Gate",
    "Statue of Liberty",
    "Cristo Redentor",
    "CN Tower",
    "Sydney Opera House",
    "Great Firewall",
    "Hubble Space Telescope",
]




# benchmark off a game file

# we can get
# city foundings
# religion pantheon + founding (but not enhanced)
# war and peace
# wonders


# block_size means it'll always be this many rows (for easier copy pasting!)
def match_events(replay, regex, event, iterate=False, block_size=6, highlight=False, extra_note=False):
    p = re.compile(regex)
    m = p.findall(replay)

    i = -1
    for i, e in enumerate(m):
        if iterate==True and i == block_size:
            return
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
    match_events(replay, "(\d*)\t0\t(.*) is founded.", "Founded City", block_size=10, iterate=True)

    # religious pantheon (for us)
    # for us
    match_events(replay, "(\d*)\t(\d*)\t(.*)has started worshipping a pantheon of gods.",
                 "Founded Pantheon", iterate=True, block_size=8, highlight=True)

    # founded religion
    match_events(replay, "(\d*)\t(\d)*\t(.*)has founded the new religion",
                 "Founded Religion", iterate=True, block_size=5, highlight=True)
    
    # war and peace (on us)


    # wonders (maybe use negative numbers if we didn't get it?)    
    for w in wonders_to_watch:
        match_events(replay, "(\d*)\t(\d*)\t(.*) completes "+w+"!",
                     w, iterate=False, block_size=1, highlight=True)
    
    # offensive wars
    match_events(replay, "(\d*)\t0\t.* declares war on (.*)!",
                 "War of Aggression", iterate=True, block_size=3, extra_note=True)

    # defensive wars
    match_events(replay, "(\d*)\t(\d*)\t(.*) declares war on " + our_leader + "!",
                 "Defensive Wars", iterate=True, block_size=3, highlight=True)

    # we make peace
    match_events(replay, "(\d*)\t0\t.* has made peace with (.*)!",
                 "We Make Peace", iterate=True, block_size=3)
                
    # they make peace
    match_events(replay, "(\d*)\t(\d*)\t(.*) has made peace with " + our_leader + "!",
                 "They Make Peace", iterate=True, block_size=3, highlight=True)

    # victory type
    match_events(replay, "(\d*)\t(\d*)\t.* has won a (.*) Victory!!!",
                 "Victory Type", iterate=False, block_size=1, highlight=True)

    # time spent
    match_events(replay, "(\d*)\t(\d*)\tTime spent: (.*)",
                 "Time spent", iterate=False, block_size=1, highlight=True)
                 


    # can pull various stats out of our histogram as well
    # (e.g. number of techs, social policy, sci/turn)

    # probably export all histograms to "game-x-all-histograms.csv"
    # and just the ones we care about to "game-x-focus.csv" (or tsv?)
    # e.g. science at turn X, turns to social policy #Z
    # turns to # of techs... whatever else is in the histograms

    # victory type goes here too

    # need to change this aspect to be horizontal instead of vertical
    


