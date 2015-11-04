from lxml import html
import pymongo as mdb
import requests
import string
import unicodedata

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

	albumTree = tree.xpath('//div[@id="colone-container"]/.//table', \
		'[@class="tracklist"]/.//a/@href')

	return albumTree

def getAlbumsFromArtist( artistUrl ):
	"""Given an artist url, collect the url for all albums."""
	page = requests.get( artistUrl )
	tree = html.fromstring( page.text )

	albumTree = tree.xpath('//div[@id="colone-container"]/.//div', \
		'[@class="listbox-album"]/.//h3/a/@href')

	return albumTree

#print str(wordDictionary)
wordDictionary = {}
artistUrl = "http://www.songlyrics.com/zac-brown-band-lyrics/"
albumUrl = "http://www.songlyrics.com/zac-brown-band/jekyll-hyde/"
songUrl = "http://www.songlyrics.com/zac-brown-band/bittersweet-lyrics/"

#albumList = getAlbumsFromArtist( artistUrl )
#songList = getSongsFromAlbum( albumUrl )

#for links in albumTree:
#	wordDictionary = getLyricsFromPage( links, wordDictionary )

#print wordDictionary

#for item in getAlbumsFromArtist():
#	print item, "\n"
