#!/usr/bin/python
from __future__ import division
import os
import time
import datetime
from   datetime import datetime

import ftplib
import ConfigParser
import operator
from   array import array
import subprocess
import Image
import math

from pylab import plot, ylim, xlim, show, xlabel, ylabel, grid
from numpy import linspace, loadtxt, ones, convolve

import matplotlib.pyplot as plt
import matplotlib as mpl

import pyfits

import numpy as np
import numpy as numpy

import sunpy
from   sunpy import lightcurve

import pandas
import pandas as pd

import scipy
import scipy as sp
from scipy.interpolate import interp1d
from scipy import stats


  


arrA = []
arrB = []
arrAvg=[]
newname = ""

Flat = [0.0]
Dark = [0.0] 
arr  = [0.0]

#path = "/home/roman/Dokumenty/Projects/Astronomy/Spectrum/2014/140611/spectra/flat/"
path="/home/roman/Dokumenty/Projects/Astronomy/Spectrum/2014/140611/spectra/AR12087/0843/"
#path="/media/roman/eHDD/Dokumenty/Projects/Astronomy/Spectrum/140611/spectra/AR12087/0807"
path_sj="/home/roman/Dokumenty/Projects/Astronomy/Spectrum/2014/140611/sj/new/"
path_hessi="/home/roman/Dokumenty/Projects/Astronomy/Spectrum/data/"
dirList = os.listdir(path)
dirList.sort()
dirListSJ = os.listdir(path_sj)
dirListSJ.sort()
print dirList

counter = 0

def corespond(path_sj, newname):
    #
    #   z newname vytrori jmeno obrazku s celou cestou
    #   
    #   in path_sj - cesta ke vsem obrazkum sj
    #   in newname - jmeno txt, ze ktereho se vytvori nazev obrazku; example "20140603_033722_40ms_00010.txt"
    #
    #   out 
    #

    name_sj = ""
    dirList = os.listdir(path_sj)
    dirList.sort()
    print newname[9:11]+"-"+newname[11:13]+"-"+newname[13:15]
    for sjfile in dirList:
        if sjfile[0:len(sjfile)-4] is newname[9:11]+"-"+newname[11:13]+"-"+newname[13:15]:
            print "shoda corespond newname a obrazek v path_sj"
            name_sj = sjfile
        name_sj = newname[9:11]+"-"+newname[11:13]+"-"+newname[13:15]+".bmp"
    return name_sj

    #   newname - 20140603_033722_40ms_00010.txt    - 
    #   sj file - Image0004 07-32-38.bmp            - 

def compose(path, newname, type, path_sj, compose):
    # type = 0 - only graph
    # type = 1 - text data
    # type = 2 - spectrum and slitjaw
    # type = 3 - 

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
    except:
        print "Error: compose neznamy typ"


def monthToNum(date):
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
    #
    #   ze souboru ze spektogramu vytvori dve pole 'arrA' a 'arrB'
    #
    #   in 'arrA'  - pole s vlnovou delkou
    #   in 'arrB'  - pole s hodnotama
    #   in 'path'  - cesta k umisteni 'soubor'u
    #   in 'soubor'- nazev souboru s daty
    #
    #   glob 'newname' - ; example "20140603_033722_40ms_00010.txt"
    #
    f=open(path+soubor)
    lines=f.readlines()
    #minutes = int(lines[2][17:19])*60 + int(lines[2][20:22]) + 4*60 + 30 # cas spekter offsetu od UTC


    seconds=(int(float(lines[2][17:19]))+4)*60*60 + (int(float(lines[2][20:22]))+30)*60 +int(float(lines[2][23:25]))
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    newname = "" + lines[2][30:34] + monthToNum(lines[2][10:13]) + lines[2][14:16] + "_" + str('%02d'% h) + str('%02d' % m) + str('%02d' % s) + "_" + soubor
    #              ^ rok             ^ cislo mesice                ^ cislo dnu v mesici    ^ hodina         ^ minuta          ^sekunda                ^ puvodni jmeno
    for i in range(18,3665):
        data = lines[i]
        arrA.append(float( data[:data.find("\t")] )*10)
        arrB.append(float( data[data.find("\t")+1:] ))
    arrA[0]=0
    arrB[0]=0
    return str(newname)#, lines[2], str('%02d'% h)

def erse (arrA, arrB):
    #
    #vycisti pole 'arrA' a 'arrB'
    arrA = []
    arrB = []

def average (arrA,arrB, size):
    for element in range(1,len(arrA)):
        if element > size and element < (len(arrA)-size):
            arrB[element] = (arrB[element]+arrB[element-size]+arrB[element+size])/(1+2*size)


def plot (arrA, arrB, newname, xmin, xmax):
    #
    # vykresli graf 'arrA' v zavislosti na 'arrB' s nadpisem 'newname' a ulozi do souboru
    #
    #   in 'arrA'    - pole s osou X
    #   in 'arrB'    - pole s osou Y
    #   in 'newname' - ; example "20140603_033722_40ms_00010.txt"
    #   in 'xmin'    - minimalni hodnota na ose x
    #   in 'xmax'    - maximalni hodnota na ose x
    #
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
    #
    # najde nejblizsi namerenou vlnovou delku dle zadane hodnoty
    #
    #   in 'myList'  - sezam vsech vln delek
    #   in 'myNumber'- hledana vln delka
    #
    #   out 'ext'    - index v 'myList'
    #   out 'closest'- hodnota nejblizsi 'myNumber hodnoty'
    #
    if myNumber < 34946 or myNumber > 48548:
        raise Exception("Hledana vlnova delka je mimo rozsah." + "Pouzijte rozsah 3494.6 az 4854.8.")
    vedle = 100
    closest = 100
    for i in xrange(1, len(myList)):
        if abs(myList[i]*10 - myNumber) < vedle:
            vedle = abs(myList[i]*10 - myNumber)
            closest = myList[i]*10
            ext=i
    return int(ext), closest


parser(arr, Flat, "/home/roman/Dokumenty/Projects/Astronomy/Spectrum/scripts/", "FlatSpectrum.TXT")
parser(arr, Dark, "/home/roman/Dokumenty/Projects/Astronomy/Spectrum/scripts/", 'DarkSpectrum.TXT')



def smooth(inarr, lenght):
    #
    #   Koluzavy prumer
    #
    inarr=np.array(inarr)
    outarr=np.array(inarr)
    for i in xrange(int(lenght/2),int(inarr.shape[0]-lenght)):
        suma=0
        for xa in xrange(int(-lenght/2),int(lenght/2)):
            #print i, xa, inarr[i]
            suma=suma+inarr[i+xa]
        outarr[i]=suma/lenght
    return outarr


def smerodatna_odchylka(data, min=0, max=0, plot=True):
    #
    #   pocita smerodatnou odchylku. Pokud min a max neni nastaveno, pocita se
    #       z celeho pole. Jinak to je vyber mezi min a max
    #
    #   in 'data'   - pole s daty
    #   in 'min'    - minimalni hodnota v poli pro posouzeni
    #   in 'max'    - maximalni hodnota v poli pro posouzeni
    #   in 'plot'   - rozhoduje o vykresleni grafu
    #
    #   out 'out'   - smerodatna odchylka
    #
    data = np.array(data)

    if min == 0 and max == 0:
        average = np.mean(data)
        hist, bin_edges = np.histogram(data, 1+3.3*math.log(np.shape(data)[0]))
        hist=np.append(hist,0)
        average = np.mean(data)
        modus = bin_edges[np.argmax(hist)]
        median = np.median(data)
        standardDeviation=math.sqrt((sum(x*x for x in data) - np.shape(data)[0]*average*average)/(np.shape(data)[0]-1))
    else:
        crop = np.array([])
        for x in data:
            if min < x < max:
                crop=np.append(crop,x)
                print np.shape(crop)[0]
        hist, bin_edges = np.histogram(crop, 1+3.3*math.log(np.shape(crop)[0]))
        hist=np.append(hist,0)
        average = np.mean(crop)
        modus = bin_edges[np.argmax(hist)]
        median = np.median(crop)
        standardDeviation=math.sqrt((sum(x*x for x in crop) - np.shape(crop)[0]*average*average)/(np.shape(crop)[0]-1))
    if average > modus:
        smer = True # tohle je pozitivni
    else:
        smer = False # tohle je negativni

    if plot:
        def pozitivita(bool):
            if bool:
                return "pozitivni"
            else:
                return "negativni"
            
        plt.figure()
        plt.axvspan(float(min), float(max), alpha=0.2, color='g')
        plt.axvline(x=median, linewidth=2, color='r')
        plt.axvline(x=average, linewidth=2, color='g')
        plt.axvline(x=modus, linewidth=2, color='b')
        plt.hist(data, 1+3.3*math.log(np.shape(data)[0]), normed=1, facecolor='green', alpha=0.75)
        plt.text(average, 5, "standartni odchylka - "+str(standardDeviation)+" - "+pozitivita(smer),
                bbox={'facecolor':'green', 'alpha':0.75, 'pad':10})
        plt.show(block=False)

        print "hodnota standartni odchylky je: "+str(standardDeviation)+" a jeji smer je "+pozitivita(smer)

    return standardDeviation, smer


def plotMenu():
    def hlavicka(msg=" "):
        print msg
        print "--------------------"
        print "Menu"
        print "____________________"
        print " "
        print "Ukoncit:", "\t\t\t" , "Enter"
        print "smerodatna odchylka", "\t\t" , "1"+" + "+"Enter"
        print ""
    input=None
    hlavicka()
    while input != "" and input != "1" and input != "2" and input != "" and input != "":
        input = raw_input("zadejte a potvrdte hodnotu: ")
        if  input != "" and input != "1" and input != "2" and input != "" and input != "":
            hlavicka("zadal jste spatnou hodnotu")
        else:
            print "zadal jste:", input
        if  input == "":
            plt.close()
            raise SystemExit("Aplikace se ukoncuje")
    return input

