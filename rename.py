#!/usr/bin/python
import os
import datetime
import time
import ftplib
import ConfigParser
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import operator
from scipy.interpolate import interp1d
from array import array
import subprocess
import Image
import pyfits
  


arrA = []
arrB = []
arrAvg=[]
newname = ""

Flat = [0.0]
Dark = [0.0] 
arr  = [0.0]
    #Flat=np.array([], dtype=np.float)
    #Dark=np.array([], dtype=np.float)  
    #arr=np.array([], dtype=np.float)

def corespond(path_sj, newname):
    name_sj = ""
    dirList = os.listdir(path_sj)
    dirList.sort()
    print newname[9:11]+"-"+newname[11:13]+"-"+newname[13:15]
    for sjfile in dirList:
        if sjfile[0:len(sjfile)-4] is newname[9:11]+"-"+newname[11:13]+"-"+newname[13:15]:
            print "shoda -------------------------------------------------------------------"
            name_sj = sjfile
        name_sj = newname[9:11]+"-"+newname[11:13]+"-"+newname[13:15]+".bmp"
        #name_sj = "07-32-35"+".bmp"
    #file.close()
    return name_sj

    #   newname - 20140603_033722_40ms_00010.txt    - 
    #   sj file - Image0004 07-32-38.bmp            - 

def compose(path, newname, type, path_sj, compose):
    # type = 0 - only graph
    # type = 1 - text data
    # type = 2 - spectrum and slitjaw
    # type = 3 - spectrum, slitjaw, textdata

    #if type is not 0 or 1 or 2 or 3:
    #   type = 0

    try:
        if type is 0:
            pass

        elif type is 1:
            print "!!!!!!!!!!!!compose type 1"
            img=Image.open("plot/"+newname+".jpg",'r')
            img_w,img_h=img.size
            background = Image.new('RGBA', (img_w,img_h), (255, 255, 255, 1))
            #bg_w,bg_h=background.size
            #offset=((bg_w-img_w)/2,(bg_h-img_h)/2)
            background.paste(img)
            background.save("plot/"+newname+".jpg")

        elif type is 2:
            print "!!!!!!!!!!!!compose type 2"
            img=Image.open("plot/"+newname+".jpg",'r')
            img_w,img_h=img.size
            background = Image.new('RGBA', (img_w,img_h*2), (200, 200, 200, 1))
            try:
                print path_sj+compose
                img2=Image.open(path_sj+compose,'r')
                img2_w,img2_h=img2.size
                background = Image.new('RGBA', (img_w,img_h+img2_h), (200, 200, 200, 1))
                offset=(0,0)
                background.paste(img2,offset)
            except:
                print "error"

            bg_w,bg_h=background.size
            offset=(0,img2_h)
            background.paste(img,offset)
            background.save("plot/"+newname+".jpg")

        elif type is 3:
            print "!!!!!!!!!!!!compose type 2"
            img=Image.open("plot/"+newname+".jpg",'r')
            img_w,img_h=img.size
            background = Image.new('RGBA', (img_w,img_h*2), (200, 200, 200, 1))
            try:
                print path_sj+compose
                img2=Image.open(path_sj+compose,'r')
                img2_w,img2_h=img2.size
                background = Image.new('RGBA', (img_w,img_h+img2_h), (200, 200, 200, 1))
                offset=(img_w-img2_w,0)
                background.paste(img2,offset)
            except:
                print "error"
            bg_w,bg_h=background.size
            offset=(0,img2_h)
            background.paste(img,offset)
            background.save("plot/"+newname+".jpg")
    except:
        print "Error: compose"

def monthToNum(date):
    print "monthToNum:" + date 
    return{
        'Jan' : '01',
        'Feb' : '02',
        'Mar' : '03',
        'Apr' : '04',
        'May' : '05',
        'Jun' : '06',
        'Jul' : '07',
        'Aug' : '08',
        'Sep' : '09', 
        'Oct' : '10',
        'Nov' : '11',
        'Dec' : '12'
    }[date]


def dayToNum(date):
    print "monthToNum:" + date 
    return{
        'Mon' : '01',
        'Tue' : '02',
        'Wed' : '03',
        'Thu' : '04',
        'Fri' : '05',
        'Sat' : '06',
        'Sun' : '07',
    }[date]

def parser(arrA, arrB, path, soubor):
    global newname

    f=open(path+soubor)
    lines=f.readlines()
    minutes = int(lines[2][17:19])*60 + int(lines[2][20:22]) + 4*60 + 30 # cas spekter offsetu od UTC
    newname = "" + lines[2][30:34] + monthToNum(lines[2][10:13]) + dayToNum(lines[2][6:9]) + "_" + str('%02d'%int(minutes/60)) + str('%02d' % int(minutes-(minutes/60)*60)) + lines[2][23:25] + "_" + soubor
    for i in range(18,3665):
        data = lines[i]
        arrA.append(float( data[:data.find("\t")] )*10)
        arrB.append(float( data[data.find("\t")+1:] ))
    arrA[0]=0
    arrB[0]=0

def erse (arrA, arrB):
    arrA = []
    arrB = []

def average (arrA,arrB, size):
    for element in range(1,len(arrA)):
        if element > size and element < (len(arrA)-size):
            arrB[element] = (arrB[element]+arrB[element-size]+arrB[element+size])/(1+2*size)


def plot (arrA, arrB, newname, xmin, xmax):
    print "elements: ", len(arrA)
    f, ax = plt.subplots()
    plt.title(r' spectrum '+ newname)
    f.set_figwidth(11.7)
    f.set_figheight(4.1)
    plt.grid()
    ax.set_xlim([xmin,xmax])
    ax.set_ylim([-1,2])
    ax.set_xlabel('Wavelength (Angstroms)')
    ax.set_ylabel('value [relative]')
    ax.set_xticks(np.arange(xmin,xmax,(xmax-xmin)/10))
    ax.plot(arrA, arrB, '-b', linewidth=0.8)
    plt.savefig("./plot/"+newname+".jpg", dpi=200)
    plt.close()


def timelaps(folder, type):
    subprocess.call(["ffmpeg", "-r 25", "-pattern_type glob", "-i 'plot/*.jpg'", "-c:v copy output.avi"])
    #ffmpeg -r 25 -pattern_type glob -i 'plot/*.jpg' -c:v copy output.avi

def takeClosest(myList, myNumber):
    vedle = 100
    closest = 100
    for i in xrange(1, len(myList)):
        if abs(myList[i]*10 - myNumber) < vedle:
            vedle = abs(myList[i]*10 - myNumber)
            closest = myList[i]*10
            ext=i
    return int(ext), closest


def main ():

    parser(arr, Flat, "/home/roman/Dokumenty/Projects/Astronomy/Spectrum/scripts/", "FlatSpectrum.TXT")
    parser(arr, Dark, "/home/roman/Dokumenty/Projects/Astronomy/Spectrum/scripts/", 'DarkSpectrum.TXT')

    #path = "/home/roman/Dokumenty/Projects/Astronomy/Spectrum/2014/140611/spectra/flat/"
    path="/home/roman/Dokumenty/Projects/Astronomy/Spectrum/2014/140611/spectra/AR12087/0843/"
    #path="/media/roman/eHDD/Dokumenty/Projects/Astronomy/Spectrum/140611/spectra/AR12087/0807"
    path_sj="/home/roman/Dokumenty/Projects/Astronomy/Spectrum/2014/140611/sj/new/"
    dirList = os.listdir(path)
    dirList.sort()
    dirListSJ = os.listdir(path_sj)
    dirListSJ.sort()
    print dirList

    xmin =          3500
    xmax = xmin +   1000

    kolo = 0
    
    init = True
    #plt.plot(arrA, arrB, 'b')
    #plt.savefig("./plot/aaa.jpg")
    #plt.show()

    counter = 0
    #for soubor in dirList:
    #    print ""
    #    counter = counter + 1
    #    arrA = [0.0]
    #    arrB = [0.0]
    #    try:
    #        parser(arrA, arrB, path, soubor)
    #    except:
    #        pass
    #    for x in range(len(arrB)):
    #        try:
    #            arrB[x]=arrB[x]-Dark[x]
    #            arrB[x]=arrB[x]/(Flat[x]-Dark[x])
    #        except Exception, e:
    #            print e
    #    average(arrA, arrB, 1)
    #    plot(arrA, arrB, newname, xmin, xmax)                              ## vytvoreni fgrafu a poskladani do celeho image
    #    compose(path, newname, 3, path_sj, corespond(path_sj,newname))

    #    print newname
    #    print "Processing ...", "\t", 'position: ', float(counter/(len(dirList)/100)), "%", " ", counter, "/", len(dirList)



    BalmerKontinuum = (3510, 36303)
    CaK= (39313, 39363)
    CaH= (39313, 39363)

    fmin = 36465
    fmax = 36473

    f2 = True
    f2min = 35500
    f2max = 42499


    arrA = [0.0]
    arrB = [0.0]

    parser(arrA, arrB, path, dirList[0])
    imin, fmin = takeClosest(arrA,fmin)
    imax, fmax = takeClosest(arrA,fmax)

    i2min, f2min = takeClosest(arrA,f2min)
    i2max, f2max = takeClosest(arrA,f2max)

    n = np.array([],float)
    n2 = np.array([],float)
    n3 = np.array([],float)
    imgarr = np.array([],float)

    #souborrange = xrange(4000,len(dirList))
    souborrange = xrange(1500,3000)

    for numsoubor in souborrange:
        soubor=dirList[numsoubor]

        counter = counter + 1
        arrA = [0.0]
        arrB = [0.0]
        try:
            parser(arrA, arrB, path, soubor)

            tmp = 0
            #print fmin, fmax, imin, imax
            for x in xrange(int(imin),int(imax)):
                    cislo = arrA[imin]
                    data = arrB[x]
                    data = data - Dark[x]
                    data = data/(Flat[x]-Dark[x])
                    tmp = tmp+data
            n=np.append(n, tmp/(imax-imin) )
            if f2:
                for x in xrange(int(i2min),int(i2max)):
                        cislo = arrA[i2min]
                        data = arrB[x]
                        data = data - Dark[x]
                        data = data/(Flat[x]-Dark[x])
                        tmp = tmp+data
                n2=np.append(n2, tmp/(i2max-i2min) )
            print fmin, fmax, imin, imax,  f2min, f2max, i2min, i2max
            n3=n/n2

        except Exception, e:
            print e
        imgarr = np.append(imgarr, newname)
        print "Processing ...", "\t", 'position: ', float(counter/(len(dirList)/100)), "%", " ", counter, "/", len(dirList)
        



    xarr = np.arange(0, n.size)
    plt.figure(0)
    plt.plot(xarr, n,linewidth=0.5, color='b' )
    plt.savefig("out.png")
    plt.figure(1)
    plt.plot(xarr, n2,linewidth=0.5, color='b' )
    plt.figure(2)
    plt.plot(xarr, n3,linewidth=0.5, color='b' )
    plt.figure(3)
    plt.hist(n3, 50, normed=1, facecolor='green', alpha=0.75)
    #plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
    plt.figure(4)
    plt.plot(n, n2,'.',linewidth=0.5, color='b', )
    plt.show()
    plt.close()

    for x in range(n.size):
         plt.plot(xarr,n,linewidth=0.5, color='b' )
         plt.axvline(x=x, linewidth=2, color='r')
         plt.savefig("out.png")
         print "!!!!!!!!!!!!compose"
         img=Image.open("out.png",'r')
         img_w,img_h=img.size
         background = Image.new('RGBA', (img_w,img_h*2), (220, 220, 220, 1))
         img2_h=0
         try:
             print path_sj+corespond(path_sj,imgarr[x])
             img2=Image.open(path_sj+corespond(path_sj,imgarr[x]),'r')
             half = 0.5
             img2 = img2.resize( [int(half * s) for s in img2.size] )
             img2_w,img2_h=img2.size
             background = Image.new('RGBA', (img_w,img_h+img2_h), (200, 200, 200, 1))
             offset=(img_w-img2_w,0)
             background.paste(img2,offset)
         except:
             print "error"
         bg_w,bg_h=background.size
         offset=(0,img2_h)
         background.paste(img,offset)
         background.save("plot/"+imgarr[x]+".jpg")
         plt.close()
 
        #print newname
         #print "Processing ...", "\t", 'position: ', float(counter/(len(dirList)/100)), "%", " ", counter, "/", len(dirList)

##################################################################################################
##################################################################################################



   # n = np.array([[0], [0]],float)
   # num_soubor=0

   # prihdr = pyfits.Header()
   # prihdr['OBSERVER'] = 'HSFA2'
   # prihdr['OBJECT'] = 'SUN'
   # prihdr['CTYPE1'] = 'SOLAR X'
   # prihdr['CTYPE2'] = 'SOLAR Y'
  # # prihdr['OBJECT'] = 'SUN'
   # prihdr['BSCALE'] = 0.025
   # prihdr['BZERO'] =  349.46
   # prihdr['BZERO'] =  "349.46"
   # prihdr['CRVAL1'] =  349.46
   # prihdr['CRPIX1'] =  349.46
   # prihdr['COMMENT'] = "Here's some commentary about this FITS file."
   # prihdr['WAT0_001'] = 'system=equispec'
   # prihdr['WAT1_001'] = 'wtype=linear label=Wavelength units=angstroms'
   # prihdr['WAT2_001'] = 'wtype=linear'

   # for soubor in dirList:
   #     counter = counter + 1
   #     arrA = [0.0]
   #     arrB = [0.0]
   #     try:
   #         parser(arrA, arrB, path, soubor)
   #     except:
   #         pass
   #     for x in range(len(arrB)):
   #         try:
   #             arrB[x]=arrB[x]-Dark[x]
   #             arrB[x]=arrB[x]/(Flat[x]-Dark[x])
   #         except Exception, e:
   #             print e
   #     print "Processing ...", "\t", 'position: ', float(counter/(len(dirList)/100)), "%", " ", counter, "/", len(dirList)
   #     a = np.array(arrB)
       # n = np.insert(a, 1, arrB, axis=0)
   #     s=n.shape
   #     n = np.resize(n, (s[0], 3648))
   #     n = np.insert(n, s[0], arrB, 0)
   #     #n[s[0]]=arrB
   #     print n.shape
   #     if s[0]==2500:
   #         hdu = pyfits.PrimaryHDU(n,prihdr)
   #         hdulist = pyfits.HDUList([hdu])
   #         hdulist.writeto('fits/new'+ str(num_soubor) +'.fits')
   #         num_soubor = num_soubor + 1
   #         n = np.array([[0], [0]],float)

    #hdu = pyfits.PrimaryHDU(n,prihdr)
    #hdulist = pyfits.HDUList([hdu])
    #hdulist = pyfits.PrimaryHDU(header=prihdr)
    #hdulist.writeto('fits/new'+str(num_soubor)+'.fits')


    #timelaps("a","x")

if __name__ == "__main__":
    main()
