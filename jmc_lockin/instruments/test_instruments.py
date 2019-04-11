import numpy as np

def main():

    from jmc_lockin.instruments.lockin import SR530
    from jmc_lockin.instruments.temp_humedad_epeloa import EpeloaSensor

    lockin = SR530()
    epeloa = EpeloaSensor()
    epeloa.set_port('/dev/ttyUSB1')
    print(lockin.get_serial_conn('/dev/ttyUSB0'))
    for i in np.arange(0.0, 10.0, 0.1):
        lockin.set_output_v(5, i)
        unlk = lockin.get_status_byte()
        while unlk:
            unlk = lockin.get_status_byte()
        t, h = epeloa.get_t_and_h()

        status = []
        for n in range(1, 8, 1):
            status.append(lockin.get_status_byte(n))

        return t, h, lockin.get_frequency(), lockin.get_channel(1), lockin.get_channel(2), status

    lockin.set_output_v(5, 0)


if __name__ == '__main__':
    main()