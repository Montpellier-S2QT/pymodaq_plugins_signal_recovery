# -*- coding: utf-8 -*-

from enum import Enum
import numpy as np
import pyvisa
class LockIn5210():

    def open_communication(self, port):
        try:
            rm = pyvisa.ResourceManager()
            self._device = rm.open_resource(port)
            self._device.baud_rate = 19200
            self._device.data_bits = 7
            self._device.parity = pyvisa.constants.Parity.even
            self._device.stop_bits = pyvisa.constants.StopBits.one
            self._device.read_termination = '\r\n'
            id = self._device.query('ID')
            initialized = True

        except:
            initialized = False
            id = None

        return id, initialized

    def close_communication(self):
        self._device.close()

    def get_acquired_data(self):
        return np.array([int(self._device.query('X')[1:])])