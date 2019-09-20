import numpy as np
from PySide2.QtCore import QThread, Signal
from jmc_lockin.instruments.lockin import SR530
from jmc_lockin.instruments.temp_humedad_epeloa import EpeloaSensor


class Worker(QThread):
    status = Signal(object)
    data_ready = Signal(object)
    msg = Signal(str)
    _status_keys = {'lb_err': 7,
                    'lb_unlk': 3,
                    'lb_ovld': 4,
                    }

    def __init__(self):
        super(Worker, self).__init__()

        self.lockin = SR530()
        self.epeloa = EpeloaSensor()
        self.f_mode = ""
        self.f_v_start = 0.0
        self.f_v_step = 0.0
        self.f_v_end = 0.0

    def set_ports(self, lockin_port, epeloa_port):

        self.epeloa.set_port(epeloa_port)
        self.lockin.get_serial_conn(lockin_port)

    def set_f_mode(self, mode, ):
        """ Recibe un string como parametro
                F: Fixed mode
                S: Scanning mode
            El modo define como se utilizará la frecuencia durante el ensayo"""
        self.f_mode = mode

    def get_lockin_data(self):
        self.status.emit({'lb_act': True})
        lockin_freq = self.lockin.get_frequency(),
        self.status.emit({'lb_act': False})

        self.status.emit({'lb_act': True})
        lockin_x = self.lockin.get_output(1),
        self.status.emit({'lb_act': False})

        self.status.emit({'lb_act': True})
        lockin_y = self.lockin.get_output(2),
        self.status.emit({'lb_act': False})

        return lockin_freq, lockin_x, lockin_y

    def wait_for_lockin_lock(self):

        self.status.emit({'lb_act': True})
        unlk = self.lockin.get_status_byte()
        self.status.emit({'lb_act': False})
        while unlk:
            self.status.emit({'lb_act': True})
            unlk = self.lockin.get_status_byte()
            self.status.emit({'lb_act': False})
            self.status.emit({'lb_unlk': unlk})

    def check_lockin_status(self):
        status = {}
        for key, value in self._status_keys.items():
            self.status.emit({'lb_act': True})
            status[key] = self.lockin.get_status_byte(value)
            self.status.emit({'lb_act': False})
        self.status.emit(status)

    def acquire_routine(self, v):
        self.lockin.set_output_v(5, v)
        self.status.emit({'lb_act': True})
        t, h = self.epeloa.get_t_and_h()
        self.status.emit({'lb_act': False})
        # Comprueba estado del oscilador y envia informacion a l apantalla principal
        self.wait_for_lockin_lock()
        # Comprueba estado del lockin y envia informacion a la pagina principal.
        self.chek_lockin_status()
        lockin_freq, lockin_x, lockin_y = self.get_lockin_data()
        self.data_ready.emmit({
            'temperatura': t,
            'humedad': h,
            'lockin_freq': lockin_freq,
            'lockin_x': lockin_x,
            'lockin_y': lockin_y,
        })

    def run(self):
        while not self.isInterruptionRequested():
            if self.f_mode == 'S':
                for v in np.arange(self.f_v_start, self.f_v_end, self.f_v_step):
                    self.acquire_routine(v)
            elif self.f_mode == 'F':
                self.acquire_routine(self.f_v_start)
            self.msleep(10)
