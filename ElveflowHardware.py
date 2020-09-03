from ScopeFoundry import HardwareComponent
from ElveflowDevice import ElveflowDevice

class ElveflowHardware(HardwareComponent):
    
    name = "ElveflowHardware"
    
    def setup(self):
        
        
        self.saved_pressures = [0, 0, 0, 0]
        
        self.set_pressure_1 = self.add_logged_quantity('set_pressure_1' , dtype=float, si=False, ro = 0, 
                                                spinbox_step = 0.0001,spinbox_decimals = 4, initial = 0,
                                                unit = 'mbar', vmin = 0, vmax = 200)
        self.read_pressure_1 = self.add_logged_quantity('read_pressure_1', dtype = float, si = False, ro = 1,
                                                       spinbox_decimals = 4 ,initial = 0, unit = 'mbar')
        
        
        
        self.set_pressure_2 = self.add_logged_quantity('set_pressure_2', dtype=float, si=False, ro = 0, 
                                                spinbox_step = 0.0001,spinbox_decimals = 4, initial = 0,
                                                unit = 'mbar', vmin = 0, vmax = 200)
        self.read_pressure_2 = self.add_logged_quantity('read_pressure_2', dtype = float, si = False, ro = 1,
                                                     initial = 0, unit = 'mbar')
        
        
        
        self.set_pressure_3 = self.add_logged_quantity('set_pressure_3' , dtype=float, si=False, ro = 0, 
                                                spinbox_step = 0.0001,spinbox_decimals = 4, initial = 0,
                                                unit = 'mbar', vmin = 0, vmax = 2000)
        self.read_pressure_3 = self.add_logged_quantity('read_pressure_3', dtype = float, si = False, ro = 1,
                                                       spinbox_decimals = 4 ,initial = 0, unit = 'mbar')
        
        
        
        self.set_pressure_4 = self.add_logged_quantity('set_pressure_4', dtype=float, si=False, ro = 0, 
                                                spinbox_step = 0.0001,spinbox_decimals = 4, initial = 0,
                                                unit = 'mbar', vmin = 0, vmax = 1000)
        self.read_pressure_4 = self.add_logged_quantity('read_pressure_4', dtype = float, si = False, ro = 1,
                                                spinbox_decimals = 4 ,initial = 0, unit = 'mbar')

        
        
        self.save_pressures = self.add_logged_quantity('save_pressures', dtype = bool, si = False, ro = 0, 
                                                       initial = False, reread_from_hardware_after_write = True)

        self.set_saved_pressures = self.add_logged_quantity('set_saved_pressures', dtype = bool, si = False, ro = 0, 
                                                       initial = False, reread_from_hardware_after_write = True)
        
    def connect(self):
        
        self.elveflow = ElveflowDevice(ni_name = "01EA543A",
                                       ch_sensor = 1,
                                       calibration_kind = "default")
        
        self.set_pressure_1.hardware_set_func = self.setPressure1
        self.set_pressure_2.hardware_set_func = self.setPressure2
        self.set_pressure_3.hardware_set_func = self.setPressure3
        self.set_pressure_4.hardware_set_func = self.setPressure4
        self.save_pressures.hardware_set_func = self.setSavePressures
        self.set_saved_pressures.hardware_set_func = self.settingSavedPressures
            
        self.read_pressure_1.hardware_read_func = self.getPressure1
        self.read_pressure_2.hardware_read_func = self.getPressure2
        self.read_pressure_3.hardware_read_func = self.getPressure3
        self.read_pressure_4.hardware_read_func = self.getPressure4
        self.save_pressures.hardware_read_func = self.falseCheckbox        
        self.set_saved_pressures.hardware_read_func = self.falseCheckbox
        self.read_from_hardware()
        
    def disconnect(self):
        
        if hasattr(self, 'elveflow'):
            self.elveflow.close()
#             error_uninit = self.hamamatsu.dcam.dcamapi_uninit()
#             if (error_uninit != DCAMERR_NOERROR):
#                 raise DCAMException("DCAM uninitialization failed with error code " + str(error_uninit))    
            del self.elveflow
            
        for lq in self.settings.as_list():
            lq.hardware_read_func = None
            lq.hardware_set_func = None
            
    def setPressure1(self, pressure):
        
        self.elveflow.setPressure(1, pressure)
    
    def setPressure2(self, pressure):
        
        self.elveflow.setPressure(2, pressure)
        
    def setPressure3(self, pressure):
        
        self.elveflow.setPressure(3, pressure)
        
    def setPressure4(self, pressure):
        
        self.elveflow.setPressure(4, pressure)
    
    def getPressure1(self):
        
        return self.elveflow.getPressure(1)

    def getPressure2(self):
        
        return self.elveflow.getPressure(2)

    def getPressure3(self):
        
        return self.elveflow.getPressure(3)

    def getPressure4(self):
        
        return self.elveflow.getPressure(4)
    
    def setSavePressures(self, flag):
        
        if flag:
            
            self.saved_pressures[0] = self.set_pressure_1.val
            self.saved_pressures[1] = self.set_pressure_2.val
            self.saved_pressures[2] = self.set_pressure_3.val
            self.saved_pressures[3] = self.set_pressure_4.val

    def settingSavedPressures(self, flag):
        
        if flag:
            
            self.set_pressure_1.update_value(new_val = self.saved_pressures[0])
            self.set_pressure_2.update_value(new_val = self.saved_pressures[1])
            self.set_pressure_3.update_value(new_val = self.saved_pressures[2])
            self.set_pressure_4.update_value(new_val = self.saved_pressures[3])
            
    def falseCheckbox(self):
        
        return False
    

