import sys, os, time
from PySide2.QtCore import Slot, Signal, SIGNAL
from PySide2 import QtWidgets, QtGui

from jmc_lockin.gui.Jmc_app_main_ui import MainApp
from jmc_lockin.threads.threads import Worker


# noinspection PyTypeChecker
class JMCLOCKINDAQ(QtWidgets.QMainWindow, MainApp):

    def __init__(self):
        super(JMCLOCKINDAQ, self).__init__()
        self.setupUi(self)
        self.load_cbx_data()
        self.worker = Worker()

    def connect_thread_signals(self):
        """

        Worker *worker = new Worker;
        worker->moveToThread(&workerThread);
        connect(&workerThread, &QThread::finished, worker, &QObject::deleteLater);
        connect(this, &Controller::operate, worker, &Worker::doWork);
        connect(worker, &Worker::resultReady, this, &Controller::handleResults);
        workerThread.start();
        :return:
        """
        self.worker.moveToThread(self.thread())
        self.worker.data_ready.connect(self.receive_data)
        self.worker.status.connect(self.update_lockin_status)
        self.worker.msg.connect(self.change_messagge)

    @Slot()
    def on_pb_start_pressed(self):
        #TODO: Rutina para iniciar el ensayo
        self.worker.start()

    @Slot(object)
    def update_lockin_status(self, status):
        """
            :param status: Diccionario cuyas claves se corresponden con los nombres de los labels que indican el estado del
            lockin en la ventana principal lb_unlk, lb_err, lb_act, lb_ovld, lb_rem
        """

        for key, value in status.items():
            if value:
                self.change_widget_text_color(self.__getattribute__(key), 245, 1, 1)
            else:
                self.change_widget_text_color(self.__getattribute__(key))

    @Slot(object)
    def receive_data(self, data):
        print(data)

    def load_available_devices(self):
        pass

    @Slot()
    def on_tlb_open_file_pressed(self):
        dialog = QtWidgets.QFileDialog()

        filename, _ = dialog.getSaveFileName(parent=self,
                                             caption="Guardar archivo de salida",
                                             dir=os.path.expanduser('~'),
                                             )

        if filename:
            self.le_output_file.setText(filename)


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
                print(err)
                DAQ.change_messagge('Error al cargar los dispositivos.{}'.format(err),
                                    duration=5000
                                    )
        if i == 70:
            DAQ.connect_thread_signals()

        while time.time() < t + 0.03:

            app.processEvents()

    DAQ.show()
    splash.finish(DAQ)
    sys.exit(app.exec_())


if __name__ == '__main__':

    main()

