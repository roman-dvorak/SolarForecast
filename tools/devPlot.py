#!/usr/bin/python
from myFunct import *


###########################################
###########################################

BalmerKontinuum = (35110, 36303, "Balmer Kontinuum")
BalmerHrana     = (36465, 36473, "Balmer Hrana")
CaK             = (39313, 39363, "CaK")
CaH             = (39313, 39363, "CaH")
C391            = (39106, 39153, "C391")
KratkeVD        = (35500, 35998, "Kratke VD")
DlouheVD        = (42003, 42499, "Dlouhe VD")
CelkovaInt      = (35500, 42499, "Celkova Intenzita")
#Gband           = (65620, 65630, "G-band") je mimo rozsah spektrometru

Moje            = (00000, 00000, "moje vlastni definice")

fmin, fmax, jmeno = BalmerHrana
f2min, f2max, jmeno2 = CaH
jmeno3= jmeno+"/"+jmeno2


souborrange = xrange(000,len(dirList))
#souborrange = xrange(1000,2000)


###########################################
###########################################


a=np.array([0])
b=np.array([0])
c=np.array([0])
i=0

hdulist = pyfits.open(path_hessi+'hsi_20140611_085140_005.fits', overwrite=True)
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


#plt.figure(5)
#plt.plot(hsi_lightcurve.data.index,hsi_lightcurve.data['12 - 25 keV'],color='cyan',label='12-25 keV')
#plt.plot(hsi_lightcurve.data.index,hsi_lightcurve.data['25 - 50 keV'],color='purple',label='25-50 keV')
#plt.ylabel('RHESSI summary counts')
#plt.legend()
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

        seconds=(int(float(newname[9:11]))+0)*60*60 + (int(float(newname[11:13]))+0)*60 +int(float(newname[13:15]))
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        ms = 0

        if s==lastSec:
            ms = secPosition*80
            secPosition = secPosition + 1
        else:
            secPosition=0
        lastSec = s
        print h,m,s,ms
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


sn = smooth(n,20)
sn2 = smooth(n2,20)
sn3 = smooth(n3,20)

fig, ax0 = plt.subplots()

p0, = ax0.plot(xarr,sn3,color="black", linewidth=2, alpha=0.5, label=jmeno3)

ax1 = ax0.twinx()
p1, = ax1.plot(hsi_lightcurve.data.index,hsi_lightcurve.data['12 - 25 keV'],linewidth=4, alpha=0.75, color='r',label='12-25 keV')
ax1.set_ylabel('12-25 keV', color="r")

ax2 = ax0.twinx()
p2, = ax2.plot(xarr, sn ,linewidth=1, alpha=0.75, color='b', label=jmeno)
p3, = ax2.plot(xarr, sn2 ,linewidth=1, alpha=0.75, color='g', label=jmeno2)

lines = [p0, p1, p2, p3]
ax0.legend(lines, [l.get_label() for l in lines])


if f2:
    #plt.figure(10)
    #plt.plot(xarr, n2,linewidth=0.5, color='b', label=jmeno2)
    #plt.plot(hsi_lightcurve.data.index,hsi_lightcurve.data['12 - 25 keV'],color='cyan',label='12-25 keV')
    #plt.legend()

    #plt.figure(3)
    #plt.plot(xarr, n3,linewidth=0.5, color='b' )

    inter = 1+3.3*math.log(np.shape(n)[0])

    plt.figure()
    plt.hist(n3, inter, normed=1, facecolor='green', alpha=0.75)

    plt.figure()
    plt.plot(n, n2,'.',linewidth=0.5, color='b', )
    plt.show(block=False)

    var1 = raw_input("zadejte min hodnotu hist: ")
    print "you entered", var1
    var2 = raw_input("zadejte max hodnotu hist: ")
    print "you entered", var1


    his=np.array([])
    for x in n3:
        if float(var1) < x < float(var2):
            print "plati"
            his=np.append(his, x)

    hist, bin_edges = np.histogram(his, 1+3.3*math.log(np.shape(his)[0]))

    hist = np.array(hist)/10
    bin_edges = np.array(bin_edges)
    hist=np.append(hist,0)

    median = np.median(his)
    average = np.mean(his)
    modus = bin_edges[np.argmax(hist)]


    print median, average,np.max(hist), modus, np.shape(his)[0], sum(x*x for x in his)

    standardDeviation=math.sqrt((sum(x*x for x in his) - np.shape(his)[0]*average*average)/(np.shape(his)[0]-1))
    if average > modus:
        smer = "pozitivni"
    else:
        smer = "negativni"
    print "standardDeviation:", standardDeviation, (standardDeviation/average)*100, "%,", smer


    plt.figure()
    plt.axvspan(float(var1), float(var2), alpha=0.2, color='red')
    plt.axvline(x=median, linewidth=2, color='r')
    plt.axvline(x=average, linewidth=2, color='g')
    plt.axvline(x=modus, linewidth=2, color='b')
    #plt.hlines(xmin=float(var1), xmax=float(var2) ,y=0.5, linewidth=2, color='grey')
    plt.plot(bin_edges, hist, color='red', alpha=0.55)
    plt.hist(n3, inter, normed=1, facecolor='green', alpha=0.75)

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

