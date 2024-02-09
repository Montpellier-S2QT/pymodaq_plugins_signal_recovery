# -*- coding: utf-8 -*-


from enum import Enum
import numpy as np
import pyvisa
import time

class EGG5210():

    _port = "ASRL3::INSTR"

    def open_communication(self):
        rm = pyvisa.ResourceManager()
        self._device = rm.open_resource(self._port)
        self._device.baud_rate = 19200
        self._device.data_bits = 7
        self._device.parity = pyvisa.constants.Parity.even
        self._device.stop_bits = pyvisa.constants.StopBits.one
        self._device.read_termination = '\r\n'
        return True


    def close_communication(self):
        pass


    def get_ready_state(self):
        """ Get the status of the camera, to know if the acquisition is finished or still ongoing.

        @return (bool): True if the camera is ready, False if an acquisition is ongoing

        As there is no synchronous acquisition in the interface, the logic needs a way to check the acquisition state.
        """
        return True

    def get_acquired_data(self):
        """ Return an array of last acquired data.

               @return: Data in the format depending on the read mode.

               Depending on the read mode, the format is :
               'FVB' : 1d array
               'MULTIPLE_TRACKS' : list of 1d arrays
               'IMAGE' 2d array of shape (width, height)
               'IMAGE_ADVANCED' 2d array of shape (width, height)

               Each value might be a float or an integer.
               """
        return np.array([int(self._device.query('X\r\n')[1:])])