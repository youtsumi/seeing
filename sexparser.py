#!/usr/bin/env python
import numpy
import re

sharp = re.compile("^#")
suffix = ".fit"

class sextractorresult:
    def __init__(self, filepath ):
	self.filepath = filepath

    def loaddata(self):
	headers = []

	# here must be fast to use "for loop" rather than filter or something
	# the header usually has several lines
	for line in open(self.filepath.replace(suffix,".cat")):
	    if sharp.match(line) is None:
		break
	    headers.append(line[6:22].replace(" ",""))

	formats = ["f4"] * len(headers) 
	    
	self.objects=numpy.loadtxt(self.filepath.replace(suffix,".cat"), \
	    dtype={'names': headers, 'formats': formats})
	self.selectstars()


