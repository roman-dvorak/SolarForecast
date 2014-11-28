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
import shutil







def main ():
	#dirList = os.listdir("/media/roman/eHDD/Dokumenty/Projects/Astronomy/Spectrum/140611/spectra/AR12085/0732")

	#path="/media/roman/eHDD/Dokumenty/Projects/Astronomy/Spectrum/140611/spectra/AR12087/0807/"
	path_sj="/media/roman/eHDD/Dokumenty/Projects/Astronomy/Spectrum/140611/sj/"
	dirList = os.listdir(path_sj)
	dirList.sort()
	print dirList

	n = 0
	for soubor in dirList:
		n = n + 1
		newsoubor = soubor[soubor.find(" ")+1:len(soubor)-4]
		shutil.copy2(path_sj+soubor, path_sj+"new/"+newsoubor+".bmp")
		print n,"/",len(dirList)



if __name__ == "__main__":
	main()
