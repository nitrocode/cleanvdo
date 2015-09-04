#!/usr/bin/python
# Description:
# 	consolidate vdo files for readability and post processing
#
# Usage: 
#	./convdo.py long.vdo > short.vdo
# 
# goals:
# - turn each of the below goals into cmd line switches
# - "--keyonly" : consolidates keyup / keydown to just key for unprintable chars
# - "--typekeys" : consolidates keyup / keydowns for sequential ascii chars to one type statement
# - "--typekeysenter" : same as --typekeys except if an enter follows, then append " key enter" to "type" cmd
# - "--insertcap dir" : inserts a capture after each line and saves to dir/
# + "--roundpause 2" : roundsup the pause to the nearest hundredths
# + "--remove move click" : removes 'move' and 'click' commands
# + "--backspace" : removes the backspace commands and the previously typed character

import sys

# begin options

insertCap = False
insertCapDir = "dir"
stripcmds = ["keyup", "move", "click"]

# end options

filePath = sys.argv[ 1 ]
f = open(filePath, "r")

screen = 0
newLines = []

for line in f:
	printLine = False
	lineargs = line.rsplit()
	if line == "":
		continue

	# round pause
	if lineargs[ 0 ] == "pause":
		lineargs[ 1 ] = str( round( float( lineargs[ 1 ] ) + 0.05, 1 ) )

	# check for more than "pause number"
	if len( lineargs ) > 2:
		# strip out unnecessary commands
		if not lineargs[ 2 ] in stripcmds:

			# if key is bsp then remove the last ascii line
			if lineargs[ 3 ] == "bsp":
				#newLines.pop()
				num = len( newLines )
				if newLines[ -1 ][ 2 ] == "key":
					del newLines[-1]		
					continue
				else:
					print "Strange... bsp was detected but prev cmd was: " + newLines[ -1 ]

			# replace keydown with just key, since we removed keyup
			if lineargs[ 2 ] == "keydown":
				lineargs[ 2 ] = "key"

			printLine = True
	else:
		printLine = True

	if printLine:
		if insertCap:
			screen += 1
			newLines.append( ["capture", insertCapDir + "/screen" + str( screen ) + ".png" ] )
		newLines.append( lineargs )

for l in newLines:
	print " ".join(l)

f.close()
