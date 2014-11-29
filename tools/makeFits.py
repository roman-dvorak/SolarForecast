#!/usr/bin/python
from myFunct import *

n = np.array([[0], [0]],float)
num_soubor=0

prihdr = pyfits.Header()
prihdr['OBSERVER'] = 'HSFA2'
prihdr['OBJECT'] = 'SUN'
prihdr['CTYPE1'] = 'SOLAR X'
prihdr['CTYPE2'] = 'SOLAR Y'
prihdr['OBJECT'] = 'SUN'
prihdr['BSCALE'] = 0.025
prihdr['BZERO'] =  349.46
prihdr['BZERO'] =  "349.46"
prihdr['CRVAL1'] =  349.46
prihdr['CRPIX1'] =  349.46
prihdr['COMMENT'] = "Here's some commentary about this FITS file."
prihdr['WAT0_001'] = 'system=equispec'
prihdr['WAT1_001'] = 'wtype=linear label=Wavelength units=angstroms'
prihdr['WAT2_001'] = 'wtype=linear'

for soubor in dirList:
    counter = counter + 1
    arrA = [0.0]
    arrB = [0.0]
    try:
        parser(arrA, arrB, path, soubor)
    except:
        pass

    for x in range(len(arrB)):
        try:
            arrB[x]=arrB[x]-Dark[x]
            arrB[x]=arrB[x]/(Flat[x]-Dark[x])
        except Exception, e:
            print e
            
    print "Processing ...", "\t", 'position: ', float(counter/(len(dirList)/100)), "%", " ", counter, "/", len(dirList)
    a = np.array(arrB)
    n = np.insert(a, 1, arrB, axis=0)
    s=n.shape
    n = np.resize(n, (s[0], 3648))
    n = np.insert(n, s[0], arrB, 0)
    print n.shape
    if s[0]==2500:
        hdu = pyfits.PrimaryHDU(n,prihdr)
        hdulist = pyfits.HDUList([hdu])
        hdulist.writeto('fits/new'+ str(num_soubor) +'.fits')
        num_soubor = num_soubor + 1
        n = np.array([[0], [0]],float)