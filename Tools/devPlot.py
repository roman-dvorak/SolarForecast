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


#souborrange = xrange(4000,len(dirList))
souborrange = xrange(1500,3000)


###########################################
###########################################
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

n = np.array([],float)
n2 = np.array([],float)
n3 = np.array([],float)
imgarr = np.array([],float)


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

            n3=n/n2

    except Exception, e:
        print e
    imgarr = np.append(imgarr, newname)
    print "Processing ...", "\t", 'position: ', float((numsoubor-souborrange[0])/(len(souborrange)/100)), "%", " ", numsoubor+1, "/", len(souborrange)+souborrange[0]
    



xarr = np.arange(0, n.size)
plt.figure(0)
plt.plot(xarr, n,linewidth=0.5, color='b' )
plt.savefig("out.png")

if f2:
    plt.figure(1)
    plt.plot(xarr, n2,linewidth=0.5, color='b' )
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

