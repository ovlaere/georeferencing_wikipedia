#!/usr/bin/python
import re
import locale
import sys
import codecs
import argparse
from xml.dom.minidom import parseString

# Regular expressions that should be matched
match_expressions = dict({
	'singlequoted' : { 'pos' : 1 , 're' : re.compile(r'\'{1,3}(.+?)\'{1,3}'), 'prefix' : ' ', 'suffix' : ' ' },
	'doublequoted' : { 'pos' : 1 , 're' : re.compile(r'\"([^\"]+)\"'), 'prefix' : ' ', 'suffix' : ' ' },
	'simplecases1' : { 'pos' : 1 , 're' : re.compile(r'\[\[([^\]\|:]+)\]\]'), 'prefix' : '', 'suffix' : '' },
	'z3_simplecases' : { 'pos' : 1 , 're' : re.compile(r'\[\[([^\]]+)\]\]'), 'prefix' : '', 'suffix' : '' },
	'images' : { 'pos' : 1 , 're' : re.compile(r'\[\[Image:[^\]]+\|([^\]]+)\]\]'), 'prefix' : '', 'suffix' : ' ' },
	'file' : { 'pos' : 1 , 're' : re.compile(r'\[\[File:[^\]]+\|([^\]]+)\]\]'), 'prefix' : '', 'suffix' : ' ' },
	'category' : { 'pos' : 1 , 're' : re.compile(r'\[\[Category:(.+?)\]\]'), 'prefix' : '', 'suffix' : ' ' },
	'a_internal_links' : { 'pos' : 2 , 're' : re.compile(r'\[\[([^\]\|]+)\|([^\]\|]+)\]\]'), 'prefix' : '', 'suffix' : '' },
	'refs' : { 'pos' : 1 , 're' : re.compile(r'<ref.*?>(.+?)</ref>'), 'prefix' : '', 'suffix' : '' },
	'translations' : { 'pos' : 1 , 're' : re.compile(r'\[\[[a-z]+?:([^:]+?)\]\]'), 'prefix' : ' ', 'suffix' : ' ' },
	'spaces_separator' : { 'pos' : 1 , 're' : re.compile(r'\s([,.:;])'), 'prefix' : '', 'suffix' : '' },
	'z1_external_links' : { 'pos' : 1, 're' : re.compile(r'\[(http://[^\s\]]+?)\]'), 'prefix' : '', 'suffix' : '' },
	'z2_external_links' : { 'pos' : 1, 're' : re.compile(r'\[http://[^\s]+?\s([^\]]+)\]'), 'prefix' : '', 'suffix' : '' },
})

# Regular expressions that should be replaced
replace_expressions = dict({
	'b1_table' : { 'replacement' : ' ' , 're' : re.compile(r'{\|\s?class.+?\|}')},
	'b2_table' : { 'replacement' : ' ' , 're' : re.compile(r'{\|.+?({\|.+?\|}.*?)*\|}')},
	'd_infobox' : { 'replacement' : ' ', 're' : re.compile(r'{{Infobox.+?({{.+?}}.+?)*}}', re.I)},
	'a_stars' : { 'replacement' : ' ', 're' : re.compile(r'\*')},
	'b_dashes' : { 'replacement' : ' ', 're' : re.compile(r'==+')},
	'c_refs_remaining' : { 'replacement' : ' ' , 're' : re.compile(r'<ref.+?>') },
	'c_refs_single' : { 'replacement' : ' ' , 're' : re.compile(r'<ref.+?/>') },
	'y_misc' : { 'replacement' : ' ', 're' : 	re.compile(r'({{.+?}})')},
	'zzz_double_spaces' : { 'replacement' : ' ', 're' : re.compile(r'\s+')},
	'x_urls' : { 'replacement' : ' ', 're' : 	re.compile(r'http://.+?\s')},
	'w_comment' : { 'replacement' : ' ', 're' : 	re.compile(r'<!--.+?-->')},
	'z1_misc' : { 'replacement' : ' ', 're' : 	re.compile(r'{')},
	'z2_misc' : { 'replacement' : ' ', 're' : 	re.compile(r'}')},
	'z3_misc' : { 'replacement' : ' ', 're' : 	re.compile(r'\[')},
	'z4_misc' : { 'replacement' : ' ', 're' : 	re.compile(r'\]')},
	'z5_misc' : { 'replacement' : ' ', 're' : 	re.compile(r'\t')},	
})

# Define a global counter
pageid = 1

def main():
	# Define the program arguments
	parser = argparse.ArgumentParser(description='Wikipedia raw XML parser.')
	parser.add_argument('inputfile', action = 'store', metavar='inputfile', nargs=1, help='File containing the raw Wikipedia XML')
	parser.add_argument('outputfile', action = 'store', metavar='inputfile', nargs=1, help='Outputfile for the processed data')
	# Parse the parameters
	args = parser.parse_args()
	infile = args.inputfile.pop()
	outfile = args.outputfile.pop()
	# Load the raw XML - careful with *very* large files here
	print "Loading XML from file..."
	fileobj = open(infile,'r')
	data = fileobj.read()
	fileobj.close()
	# Parsing can take a while if the file is big
	print "Parsing document..."
	doc = parseString(data)
	pages = doc.getElementsByTagName("page")
	print "Processing data..."
	# Open a result file, UTF-8 coding
	f = codecs.open(outfile,'w', 'utf-8')
	# For each of the page tags found in the Wiki XML
	for page in pages:
		# process the page object and write it to the output file
		processPage(page, f)
	f.close()
	print "All done."

def processPage(page, f):
	# Fetch the page title
	title = page.getElementsByTagName("title")[0].firstChild.data
	# Fetch the Wikipedia page id - unused in this script
	id = page.getElementsByTagName("id")[0].firstChild.data
	# Fetch the revision object, used for eventually getting to the text
	revision = page.getElementsByTagName("revision")[0]
	# Fetch the actual text for this revision
	text = revision.getElementsByTagName("text")[0].firstChild.data.replace('\n', '')
	# Assume there are no coordinates found
	coords = None

	try:
		# Try and parse the coordinate template using 3 given regex, details below
		coord_format1 = re.compile(r'{{coord\|([^\|]+)\|([^\|]+)\|[^\|]+\|[^\|]+}}', re.I)
		matchfmt_1 = re.search(coord_format1, text)
		coord_format2 = re.compile(r'{{coord\|([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|[^\|]+\|[^\|]+}}', re.I)
		matchfmt_2 = re.search(coord_format2, text)
		coord_format3 = re.compile(r'{{coord\|([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|[^\|]+\|[^\|]+}}', re.I)
		matchfmt_3 = re.search(coord_format3, text)
		
		# Default coords to None
		coords = None
		# Check the first coordinate infobox format - decimal format
		if matchfmt_1 <> None:
			match = matchfmt_1
			lat = float(match.group(1))
			lon = float(match.group(2))
			coords = number_format(lat,6) + "\t" + number_format(lon,6)
		# Check the second coordinate infobox format - N/S/E/W notation
		elif matchfmt_2 <> None:
			match = matchfmt_2
			lat = float(match.group(1))
			lon = float(match.group(3))
			lat *= 1 if match.group(2) == 'N' else -1
			lon *= 1 if match.group(4) == 'E' else -1
			coords = number_format(lat,6) + "\t" + number_format(lon,6)
		# Check the third coordinate infobox format - degrees minutes seconds + N/S/E/W notation
		elif matchfmt_3 <> None:
			match = matchfmt_3
			lat = float(match.group(1))
			lat += float(match.group(2)) / 60
			lat += float(match.group(3)) / 3600
			lat *= 1 if match.group(4) == 'N' else -1
			lon = float(match.group(5))
			lon += float(match.group(6)) / 60
			lon += float(match.group(7)) / 3600
			lon *= 1 if match.group(8) == 'E' else -1
			coords = number_format(lat,6) + "\t" + number_format(lon,6)
		
		# Load global variables
		global expressions, manual_replaces, pageid
	
		# Process (in a given order) the expressions that subsitute text using regex matches
		for key in sorted(iter(match_expressions)):
			text = process_using_match(match_expressions[key]['re'], match_expressions[key]['pos'], match_expressions[key]['prefix'], match_expressions[key]['suffix'], text)
		# Process (in a given order) the expressions that subsitute text using predefined replacements
		for key in sorted(iter(replace_expressions)):
			text = process_using_replacement(replace_expressions[key]['re'], replace_expressions[key]['replacement'], text)
			
	except ValueError:
		coords = None
	
	# If a valid coordinate was found using the coord template and no parsing errors occured
	if coords <> None:
		# Write to file: id    title    lat    lon    text
		f.write(str(pageid) + "\t" + title + "\t" + coords + "\t" + text + "\n")
		# Increment the document id we assign
		pageid += 1

# Helper function that subsitutes text using regex matches
def process_using_match(expression, matchnr, prefix, suffix, text):
	return re.sub(expression, lambda m: prefix + m.group(matchnr) + suffix, text)

# Helper function that subsitutes text using predefined replacements
def process_using_replacement(expression, replacement, text):
	return re.sub(expression, lambda m: replacement, text)

# debug functions
def printMatches(exp, text):
	iterator = exp.finditer(text)
	for match in iterator:
		print match.group() + "\t" + match.group(1)

# Number formatting
def number_format(num, places=0):
	return locale.format("%.*f", (places, num), True)

# Main function	
if __name__ == '__main__':	
	main()