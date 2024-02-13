# -*- coding: utf-8 -*-

from enum import Enum
import numpy as np
import pyvisa
class LockIn5210():

    def get_ready_state(self):
        return True

    def open_communication(self, port):
        #port = 'ASRL3::INSTR' # A passer absolument en paramètre
        try:
            rm = pyvisa.ResourceManager()
            self._device = rm.open_resource(port)
            self._device.baud_rate = 19200  # en qudi, on avait mis 19200
            self._device.data_bits = 7
            self._device.parity = pyvisa.constants.Parity.even
            self._device.stop_bits = pyvisa.constants.StopBits.one
            self._device.read_termination = '\r\n'
            self._device.query('ID')
            initialized = True

        except:
            initialized = False

        return initialized

    def close_communication(self):
        self._device.close()

    def get_acquired_data(self):
        return np.array([int(self._device.query('X')[1:])])