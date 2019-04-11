# function[temperatura, humedad] = serie()
# global puerto_serial;
# PS = serial(puerto_serial);
# set(PS, 'Baudrate', 9600); % se
# configura la velocidad a 9600 Baudios
# set(PS, 'StopBits', 1); % se configura bit de parada a uno
# set(PS, 'DataBits', 8); % se configura que el dato es de 8 bits, debe estar entre 5 y 8
# set(PS, 'Parity', 'none'); % se configura sin paridad
# set(PS, 'Terminator', 'CR/LF'); % �c� caracter con que finaliza el env�o
# set(PS, 'OutputBufferSize', 1); % �n� es el n�mero de bytes a enviar
# set(PS, 'InputBufferSize', 24); % �n� es el n�mero de bytes a recibir
# set(PS, 'Timeout', 30); % 30 segundos de tiempo de espera despues lo tango que bajar el sistema envia
# mucho mas rapido, en milisegundos ya estaria
# fopen(PS);
# a = fread(PS, 24, 'uchar');
# a = a
# ';
# if numel(a) == 24
#     if a(1) == 't' & & a(2) == 'b' & & a(3) == 'a' & & a(4) == 'j' & & a(5) == 'a'
#         t_unidad = a(6);
# end
# if a(7) == 't' & & a(8) == 'a' & & a(9) == 'l' & & a(10) == 't' & & a(11) == 'a'
#     t_decena = a(12);
# end
#
# if a(13) == 'h' & & a(14) == 'b' & & a(15) == 'a' & & a(16) == 'j' & & a(17) == 'a'
#     h_unidad = a(18);
# end
#
# if a(19) == 'h' & & a(20) == 'a' & & a(21) == 'l' & & a(22) == 't' & & a(23) == 'a'
#     h_decena = a(24);
# end
# fclose(PS);
# tsensor = 256 * t_decena + t_unidad;
# hsensor = 256 * h_decena + h_unidad;
#
# temperatura = -39.9 + 0.01. * tsensor;
#
# humedad = -2.0468 + 0.0367. * hsensor - 1.5955e-06;
# humedad = (temperatura - 25). * (0.01 + 0.00008. * hsensor) + humedad; % ver
#
# else
# disp('error de lectura'); % % aca puedo mandar esta salida a la interfaz para que me muestre el error
# fclose(PS);
# end
# return;

import serial
import time


class EpeloaSensor:

    def __init__(self):
        super(EpeloaSensor, self).__init__()
        self.serial = serial.Serial(baudrate=9600,
                                    stopbits=serial.STOPBITS_ONE,
                                    parity=serial.PARITY_NONE,
                                    bytesize=serial.EIGHTBITS,
                                    timeout=2)
        self.eof = b'\r\n'
        self.input_buffer_size = 24
        self.output_buffer_size = 1
        self.serial.close()

    def set_port(self, port):
        self.serial.setPort(port)

    def get_t_and_h(self):
        lectura=b''
        tsensor = False
        hsensor = False
        try:
            self.serial.open()
            while len(lectura) != 24:
                lectura = self.serial.read(24)
                if len(lectura) == 24:
                    if lectura[0:5] == b'tbaja':
                        t_unidad = lectura[5]
                        if lectura[6:11]==b'talta':
                            t_decena = lectura[11]
                            tsensor = 256 * t_decena + t_unidad
                    if lectura[12:17] == b'hbaja':
                        h_unidad=lectura[17]
                        if lectura[18:23]==b'halta':
                            h_decena = lectura[23]
                            hsensor = 256 * h_decena + h_unidad
                    if tsensor and hsensor:
                        self.serial.close()
                        temperatura = -39.9 + 0.01 * tsensor
                        humedad = -2.0468 + 0.0367 * hsensor - 1.5955e-06
                        humedad = (temperatura - 25) * (0.01 + 0.00008 * hsensor) + humedad
                        return round(temperatura, 4), round(humedad, 4)
                    else:
                        self.serial.close()
                        print("Mala lectura: ", lectura)

        except Exception as e:
            self.serial.close()
            print("No se pudo abrir el puerto seleccionado: {}".format(str(e)))
        self.serial.close()
