# civ 5 replay parser (for brave new world)

## Goal

Made this for personal use -- not focused on creating pretty
HTML map animations because that is now in-game. 

Goal is to export the Notification Log so it can be parsed and then
used to easily benchmark games.

Feel free to play with this and expand it to your liking.

## Credit

Over at civfanatics' forum, dannythefool's original civ5replay.py and
[associated forum
thread](http://forums.civfanatics.com/showthread.php?t=388160) was
helpful in reverse-engineering how the new BNW file format
works. There have been some changes from Vanilla, but some other
things have stayed the same, and having a guidepost of how things once
used, and code to parse them back then, was an immense help.

## Overview

There are two python scripts:

* bench.py, which parses a replay file
* mark.py, which takes the output from
  bench.py and converts it into handy tab separated benchmarks,
  suitable for opening in excel (to track progress across multiple
  games)

There is also a bash shell script:

* build, which runs bench.py on a replay file and then mark.py on a
  replay file. You may need to chmod +x this to run it. I use Mac OS X
  or cygwin, so there's no DOS batch file. Feel free to submit a pull
  request with one, though!

## Use

 Copy the Civ5Replay file from /My Games/Sid Meier's Civilization
 5/Replays into the folder for this replay parse. 

 Then run build on the replay, ignoring the file extension. You'll
 need to put quotes around the name if it has spaces. Or just rename
 it something shorter and less annoying. For example:

    ./build "Casimir III_0238 AD-1936_39"

 Or, after a rename:

    ./build game-3

## Results

You can find the raw text of the parse in <filename>.txt and the tab
separated benchmarks in <filename>.tsv. My convention in the
benchmarks is I use a negative turn number for wonders the AI gets.

## Known Bugs and Limitations

* So far it only looks at the notification log.

* Successfully parses the histograms and map, but doesn't do anything
  with them.

## Todo?

* Prettify





