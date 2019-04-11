import sys, os, time

from PySide2.QtCore import Slot, QThread, Signal, SIGNAL
from PySide2 import QtWidgets, QtGui
from jmc_lockin.gui.Jmc_app_main_ui import MainApp
import numpy as np
from configobj import ConfigObj


# noinspection PyTypeChecker
class JMCLOCKINDAQ(QtWidgets.QMainWindow, MainApp):

    def __init__(self):
        super(JMCLOCKINDAQ, self).__init__()
        self.setupUi(self)
        self.load_cbx_data()

    def load_available_devices(self):
        pass

    def connect_worker(self):
        pass

    def change_message(self, msg):
        self.statusbar.showMessage(msg, 5000)


# noinspection PyTypeChecker
def main():

    app = QtWidgets.QApplication(sys.argv)
    # Create a pixmap - not needed if you have your own.
    QtGui.QFontDatabase.addApplicationFont('./gui/fonts/EXO2REGULAR.TTF')
    app.processEvents()
    DAQ = JMCLOCKINDAQ()

    from jmc_lockin.gui.splash import SplashScreen
    pixmap = QtGui.QPixmap('./gui/images/splash.png')
    splash = SplashScreen(pixmap)
    splash.setTitle('Lock-in SR530')
    splash.show()

    splash.connect(DAQ,
                   SIGNAL('splashUpdate(QString, int)'),
                   splash.showMessage)

    for i in range(0, 101):
        splash.progressBar.setValue(i)
        # Do something which takes some time.
        t = time.time()

        if i == 5:
            try:
                DAQ.load_available_devices()
            except Exception as err:
                print (err)
                DAQ.change_messagge('Error al cargar los dispositivos.{}'.format(err),
                                    duration=5000
                                    )
        if i == 70:
            DAQ.connect_worker()

        while time.time() < t + 0.03:

            app.processEvents()

    DAQ.show()
    splash.finish(DAQ)
    sys.exit(app.exec_())


if __name__ == '__main__':

    main()

