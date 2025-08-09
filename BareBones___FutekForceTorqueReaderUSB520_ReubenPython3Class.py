# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision D, 08/--/2025

Verified working on: Python 3.11/12 for Windows 10/11 64-bit.
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################
import os
import sys
import time
import traceback
import keyboard
import signal #for CTRLc_HandlerFunction

import platform
print("platform.architecture(): " + str(platform.architecture()))
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
'''
Must use the 64-bit version of the file "FUTEK_USB_DLL.dll", downloaded from 
https://media.futek.com/content/futek/files/downloads/futek-usb-dll.zip

Once downloaded and extracted, right-click the DLL file and click "Unblock" from bottom of the tab (default is to block it for security reasons).
Alternatively, you can enter into the DLL-containing-folder from Admin PowerShell and enter the command:
Get-ChildItem -Path . -Filter *.dll | Unblock-File

For loading the DLL via the clr module, it's critical to use the clr *from the pythonnet module ("pip install pythonnet"), not from a stand-alone clr module.

Excellent API documentation for the FUTEK here: https://media.futek.com/docs/dotnet/api/FUTEK_USB_DLL~FUTEK_USB_DLL.USB_DLL_methods.html
'''

import clr
clr.AddReference("FUTEK_USB_DLL")

import FUTEK_USB_DLL #This is NOT a Python module that gets installed; instead, it refers to the line "clr.AddReference("FUTEK_USB_DLL")" above.
from FUTEK_USB_DLL import USB_DLL
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def CTRLc_RegisterHandlerFunction():

    signal.signal(signal.SIGINT, CTRLc_HandlerFunction)

##########################################################################################################
##########################################################################################################

########################################################################################################## MUST ISSUE CTRLc_RegisterHandlerFunction() AT START OF PROGRAM
##########################################################################################################
def CTRLc_HandlerFunction(signum, frame):
    global EXIT_PROGRAM_FLAG

    EXIT_PROGRAM_FLAG = 1
    print("CTRLc_HandlerFunction event firing!")

    CloseDevice()

    sys.exit(0)  #Exit gracefully
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def TareSensor_Callback(OptionalArugment = 0):
    global TareSensor_EventNeedsToBeFiredFlag

    TareSensor_EventNeedsToBeFiredFlag = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def CloseDevice():

    global FUTEK_USB_DLL_Object
    global DeviceHandle
    global DeviceChannel

    FUTEK_USB_DLL_Object.Reset_Board(DeviceHandle)  # Without this call, the board gets into a bad state

    print("CloseDevice event fired!")

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def InitializeDevice(TypeOfBoard_EnglishNameString = "", SerialNumber = "", SamplingRateInHz = -1, ResetAngleOnInitializationFlag = 0, PrintInfoForDebuggingFlag = 0):

    global FUTEK_USB_DLL_Object
    global DeviceHandle
    global DeviceChannel

    global Offset_Load
    global Offset_Value
    global Offset_Load
    global Fullscale_Load
    global Fullscale_Value
    global DecimalPoint_ConversionFactor
    global Rotation_PulsesPerRotation_ActualValue
    global AngularResolution_ActualValue_Deg

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    try:

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict = dict([(5, 0), (10, 1), (15, 2), (20, 3), (25, 4), (30, 5), (50, 6), (60, 7), (100, 8), (600, 9), (960, 10), (1200, 11), (2400, 12), (4800, 13)])
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict: " + str(SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict))

        SamplingRateCode_USB520_HexValueAsKey_Dict = {v: k for k, v in SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict.items()}
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, SamplingRateCode_USB520_HexValueAsKey_Dict: " + str(SamplingRateCode_USB520_HexValueAsKey_Dict))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        TypeOfBoard_EnglishNameStringAsKey_Dict = dict([("USB100/USB200", 0x00),
                                                       ("USB110", 0x01),
                                                       ("USB210", 0x02),
                                                       ("USB220", 0x03),
                                                       ("USB230", 0x04),
                                                       ("IHH500", 0x05),
                                                       ("USB120", 0x06),
                                                       ("USB320", 0x07),
                                                       ("USB410", 0x08),
                                                       ("USB240", 0x09),
                                                       ("IPM650", 0x0A),
                                                       ("USB520", 0x0B),
                                                       ("USB215", 0x0C),
                                                       ("ETH100", 0x0D),
                                                       ("USB530", 0x0E),
                                                       ("ITB100", 0x0F),
                                                       ("IDA100", 0x10)])

        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, TypeOfBoard_EnglishNameStringAsKey_Dict: " + str(TypeOfBoard_EnglishNameStringAsKey_Dict))

        TypeOfBoard_HexValueAsKey_Dict = {v: k for k, v in TypeOfBoard_EnglishNameStringAsKey_Dict.items()}
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, TypeOfBoard_HexValueAsKey_Dict: " + str(TypeOfBoard_HexValueAsKey_Dict))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if TypeOfBoard_EnglishNameString == "":
            print("InitializeDevice: Error, must input the device's TypeOfBoard_EnglishNameString.")
            return 0
        else:
            if TypeOfBoard_EnglishNameString not in TypeOfBoard_EnglishNameStringAsKey_Dict:
                print("InitializeDevice, Error: TypeOfBoard_EnglishNameString of " + str(TypeOfBoard_EnglishNameString) + " is not in TypeOfBoard_EnglishNameStringAsKey_Dict = " + str(TypeOfBoard_EnglishNameStringAsKey_Dict))
                return 0
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if SerialNumber == "":
            print("InitializeDevice: Error, must input the device's serial number.")
            return 0
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if SamplingRateInHz == -1:
            print("InitializeDevice, SamplingRateInHz: Error, must input the device's sampling rate.")
            return 0
        else:
            if SamplingRateInHz not in SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict:
                print("InitializeDevice, Error: SamplingRateInHz of " + str(SamplingRateInHz) + " is not in SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict = " + str(SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict))
                return 0
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        FUTEK_USB_DLL_Object = FUTEK_USB_DLL.USB_DLL()
        FUTEK_USB_DLL_Object.Open_Device_Connection(SerialNumber)

        DeviceHandle = FUTEK_USB_DLL_Object.DeviceHandle
        DeviceChannel = 0 #Hard-coded for the USB520

        time.sleep(0.25)  #To allow the board to open properly before querying it.
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ########################################################################################################## ALL OF THESE VALUES ARE REBOOT/POWER-OFF-SAFE (PERSISTENT IN EEPROM), INCLUDING THE SAMPLING RATE.
        ##########################################################################################################
        ##########################################################################################################
        try:

            ######################################################################################################
            TypeOfBoard_ActualHexValue = int(FUTEK_USB_DLL_Object.Get_Type_of_Board(DeviceHandle))
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, TypeOfBoard_ActualHexValue: " + str(TypeOfBoard_ActualHexValue) + ", type: " + str(type(TypeOfBoard_ActualHexValue)))
            ######################################################################################################

            ######################################################################################################
            TypeOfBoard_ActualEnglishNameString = TypeOfBoard_HexValueAsKey_Dict[TypeOfBoard_ActualHexValue]
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, TypeOfBoard_ActualEnglishNameString: " + str(TypeOfBoard_ActualEnglishNameString) + ", type: " + str(type(TypeOfBoard_ActualEnglishNameString)))

            if TypeOfBoard_ActualEnglishNameString != TypeOfBoard_EnglishNameString:
                print("InitializeDevice, TypeOfBoard_EnglishNameString does not match Actual.")
                return 0
            ######################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("InitializeDevice, exceptions: %s" % exceptions)
            #traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################


        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ''' #07/18/25: This function doesn't appear to be supported at this time.
        ######################################################################################################
        DeviceSerialNumber_ActualValue = int(FUTEK_USB_DLL_Object.Get_ (DeviceHandle))
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, DeviceSerialNumber_ActualValue: " + str(DeviceSerialNumber_ActualValue) + ", type: " + str(type(DeviceSerialNumber_ActualValue)))
        ######################################################################################################
        '''

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        DecimalPoint = float(FUTEK_USB_DLL_Object.Get_Decimal_Point(DeviceHandle, DeviceChannel)) #Get_Decimal_Point sets the precision of the memory storage for proper conversion of ADC to Torque values.
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, DecimalPoint: " + str(DecimalPoint) + ", type: " + str(type(DecimalPoint)))

        DecimalPoint_ConversionFactor = pow(10.0, DecimalPoint)
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, DecimalPoint_ConversionFactor: " + str(DecimalPoint_ConversionFactor) + ", type: " + str(type(DecimalPoint_ConversionFactor)))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        Rotation_PulsesPerRotation_ActualValue = float(FUTEK_USB_DLL_Object.Get_Pulses_Per_Rotation(DeviceHandle, DeviceChannel))
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, Rotation_PulsesPerRotation_ActualValue: " + str(Rotation_PulsesPerRotation_ActualValue) + ", type: " + str(type(Rotation_PulsesPerRotation_ActualValue)))

        AngularResolution_ActualValue_Deg = 360.0 / (Rotation_PulsesPerRotation_ActualValue * 4.0 * 10.0)  # *4.0 is quadrature, and *10 appears to be their internal precision scaling
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, AngularResolution_ActualValue_Deg: " + str(AngularResolution_ActualValue_Deg) + ", type: " + str(type(AngularResolution_ActualValue_Deg)))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        Offset_Load = float(FUTEK_USB_DLL_Object.Get_Offset_Load(DeviceHandle, DeviceChannel)) #Get_Offset_Load means the load that was used for factory calibration at no-load.
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, Offset_Load: " + str(Offset_Load) + ", type: " + str(type(Offset_Load)))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        Offset_Value = float(FUTEK_USB_DLL_Object.Get_Offset_Value(DeviceHandle, DeviceChannel)) #Get_Offset_Value means the ADC value without load on the sensor, like a zero offset, calibrated at factory at no-load.
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, Offset_Value: " + str(Offset_Value) + ", type: " + str(type(Offset_Value)))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        Fullscale_Load = float(FUTEK_USB_DLL_Object.Get_Fullscale_Load(DeviceHandle, DeviceChannel)) #Get_Fullscale_Load means the sensor's full-capacity that was used for calibration at factory.
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, Fullscale_Load: " + str(Fullscale_Load) + ", type: " + str(type(Fullscale_Load)))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        Fullscale_Value = float(FUTEK_USB_DLL_Object.Get_Fullscale_Value(DeviceHandle, DeviceChannel)) #Get_Fullscale_Value means the ADC value corresponding to the full-load/capacity calibration at the factory.
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, Fullscale_Value: " + str(Fullscale_Value) + ", type: " + str(type(Fullscale_Value)))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        LoadingPoint_CW = []
        LoadOfLoadingPoint_CW = []
        for PointIndex_CW in [1, 2, 3, 4, 5]:
            LoadingPoint_CW.append(float(FUTEK_USB_DLL_Object.Get_Loading_Point(DeviceHandle, PointIndex_CW, DeviceChannel)))
            LoadOfLoadingPoint_CW.append(float(FUTEK_USB_DLL_Object.Get_Load_of_Loading_Point(DeviceHandle, PointIndex_CW, DeviceChannel)))
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, LoadOfLoadingPoint: " + str(LoadOfLoadingPoint_CW) + ", LoadingPoint_CW: " + str(LoadingPoint_CW))

        LoadingPoint_CCW = []
        LoadOfLoadingPoint_CCW = []
        for PointIndex_CCW in [8, 9, 10, 11, 12]:
            LoadingPoint_CCW.append(float(FUTEK_USB_DLL_Object.Get_Loading_Point(DeviceHandle, PointIndex_CCW, DeviceChannel)))
            LoadOfLoadingPoint_CCW.append(float(FUTEK_USB_DLL_Object.Get_Load_of_Loading_Point(DeviceHandle, PointIndex_CCW, DeviceChannel)))
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, LoadOfLoadingPoint: " + str(LoadOfLoadingPoint_CCW) + ", LoadingPoint_CCW: " + str(LoadingPoint_CCW))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ListOfCalibrationPoints_Load_CW = [Offset_Load] + LoadOfLoadingPoint_CW + [Fullscale_Load]
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, ListOfCalibrationPoints_Load_CW: " + str(ListOfCalibrationPoints_Load_CW))

        ListOfCalibrationPoints_Value_CW = [Offset_Value] + LoadingPoint_CW + [Fullscale_Value]
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, ListOfCalibrationPoints_Value_CW: " + str(ListOfCalibrationPoints_Value_CW))

        ListOfCalibrationPoints_Load_CCW = [Offset_Load] + LoadOfLoadingPoint_CCW + [Fullscale_Load]
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, ListOfCalibrationPoints_Load_CCW: " + str(ListOfCalibrationPoints_Load_CCW))

        ListOfCalibrationPoints_Value_CCW = [Offset_Value] + LoadingPoint_CCW + [Fullscale_Value]
        if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, ListOfCalibrationPoints_Value_CCW: " + str(ListOfCalibrationPoints_Value_CCW))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ActualSamplingRate_HexValue = int(FUTEK_USB_DLL_Object.Get_ADC_Sampling_Rate_Setting(DeviceHandle, DeviceChannel)) #https://media.futek.com/docs/dotnet/api/SamplingRateCodes.html
        ActualSamplingRate_HzValue = SamplingRateCode_USB520_HexValueAsKey_Dict[ActualSamplingRate_HexValue]

        if ActualSamplingRate_HzValue != SamplingRateInHz:
            print("Issuing Set_ADC_Configuration command.")
            Set_ADC_Configuration_TempReturnedValue = FUTEK_USB_DLL_Object.Set_ADC_Configuration(DeviceHandle, SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict[SamplingRateInHz], DeviceChannel)

            time.sleep(4.0) #Reader needs time to reset the ADC.

            ActualSamplingRate_HexValue = int(FUTEK_USB_DLL_Object.Get_ADC_Sampling_Rate_Setting(DeviceHandle, DeviceChannel)) #https://media.futek.com/docs/dotnet/api/SamplingRateCodes.html
            ActualSamplingRate_HzValue = SamplingRateCode_USB520_HexValueAsKey_Dict[ActualSamplingRate_HexValue]
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if ResetAngleOnInitializationFlag == 1:
            FUTEK_USB_DLL_Object.Reset_Angle(DeviceHandle, DeviceChannel)
            print("@@@@@@@@@@@ InitializeDevice, FUTEK_USB_DLL_Object.Reset_Angle event fired! @@@@@@@@@@@")
            time.sleep(4.0)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        return 1
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    except:
        exceptions = sys.exc_info()[0]
        print("InitializeDevice: Exceptions: %s" % exceptions)
        #return 0
        traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    print("Starting BareBones___FutekForceTorqueReaderUSB520_ReubenPython3Class.py")

    ######################################################################################################
    ######################################################################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    keyboard.on_press_key("esc", ExitProgram_Callback)
    keyboard.on_press_key("t", TareSensor_Callback)

    CTRLc_RegisterHandlerFunction()
    ######################################################################################################
    ######################################################################################################

    global ADC_RawValue
    ADC_RawValue = -11111.0

    global Torque_RawValue
    Torque_RawValue = -11111.0

    global AngleValue_EncoderCounts
    AngleValue_EncoderCounts = -11111.0

    global AngleValue_Deg
    AngleValue_Deg = -11111.0

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global LooperCounter_MainLoopThread
    LooperCounter_MainLoopThread = 0

    global FUTEK_USB_DLL_Object
    global DeviceHandle
    global DeviceChannel

    global Offset_Load
    global Offset_Value
    global Offset_Load
    global Fullscale_Load
    global Fullscale_Value
    global DecimalPoint_ConversionFactor
    global Rotation_PulsesPerRotation_ActualValue
    global AngularResolution_ActualValue_Deg

    global TareSensor_EventNeedsToBeFiredFlag
    TareSensor_EventNeedsToBeFiredFlag = 0

    TypeOfBoard_EnglishNameString = "USB520"
    SerialNumber = "1132494"
    SamplingRateInHz = 10

    PrintForceTorqueValuesFlag = 1 #unicorn
    PrintAngleValuesFlag = 1

    ######################################################################################################
    ######################################################################################################
    InitializeDevice_SuccessFlag = InitializeDevice(TypeOfBoard_EnglishNameString,
                                                    SerialNumber,
                                                    SamplingRateInHz,
                                                    ResetAngleOnInitializationFlag=0, #half of the time this works, and half of the time this doesn't work
                                                    PrintInfoForDebuggingFlag=1)

    if InitializeDevice_SuccessFlag == 0:
        EXIT_PROGRAM_FLAG = 1
    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################tt
    StartingTime_MainLoopThread = time.time()
    while EXIT_PROGRAM_FLAG == 0:

        ######################################################################################################
        CurrentTime_MainLoopThread = time.time() - StartingTime_MainLoopThread
        ######################################################################################################

        ######################################################################################################
        if TareSensor_EventNeedsToBeFiredFlag == 1:
            TareSensorReturnValue = FUTEK_USB_DLL_Object.Change_Tare_Up(DeviceHandle)
            print("TareSensor even fired!t")
            TareSensor_EventNeedsToBeFiredFlag = 0
        ######################################################################################################

        ######################################################################################################
        ADC_RawValue = float(FUTEK_USB_DLL_Object.Normal_Data_Request(DeviceHandle, DeviceChannel))
        Torque_RawValue = (ADC_RawValue - Offset_Value) * ((Fullscale_Load - Offset_Load) / (Fullscale_Value - Offset_Value)) / DecimalPoint_ConversionFactor

        #Linear interpolation between two points (from https://media.futek.com/content/futek/files/pdf/Manuals_and_Technical_Documents/USBLabVIEWExampleGuide.pdf)
        #Note that there is also an interpolation that involves the 5-point calibration that isn't included here.

        if PrintForceTorqueValuesFlag == 1:
            print("ADC_RawValue: " + str(ADC_RawValue) + ", Torque_RawValue: " + str(Torque_RawValue))
        ######################################################################################################

        ######################################################################################################
        if LooperCounter_MainLoopThread >= round(SamplingRateInHz/10.0): #Max pf 10Hz for new angular measurements

            Direction = float(FUTEK_USB_DLL_Object.Get_Direction(DeviceHandle, DeviceChannel)) #THIS REFERS TO USB DIRECTION, NOT ROTATION DIRECTION

            RotationValue_SuccessFlag = float(FUTEK_USB_DLL_Object.Get_Rotation_Values(DeviceHandle)) #This is what tells the reader to update its FUTEK_USB_DLL_Object.AngleValue and FUTEK_USB_DLL_Object.RPMValue
            AngleValue_EncoderCounts = float(FUTEK_USB_DLL_Object.AngleValue) #The value must be between -8,388,608 and +8,388,607. We're expecting a 0.25deg resolution (1/(360.0*4))

            AngleValue_Deg = AngleValue_EncoderCounts*AngularResolution_ActualValue_Deg
            RPMValue = float(FUTEK_USB_DLL_Object.RPMValue)*AngularResolution_ActualValue_Deg #The value must be between -8,388,608 and +8,388,607.

            if PrintAngleValuesFlag == 1:
                print("AngleValue_EncoderCounts: " + str(AngleValue_EncoderCounts) + ", AngleValue_Deg: " + str(AngleValue_Deg) + ", RPMValue: " + str(RPMValue))

            LooperCounter_MainLoopThread = 0
        ######################################################################################################

        ######################################################################################################
        time.sleep((1.0/SamplingRateInHz) + 0.001) #This is what sets the data-rate, there's no hand-shaking. If you're reading too fast, you'll get the same point over and over, so it'll look like a stair-step.
        LooperCounter_MainLoopThread = LooperCounter_MainLoopThread + 1
        ######################################################################################################

    ######################################################################################################
    ######################################################################################################

    ######################################################################################################
    ######################################################################################################
    #Nothing needed to close the FUTEK_USB_DLL_Object.

    CloseDevice()
    print("Exiting BareBones___FutekForceTorqueReaderUSB520_ReubenPython3Class.py")
    ######################################################################################################
    ######################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################





