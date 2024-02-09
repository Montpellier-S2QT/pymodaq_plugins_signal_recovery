import numpy as np
from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.data import DataFromPlugins, DataToExport
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.parameter import Parameter
import pymodaq.utils.parameter
import pyvisa
#from pymodaq_plugins_physical_measurements.hardware.egg5210.egg_5210 import EGG5210

class DAQ_0DViewer_Lockin5210(DAQ_Viewer_base):
    """ Instrument plugin class for a OD viewer.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Viewer module through inheritance via
    DAQ_Viewer_base. It makes a bridge between the DAQ_Viewer module and the Python wrapper of a particular instrument.

    This plugins controls EGG 5210 Lock-In also Signal Recovery or Ametek 5210)
    It has been tested with an RS232 5210 Lock-In with Pymodaq 4.1 in a Win10 operating system by P. Valvin@L2C-Montpellier

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    """
    try:
        rm = pyvisa.ResourceManager()
        devices = list(rm.list_resources())
        device = ''

    except:
        devices = []
        device = ''

    params = comon_parameters+[
                {'title': 'VISA:','name': 'VISA_ressources', 'type': 'list', 'limits': devices, 'value': device },
                {'title': 'Manufacturer:', 'name': 'manufacturer', 'type': 'str', 'value': "" },
                {'title': 'Serial number:', 'name': 'serial_number', 'type': 'str', 'value': "" },
                {'title': 'Model:', 'name': 'model', 'type': 'str', 'value': "" },
                {'title': 'Timeout (ms):', 'name': 'timeout', 'type': 'int', 'value': 2000, 'default': 2000, 'min': 1000 },
    ]
    def __init__(self, parent=None, params_state=None):
        super().__init__(parent, params_state)
        self.controller = None

    def query_data(self,cmd):
        try:
            res=self.inst.query(cmd)
            searched=re.search('\n',res)
            status_byte=res[searched.start()+1]
            overload_byte=res[searched.start()+3]
            if searched.start!=0:
                data=np.array([float(x) for x in res[0:searched.start()].split(",")])
            else:
                data=None
            return (status_byte,overload_byte,data)
        except:
            return ('\x01','\x00',None)

    def query_string(self,cmd):
        try:
            res=self.inst.query(cmd)
            searched=re.search('\n',res)
            status_byte=res[searched.start()+1]
            overload_byte=res[searched.start()+3]
            if searched.start!=0:
                str=res[0:searched.start()]
            else:
                str=""
            return (status_byte,overload_byte,str)
        except:
            return ('\x01','\x00',"")

    def ini_attributes(self):
        pass

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        ## TODO for your custom plugin
        if param.name() == "a_parameter_you've_added_in_self.params":
           self.controller.your_method_to_apply_this_param_change()  # when writing your own plugin replace this line
#        elif ...
        ##

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
        self.status.update(edict(initialized=False, info="", x_axis=None, y_axis=None, controller=None))
        try:

            if self.settings.child(('controller_status')).value() == "Slave":
                if controller is None:
                    raise Exception('no controller has been defined externally while this detector is a slave one')
                else:
                    self.controller = controller
            else:
                self.controller = self.VISA_rm.open_resource(self.settings.child(('VISA_ressources')).value())

            self.controller.timeout = self.settings.child(('timeout')).value()
            idn = self.controller.query('OUTX1;*IDN?;')
            idn = idn.rstrip('\n')
            idn = idn.rsplit(',')
            if len(idn) >= 0:
                self.settings.child(('manufacturer')).setValue(idn[0])
            if len(idn) >= 1:
                self.settings.child(('model')).setValue(idn[1])
            if len(idn) >= 2:
                self.settings.child(('serial_number')).setValue(idn[2])

            # self.reset()

            self.status.controller = self.controller
            self.status.initialized = True

            return self.status

        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status', [getLineInfo() + str(e), 'log']))
            self.status.info = getLineInfo() + str(e)
            self.status.initialized = False
            return self.status


        #self.ini_detector_init(old_controller=controller,
        #                       new_controller=EGG5210())

        # TODO for your custom plugin (optional) initialize viewers panel with the future type of data
        #self.dte_signal_temp.emit(DataToExport(name='myplugin',
        #                                       data=[DataFromPlugins(name='Mock1',
        #                                                            data=[np.array([0]), np.array([0])],
        #                                                            dim='Data0D',
        #                                                            labels=['Mock1', 'label2'])]))

        #info = "Je vais initialiser le Lock-In"
        #initialized = self.controller.open_communication()
        #return info, initialized

    def close(self):
        """Terminate the communication protocol"""

        self.controller.close_communication()  # when writing your own plugin replace this line

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
        self.dte_signal.emit(DataToExport(name='myplugin',
                                          data=[DataFromPlugins(name='Mock1', data=data_tot,
                                                                dim='Data0D', labels=['dat0', 'data1'])]))
        #########################################################

        # asynchrone version (non-blocking function with callback)
        # raise NotImplemented  # when writing your own plugin remove this line
        # self.controller.your_method_to_start_a_grab_snap(self.callback)  # when writing your own plugin replace this line
        #########################################################


    def callback(self):
        """optional asynchrone method called when the detector has finished its acquisition of data"""
        data_tot = self.controller.your_method_to_get_data_from_buffer()
        self.dte_signal.emit(DataToExport(name='myplugin',
                                          data=[DataFromPlugins(name='Mock1', data=data_tot,
                                                                dim='Data0D', labels=['dat0', 'data1'])]))

    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        ## TODO for your custom plugin
        raise NotImplemented  # when writing your own plugin remove this line
        self.controller.your_method_to_stop_acquisition()  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))
        ##############################
        return ''


if __name__ == '__main__':
    main(__file__)
