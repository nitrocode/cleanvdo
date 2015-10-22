#!/usr/bin/python
# Description:
# 	consolidate vdo files for readability and post processing
#
# Usage: 
#	./convdo.py long.vdo > short.vdo

from __future__ import print_function
import argparse
import sys
import os

# setup arguments
parser = argparse.ArgumentParser(description='Consolidate vdo files for readability',
                                 prefix_chars='-+/')
#parser.add_argument('--', help='')
parser.add_argument('input', nargs='?', default=sys.stdin,
                    help='File to convert')
#parser.add_argument('--input', '-i', metavar='input file', type=argparse.FileType('rt'), 
#		    dest='input',
#                    help='File to convert')
parser.add_argument('--keyonly', '-k', action="store_true", default=False, 
		    dest='keyonly',
                    help='consolidates keyup / keydown to just key for unprintable chars')
parser.add_argument('--typekeys', '-t', action="store_true", default=False,
                    dest='typekeys',
                    help='consolidates keyup / keydowns for sequential ascii chars to one type statement')
parser.add_argument('--typekeysenter', '-e', action="store_true", default=False,
                    dest='typekeysenter',
                    help='same as --typekeys except if an enter follows, then append " key enter" to "type" cmd')
parser.add_argument('--insertcap', '-c', action="store", default=False,
                    dest='insertcap',
                    help='inserts a capture after each line and saves to dir')
parser.add_argument('--roundpause', '-R', action="store", default=2, type=int,
                    dest='roundpause',
                    help='roundsup the pause to the nearest hundredths')
#parser.add_argument('--remove', action="const_collection", default=['move','click'],
parser.add_argument('--remove', '-r', action="append", default=['move','click','keyup','rshift','lshift'],
                    dest='remove',
                    help='removes move and click commands')
parser.add_argument('--backspace', '-b', action="store_true", default=False, 
                    dest='backspace',
                    help='removes the backspace commands and the previously typed character')
parser.add_argument('--version', '-v', action="version", version='')

# printe will print only to stderr so print statements do not show in the clean vdo file
def printe( str ):
	print( str, file=sys.stderr )

try:
	results = parser.parse_args()
	printe( results )
except:
	#parser.error( str(msg) )
	sys.exit( 0 )

# if ~ is used then convert it to the home directory
inputFile = results.input
if "~" in inputFile:
	inputFile = inputFile.replace( "~", os.path.expanduser("~") )

insertCapDir = "dir"

#filePath = sys.argv[ 1 ]
filePath = inputFile
f = open(filePath, "r")

screen = 0
newLines = []
totalLines = 0
for line in f:
	totalLines += 1

	printLine = False
	lineargs = line.rsplit()
	if line == "":
		continue

	printe( lineargs )

	# round pause
	if lineargs[ 0 ] == "pause":
		lineargs[ 1 ] = str( round( float( lineargs[ 1 ] ) + 0.05, 1 ) )

	# check for more than "pause number"
	if len( lineargs ) > 2:
		# strip out unnecessary commands
		if not lineargs[ 2 ] in results.remove and not lineargs[ 3 ] in results.remove:
			# if key is bsp then remove the last ascii line
			if results.backspace and lineargs[ 3 ] == "bsp":
				#newLines.pop()
				#print lineargs
				#print newLines[ -1 ]
				if newLines[ -1 ][ 2 ] == "key":
					del newLines[ -1 ]		
					continue
				else:
					printe( "Strange... bsp was detected but prev cmd was: " + newLines[ -1 ] )
			# replace keydown with just key, since we removed keyup
			if lineargs[ 2 ] == "keydown":
				lineargs[ 2 ] = "key"
			# check if key is enter
			# if so:
			#	iterate backwards in newlines and grab all the pauses and alphanumerics
			#	remove all those lines from newLines
			#	newLine=sum all the pauses and concatenate all the characters and append with enter
			#	add that new line
			if results.typekeys and lineargs[ 3 ] == "enter":
				tmpstr = ""
				pausetime = 0
				pop = 0
				for l in reversed( newLines ):
					if len( l ) > 2:
						#printe( l )
						if l[ 3 ] == "enter":
							tmpstr += " key enter"
							#print( "found" )
							break
						pop += 1
						pausetime += float( l[ 1 ] )
						tmpstr = l[ 3 ] + tmpstr
				for i in range(0, pop):
					newLines.pop()
				newLines.append( ['pause', str(pausetime), 'type', tmpstr] )
				#lineargs = ['pause', str(pausetime), 'type', tmpstr]
				#print( "pause " + str( pausetime ) + " type " + tmpstr )
				#print( pausetime )

			printLine = True
	else:
		printLine = True

	if printLine:
		if results.insertcap:
			screen += 1
			newLines.append( ["capture", insertCapDir + "/screen" + str( screen ) + ".png" ] )
		newLines.append( lineargs )

for l in newLines:
	print( " ".join( l ) )

totalNewLines = len( newLines )

printe( "Original total lines: " + str( totalLines ) )
printe( "New total lines: " + str( totalNewLines ) )
printe( "Decreased lines by: " + str( totalLines - totalNewLines ) )

f.close()
