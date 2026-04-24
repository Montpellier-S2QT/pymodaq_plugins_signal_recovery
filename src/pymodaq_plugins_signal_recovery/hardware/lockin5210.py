# -*- coding: utf-8 -*-

import numpy as np
import pyvisa
import time

class LockIn5210():


    def open_communication(self, port):
        initialized = False
        timeout = time.time() + 10
        my_id = None

        while (not initialized) and (time.time() < timeout):
            try:
                rm = pyvisa.ResourceManager()
                self._device = rm.open_resource(port)
                self._device.baud_rate = 19200
                self._device.data_bits = 7
                self._device.parity = pyvisa.constants.Parity.even
                self._device.stop_bits = pyvisa.constants.StopBits.one
                self._device.read_termination = '\r\n'
                my_id = self._device.query('ID')
                initialized = True

            except:
                time.sleep(1)

        if not initialized:
            print('Resource could not be initialized')

        return my_id, initialized

    def close_communication(self):
        self._device.close()

    def get_acquired_data(self):
        return np.array([int(self._device.query('X')[1:])])