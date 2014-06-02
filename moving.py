#!/usr/bin/env python
import sexparser
import pyflann
import numpy
import pylab
import re
import pyfits
import fwhmdensity



def buildvec( x, y ):
    return numpy.transpose([x,y])

def getvectorfield( fitsa, fitsb, graph=False):
    mysex = sexparser.sextractorresult(fitsa)
    mysex.loaddata()
    testsex = sexparser.sextractorresult(fitsb)
    testsex.loaddata()

    flann = pyflann.FLANN()
    dataset = buildvec( mysex.objects["X_IMAGE"], mysex.objects["Y_IMAGE"] )
    testset = buildvec( testsex.objects["X_IMAGE"], testsex.objects["Y_IMAGE"] )

    ids, dists = flann.nn(dataset,testset,1,algorithm="linear")

    
    f=numpy.vectorize( lambda x:  x > 0 and x < 100 )
    cond = numpy.where( f(dists) )

    if graph:
	pylab.hist(dists,bins=100,range=(0,10),histtype="bar")
	pylab.hist(dists[cond],bins=100,range=(0,10))
	pylab.show()
    
    diffvec = dataset[ids[cond]]-testset[cond]

    x,y=numpy.transpose(testset)
    q,u=numpy.transpose(diffvec)

    if graph:
	pylab.quiver(x,y,q,u)
	pylab.xlim(0,2048)
	pylab.ylim(0,2048)
	pylab.show()

    return q.mean(), u.mean(), q.std(), u.std()

def loadhonirlog( filepath ):
    return numpy.loadtxt(filepath, unpack=True)

def main():
    import os
    cat=re.compile("%s$" % sexparser.suffix)

    former=None
    targets = filter(lambda x: True if cat.search(x) else False, \
	[ filename for filename in  os.listdir(".") ])
    
    qmeanarray = []
    umeanarray = []
    qsigarray = []
    usigarray = []
    jdarray = []
    count = 0

    for i in range(len(targets)-1):
	try:
	    jdnext    = pyfits.open(targets[i+1])[0].header["JD"]
	    jdcurrent = pyfits.open(targets[i  ])[0].header["JD"]
	    dt=(jdnext-jdcurrent)*3600*24

	    jdarray.append(jdcurrent-2400000.5)
	    q,u,dq,du=getvectorfield(targets[i], targets[i+1])

	    qmeanarray.append(q/dt)
	    umeanarray.append(u/dt)
	    qsigarray.append(dq/dt)
	    usigarray.append(dq/dt)

	    count += 1
	    if count == 100:
		continue

	except:
	    raise

    pixscale = fwhmdensity.pixelscale
    qmeanarray = numpy.array(qmeanarray)
    umeanarray = numpy.array(umeanarray)
    qsigarray= numpy.array(qsigarray)
    usigarray= numpy.array(usigarray)
    
    pylab.subplot(211)
    pylab.xlabel("MJD")
    pylab.ylabel("Poinging differences in arcsec")
    pylab.errorbar(jdarray,qmeanarray*pixscale,qsigarray*pixscale,fmt="o")
    pylab.errorbar(jdarray,umeanarray*pixscale,usigarray*pixscale,fmt="o")
    xmin,xmax=pylab.xlim()

    pylab.subplot(212)
    mjd, az, al, vrot=loadhonirlog("../honir/20140530/inr.log")
    pylab.plot(mjd,al,"-",label="Altitude")
    pylab.plot(mjd,az,"-",label="Azimuth")
    pylab.plot(mjd,vrot,"-",label="Vrot")
    pylab.xlim(xmin,xmax)
    pylab.xlabel("MJD")
    pylab.ylabel("El (deg or arcsec/sec)")
    pylab.legend(loc="upper left")
    pylab.savefig("positiondifference.png")
    

if __name__ == "__main__":
    main()
    
