def get_value(keystring, dictionary):
	amountkeys = keystring.count('.')+1
	lastfoundindex = 0
	counter = 0

	while counter < amountkeys:
	        if counter == 0:
	                value = dictionary[keystring[lastfoundindex:keystring.find(
	                	'.')]]

	        elif counter == amountkeys - 1:
	                value = value[keystring[lastfoundindex:]]
	                break
	        else:
	                value = value[keystring[lastfoundindex:keystring.find(
	                	'.', lastfoundindex)]]

	        lastfoundindex = keystring.find('.', lastfoundindex)+1
	        counter += 1

	return value


def set_value(keystring, dictionary, new_value):
	amountkeys = keystring.count('.')+1
	lastfoundindex = 0
	counter = 0

	while counter < amountkeys:
	        if counter == 0:
	                value = dictionary[keystring[lastfoundindex:keystring.find(
	                	'.')]]

	        elif counter == amountkeys - 1:
	                value[keystring[lastfoundindex:]] = new_value
	                break
	        else:
	                value = value[keystring[lastfoundindex:keystring.find(
	                	'.', lastfoundindex)]]

	        lastfoundindex = keystring.find('.', lastfoundindex)+1
	        counter += 1

	value = new_value
	return value


def del_entry(keystring, dictionary):
	amountkeys = keystring.count('.')+1
	lastfoundindex = 0
	counter = 0

	while counter < amountkeys:
	        if counter == 0:
	                value = dictionary[keystring[lastfoundindex:keystring.find(
	                	'.')]]

	        elif counter == amountkeys - 1:
	                del value[keystring[lastfoundindex:]]
	                break
	        else:
	                value = value[keystring[lastfoundindex:keystring.find(
	                	'.', lastfoundindex)]]

	        lastfoundindex = keystring.find('.', lastfoundindex)+1
	        counter += 1


def add_entry(keystring, dictionary, entry_name, entry_value=None):
	amountkeys = keystring.count('.')+1
	lastfoundindex = 0
	counter = 0

	while counter < amountkeys:
	        if counter == 0:
	                value = dictionary[keystring[lastfoundindex:keystring.find(
	                	'.')]]

	        elif counter == amountkeys - 1:
	                value[keystring[lastfoundindex:]][entry_name] = entry_value
	                break
	        else:
	                value = value[keystring[lastfoundindex:keystring.find(
	                	'.', lastfoundindex)]]

	        lastfoundindex = keystring.find('.', lastfoundindex)+1
	        counter += 1
