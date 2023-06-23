#!python

from playsound import playsound
from time import sleep
import gtts
import pyttsx3
import os
from random import randint
from sys import argv

welcome = "\nSpellings Reader\n----------------"

def readSpellings():
	directory = os.getcwd() + "\\" # Place dictionary text files within the same directory as the script
	spellingsFilename = argv[1] # grab the name of the dictionary file
	iterations = 10 # The number of spellings to read out. 
	engine = pyttsx3.init() # Initialise a speech synthesis engine
	numbers = []
	count = 1
	delayBetweenWords = 10
	if len(argv) == 3:
		try:
			delayBetweenWords = int(argv[2])
		except:
			print("[e] Cannot convert \"" + argv[2] + "\" into a number to use for a delay. Assuming default delay of 10 seconds.")
			delayBetweenWords = 10

	print("[i] Reading from \"" + spellingsFilename + "\".")
	print("[i] There will be a " + str(delayBetweenWords) + " second delay between words.\n")

	try:
		with(open(directory + spellingsFilename, "r") as file):
			dictionary = file.readlines()
	except FileNotFoundError:
		print("[e] File \"" + spellingsFilename + "\" not found in " + directory + ".")
		usage()

	while count <= iterations:
		try:
			number = randint(0,len(dictionary)-1)
			if number not in numbers:
				numbers.append(number)
				spelling = dictionary[number].rstrip()
				speechString = "Spelling " + str(count) + ": " + spelling.capitalize()
				print(speechString)
				engine.say(speechString)
				engine.runAndWait()
				filename = directory + spelling + ".mp3"
				tts = gtts.gTTS(speechString)
				tts.save(filename)
				playsound(filename)
				if os.path.exists(filename):
					os.remove(filename)
				sleep(delayBetweenWords)
				count = count + 1
		except KeyboardInterrupt:
			print("[e] Interrupted - Ctrl-c")
			if os.path.exists(filename):
				os.remove(filename)
			exit(1)

def usage():
	print("Usage: Run this program with the following syntax:\n\n\tpython " + argv[0] + " <spellings dictionary filename> <delay between spellings (s)>\n")
	exit(1)

if __name__ == '__main__':
	print(welcome)
	if len(argv) < 2 or len(argv) > 3:
		usage()
	readSpellings()
