#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import numpy
import ConfigParser
try:
    import pygtk
    pygtk.require("2.0")
    import gtk
except:
    print "Error: PyGTK, GTK 2.xx and Glib must be installed to run this application. Exiting"
    sys.exit(1)
try:
    import cv2
    import cv
    import numpy as np
    import scipy
    import Image
    import matplotlib.pyplot as plt
except:
    print "Error: cv2.xx and numpy must be installed to run this application. Exiting"
    sys.exit(1)
import threading
import time
import random




def MakeHist(img, histH, histW, position, Mask):
# img muze byt CV2 i NUMPY obr
# position  - 5     - zmeni se velikost pozadi a bude pres cele
#           - 1-4   - do urciteho kvadratu
    #histW = 200
    #histH = 200
    border = 10
    a = np.zeros((histW, histH))
    a = np.asarray(img)
    if position is 1:
        Xoffset = a.shape[1]-histW-border
        Yoffset = border
    elif position is 2:
        Xoffset = border
        Yoffset = border
    elif position is 3:
        Xoffset = border
        Yoffset = a.shape[0]-histH-border
    elif position is 4:
        Xoffset = a.shape[1]-histW-border
        Yoffset = a.shape[0]-histH-border

    hmax = np.amax(a)+1
    hmin = np.amin(a)
    hist = cv2.calcHist([img],[0],Mask,[histW],[int(hmin),int(hmax)]) # none je maska
    for x in xrange(0,len(hist)):
        cv2.line(a, (x+Xoffset,histH+Yoffset), (x+Xoffset, (histH-(float(histH)/np.amax(hist))*hist[x])+Yoffset), 100)
    return a



class SJThread (threading.Thread):
    def __init__(self, status):
        threading.Thread.__init__(self)
        self.status = status
    
    def run(self):

        print "Starting " + self.name + str(self.status)
        for x in xrange(1,10):
            print x
            print "camera funguje"
            time.sleep(500)
        print "Exiting " + self.name + str(self.status)

    def stop(self):
        self.status=False


class LiveSJ(gtk.Window):

    def __init__(self):
        self.SnapshotMessage=0
        self.ImgSource=False
        self.ImgPath=""
        self.cfg = ConfigParser.RawConfigParser()
        self.cfg.read("LiveSJ.ini")
        self.cam = cv2.VideoCapture(0)
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_title("LiveSJ.__init__")
        self.move(100,100)
        self.set_size_request(450, gtk.ICON_SIZE_MENU+200+gtk.ICON_SIZE_MENU)
        self.kostra = gtk.VBox(homogeneous=False, spacing=2)
        self.add(self.kostra)

        self.toolbar = gtk.Toolbar()
        self.toolbar.set_icon_size(gtk.ICON_SIZE_MENU)
        self.kostra.pack_start(self.toolbar, False, False)


        self.show_all()

    def spust(self):
        play = False

        self.toolbar_item01 = gtk.ToolButton("Quit")
        self.toolbar_item01.set_stock_id(gtk.STOCK_QUIT)
        self.toolbar_item01.connect("clicked", exit)
        self.toolbar.insert(self.toolbar_item01,0)

        self.toolbar_item02 = gtk.ToolButton("Play")
        self.toolbar_item02.set_stock_id(gtk.STOCK_MEDIA_PLAY)
        self.toolbar_item02.connect("clicked", self.SJLivePlay)
        self.toolbar.insert(self.toolbar_item02,1)

        self.toolbar_item03 = gtk.ToolButton("Open")
        self.toolbar_item03.set_stock_id(gtk.STOCK_OPEN)
        self.toolbar_item03.connect("clicked", self.SJLiveOpen)
        self.toolbar.insert(self.toolbar_item03,2)

        self.toolbar_item04 = gtk.ToolButton("Stop")
        self.toolbar_item04.set_stock_id(gtk.STOCK_MEDIA_STOP)
        self.toolbar_item04.connect("clicked", self.SJLiveStop)
        self.toolbar.insert(self.toolbar_item04,3)

        self.toolbar_item05 = gtk.ToolButton("Record")
        self.toolbar_item05.set_stock_id(gtk.STOCK_MEDIA_RECORD)
        self.toolbar_item05.connect("clicked", self.SJLiveStop)
        self.toolbar.insert(self.toolbar_item05,4)

        self.toolbar_item06 = gtk.ToolButton("Setting")
        self.toolbar_item06.set_stock_id(gtk.STOCK_PREFERENCES)
        self.toolbar_item06.connect("clicked", self.SJLiveSetting)
        self.toolbar.insert(self.toolbar_item06,5)

        self.toolbar_item07 = gtk.ToolButton("SnapshotNahled")
        self.toolbar_item07.set_stock_id(gtk.STOCK_PRINT_PREVIEW)
        self.toolbar_item07.connect("clicked", self.MakeSnap,1)
        self.toolbar.insert(self.toolbar_item07,6)

        self.toolbar_item08 = gtk.ToolButton("SnapshotRAW")
        self.toolbar_item08.set_stock_id(gtk.STOCK_PRINT)
        self.toolbar_item08.connect("clicked", self.MakeSnap,2)
        self.toolbar.insert(self.toolbar_item08,7)
        
        adjV = gtk.Adjustment(1, 1, 120, 1, 1, 0)
        adjH = gtk.Adjustment(1, 1, 120, 1, 1, 0)
        self.scrollImg = gtk.ScrolledWindow(adjH, adjV)
        self.kostra.pack_start(self.scrollImg, True, True)
        self.image = gtk.Image()
        self.image.set_from_file("icon.png")
        self.scrollImg.add_with_viewport(self.image)

        progressbar = gtk.ProgressBar()
        progressbar.set_fraction(random.random())
        self.kostra.pack_start(progressbar, False, False)
        
        self.show_all()
        gtk.main()

    def MakeSnap(self, widget, witch):
        #if witch.isdigit():
        self.SnapshotMessage=witch

    def SJLiveSetting(self, widget):

        okno = gtk.Window()
        okno.move(100,100)
        okno.resize(350,500)
        okno.set_title("Setting")

        adjV = gtk.Adjustment(1, 1, 120, 1, 1, 5)
        adjH = gtk.Adjustment(1, 1, 120, 1, 1, 5)
        scrollSet = gtk.ScrolledWindow(adjH, adjV)
        okno.add(scrollSet)
        kostra = gtk.VBox()

        self.HboxSetting = gtk.HBox(False,2)


        frKamera = gtk.Frame("Nastavení kamery")
        # Vytvoreni a vyplneni tabulky
        tabGeneral = gtk.Table(5, 2, True) # 2 radky, 2 sloupce a stejna velikost policek
        tabGeneral.set_row_spacings(2)
        tabGeneral.set_col_spacings(5)


# Nastaveni - Zdroj kamery
        #hbkamera = gtk.HBox(False, 2)
        labelKamera = gtk.Label("Kamera:")
        self.cbKamera = gtk.combo_box_new_text()
        self.cbKamera.append_text(str(0))
        for x in xrange(0,10):
            if cv2.VideoCapture(x).isOpened():
                self.cbKamera.append_text(str(x))
        self.cbKamera.set_active( int(self.cfg.get("CAMERA","cam")) )
        self.cbKamera.connect("changed", self.KameraSettingChanged)
        tabGeneral.attach(labelKamera,0,1,0,1)
        tabGeneral.attach(self.cbKamera,1,2,0,1)


# Nastaveni - Zaverka
        #hbShutter = gtk.HBox(False, 2)
        labelShutter = gtk.Label("Zaverka: 1/")
        adjShutter = gtk.Adjustment(100, 1, 1000, 1, 1, 0)
        self.sbShutter = gtk.SpinButton(adjShutter,1,0)
        self.sbShutter.set_value( float(self.cfg.get("CAMERA","shutter")) )
        self.sbShutter.connect("changed", self.KameraSettingChanged)

        tabGeneral.attach(labelShutter,0,1,1,2)
        tabGeneral.attach(self.sbShutter,1,2,1,2)

# Nastaveni - FrameRate
        #hbFPS = gtk.HBox(False, 2)
        labelFPS = gtk.Label("Snimkovaci rychlost FPS: ")
        adjFPS = gtk.Adjustment(1, 0.01, 120, 0.01, 0.01, 0)
        self.sbFPS = gtk.SpinButton(adjFPS,0.01,2)
        self.sbFPS.set_value( float(self.cfg.get("CAMERA","fps")) )
        self.sbFPS.connect("changed", self.KameraSettingChanged)

        tabGeneral.attach(labelFPS,0,1,2,3)
        tabGeneral.attach(self.sbFPS,1,2,2,3)

        frKamera.add(tabGeneral)
        kostra.pack_start(frKamera, False, False, 10)


        frMaska = gtk.Frame("Nastavení Masky")
        # Vytvoreni a vyplneni tabulky
        tabMaska = gtk.Table(5, 2, True) # 2 radky, 2 sloupce a stejna velikost policek
        tabMaska.set_row_spacings(2)
        tabMaska.set_col_spacings(5)

        labelZobrazMasku = gtk.Label("Zobrazit masku:")
        self.cbZobrazMasku = gtk.combo_box_new_text()
        self.cbZobrazMasku.append_text("Vypnuto")
        self.cbZobrazMasku.append_text("Obrys - silný")
        self.cbZobrazMasku.append_text("Obrys - slabý")
        self.cbZobrazMasku.append_text("Obsah")
        self.cbZobrazMasku.append_text("Přesah")
        self.cbZobrazMasku.append_text("Maska")
        self.cbZobrazMasku.set_active( int(self.cfg.get("MASK","type")) )
        self.cbZobrazMasku.connect("changed", self.KameraSettingChanged)
        tabMaska.attach(labelZobrazMasku,0,1,0,1)
        tabMaska.attach(self.cbZobrazMasku,1,2,0,1)


        HboxMask = gtk.HBox()
        HboxX = gtk.HBox()
        HboxY = gtk.HBox()
        HboxR = gtk.HBox()

        labelX = gtk.Label("X")
        labelY = gtk.Label("Y")
        labelR = gtk.Label("R")

        adjX = gtk.Adjustment(1, 1, self.cam.get(3), 1, 1, 0)
        adjY = gtk.Adjustment(1, 1, self.cam.get(4), 1, 1, 0)
        adjR = gtk.Adjustment(1, 1, self.cam.get(3), 1, 1, 0)

        self.sbMaskX = gtk.SpinButton(adjX,1,0)
        self.sbMaskY = gtk.SpinButton(adjY,1,0)
        self.sbMaskR = gtk.SpinButton(adjR,1,0)

        HboxX.pack_start(labelX)
        HboxX.pack_start(self.sbMaskX)
        HboxY.pack_start(labelY)
        HboxY.pack_start(self.sbMaskY)
        HboxR.pack_start(labelR)
        HboxR.pack_start(self.sbMaskR)

        self.sbMaskX.set_value( float(self.cfg.get("MASK","maskX")) )
        self.sbMaskY.set_value( float(self.cfg.get("MASK","maskY")) )
        self.sbMaskR.set_value( float(self.cfg.get("MASK","maskR")) )

        self.sbMaskX.connect("changed", self.KameraSettingChanged)
        self.sbMaskY.connect("changed", self.KameraSettingChanged)
        self.sbMaskR.connect("changed", self.KameraSettingChanged)

        HboxMask.pack_start(HboxX)
        HboxMask.pack_start(HboxY)
        HboxMask.pack_start(HboxR)
        tabMaska.attach(HboxMask,0,2,1,2)

        frMaska.add(tabMaska)
        kostra.pack_start(frMaska, False, False, 10)

        labelHist = gtk.Label("Zobrazit Histogram:")
        self.cbHist = gtk.combo_box_new_text()
        self.cbHist.append_text("Vypnuto")
        self.cbHist.append_text("In SJ - I")
        self.cbHist.append_text("In SJ - II")
        self.cbHist.append_text("In SJ - III")
        self.cbHist.append_text("In SJ - IV")
        self.cbHist.append_text("Vlastní okno")
        self.cbHist.set_active( int(self.cfg.get("MASK","hist")) )
        self.cbHist.connect("changed", self.KameraSettingChanged)
        tabMaska.attach(labelHist,0,1,2,3)
        tabMaska.attach(self.cbHist,1,2,2,3)

        self.cbScale = gtk.HScale()
        self.cbScale.set_range(0, 100)
        self.cbScale.set_increments(1, 10)
        self.cbScale.set_digits(0)
        self.cbScale.set_size_request(160, 35)
        self.cbScale.set_value( int(self.cfg.get("MASK","scaleOver")) )
        self.cbScale.connect("value-changed", self.KameraSettingChanged)
        tabMaska.attach( self.cbScale,0,2,3,4)

        labelPlotFlare = gtk.Label("Vykreslení erupcí:")
        self.cbPlotFlare = gtk.combo_box_new_text()
        self.cbPlotFlare.append_text("Vypnuto")
        self.cbPlotFlare.append_text("Red")
        self.cbPlotFlare.append_text("Blue")
        self.cbPlotFlare.append_text("In JS - III")
        self.cbPlotFlare.append_text("In JS - IV")
        self.cbPlotFlare.append_text("Vlastní okno")
        self.cbPlotFlare.set_active( int(self.cfg.get("MASK","type")) )
        self.cbHist.connect("changed", self.KameraSettingChanged)
        tabMaska.attach(labelPlotFlare,0,1,4,5)
        tabMaska.attach(self.cbPlotFlare,1,2,4,5)


        scrollSet.add_with_viewport(kostra)
        okno.show_all()



    def KameraSettingChanged(self,widget):
        print "Změna v 'KameraSetting':"

        #print "ziskano1: ", self.cam.get() 
        if widget is self.cbKamera:
            self.cam.set(6, self.sbFPS.get_value())
            self.cam.release()
            self.cam = cv2.VideoCapture(int(self.cbKamera.get_active()))
            print"RES",self.cam.get(3),self.cam.get(4)
            #print self.sbMaskX.get_value(), ":::::::::::;"
            self.sbMaskX.set_value( int(int(self.cam.get(3))/2) )
            self.sbMaskY.set_value( int(int(self.cam.get(4))/2) )
            
            self.cfg.set('CAMERA','cam',self.cbKamera.get_active())
            self.cfg.set('CAMERA','camx',self.cam.get(3))
            self.cfg.set('CAMERA','camy',self.cam.get(4))
            self.cfg.set('MASK','maskX', int(int(self.cam.get(3))/2) )
            self.cfg.set('MASK','maskY', int(int(self.cam.get(4))/2) )
            #self.sbMaskX.set_value()
            #elf.sbMaskX.get_value()

        self.cfg.set('CAMERA','FPS',self.sbFPS.get_value())
        self.cfg.set('CAMERA','shutter',self.sbShutter.get_value())
        self.cfg.set('MASK','type', self.cbZobrazMasku.get_active())
        self.cfg.set('MASK','hist', self.cbHist.get_active())
        #print "---------", self.sbMaskX.get_value()
        self.cfg.set('MASK','maskR',int( self.sbMaskR.get_value()) )
        self.cfg.set('MASK','maskX',int( self.sbMaskX.get_value()) )
        self.cfg.set('MASK','maskY',int( self.sbMaskY.get_value()) )
        self.cfg.set('MASK','scaleOver',int( self.cbScale.get_value()) )

        if self.ImgSource:
            self.SJLiveOpen(widget)


        with open('LiveSJ.ini', 'w') as configfile:    # save
            self.cfg.write(configfile)


    #    cap.set(1, 1)    # CV_CAP_PROP_POS_MSEC               Current position of the video file in milliseconds.
    #    cap.set(2, 1)    # CV_CAP_PROP_POS_FRAMES             0-based index of the frame to be decoded/captured next.
    #    cap.set(3, 1)    # CV_CAP_PROP_POS_AVI_RATIO          Relative position of the video file
    #    cap.set(4, 1)    # CV_CAP_PROP_FRAME_WIDTH            Width of the frames in the video stream.
    #    cap.set(5, 1)    # CV_CAP_PROP_FRAME_HEIGHT           Height of the frames in the video stream.
    #    cap.set(6, 1)    # CV_CAP_PROP_FPS                    Frame rate.
    #    cap.set(7, 1)    # CV_CAP_PROP_FOURCC                 4-character code of codec.
    #    cap.set(8, 1)    # CV_CAP_PROP_FRAME_COUNT            Number of frames in the video file.
    #    cap.set(9, 1)    # CV_CAP_PROP_FORMAT                 Format of the Mat objects returned by retrieve() .
    #    cap.set(10, 1)   # CV_CAP_PROP_MODE                   Backend-specific value indicating the current capture mode.
    #    cap.set(11, 1)   # CV_CAP_PROP_BRIGHTNESS             Brightness of the image (only for cameras).
    #    cap.set(12, 1)   # CV_CAP_PROP_CONTRAST               Contrast of the image (only for cameras).
    #    cap.set(13, 1)   # CV_CAP_PROP_SATURATION             Saturation of the image (only for cameras).
    #    cap.set(14, 1)   # CV_CAP_PROP_HUE                    Hue of the image (only for cameras).
    #    cap.set(15, 1)   # CV_CAP_PROP_GAIN                   Gain of the image (only for cameras).
    #    cap.set(16, 1)   # CV_CAP_PROP_EXPOSURE               Exposure (only for cameras).
    #    cap.set(17, 1)   # CV_CAP_PROP_CONVERT_RGB            Boolean flags indicating whether images should be converted to RGB.
    #    cap.set(18, 1)   # CV_CAP_PROP_WHITE_BALANCE          Currently unsupported
    #    cap.set(19, 1)   # CV_CAP_PROP_RECTIFICATION          Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)

    
    def SJLiveStop(self, widget):
        print "SJLiveStop"

        self.play=False
        self.cam.release()
        

    def SJLivePlay(self, widget):
        print "SJLivePlay"
        self.play = True


        print "Starting "

        self.cam.set(15, 0.1)
        s, img = self.cam.read()
        cv2.imwrite("test.png", img)
        self.image.set_from_file("test.png")
        self.show_all()
        Playcfg = ConfigParser.RawConfigParser()
        Playcfg.read("LiveSJ.ini")


        while self.play:
            Playcfg.read("LiveSJ.ini")
            s, img = self.cam.read()
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)


            if self.SnapshotMessage is 2:
                print "Ulozit cisty snimek"

                im = Image.fromarray(img)
                im.save("testb.png")
                self.SnapshotMessage = 0


            if int(Playcfg.get("MASK","hist")) is 0:
                a = numpy.asarray(img)
            else:
                height, width, depth = img.shape
                mask_image = cv2.imread('mask.png',0)
                mask_image = cv2.resize(mask_image , (width,height))
                cv2.circle(mask_image, ( int(Playcfg.get("MASK","maskx")),int(Playcfg.get("MASK","masky")) ), int(Playcfg.get("MASK","maskr"))+1,(255,255,255),-1)
                cv2.imwrite("makout.png",mask_image)
                a = numpy.asarray(MakeHist(img,100,200,int(Playcfg.get("MASK","hist")),mask_image))


            ret,a = cv2.threshold(a,self.cfg.getint("MASK","scaleOver")*2,255,cv2.THRESH_TOZERO)

            if int(Playcfg.get("MASK","type")) is 0:
                pass
            elif int(Playcfg.get("MASK","type")) is 1:
                cv2.circle(a, ( int(Playcfg.get("MASK","maskx")),int(Playcfg.get("MASK","masky")) ), int(Playcfg.get("MASK","maskr"))+2,(150,150,150),3, cv2.CV_AA)    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
            elif int(Playcfg.get("MASK","type")) is 2:
                cv2.circle(a, ( int(Playcfg.get("MASK","maskx")),int(Playcfg.get("MASK","masky")) ), int(Playcfg.get("MASK","maskr"))+1,(150,150,150),1, cv2.CV_AA)    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
                cv2.circle(a, ( int(Playcfg.get("MASK","maskx")),int(Playcfg.get("MASK","masky")) ), int(Playcfg.get("MASK","maskr"))+5,(150,150,150),2, cv2.CV_AA)    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])   
            self.image.set_from_pixbuf( gtk.gdk.pixbuf_new_from_array(a, gtk.gdk.COLORSPACE_RGB, 8) )
            if self.SnapshotMessage is 1:
                print "Ulozit Pixbuf snimek"
                im = Image.fromarray(a)
                im.save('test.png')
                self.SnapshotMessage = 0

            self.show_all()
            while gtk.events_pending():
                gtk.main_iteration()
        print "Exiting "

    def getfile(self):
        print "Otevrit neco"
        dialog = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            print dialog.get_filename(), 'selected'
        elif response == gtk.RESPONSE_CANCEL:
           print 'Closed, no files selected'
        fileA = dialog.get_filename()
        dialog.destroy()
        return fileA

    def SJLiveOpen(self, widget):
        self.play = True

        if not self.ImgSource:
            self.ImgSource = True
            self.ImgPath = self.getfile()

            img = cv2.imread(self.ImgPath)
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

            self.toolbar_item03.set_stock_id(gtk.STOCK_CLOSE)

            height, width, depth = img.shape
            print  height, width

            #self.sbMaskX.set_range( 1, width )
            #self.sbMaskY.set_range( 1, height)
            #self.sbMaskR.set_range( 1, width )

            Playcfg = ConfigParser.RawConfigParser()
            Playcfg.read("LiveSJ.ini")


            if self.SnapshotMessage is 2:
                print "Ulozit cisty snimek"

                im = Image.fromarray(img)
                im.save("testb.png")
                self.SnapshotMessage = 0


            if int(Playcfg.get("MASK","hist")) is 0:
                a = numpy.asarray(img)
            else:
                height, width, depth = img.shape
                mask_image = cv2.imread('mask.png',0)
                mask_image = cv2.resize(mask_image , (width,height))
                cv2.circle(mask_image, ( int(Playcfg.get("MASK","maskx")),int(Playcfg.get("MASK","masky")) ), int(Playcfg.get("MASK","maskr"))+1,(255,255,255),-1)
                cv2.imwrite("makout.png",mask_image)
                a = numpy.asarray(MakeHist(img,100,200,int(Playcfg.get("MASK","hist")),mask_image))


            ret,a = cv2.threshold(a,self.cfg.getint("MASK","scaleOver")*2,255,cv2.THRESH_TOZERO)

            if int(Playcfg.get("MASK","type")) is 0:
                pass
            elif int(Playcfg.get("MASK","type")) is 1:
                cv2.circle(a, ( int(Playcfg.get("MASK","maskx")),int(Playcfg.get("MASK","masky")) ), int(Playcfg.get("MASK","maskr"))+2,(150,150,150),3, cv2.CV_AA)    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
            elif int(Playcfg.get("MASK","type")) is 2:
                cv2.circle(a, ( int(Playcfg.get("MASK","maskx")),int(Playcfg.get("MASK","masky")) ), int(Playcfg.get("MASK","maskr"))+1,(150,150,150),1, cv2.CV_AA)    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
                cv2.circle(a, ( int(Playcfg.get("MASK","maskx")),int(Playcfg.get("MASK","masky")) ), int(Playcfg.get("MASK","maskr"))+5,(150,150,150),2, cv2.CV_AA)    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])   
            self.image.set_from_pixbuf( gtk.gdk.pixbuf_new_from_array(a, gtk.gdk.COLORSPACE_RGB, 8) )
            if self.SnapshotMessage is 1:
                print "Ulozit Pixbuf snimek"
                im = Image.fromarray(a)
                im.save('test.png')
                self.SnapshotMessage = 0

            self.show_all()

        elif self.ImgSource and widget is not self.toolbar_item03:

            self.toolbar_item03.set_stock_id(gtk.STOCK_CLOSE)

            Playcfg = ConfigParser.RawConfigParser()
            Playcfg.read("LiveSJ.ini")

            img = cv2.imread(self.ImgPath)
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

            if int(Playcfg.get("MASK","hist")) is 0:
                a = numpy.asarray(img)
            else:
                a = numpy.asarray(MakeHist(img,100,200,int(Playcfg.get("MASK","hist")),None))

            ret,a = cv2.threshold(a,self.cfg.getint("MASK","scaleOver")*2,255,cv2.THRESH_TOZERO)


            if int(Playcfg.get("MASK","type")) is 0:
                pass
            elif int(Playcfg.get("MASK","type")) is 1:
                cv2.circle(a, ( int(Playcfg.get("MASK","maskx")),int(Playcfg.get("MASK","masky")) ), int(Playcfg.get("MASK","maskr"))+2,(150,150,150),3, cv2.CV_AA)    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
            elif int(Playcfg.get("MASK","type")) is 2:
                cv2.circle(a, ( int(Playcfg.get("MASK","maskx")),int(Playcfg.get("MASK","masky")) ), int(Playcfg.get("MASK","maskr"))+1,(150,150,150),1, cv2.CV_AA)    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
                cv2.circle(a, ( int(Playcfg.get("MASK","maskx")),int(Playcfg.get("MASK","masky")) ), int(Playcfg.get("MASK","maskr"))+5,(150,150,150),2, cv2.CV_AA)    # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])   
            self.image.set_from_pixbuf( gtk.gdk.pixbuf_new_from_array(a, gtk.gdk.COLORSPACE_RGB, 8) )

            self.show_all()

        elif self.ImgSource and widget is self.toolbar_item03:
            self.ImgSource = False
            self.toolbar_item03.connect("clicked", self.SJLiveOpen)


    def info(self, widget, text):
        md = gtk.MessageDialog(self, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, "Download completed"+text)
        md.run()
        md.destroy()

def main():
    print "Succesfly loaded modul LiveSJ"
    Okno = LiveSJ()
    Okno.spust()