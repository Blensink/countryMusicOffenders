import MySQLdb

def getConnection( host, user, password, dbName ):
	"""Get our connection to the database and return it."""
	try:
		con = MySQLdb.connect( host, user, password, dbName, 
			unix_socket='/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock')
		cursor = con.cursor()

	except _mysql.Error, e:
		print e.args[0], e.args[1]

	return cursor

def writeArtist( con, artist ):
	"""Write our artist name to the database and return their id."""
	con.execute( "INSERT INTO artist(name) VALUES(\'" + artist + "\')" )

	return int(con.lastrowid)

def writeAlbum( con, album ):
	"""Write our album name into the database and return the id."""
	con.execute( "INSERT INTO album(name) VALUES(\'" + album + "\')" )

	return int(con.lastrowid)

def writeWord( con, word ):
	"""Write our word into the database and return the id."""
	con.execute( "INSERT INTO word(name) VALUES(\'" + word + "\')" )

	return int(con.lastrowid)

def writeLyrics( con, artistId, albumId, wordId, count ):
	"""Write a lyric to the database with all the info we've collected."""
	stmt = "INSERT INTO lyrics(artistId, albumId, wordId, count)" \
		" VALUES(\'" + str(artistId) + "\', \'" + str(albumId) + "\', \'" +\
			str(wordId) + "\', \'" + str(count) + "\')"

	con.execute(stmt)

	return int(con.lastrowid)

def checkIfArtistExists( con, artist ):
	return checkIfExists( con, "artist", artist )

def checkIfAlbumExists( con, album ):
	return checkIfExists( con, "album", album )

def checkifWordExists( con, word ):
	return checkIfExists( con, "word", word )

def checkIfExists( con, key, value ):
	""" Check if a given word/artist/album already exists in the database."""
	stmt = "SELECT id FROM " + key + " WHERE name = \'" + value + "\'"

	return con.execute( stmt )
