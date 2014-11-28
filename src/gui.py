import sys
import LiveSJ

try:
    import pygtk
    pygtk.require("2.0")
    import gtk
except:
    print "Error: PyGTK and GTK 2.xx must be installed to run this application. Exiting"
    sys.exit(1)


class prvni_okno(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        #self.okno = gtk.Window()
        self.tlacitko = gtk.Button("self")
        self.set_title("Okno 1")
        #self.set_default_size(200, 100)
        self.move(40,40)
        self.kostra = gtk.VBox(homogeneous=False, spacing=3)
        #self.add(self.tlacitko)
        self.add(self.kostra)
        self.tlacitko.connect("clicked", gtk.main_quit)

        self.show_all()

    def spust(self):

        gtk.main()

    def MainScreen(self):
        objects = []

        self.set_title("SolarSpotFinder - "+"Home"+" v."+str(0.1))
 
        objects.append([0, "LiveWiew" , "LiveWiewShow", "LiveWiewSetting", " -data3", " -data4"])
        objects.append([1, "LiveSpectrum" , " -data1", " -data2", " -data3", " -data4"])
        objects.append([2, "LiveWiew" , " -data1", " -data2", " -data3", " -data4"])

        for obj in objects:
            print "---" + str(obj[0]),obj[1]
            obj[0] = gtk.Button(str(obj[1]))
            self.kostra.pack_start(obj[0], True)
            obj[0].connect("clicked", getattr(self, obj[1]))

        self.tlExit = gtk.Button("Exit")
        self.tlExit.connect("clicked", exit)
        self.kostra.pack_end(self.tlExit, True)

        self.show_all()

    def info(self, widget, text):
        md = gtk.MessageDialog(self, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, "Download completed"+text)
        md.run()
        md.destroy()

    def LiveWiew(self, widget):
        print "LiveWiew connector"
        LiveSJ.main()

    def LiveSpectrum(self, widget):
        print "LiveSpectrum connector"


if __name__ == "__main__" :

    aplikace = prvni_okno()
    aplikace.MainScreen()

    aplikace.spust()