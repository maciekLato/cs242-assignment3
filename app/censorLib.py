from string import replace
swearWords = ["fuck", "bitch", "asshole", "shit", "cunt", "dick", "bastard", "motherfucker", "fucker", "fucking", "motherfucking", "pussy", "ass"]

#takes a string myString and returns a censored string
def censor(myString):
	for word in myString.split(" "):
		if word in swearWords:
			myString = replace(myString, word, word[0] +"*" * (len(word)-1))
	return myString