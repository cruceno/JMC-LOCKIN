# -*- coding: utf-8 -*-

"""

Created on 05/09/2016

@author: Cruceno Javier
    
"""

from time import sleep
import serial

_SENSITIVITIES = {'1': ('10', 'nV', 1e9),
                  '2': ('20', 'nV', 1e9),
                  '3': ('50', 'nV', 1e9),
                  '4': ('100', 'nV', 1e9),
                  '5': ('200', 'nV', 1e9),
                  '6': ('500', 'nV', 1e9),
                  '7': ('1', 'uV', 1e6),
                  '8': ('2', 'uV', 1e6),
                  '9': ('5', 'uV', 1e6),
                  '10': ('10', 'uV', 1e6),
                  '11': ('20', 'uV', 1e6),
                  '12': ('50', 'uV', 1e6),
                  '13': ('100', 'uV', 1e6),
                  '14': ('200', 'uV', 1e6),
                  '15': ('500', 'uV', 1e6),
                  '16': ('1', 'mV', 1e3),
                  '17': ('2', 'mV', 1e3),
                  '18': ('5', 'mV', 1e3),
                  '19': ('10', 'mV', 1e3),
                  '20': ('20', 'mV', 1e3),
                  '21': ('50', 'mV', 1e3),
                  '22': ('100', 'mV', 1e3),
                  '23': ('200', 'mV', 1e3),
                  '24': ('500', 'mV', 1e3),
                  }

_PRE_TIME_CONSTANTS = {'1': (1, 'mS'),
                       '2': (3, 'mS'),
                       '3': (10, 'mS'),
                       '4': (30, 'mS'),
                       '5': (100, 'mS'),
                       '6': (300, 'mS'),
                       '7': (1, 'S'),
                       '8': (3, 'S'),
                       '9': (10, 'S'),
                       '10': (30, 'S'),
                       '11': (100, 'S')
                       }

_POST_TIME_CONSTANTS = {
                        '0': 'None',
                        '1': '0.1',
                        '2': '1'
                        }

_CHANNEL_OPTIONS = {
                    '0': ('X', 'Y'),
                    '1': ('X Offset', 'Y Offset'),
                    '2': ('R', '\u03F4'),
                    '3': ('R Offset', '\u03F4'),
                    '4': ('X Noise', 'Y Noise'),
                    '5': ('X5 D/A', 'X6 D/A')
                    }

_SINUSOIDAL_SCALES = {0: '10 mV', 1: '100 mV', 2: '1 V'}

_OSCILLATOR_RANGE = {0: '1 Hz/V', 1: '100 Hz/V', 2: '10 KHz/V'}


class SR530:

    """

        SOFTWARE DE COMUNICACION CON LOCK-IN SR530
        INTERFACE: RS232

    """
    serial = serial.Serial()

    def get_serial_conn(self, s_port):
        import serial
        try:
            self.serial = serial.Serial(
                            port=s_port,
                            baudrate=19200,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            timeout=2

                            )

            self.serial.close()
            sleep(1)
            self.serial.open()
            # self.write('Z\r')#Resetea el Lock-In la luz ERR se encendera por 3 seg
            # sleep(4)
            # Pone el valor de espera entre envio de caracteres del lock-in en 4ms
            self.write('W 1\r')
            jcmd = 'J '+str(ord('\n'))
            # Especifica el fin de linea enviado por el lock in en <cr>
            self.write(jcmd)

            return 'Conectado.'
            
        except Exception as e:

            return 'Error al conectar al puerto serie: {}'.format(str(e))

    def get_channel(self, n):

        self.write('Q {}'.format(n))
        return self.read().decode().strip('\n')

    def set_output_v(self, n, v):

        if (n == 5 or n == 6) and (-10 <= v <= 10):
            self.write('X{}, {}'.format(n, v))

    def get_ad_v(self, n):
        if 0 < n < 7:
            self.write('X{}'.format(n))
            return self.read()
        else:
            return "El valor de n debe estar entre 1 y 4"

    def get_sensitivity(self):

        self.write('G')    
        s = self.read().decode().strip('\n')
        return _SENSITIVITIES[s]

    def set_sensitivity(self, s):
        self.write('G{}'.format(s))

    def get_frequency(self):
        self.write('F')
        return self.read().strip(b'\n').decode()

    def read(self):

        return self.serial.readline()

    def write(self, command):
        command=command+'\r'
        self.serial.write(command.encode())

    def get_status_byte(self, n=3):
        self.write('Y {}'.format(n))
        return bool(int(self.read().strip(b'\n')))

    def reset(self):
        self.write('Z')

    def get_status(self):

        """

          Funcion para obtener el estado de todas las configuraciones del lock-in.
          Utiliza: read() write().
          Devuelve: Diccionario con los parametros de configuracion.

        """

        sr530commands = {'bandpass': 'B',
                         'dyn': 'D',
                         'ref-display': 'C',
                         'expandch1': 'E1',
                         'expandch2': 'E2',
                         'frequency': 'F',
                         'gain': 'G',
                         'pre-amplifier': 'H',
                         'remote': 'I',
                         'line-filter': 'L1',
                         'linex2-filter': 'L2',
                         'ref-mode': 'M',
                         'enbw': 'N',
                         'offsertx': 'OX',
                         'offserty': 'OY',
                         'offsertr': 'OR',
                         'phase-shift': 'P',
                         'ref-trigger': 'R',
                         'pre-time': 'T1',
                         'post-time': 'T2',
                         'aportx1': 'X1',
                         'aportx2': 'X2',
                         'aportx3': 'X3',
                         'aportx4': 'X4',
                         'aportx5': 'X5',
                         'aportx6': 'X6',
                         }
        state = ""
        for cfg, value in sr530commands.items():
            self.write(value+'\r')
            state += cfg + ': ' + self.read().decode()

        return state
    
    def __del__(self):
        self.serial.close()
