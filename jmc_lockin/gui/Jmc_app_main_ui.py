# Se importan los archivos generados por Pyside2-uic
import os
from .mainwindow import Ui_jmc_lockin

from PySide2.QtGui import (QIcon, QPixmap, QFont)
from jmc_lockin.instruments.lockin import ( _SENSITIVITIES, _OSCILLATOR_RANGE,_SINUSOIDAL_SCALES, _PRE_TIME_CONSTANTS,
                                           _POST_TIME_CONSTANTS )
from jmc_lockin.plot.QtMatplotLibPlot import canvas, NavigationToolbar
from PySide2.QtWidgets import QVBoxLayout, QFileDialog
from PySide2.QtCore import SIGNAL, Slot
import numpy as np

from jmc_lockin.instruments.serialutil import scan_serial_ports


class MainApp (Ui_jmc_lockin):

    def setupUi(self, app):

        super(MainApp, self).setupUi(app)
        # Generar los planos donde graficaremos los datos
        # Inicializar base de ploteo para mainplot

        app.vbl_xy_plot = QVBoxLayout(app.w_plot_xy)
        app.xy_canvas = canvas(app.w_plot_xy)
        app.xy_canvas.setStyleSheet("background-color:transparent;")
        # jmc_prensa_daq.presure_tlb = NavigationToolbar(jmc_prensa_daq.presure_canvas,
        #                                      jmc_prensa_daq.plot_e_p)
        app.vbl_xy_plot.insertWidget(0, app.xy_canvas)
        # jmc_prensa_daq.vbl_presure_plot.insertWidget(1, jmc_prensa_daq.presure_tlb)

        app.vbl_freq_plot = QVBoxLayout(app.w_plot_freq)
        app.f_canvas = canvas(app.w_plot_freq)
        app.f_canvas.setStyleSheet("background-color:transparent;")
        app.vbl_freq_plot.insertWidget(0, app.f_canvas)

        app.vbl_aux_plot = QVBoxLayout(app.w_plot_aux)
        app.aux_canvas = canvas(app.w_plot_aux, double=True)
        app.aux_canvas.setStyleSheet("background-color:transparent;")
        app.vbl_aux_plot.insertWidget(0, app.aux_canvas)

        font = QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        font.setWeight(50)
        font.setBold(False)
        app.setFont(font)

        icon = QIcon()
        icon.addPixmap(QPixmap("gui/images/logo-symbol-64x64.png"),
                       QIcon.Normal,
                       QIcon.Off
                       )
        app.setWindowIcon(icon)

    def load_cbx_data(self):

        for device in scan_serial_ports():
            self.cbx_aux_1_port.addItem(device, device)
            self.cbx_lockin_port.addItem(device, device)

        for key, value in sorted(_PRE_TIME_CONSTANTS.items()):
            self.cbx_pre.addItem(' '. join([str(value[0]), str(value[1])]), key)

        for key, value in sorted(_POST_TIME_CONSTANTS.items()):
            self.cbx_post.addItem(str(value), key)

        for key, value in sorted(_OSCILLATOR_RANGE.items()):
            self.cbx_freq_range.addItem(str(value), key)

        for key, value in sorted(_SINUSOIDAL_SCALES.items()):
            self.cbx_sine_scale.addItem(str(value), key)

        self.cbx_sensitivity_scale.addItem('nV', 'nV')
        self.cbx_sensitivity_scale.addItem('uV', 'uV')
        self.cbx_sensitivity_scale.addItem('mV', 'mV')
        self.cbx_sensitivity_scale.setCurrentText('uV')

    @Slot(str)
    def on_cbx_sensitivity_scale_currentIndexChanged(self, index):

        if index == 'nV':
            self.hs_sensitivity_value.setMinimum(1)
            self.hs_sensitivity_value.setMaximum(6)
            self.hs_sensitivity_value.setPageStep(1)
            self.hs_sensitivity_value.setTracking(True)
            self.hs_sensitivity_value.setValue(1)

        elif index == 'uV':
            self.hs_sensitivity_value.setMinimum(7)
            self.hs_sensitivity_value.setMaximum(15)
            self.hs_sensitivity_value.setPageStep(1)
            self.hs_sensitivity_value.setTracking(True)
            self.hs_sensitivity_value.setValue(7)

        else:
            self.hs_sensitivity_value.setMinimum(16)
            self.hs_sensitivity_value.setMaximum(24)
            self.hs_sensitivity_value.setPageStep(1)
            self.hs_sensitivity_value.setTracking(True)
            self.hs_sensitivity_value.setValue(16)

    @Slot()
    def on_hs_sensitivity_value_valueChanged(self):
        selected = _SENSITIVITIES[str(self.hs_sensitivity_value.value())]
        self.lb_sensitivity_value.setText(' '.join([selected[0], selected[1]]))

    @staticmethod
    def get_cbx_data(cbx):
        return cbx.itemData(cbx.currentIndex())

    def splash_message(self, message):
        self.emit(SIGNAL("splashUpdate(QString, int)"),
                  message,
                  132)

    @Slot(bool)
    def on_chx_freq_scanning_toggled(self, state):
        self.lb_end_freq.setEnabled(state)
        self.dsb_end_freq.setEnabled(state)
        self.lb_freq_step.setEnabled(state)
        self.dsb_freq_step.setEnabled(state)

    @Slot()
    def change_messagge(self, message, duration=1000):
        self.statusbar.showMessage(message, duration)

    @staticmethod
    def change_widget_text_color(widget, r=255, g=255, b=255, a=100):
        widget.setStyleSheet("color: rgb({},{},{},{});".format(r, g, b, a))

