#!/usr/bin/python
from myFunct import *


###########################################
###########################################

BalmerKontinuum = (35110, 36303)
BalmerHrana     = (36465, 36473)
CaK             = (39313, 39363)
CaH             = (39313, 39363)
C391            = (39106, 39153)
KratkeVD        = (35500, 35998)
DlouheVD        = (42003, 42499)
CelkovaInt      = (35500, 42499)
Gband           = (00000, 00000)

fmin, fmax = BalmerHrana
f2min, f2max = CelkovaInt


souborrange = xrange(000,len(dirList))
#souborrange = xrange(1500,2000)


###########################################
###########################################


a=np.array([0])
b=np.array([0])
c=np.array([0])
i=0

hdulist = pyfits.open(path_hessi+'hsi_20140611_085140_005.fits')
tbdata = hdulist[2].data
print len(tbdata)
#for x in xrange(1,len(tbdata)):
#    if i==25:
#        i=0
#        print tbdata[x][3], x
#        a=np.append(a,x)
#        b=np.append(b,tbdata[x][4][23])
#        c=np.append(b,tbdata[x][4][7])
#        #c=np.append(c,tbdata[x][4][40])
#    i=i+1



#plt.figure(0)
##plt.plot(a, b,linewidth=0.5, color='b' )
#plt.plot(a, b,linewidth=0.5, color='r' )
##plt.set_yscale('log')
#plt.show()


#hsi_lightcurve = lightcurve.RHESSISummaryLightCurve.create('2014-06-11 06:00','2014-08-44 09:09')
hsi_lightcurve = lightcurve.RHESSISummaryLightCurve.create('2014-06-11 08:45','2014-06-11 09:10')


plt.figure(5)
plt.plot(hsi_lightcurve.data.index,hsi_lightcurve.data['12 - 25 keV'],color='cyan',label='12-25 keV')
plt.plot(hsi_lightcurve.data.index,hsi_lightcurve.data['25 - 50 keV'],color='purple',label='25-50 keV')
plt.ylabel('RHESSI summary counts')
plt.legend()
#plt.show()





























try:
    if f2min and f2max:
        f2 = True
except:
    f2 = False

arrA = [0.0]
arrB = [0.0]

parser(arrA, arrB, path, dirList[0])
imin, fmin = takeClosest(arrA,fmin)
imax, fmax = takeClosest(arrA,fmax)

if f2:
    i2min, f2min = takeClosest(arrA,f2min)
    i2max, f2max = takeClosest(arrA,f2max)

xarr = np.array([])
n = np.array([],float)
n2 = np.array([],float)
n3 = np.array([],float)
imgarr = np.array([],float)
lastSec=0
secPosition=0


for numsoubor in souborrange:
    soubor=dirList[numsoubor]

    counter = counter + 1
    arrA = [0.0]
    arrB = [0.0]
    try:
        newname = parser(arrA, arrB, path, soubor)

        tmp = 0
        #print fmin, fmax, imin, imax
        try:
          print newname[:4]+"-"+newname[4:6]+"-"+newname[6:8]+" "+newname[9:11]+":"+newname[11:13]+":"+newname[13:15]
        except Exception, e:
            pass
        for x in xrange(int(imin),int(imax)):
                cislo = arrA[imin]
                data = arrB[x]
                data = data - Dark[x]
                data = data/(Flat[x]-Dark[x])
                tmp = tmp+data
#
#datetime.date(year=1971, month=12, day=31)
#       
        print newname, "--", int(float(newname[9:11]))
        seconds=(int(float(newname[9:11]))+0)*60*60 + (int(float(newname[11:13]))+0)*60 +int(float(newname[13:15]))
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        ms = 0
        if s==lastSec:
            ms = secPosition*9
            secPosition=1
        lastSec=s
        secPosition =+1
        xarr = np.append(xarr, datetime(year=int(float(newname[:4])), month=int(float(newname[4:6])), day=int(float(newname[6:8])), hour=h, minute=m, second=s, microsecond=ms*1000))
        n=np.append(n, tmp/(imax-imin) )
        if f2:
            for x in xrange(int(i2min),int(i2max)):
                    cislo = arrA[i2min]
                    data = arrB[x]
                    data = data - Dark[x]
                    data = data/(Flat[x]-Dark[x])
                    tmp = tmp+data
            n2=np.append(n2, tmp/(i2max-i2min) )

            n3=n/n2

    except Exception, e:
        print e
    imgarr = np.append(imgarr, newname)
    print "Processing ...", "\t", 'position: ', float((numsoubor-souborrange[0])/(len(souborrange)/100)), "%", " ", numsoubor+1, "/", len(souborrange)+souborrange[0]
    

x = np.arange(0, n.size)

#dft = pd.DataFrame(np.random.randn(100000,1),columns=['A'],index=pd.date_range('20130101',periods=100000,freq='T'))
#xdate = dft
#print xdate


dates = mpl.dates.date2num(xarr)
plt.figure(0)
plt.plot(hsi_lightcurve.data.index,hsi_lightcurve.data['12 - 25 keV'],linewidth=0.5, color='r')
plt.plot(xarr, n*100,linewidth=0.5, color='b')
plt.gcf().autofmt_xdate()
plt.savefig("out.png")

plt.figure(6)
fig, ax1 = plt.subplots()
ax1.plot(hsi_lightcurve.data.index,hsi_lightcurve.data['12 - 25 keV'],linewidth=0.5, color='r')
ax2 = ax1.twinx()
ax2.plot(xarr, n,linewidth=0.5, color='b')
#plt.show()

if f2:
    plt.figure(1)
    plt.plot(xarr, n2*100,linewidth=0.5, color='b' )
    plt.plot(hsi_lightcurve.data.index,hsi_lightcurve.data['12 - 25 keV'],color='cyan',label='12-25 keV')
    plt.figure(2)
    plt.plot(xarr, n3,linewidth=0.5, color='b' )
    plt.figure(3)
    plt.hist(n3, 50, normed=1, facecolor='green', alpha=0.75)
    plt.figure(4)
    plt.plot(n, n2,'.',linewidth=0.5, color='b', )
plt.show()
plt.close()

#for x in range(n.size):
#     plt.plot(xarr,n,linewidth=0.5, color='b' )
#     plt.axvline(x=x, linewidth=2, color='r')
#     plt.savefig("out.png")
#     print "!!!!!!!!!!!!compose"
#     img=Image.open("out.png",'r')
#     img_w,img_h=img.size
#     background = Image.new('RGBA', (img_w,img_h*2), (220, 220, 220, 1))
#     img2_h=0
#     try:
#         print path_sj+corespond(path_sj,imgarr[x])
#         img2=Image.open(path_sj+corespond(path_sj,imgarr[x]),'r')
#         half = 0.5
#         img2 = img2.resize( [int(half * s) for s in img2.size] )
#         img2_w,img2_h=img2.size
#         background = Image.new('RGBA', (img_w,img_h+img2_h), (200, 200, 200, 1))
#         offset=(img_w-img2_w,0)
#         background.paste(img2,offset)
#     except:
#         print "error"
#     bg_w,bg_h=background.size
#     offset=(0,img2_h)
#     background.paste(img,offset)
#     background.save("plot/"+imgarr[x]+".jpg")
#     plt.close()

    #print newname
    #print "Processing ...", "\t", 'position: ', float(counter/(len(dirList)/100)), "%", " ", counter, "/", len(dirList)

