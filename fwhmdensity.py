#!/usr/bin/env python
import numpy
import re
import pylab
import datetime
import pyfits

sharp = re.compile("^#")
pixelscale=0.675
fwhmmin = 0.0
fwhmmax = 4.0
gridsize=5
fwhmmincond = 0.5
peakintensitymax = 30000
peakintensitymin = 300
starcondition = 0.95
magkey = "MAG_AUTO"
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

    def selectstars(self):
	self.stars=self.objects[numpy.where(self.objects["CLASS_STAR"]>starcondition)]
	self.stars=self.stars[numpy.where(self.stars["FLUX_MAX"] < peakintensitymax)]
	self.stars=self.stars[numpy.where(self.stars["FLUX_MAX"] > peakintensitymin)]
	self.stars=self.stars[numpy.where(self.stars["FWHM_IMAGE"] > fwhmmincond)]

    def showfwhmdensity(self,gridsize):
	x =self.stars["X_IMAGE"]
	y =self.stars["Y_IMAGE"]
	fwhm = self.stars["FWHM_IMAGE"]*pixelscale
	pylab.hexbin( \
		x, y, fwhm, \
		gridsize=gridsize, \
		vmin=fwhmmin, \
		vmax=fwhmmax
	    )
	pylab.colorbar()
	mfwhm = fwhm.mean()
	dfwhm = fwhm.std()/numpy.sqrt(fwhm.size)
	pylab.title("fwhm = %.2lf(+/-)%.2lf arcsec" % (mfwhm, dfwhm) )
	return mfwhm, dfwhm

    def showellipticitydensity(self,gridsize):
	x =self.stars["X_IMAGE"]
	y =self.stars["Y_IMAGE"]
	ellipticity = self.stars["ELLIPTICITY"]*pixelscale
	pylab.hexbin( \
		x, y, ellipticity, \
		gridsize=gridsize, \
		vmin=0.0, \
		vmax=0.3
	    )
	pylab.colorbar()
	pylab.title("ellipticity= %.3lf(+/-)%.3lf" \
	    % (numpy.median(ellipticity), ellipticity.std()/numpy.sqrt(ellipticity.size)) )

    def showhistogram(self):
	fwhm = self.objects["FWHM_IMAGE"]*pixelscale
	pylab.hist(fwhm,range=(fwhmmin,fwhmmax),bins=20)
	pylab.xlabel("FWHM")
	pylab.ylabel("frequency")

    def showfwhmmag(self):
	pylab.plot(self.objects["FWHM_IMAGE"]*pixelscale,self.objects[magkey],",")
	pylab.plot(self.stars["FWHM_IMAGE"]*pixelscale,self.stars[magkey],".")
	pylab.xlim(fwhmmin,fwhmmax)
	pylab.ylim(-4,-16)
	pylab.xlabel("FWHM")
	pylab.ylabel("magnitude")


def main(filename):
    pylab.clf()
    mysex = sextractorresult(filename)
    echosys("sex %s -CATALOG_NAME %s" \
	% ( filename, filename.replace(suffix,".cat")) )
    mysex.loaddata()
    candidatefwhm = numpy.median(mysex.objects["FWHM_IMAGE"])*pixelscale
    print candidatefwhm
    echosys("sex %s -CATALOG_NAME %s -SEEING_FWHM %.1lf" \
	% ( filename, filename.replace(suffix, ".cat"), candidatefwhm) )
    mysex.loaddata()
    candidatefwhm = numpy.median(mysex.objects["FWHM_IMAGE"])*pixelscale
    print candidatefwhm
    pylab.subplot(221)
    mysex.showfwhmmag()
    pylab.subplot(222)
    fwhm, dfwhm = mysex.showfwhmdensity(gridsize)
    pylab.subplot(223)
    mysex.showhistogram()
    pylab.subplot(224)
    mysex.showellipticitydensity(gridsize)
    pylab.savefig(filename.replace(suffix,".png"))
    return fwhm, dfwhm

def echosys(cmd):
    print cmd
    os.system(cmd)
    

if __name__ == "__main__":
    import os
    cat=re.compile("%s$" % suffix)
    
    jdarray = []
    fwhmarray = []
    dfwhmarray = []
    count = 0
    for filename in  os.listdir("."):
	try:
	    if cat.search(filename) is None:
		continue
	    fwhm, dfwhm = main(filename)
	    jdarray.append(pyfits.open(filename)[0].header["JD"])
	    fwhmarray.append(fwhm*pixelscale)
	    dfwhmarray.append(dfwhm*pixelscale)
	    count += 1
	    if count == 10:
		continue
	except:
	    pass

    pylab.clf()
    pylab.errorbar(jdarray,fwhmarray,dfwhmarray,fmt="o")
    pylab.xlabel("JD")
    pylab.ylabel("FWHM in arcsec")
    pylab.ylim(fwhmmin,fwhmmax)
    pylab.savefig("timeseries.png")
