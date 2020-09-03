import sys
from email.header import UTF8
sys.path.append('C:/LabPrograms/Python/ElveflowScopeFoundry/SDK/DLL64')#add the path of the library here
sys.path.append('C:/LabPrograms/Python/ElveflowScopeFoundry/SDK')#add the path of the LoadElveflow.py

from ctypes import *

from array import array

from Elveflow64 import *

Z_REGULATOR_TYPE_NONE = 0
Z_REGULATOR_TYPE__0_200_MBAR = 1
Z_REGULATOR_TYPE__0_2000_MBAR = 2
Z_REGULATOR_TYPE__0_8000_MBAR = 3
Z_REGULATOR_TYPE_M1000_1000_MBAR = 4
Z_REGULATOR_TYPE_M1000_6000_MBAR = 5

Z_SENSOR_TYPE_NONE = 0
Z_SENSOR_TYPE_FLOW_1_5_MUL_MIN = 1
Z_SENSOR_TYPE_FLOW_7_MUL_MIN = 2
Z_SENSOR_TYPE_FLOW_50_MUL_MIN = 3
Z_SENSOR_TYPE_FLOW_80_MUL_MIN = 4
Z_SENSOR_TYPE_FLOW_1000_MUL_MIN = 5
Z_SENSOR_TYPE_FLOW_5000_MUL_MIN = 6
Z_SENSOR_TYPE_PRESS_340_MBAR = 7
Z_SENSOR_TYPE_PRESS_1_BAR = 8
Z_SENSOR_TYPE_PRESS_2_BAR = 9
Z_SENSOR_TYPE_PRESS_7_BAR = 10
Z_SENSOR_TYPE_PRESS_16_BAR = 11
Z_SENSOR_TYPE_LEVEL = 12

Z_SENSOR_DIGIT_ANALOG_ANALOG = 0
Z_SENSOR_DIGIT_ANALOG_DIGITAL = 1

Z_SENSOR_FSD_CALIB_H20 = 0
Z_SENSOR_FSD_CALIB_IPA = 1

Z_D_F_S_RESOLUTION__9BIT = 0
Z_D_F_S_RESOLUTION__10BIT = 1
Z_D_F_S_RESOLUTION__11BIT = 2
Z_D_F_S_RESOLUTION__12BIT = 3
Z_D_F_S_RESOLUTION__13BIT = 4
Z_D_F_S_RESOLUTION__14BIT = 5
Z_D_F_S_RESOLUTION__15BIT = 6
Z_D_F_S_RESOLUTION__16BIT = 7

error_dict = {8000 : "No Digital Sensor found",
              8001 : "No pressure sensor compatible with OB1 MK3",
              8002 : "No Digital pressure sensor compatible with OB1 MK3+",
              8003 : "No Digital Flow sensor compatible with OB1 MK3",
              8004 : "No IPA config for this sensor",
              8005 : "Sensor not compatible with AF1",
              8006 : "No Instrument with selected ID"}

class ElveflowDevice():
    
    """
    Device class for the Elveflow Pump System (OB1). Mainly based on the _OB1_EX.py file.
    
    """
    
    def __init__(self, 
                 ni_name = "01EA543A", 
                 ch_sensor = 1,
                 calibration_kind = "default"):
        
        
        self.instr_id=c_int32()
        self.calib=(c_double*1000)()
        
        self.initElveflow(ni_name = ni_name, 
                          reg_ch_1=Z_REGULATOR_TYPE__0_200_MBAR, 
                          reg_ch_2=Z_REGULATOR_TYPE__0_200_MBAR, 
                          reg_ch_3=Z_REGULATOR_TYPE__0_2000_MBAR, 
                          reg_ch_4=Z_REGULATOR_TYPE_M1000_1000_MBAR)
        
#         #self.addSensor(ch_number=ch_sensor, 
#                        sensor_type=Z_SENSOR_TYPE_FLOW_1_5_MUL_MIN, 
#                        is_digital=Z_SENSOR_DIGIT_ANALOG_DIGITAL, 
#                        calib_type=Z_SENSOR_FSD_CALIB_H20, 
#                        resolution=Z_D_F_S_RESOLUTION__16BIT)
#         
        self.calibrate(kind = "new",
                       calib_path = "C:\\Users\Admin\\Desktop\\calib.txt")

        self.calibrate(kind = "load",
                       calib_path = "C:\\Users\Admin\\Desktop\\calib.txt")

    def checkError(self, error):
        
        if error != 0:
            
            print("Error number ", error, ": " ,error_dict[error])
    
    def initElveflow(self, 
                    ni_name='01EA543A', 
                    reg_ch_1=Z_REGULATOR_TYPE__0_200_MBAR, 
                    reg_ch_2=Z_REGULATOR_TYPE__0_200_MBAR, 
                    reg_ch_3=Z_REGULATOR_TYPE__0_2000_MBAR, 
                    reg_ch_4=Z_REGULATOR_TYPE_M1000_1000_MBAR):
        

        
        error=OB1_Initialization(ni_name.encode('ascii'),reg_ch_1,reg_ch_2,reg_ch_3,reg_ch_4,byref(self.instr_id)) 
        #all functions will return error codes to help you to debug your code, for further information refer to User Guide
        self.checkError(error)
        
        print("OB1 ID: %d" % self.instr_id.value)
    
    def addSensor(self,
                  ch_number=1, #the channel to which the sensor is connected
                  sensor_type=Z_SENSOR_TYPE_FLOW_1_5_MUL_MIN,
                  is_digital=Z_SENSOR_DIGIT_ANALOG_DIGITAL,
                  calib_type=Z_SENSOR_FSD_CALIB_H20,
                  resolution=Z_D_F_S_RESOLUTION__16BIT):
        
        error=OB1_Add_Sens(self.instr_id, ch_number, sensor_type, is_digital, calib_type, resolution)
        
        self.checkError(error)
    
    def newCalibration(self,
                       calib_path):
        
        #example : Calib_path='C:\\Users\\Public\\Desktop\\Calibration\\Calib.txt'
        
        OB1_Calib(self.instr_id.value, self.calib, 1000)
        error=Elveflow_Calibration_Save(calib_path.encode('ascii'), byref(self.calib), 1000)
        print ('calib saved in %s' % calib_path.encode('ascii'))
        self.checkError(error)
        
    def loadCalibration(self,
                        calib_path):
        
        error=Elveflow_Calibration_Load (calib_path.encode('ascii'), byref(self.calib), 1000)
        self.checkError(error)
        
    def defaultCalibration(self):
        
        error=Elveflow_Calibration_Default (byref(self.calib),1000)
        self.checkError(error)
    
    def calibrate(self,
                  kind = "default",
                  calib_path = None):
        
        if kind == "default":
            self.defaultCalibration()
        
        elif kind == "load":
            self.loadCalibration(calib_path)
            
        elif kind == "new":
            self.newCalibration(calib_path)


    def setPressure(self,
                    ch_number,
                    pressure):
        
        ch_number_int32 = c_int32(ch_number)
        pressure_double = c_double(pressure)
        
        error=OB1_Set_Press(self.instr_id.value, ch_number_int32, pressure_double, byref(self.calib),1000)
        self.checkError(error)

    def getPressure(self,
                    ch_number):
        
        ch_number_int32 = c_int32(ch_number)
        pressure_double = c_double()
        
        error=OB1_Get_Press(self.instr_id.value, ch_number_int32, 1, byref(self.calib),byref(pressure_double), 1000)
        self.checkError(error)
        
        return pressure_double.value
    
    def getSensorFlow(self,
                      ch_number):
        
        ch_number_int32 = c_int32(ch_number)
        flow_double = c_double()

        error=OB1_Get_Sens_Data(self.instr_id.value,ch_number_int32, 1,byref(flow_double))
        self.checkError(error)
        
        return flow_double.value
    
    def close(self):
        
        error=OB1_Destructor(self.instr_id.value)
        self.checkError(error)
        