# -*- coding: utf-8 -*-

from enum import Enum
import numpy as np
import pyvisa
class LockIn5210():

    def get_ready_state(self):
        return True

    def open_communication(self):
        address = 'ASRL3::INSTR' # A passer absolument en paramètre
        rm = pyvisa.ResourceManager()
        self._device = rm.open_resource(address)
        self._device.baud_rate = 19200
        self._device.data_bits = 7
        self._device.parity = pyvisa.constants.Parity.even
        self._device.stop_bits = pyvisa.constants.StopBits.one
        self._device.read_termination = '\r\n'
        return True

    def close_communication(self):
        pass
    def get_acquired_data(self):
        return np.array([int(self._device.query('X\r\n')[1:])])