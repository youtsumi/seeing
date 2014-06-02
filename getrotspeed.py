#!/usr/bin/env python
# http://www.mmto.org/MMTpapers/pdfs/itm/itm04-1.pdf
from numpy import cos, sin, pi, arctan2, sqrt
import pylab
import numpy

rad2deg = 180./pi
def rotspeed(azimuth,el):
    latitude = 34.5 # Hiroshima
    return -0.262*cos(latitude/rad2deg)*cos(azimuth/rad2deg)/cos(el/rad2deg)*rad2deg*3600/3600

if __name__ == "__main__":
    vrotspeed=numpy.vectorize(rotspeed)
    az = numpy.arange(0,361,3)
    el = numpy.arange(0,86,3)
    AZ, EL = numpy.meshgrid(az,el)
    pylab.subplot(111,polar=True)
    pylab.pcolor(AZ/rad2deg,(90-EL),vrotspeed(AZ-90,EL))
    pylab.colorbar()
    pylab.xlim(pi/4.,(2.+1/4)*pi)
    pylab.xticks((0,pi/2,2*pi/2,3*pi/2),("E(90)","N(180)","W(-90)","S(0)"))
    pylab.grid()
    pylab.title("Field rotation velocity map [arcsec/s]")
    pylab.savefig("FieldRotation.png")
