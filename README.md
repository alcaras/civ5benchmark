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

* Successfully parses the map, but doesn't do anything with them.

## Todo?

* Perhaps generate a "summary log" that's suitable for pasting on
  forums (using BBCode?) to summarize a game? Could be handy for
  succession games or after action reports. (This would go turn by
  turn)
* Fix the bug with histogram data where the save file shows max_turn
  instead of a -1. Just make it show -1 where it's max_turn.
* Ignore city-states in wars of aggression/defensive wars. Easily done
  -- just make it so if the civ idea is greater than the number of
  non-city-state civs, ignore and go to the next match.






