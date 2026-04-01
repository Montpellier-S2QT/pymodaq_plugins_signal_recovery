import numpy as np
from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.data import DataFromPlugins, DataToExport
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.parameter import Parameter
from pymodaq_plugins_signal_recovery.hardware.lockin5210 import LockIn5210
from pymodaq_plugins_signal_recovery.hardware.utils import get_resources


class DAQ_0DViewer_Lockin5210(DAQ_Viewer_base):
    """ Instrument plugin class for a OD viewer.

    This plugins controls an EGG 5210 Lock-In (also Signal Recovery or Ametek 5210)
    It has been tested with an RS232 5210 Lock-In with Pymodaq 4.1 in a Win10 operating system by P. Valvin@L2C-Montpellier
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Viewer module through inheritance via
    DAQ_Viewer_base. It makes a bridge between the DAQ_Viewer module and the Python wrapper of a particular instrument.

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    """

    params = comon_parameters + [
        {'title': 'Address:', 'name': 'address', 'type': 'list', 'limits': get_resources()},
        {'title': 'ID:', 'name': 'id', 'type': 'str'},
        ]

    def ini_attributes(self):
        self.controller: LockIn5210 = None
        pass

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        if param.name() == 'address':
            self.controller.close_communication()
            id, initialized = self.controller.open_communication(param.value())
            self.settings.child('id').setValue(id)
        pass

    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator/detector by controller
            (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        self.ini_detector_init(old_controller=controller,
                               new_controller=LockIn5210())

        self.dte_signal_temp.emit(DataToExport(name='signal_recovery',
                                               data=[DataFromPlugins(name='Mock1',
                                                                    data=[np.array([0]), np.array([0])],
                                                                    dim='Data0D',
                                                                    labels=['Mock1', 'label2'])]))

        info = "Initializing EGG 5210"
        address = self.settings.child(('address')).value()
        id, initialized = self.controller.open_communication(address)
        self.settings.child('id').setValue(id)
        return info, initialized

    def close(self):
        """Terminates the communication protocol"""
        self.controller.close_communication()

    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """

        # synchrone version (blocking function)
        data_tot = self.controller.get_acquired_data()
        self.dte_signal.emit(DataToExport(name='signal_recovery',
                                          data=[DataFromPlugins(name='Mock1', data=data_tot,
                                                                dim='Data0D', labels=['data0', 'data1'])]))



    def callback(self):
        """optional asynchrone method called when the detector has finished its acquisition of data"""
        data_tot = self.controller.your_method_to_get_data_from_buffer()
        self.dte_signal.emit(DataToExport(name='signal_recovery',
                                          data=[DataFromPlugins(name='Mock1', data=data_tot,
                                                                dim='Data0D', labels=['dat0', 'data1'])]))

    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        self.controller.close_communication()
        self.emit_status(ThreadCommand('Update_Status', ['Communication aborted']))
        return ''


if __name__ == '__main__':
    main(__file__)
