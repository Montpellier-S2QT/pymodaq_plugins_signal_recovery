# -*- coding: utf-8 -*-
"""
Created the 17/04/2023

@author: Sebastien Weber
"""
from typing import List

from pymeasure.instruments.ametek import Ametek7270
from pymodaq_plugins_signal_recovery.hardware.utils import get_resources
from enum import Enum


class DSP7270:
    channels = ['x', 'y', 'mag', 'phase']

    def __init__(self):
        self._dev:  Ametek7270 = None

    def open_communication(self, id: str):
        self._dev = Ametek7270(id)

    def get_data(self, channels: List[str]):
        return [getattr(self._dev, channel) for channel in channels]

    def close(self):
        self._dev.shutdown()


if __name__ == '__main__':

    dsp = DSP7270()
    dsp.open_communication('USB0::0x0A2D::0x001B::16216344::RAW')

    print(dsp.get_data(['y', 'x', 'phase', 'mag']))

    dsp.close()


