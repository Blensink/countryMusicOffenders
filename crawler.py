from lxml import html
import localConfig as config
import requests
import string
import unicodedata
import db

user = config.user()
password = config.password()
dbName = config.db()
host = config.host()

def getLyricsFromPage(songUrl, wordDictionary):
	#"This is the function to get they lyrics of a song on a given page."
	page = requests.get(songUrl)
	tree = html.fromstring(page.text)

	lyricsTree = tree.xpath('//p[@id="songLyricsDiv"]/text()')

	for item in lyricsTree:
		line = item.split(" ")

		for word in line:
			try:
				word = word.translate(None, '\'!,@#$\r\n\t()').lower()
			except Exception, e: 
				#This will trigger if the word is encoded in unicode 
				#instead of string for whatever reason
				word = unicodedata.normalize('NFKD', word).encode('ascii',
																 'ignore')
				word.translate(None, '\'!,@#$\r\n\t()').lower()	

			if wordDictionary.has_key(word):
				wordDictionary[word] = wordDictionary[word] + 1
			else:
				wordDictionary[word] = 1

			#print word, wordDictionary[word]
	return wordDictionary	

def getSongsFromAlbum( albumUrl ):
	"""Given an album page, collect the link to each song on the album."""
	page = requests.get( albumUrl )
	tree = html.fromstring( page.text )	

	albumTree = tree.xpath('//div[@id="colone-container"]/.//table' \
		'[@class="tracklist"]/.//a/@href')

	return albumTree

def getAlbumsFromArtist( artistUrl ):
	"""Given an artist url, collect the url for all albums."""
	page = requests.get( artistUrl )
	tree = html.fromstring( page.text )

	albumTree = tree.xpath('//div[@id="colone-container"]/.//div' \
		'[@class="listbox-album"]/.//h3/a/@href')

	return albumTree

def writeResults( ):
	"""Write the results of our web crawling to our database."""
	con = db.getConnection( host, user, password, dbName )

	print db.checkIfArtistExists( con, "testAratiast")
	

def saveResultsToFile( table ):
	"""Save the crawler results to a temp file so we can read it later"""
	f = open('tempFile.txt', 'w+')

	for key, values in wordDictionary.iteritems():
		f.write( key + " " + str(values) + "\n")

	f.close()

	return ""

def readTestFile():
	"""Read the test file that we wrote out from crawling"""
	dict = {}

	f = open("tempFile.txt") 

	lines = [line.rstrip('\n') for line in f]

	for item in lines:
		stuff = item.split( " " )

		if( len(stuff) == 2 ):
			dict[stuff[0]] = stuff[1]

	return dict

#print str(wordDictionary)
wordDictionary = {}
artistUrl = "http://www.songlyrics.com/zac-brown-band-lyrics/"
albumUrl = "http://www.songlyrics.com/zac-brown-band/jekyll-hyde/"
songUrl = "http://www.songlyrics.com/zac-brown-band/bittersweet-lyrics/"

wordDictionary = readTestFile()
writeResults()
#albumList = getAlbumsFromArtist( artistUrl )
#print albumList

#songList = getSongsFromAlbum( albumUrl )
#print songList

#for links in songList:
#	wordDictionary = getLyricsFromPage( links, wordDictionary )

#print wordDictionary

