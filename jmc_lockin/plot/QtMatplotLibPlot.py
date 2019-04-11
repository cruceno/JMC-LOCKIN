'''
Created on 6 abr. 2017

@author: cruce
'''

# Librerias para graficar en el ploter
import matplotlib; matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class canvas(FigureCanvas):

    def __init__(self, parent, double=False):

        # Se instancia el objeto figure
        self.fig = Figure()
        self.fig.set_alpha(0)
        self.fig.patch.set_facecolor('None')
        self.fig.patch.set_alpha(0.0)
        # Se define la grafica en coordenadas polares
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('None')
        self.axes.set_alpha(0.0)
        # Se define una grilla
        self.axes.grid(color='xkcd:mint green', linestyle='-', linewidth=0.5, visible=True)

        # se inicializa FigureCanvas
        super(canvas, self).__init__(self.fig)
        # se define el widget padre
        self.axes.tick_params(axis='x', colors='xkcd:mint green')
        self.axes.tick_params(axis='y', colors='xkcd:mint green')

        if double:
            self.ax2 = self.axes.twinx()
            self.ax2.tick_params('y', colors='xkcd:mint green')

        self.setParent(parent)
        self.fig.canvas.draw()

    def reload(self, double=False):
        self.axes.cla()
        # Se define una grilla
        self.axes.grid(True)

    def plot(self, x, y, y2=None, color1='r',color2='b', double=False ):

        # Dibujar Curva
        self.reload()
        if double:
            self.axes.plot(x, y, color1)
            self.ax2.plot(x, y2, color2)
        else:
            if y2:
                self.axes.plot(x, y, y2,  color1)
            else:
                self.axes.plot(x, y, color1)
        self.fig.canvas.draw()
