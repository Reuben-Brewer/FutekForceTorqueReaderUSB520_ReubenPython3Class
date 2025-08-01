# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision C, 08/01/2025

Verified working on: Python 3.11/3.12 for Windows 10, 11 64-bit.
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

##########################################
from LowPassFilterForDictsOfLists_ReubenPython2and3Class import *
from ZeroAndSnapshotData_ReubenPython2and3Class import *
##########################################

##########################################
import os
import sys
import platform
import time
import datetime
import math
import queue as Queue
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
import subprocess
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
import signal #for CTRLc_HandlerFunction
##########################################

##########################################
try:
    import platform

    if platform.architecture()[0].find("64") != -1:
        OS64bitFlag = 1

    print("FutekForceTorqueReaderUSB520_ReubenPython3Class, OS64bitFlag: " + str(OS64bitFlag))

except:
    OS64bitFlag = 0
##########################################

##########################################
try:
    import platform

    if platform.system() == "Windows":
        import ctypes
        winmm = ctypes.WinDLL('winmm')
        winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.

except:
    print("FutekForceTorqueReaderUSB520_ReubenPython3Class,winmm.timeBeginPeriod(1) failed.")
##########################################

##########################################
'''
Must use the 64-bit version of the file "FUTEK_USB_DLL.dll", downloaded from 
https://media.futek.com/content/futek/files/downloads/futek-usb-dll.zip

Once downloaded and extracted, right-click the DLL file and click "Unblock" from bottom of the tab (default is to block it for security reasons).
Alternatively, you can enter into the DLL-containing-folder from Admin PowerShell and enter the command:
Get-ChildItem -Path . -Filter *.dll | Unblock-File

For loading the DLL via the clr module, it's critical to use the clr *from the pythonnet module ("pip install pythonnet"), not from a stand-alone clr module.

Excellent API documentation for the FUTEK here: https://media.futek.com/docs/dotnet/api/FUTEK_USB_DLL~FUTEK_USB_DLL.USB_DLL_methods.html
'''

try:

    import clr
    clr.AddReference("FUTEK_USB_DLL")

    import FUTEK_USB_DLL #This is NOT a Python module that gets installed; instead, it refers to the line "clr.AddReference("FUTEK_USB_DLL")" above.
    from FUTEK_USB_DLL import USB_DLL

    FUTEK_USB_DLL_ImportedFlag = 1

except:
    FUTEK_USB_DLL_ImportedFlag = 0

##########################################

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
class FutekForceTorqueReaderUSB520_ReubenPython3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, SetupDict): #Subclass the Tkinter Frame

        print("#################### FutekForceTorqueReaderUSB520_ReubenPython3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.PrintForceTorqueValuesFlag = 0
        self.PrintAngleValuesFlag = 0

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        
        self.DedicatedRxThread_StillRunningFlag = 0

        self.ZeroAndSnapshotData_OPEN_FLAG = -1
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if OS64bitFlag != 1:
            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: Error, OS64bitFlag = 0")
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if FUTEK_USB_DLL_ImportedFlag != 1:
            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: Error, FUTEK_USB_DLL_ImportedFlag = 0")
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict = dict([(5, 0), (10, 1), (15, 2), (20, 3), (25, 4), (30, 5), (50, 6), (60, 7), (100, 8), (600, 9), (960, 10), (1200, 11), (2400, 12), (4800, 13)])
        print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__, SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict: " + str(self.SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict))

        self.SamplingRateCode_USB520_HexValueAsKey_Dict = {v: k for k, v in self.SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict.items()}
        print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__, SamplingRateCode_USB520_HexValueAsKey_Dict: " + str(self.SamplingRateCode_USB520_HexValueAsKey_Dict))

        self.TypeOfBoard_EnglishNameStringAsKey_Dict = dict([("USB100/USB200", 0x00),
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

        print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__, TypeOfBoard_EnglishNameStringAsKey_Dict: " + str(self.TypeOfBoard_EnglishNameStringAsKey_Dict))

        self.TypeOfBoard_HexValueAsKey_Dict = {v: k for k, v in self.TypeOfBoard_EnglishNameStringAsKey_Dict.items()}
        print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__, TypeOfBoard_HexValueAsKey_Dict: " + str(self.TypeOfBoard_HexValueAsKey_Dict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.LoopCounter_CalculatedFromDedicatedRxThread_EnocderQueriesOnly = 0

        self.AngleValue_EncoderCounts = 0.0
        self.AngularSpeedValue_RevPerMin = 0.0

        self.AngleValue_AllUnitsDict = dict([("EncoderTicks", -11111.0),
                                            ("Deg", -11111.0),
                                            ("Rad", -11111.0),
                                            ("Rev", -11111.0)])

        self.AngularSpeedValue_AllUnitsDict = dict([("EncoderTicksPerSec", -11111.0),
                                                ("DegPerSec", -11111.0),
                                                ("RadPerSec", -11111.0),
                                                ("RevPerSec", -11111.0),
                                                ("RevPerMin", -11111.0)])

        self.CurrentFTmeasurement_Raw = 0.0
        self.LastFTmeasurement_Raw = 0.0

        self.CurrentFTmeasurement_Filtered = 0.0
        self.LastFTmeasurement_Filtered = 0.0

        self.CurrentFTmeasurementDerivative_Raw = 0.0
        self.CurrentFTmeasurementDerivative_Filtered = 0.0

        self.ResetTare_EventNeedsToBeFiredFlag = 0
        self.ResetTare_EventIsCurrentlyBeingExecutedFlag = 0
        self.ResetTare_EventHasHappenedFlag = 0
        self.ResetTare_TimeOfLastEvent = 0.0

        self.MostRecentDataDict = dict()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.CurrentTime_CalculatedFromGUIthread = -11111.0
        self.LastTime_CalculatedFromGUIthread = -11111.0
        self.StartingTime_CalculatedFromGUIthread = -11111.0
        self.DataStreamingFrequency_CalculatedFromGUIthread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromGUIthread = -11111.0
        self.LoopCounter_CalculatedFromDedicatedGUIthread = 0

        self.CurrentTime_CalculatedFromDedicatedRxThread = -11111.0
        self.LastTime_CalculatedFromDedicatedRxThread = -11111.0
        self.StartingTime_CalculatedFromDedicatedRxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedRxThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread = -11111.0
        self.LoopCounter_CalculatedFromDedicatedRxThread = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in SetupDict:

            GUIparametersDict = SetupDict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "root" in GUIparametersDict:
                self.root = GUIparametersDict["root"]
            else:
                print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: ERROR, must pass in 'root'")
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            ##########################################
            if "GUI_ROWSPAN" in GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in GUIparametersDict:
                self.GUI_STICKY = str(GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: GUIparametersDict: " + str(GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ZeroAndSnapshotData___USE_GUI_FLAG" in SetupDict:
            self.ZeroAndSnapshotData___USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("ZeroAndSnapshotData___USE_GUI_FLAG", SetupDict["ZeroAndSnapshotData___USE_GUI_FLAG"])
        else:
            self.ZeroAndSnapshotData___USE_GUI_FLAG = 0

        print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: ZeroAndSnapshotData___USE_GUI_FLAG: " + str(self.ZeroAndSnapshotData___USE_GUI_FLAG))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in SetupDict:
            self.NameToDisplay_UserSet = str(SetupDict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: NameToDisplay_UserSet" + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "SerialNumber_Desired" in SetupDict:
            self.SerialNumber_Desired = SetupDict["SerialNumber_Desired"]
        else:
            self.SerialNumber_Desired = ""

        print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: SerialNumber_Desired: " + str(self.SerialNumber_Desired))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "SamplingRateInHz" in SetupDict:
            SamplingRateInHz_TEMP = SetupDict["SamplingRateInHz"]

            if SamplingRateInHz_TEMP not in self.SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict:
                print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__ Error: SamplingRateInHz of " + str(SamplingRateInHz_TEMP) + " is not in SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict = " + str(self.SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict))
                return

            self.SamplingRateInHz = SamplingRateInHz_TEMP

        else:
            print("InitializeDevice, SamplingRateInHz: Error, must input the device's sampling rate.")
            return

        print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: SamplingRateInHz: " + str(self.SamplingRateInHz))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "TypeOfBoard_EnglishNameString" in SetupDict:
            TypeOfBoard_EnglishNameString_TEMP = str(SetupDict["TypeOfBoard_EnglishNameString"])

            if TypeOfBoard_EnglishNameString_TEMP not in self.TypeOfBoard_EnglishNameStringAsKey_Dict:
                print("InitializeDevice, Error: TypeOfBoard_EnglishNameString of " + str(TypeOfBoard_EnglishNameString_TEMP) + " is not in TypeOfBoard_EnglishNameStringAsKey_Dict = " + str(self.TypeOfBoard_EnglishNameStringAsKey_Dict))
                return

            self.TypeOfBoard_EnglishNameString = TypeOfBoard_EnglishNameString_TEMP

        else:
            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: Error, must input the device's TypeOfBoard_EnglishNameString.")
            return

        print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: TypeOfBoard_EnglishNameString: " + str(self.TypeOfBoard_EnglishNameString))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ResetAngleOnInitializationFlag" in SetupDict:
            self.ResetAngleOnInitializationFlag = self.PassThrough0and1values_ExitProgramOtherwise("ResetAngleOnInitializationFlag", SetupDict["ResetAngleOnInitializationFlag"])
        else:
            self.ResetAngleOnInitializationFlag = 1

        print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: ResetAngleOnInitializationFlag: " + str(self.ResetAngleOnInitializationFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.DedicatedRxThread_TimeToSleepEachLoop = 1.0/(1.15*self.SamplingRateInHz) #Wasteful to query much faster than the sensor can sample.
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DataCollectionDurationInSecondsForSnapshottingAndZeroing" in SetupDict:
            self.DataCollectionDurationInSecondsForSnapshottingAndZeroing = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DataCollectionDurationInSecondsForSnapshottingAndZeroing", SetupDict["DataCollectionDurationInSecondsForSnapshottingAndZeroing"], 0.0, 60.0)

        else:
            self.DataCollectionDurationInSecondsForSnapshottingAndZeroing = 1.0

        print("ForceTorqueReaderOmegaDFGRS5_ReubenPython3Class __init__: DataCollectionDurationInSecondsForSnapshottingAndZeroing: " + str(self.DataCollectionDurationInSecondsForSnapshottingAndZeroing))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "FTmeasurement_ExponentialSmoothingFilterLambda" in SetupDict:
            self.FTmeasurement_ExponentialSmoothingFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("FTmeasurement_ExponentialSmoothingFilterLambda", SetupDict["FTmeasurement_ExponentialSmoothingFilterLambda"], 0.0, 1.0)

        else:
            self.FTmeasurement_ExponentialSmoothingFilterLambda = 0.95 #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        print("ForceTorqueReaderOmegaDFGRS5_ReubenPython3Class __init__: FTmeasurement_ExponentialSmoothingFilterLambda: " + str(self.FTmeasurement_ExponentialSmoothingFilterLambda))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "FTmeasurementDerivative_ExponentialSmoothingFilterLambda" in SetupDict:
            self.FTmeasurementDerivative_ExponentialSmoothingFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("FTmeasurementDerivative_ExponentialSmoothingFilterLambda", SetupDict["FTmeasurementDerivative_ExponentialSmoothingFilterLambda"], 0.0, 1.0)

        else:
            self.FTmeasurementDerivative_ExponentialSmoothingFilterLambda = 0.95 #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        print("ForceTorqueReaderOmegaDFGRS5_ReubenPython3Class __init__: FTmeasurementDerivative_ExponentialSmoothingFilterLambda: " + str(self.FTmeasurementDerivative_ExponentialSmoothingFilterLambda))
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings = dict([("DataStreamingFrequency_CalculatedFromDedicatedRxThread", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                            ("DataStreamingFrequency_CalculatedFromGUIthread", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1), ("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                            ("FTmeasurement", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", self.FTmeasurement_ExponentialSmoothingFilterLambda)])),
                                                                                                            ("FTmeasurementDerivative", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", self.FTmeasurementDerivative_ExponentialSmoothingFilterLambda)]))])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_SetupDict = dict([("DictOfVariableFilterSettings", self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings)])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject = LowPassFilterForDictsOfLists_ReubenPython2and3Class(self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_SetupDict)
        self.LOWPASSFILTER_OPEN_FLAG = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG
        #########################################################

        #########################################################
        if self.LOWPASSFILTER_OPEN_FLAG != 1:
            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: Failed to open LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.")
            return
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            SuccessFlag = self.InitializeDevice(PrintInfoForDebuggingFlag=1)

            if SuccessFlag != 1:
                print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: self.InitializeDevice() failed.")
                return

        except:
            exceptions = sys.exc_info()[0]
            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.CTRLc_RegisterHandlerFunction()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.DedicatedRxThread_ThreadingObject = threading.Thread(target=self.DedicatedRxThread, args=())
        self.DedicatedRxThread_ThreadingObject.start()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.USE_GUI_FLAG == 1:
            self.StartGUI(self.root)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.ZeroAndSnapshotData_Variables_ListOfDicts = [dict([("Variable_Name", "CurrentFTmeasurement"), ("DataCollectionDurationInSecondsForSnapshottingAndZeroing", self.DataCollectionDurationInSecondsForSnapshottingAndZeroing)])]

        self.ZeroAndSnapshotData_GUIparametersDict = dict([("USE_GUI_FLAG", self.ZeroAndSnapshotData___USE_GUI_FLAG),
                                        ("root", self.root),
                                        ("EnableInternal_MyPrint_Flag", 0),
                                        ("NumberOfPrintLines", 10),
                                        ("UseBorderAroundThisGuiObjectFlag", 1),
                                        ("GUI_ROW", 10),
                                        ("GUI_COLUMN", 0),
                                        ("GUI_PADX", 1),
                                        ("GUI_PADY", 1),
                                        ("GUI_ROWSPAN", 1),
                                        ("GUI_COLUMNSPAN", 1)])

        self.ZeroAndSnapshotData_SetupDict = dict([("GUIparametersDict", self.ZeroAndSnapshotData_GUIparametersDict),
                                                    ("NameToDisplay_UserSet", "ZeroAndSnapshotData"),
                                                    ("Variables_ListOfDicts", self.ZeroAndSnapshotData_Variables_ListOfDicts)])


        try:
            self.ZeroAndSnapshotData_Object = ZeroAndSnapshotData_ReubenPython2and3Class(self.ZeroAndSnapshotData_SetupDict)
            self.ZeroAndSnapshotData_OPEN_FLAG = self.ZeroAndSnapshotData_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

            if self.ZeroAndSnapshotData_OPEN_FLAG != 1:
                print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: ZeroAndSnapshotData_Object could not be opened.")
                return

        except:
            exceptions = sys.exc_info()[0]
            print("FutekForceTorqueReaderUSB520_ReubenPython3Class __init__: Exceptions: %s" % exceptions)
            #traceback.print_exc()
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
        #########################################################
        #########################################################

        print("#################### FutekForceTorqueReaderUSB520_ReubenPython3Class __init__ ending. ####################")

    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CTRLc_RegisterHandlerFunction(self):

        signal.signal(signal.SIGINT, self.CTRLc_HandlerFunction)

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## MUST ISSUE CTRLc_RegisterHandlerFunction() AT START OF PROGRAM
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CTRLc_HandlerFunction(self, signum, frame):

        print("FutekForceTorqueReaderUSB520_ReubenPython3Class, CTRLc_HandlerFunction event firing!")

        self.ExitProgram_Callback()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_FloatOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = float(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber, ExitProgramIfFailureFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a numerical value, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
                return InputNumber_ConvertedToFloat

            else:

                print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. '" +
                              str(InputNameString) +
                              "' must be 0 or 1 (value was " +
                              str(InputNumber_ConvertedToFloat) +
                              "). Press any key (and enter) to exit.")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()

                else:
                    return -1
                ##########################

            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        try:
            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a float value, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat_Limited = self.LimitNumber_FloatOutputOnly(RangeMinValue, RangeMaxValue, InputNumber_ConvertedToFloat)

            if InputNumber_ConvertedToFloat_Limited != InputNumber_ConvertedToFloat:
                print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be in the range [" +
                      str(RangeMinValue) +
                      ", " +
                      str(RangeMaxValue) +
                      "] (value was " +
                      str(InputNumber_ConvertedToFloat) + ")")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()
                else:
                    return -11111.0
                ##########################

            else:
                return InputNumber_ConvertedToFloat_Limited
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict()  # So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateVariableFilterSettingsFromExternalProgram(self, VariableNameString, UseMedianFilterFlag, UseExponentialSmoothingFilterFlag, ExponentialSmoothingFilterLambda):
        try:
            self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.UpdateVariableFilterSettingsFromExternalProgram(VariableNameString, UseMedianFilterFlag, UseExponentialSmoothingFilterFlag, ExponentialSmoothingFilterLambda)

            self.FTmeasurement_ExponentialSmoothingFilterLambda = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.GetMostRecentDataDict()["FTmeasurement"]["ExponentialSmoothingFilterLambda"]
            self.FTmeasurementDerivative_ExponentialSmoothingFilterLambda = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.GetMostRecentDataDict()["FTmeasurementDerivative"]["ExponentialSmoothingFilterLambda"]

        except:
            exceptions = sys.exc_info()[0]
            print("UpdateVariableFilterSettingsFromExternalProgram, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_DedicatedRxThread_Filtered(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread = self.CurrentTime_CalculatedFromDedicatedRxThread - self.LastTime_CalculatedFromDedicatedRxThread

            if self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread != 0.0:
                DataStreamingFrequency_CalculatedFromDedicatedRxThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromDedicatedRxThread", DataStreamingFrequency_CalculatedFromDedicatedRxThread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromDedicatedRxThread = ResultsDict["DataStreamingFrequency_CalculatedFromDedicatedRxThread"]["Filtered_MostRecentValuesList"][0]

            self.LoopCounter_CalculatedFromDedicatedRxThread = self.LoopCounter_CalculatedFromDedicatedRxThread + 1
            self.LastTime_CalculatedFromDedicatedRxThread = self.CurrentTime_CalculatedFromDedicatedRxThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_DedicatedRxThread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_GUIthread_Filtered(self):

        try:
            self.CurrentTime_CalculatedFromGUIthread = self.getPreciseSecondsTimeStampString()

            self.DataStreamingDeltaT_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread - self.LastTime_CalculatedFromGUIthread

            if self.DataStreamingDeltaT_CalculatedFromGUIthread != 0.0:
                DataStreamingFrequency_CalculatedFromGUIthread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromGUIthread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromGUIthread", DataStreamingFrequency_CalculatedFromGUIthread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromGUIthread = ResultsDict["DataStreamingFrequency_CalculatedFromGUIthread"]["Filtered_MostRecentValuesList"][0]

            self.LoopCounter_CalculatedFromDedicatedGUIthread = self.LoopCounter_CalculatedFromDedicatedGUIthread + 1
            self.LastTime_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_GUIthread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def InitializeDevice(self, PrintInfoForDebuggingFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ######################################################################################################
            ######################################################################################################
            self.FUTEK_USB_DLL_Object = FUTEK_USB_DLL.USB_DLL()
            self.FUTEK_USB_DLL_Object.Open_Device_Connection(self.SerialNumber_Desired)

            self.DeviceHandle = self.FUTEK_USB_DLL_Object.DeviceHandle
            self.DeviceChannel = 0 #Hard-coded for the USB520

            time.sleep(0.25) #To allow the board to open properly before querying it.
            ######################################################################################################
            ######################################################################################################

            ###################################################################################################### ALL OF THESE VALUES ARE REBOOT/POWER-OFF-SAFE (PERSISTENT IN EEPROM), INCLUDING THE SAMPLING RATE.
            ######################################################################################################

            ######################################################################################################
            RequestCounter = 0
            while 1:
                try:

                    if RequestCounter <= 10:
                        self.TypeOfBoard_ActualHexValue = int(self.FUTEK_USB_DLL_Object.Get_Type_of_Board(self.DeviceHandle))

                        break #If we get a valid integer, then we exit the loop.

                    else:

                        break

                except:
                    print("*** InitializeDevice: Calling 'Get_Type_of_Board' again, RequestCounter = " + str(RequestCounter) + " ***")
                    RequestCounter = RequestCounter + 1
                    time.sleep(0.25)

            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, TypeOfBoard_ActualHexValue: " + str(self.TypeOfBoard_ActualHexValue) + ", type: " + str(type(self.TypeOfBoard_ActualHexValue)))
            ######################################################################################################

            ######################################################################################################
            self.TypeOfBoard_ActualEnglishNameString = self.TypeOfBoard_HexValueAsKey_Dict[self.TypeOfBoard_ActualHexValue]
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, TypeOfBoard_ActualEnglishNameString: " + str(self.TypeOfBoard_ActualEnglishNameString) + ", type: " + str(type(self.TypeOfBoard_ActualEnglishNameString)))

            if self.TypeOfBoard_ActualEnglishNameString != self.TypeOfBoard_EnglishNameString:
                print("InitializeDevice, TypeOfBoard_EnglishNameString doesn not match Actual.")
                return 0
            ######################################################################################################

            ######################################################################################################
            self.DecimalPoint = float(self.FUTEK_USB_DLL_Object.Get_Decimal_Point(self.DeviceHandle, self.DeviceChannel)) #Get_Decimal_Point sets the precision of the memory storage for proper conversion of ADC to Torque values.
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, DecimalPoint: " + str(self.DecimalPoint) + ", type: " + str(type(self.DecimalPoint)))

            self.DecimalPoint_ConversionFactor = pow(10.0, self.DecimalPoint)
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, DecimalPoint_ConversionFactor: " + str(self.DecimalPoint_ConversionFactor) + ", type: " + str(type(self.DecimalPoint_ConversionFactor)))
            ######################################################################################################

            ######################################################################################################
            self.Rotation_PulsesPerRotation_ActualValue = float(self.FUTEK_USB_DLL_Object.Get_Pulses_Per_Rotation(self.DeviceHandle, self.DeviceChannel))
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, Rotation_PulsesPerRotation_ActualValue: " + str(self.Rotation_PulsesPerRotation_ActualValue) + ", type: " + str(type(self.Rotation_PulsesPerRotation_ActualValue)))

            self.AngularResolution_ActualValue_Deg = 360.0 / (self.Rotation_PulsesPerRotation_ActualValue * 4.0 * 10.0)  # *4.0 is quadrature, and *10 appears to be their internal precision scaling
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, AngularResolution_ActualValue_Deg: " + str(self.AngularResolution_ActualValue_Deg) + ", type: " + str(type(self.AngularResolution_ActualValue_Deg)))
            ######################################################################################################

            ######################################################################################################
            self.Offset_Load = float(self.FUTEK_USB_DLL_Object.Get_Offset_Load(self.DeviceHandle, self.DeviceChannel)) #Get_Offset_Load means the load that was used for factory calibration at no-load.
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, Offset_Load: " + str(self.Offset_Load) + ", type: " + str(type(self.Offset_Load)))
            ######################################################################################################

            ######################################################################################################
            self.Offset_Value = float(self.FUTEK_USB_DLL_Object.Get_Offset_Value(self.DeviceHandle, self.DeviceChannel)) #Get_Offset_Value means the ADC value without load on the sensor, like a zero offset, calibrated at factory at no-load.
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, Offset_Value: " + str(self.Offset_Value) + ", type: " + str(type(self.Offset_Value)))
            ######################################################################################################

            ######################################################################################################
            self.Fullscale_Load = float(self.FUTEK_USB_DLL_Object.Get_Fullscale_Load(self.DeviceHandle, self.DeviceChannel)) #Get_Fullscale_Load means the sensor's full-capacity that was used for calibration at factory.
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, Fullscale_Load: " + str(self.Fullscale_Load) + ", type: " + str(type(self.Fullscale_Load)))
            ######################################################################################################

            ######################################################################################################
            self.Fullscale_Value = float(self.FUTEK_USB_DLL_Object.Get_Fullscale_Value(self.DeviceHandle, self.DeviceChannel)) #Get_Fullscale_Value means the ADC value corresponding to the full-load/capacity calibration at the factory.
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, Fullscale_Value: " + str(self.Fullscale_Value) + ", type: " + str(type(self.Fullscale_Value)))
            ######################################################################################################

            ######################################################################################################
            self.LoadingPoint_CW = []
            self.LoadOfLoadingPoint_CW = []
            for PointIndex_CW in [1, 2, 3, 4, 5]:
                self.LoadingPoint_CW.append(float(self.FUTEK_USB_DLL_Object.Get_Loading_Point(self.DeviceHandle, PointIndex_CW, self.DeviceChannel)))
                self.LoadOfLoadingPoint_CW.append(float(self.FUTEK_USB_DLL_Object.Get_Load_of_Loading_Point(self.DeviceHandle, PointIndex_CW, self.DeviceChannel)))
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, LoadOfLoadingPoint: " + str(self.LoadOfLoadingPoint_CW) + ", LoadingPoint_CW: " + str(self.LoadingPoint_CW))

            self.LoadingPoint_CCW = []
            self.LoadOfLoadingPoint_CCW = []
            for PointIndex_CCW in [8, 9, 10, 11, 12]:
                self.LoadingPoint_CCW.append(float(self.FUTEK_USB_DLL_Object.Get_Loading_Point(self.DeviceHandle, PointIndex_CCW, self.DeviceChannel)))
                self.LoadOfLoadingPoint_CCW.append(float(self.FUTEK_USB_DLL_Object.Get_Load_of_Loading_Point(self.DeviceHandle, PointIndex_CCW, self.DeviceChannel)))
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, LoadOfLoadingPoint: " + str(self.LoadOfLoadingPoint_CCW) + ", LoadingPoint_CCW: " + str(self.LoadingPoint_CCW))
            ######################################################################################################

            ######################################################################################################
            self.ListOfCalibrationPoints_Load_CW = [self.Offset_Load] + self.LoadOfLoadingPoint_CW + [self.Fullscale_Load]
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, ListOfCalibrationPoints_Load_CW: " + str(self.ListOfCalibrationPoints_Load_CW))

            self.ListOfCalibrationPoints_Value_CW = [self.Offset_Value] + self.LoadingPoint_CW + [self.Fullscale_Value]
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, ListOfCalibrationPoints_Value_CW: " + str(self.ListOfCalibrationPoints_Value_CW))

            self.ListOfCalibrationPoints_Load_CCW = [self.Offset_Load] + self.LoadOfLoadingPoint_CCW + [self.Fullscale_Load]
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, ListOfCalibrationPoints_Load_CCW: " + str(self.ListOfCalibrationPoints_Load_CCW))

            self.ListOfCalibrationPoints_Value_CCW = [self.Offset_Value] + self.LoadingPoint_CCW + [self.Fullscale_Value]
            if PrintInfoForDebuggingFlag == 1: print("InitializeDevice, ListOfCalibrationPoints_Value_CCW: " + str(self.ListOfCalibrationPoints_Value_CCW))
            ######################################################################################################

            ######################################################################################################
            self.ActualSamplingRate_HexValue = int(self.FUTEK_USB_DLL_Object.Get_ADC_Sampling_Rate_Setting(self.DeviceHandle, self.DeviceChannel)) #https://media.futek.com/docs/dotnet/api/SamplingRateCodes.html
            self.ActualSamplingRate_HzValue = self.SamplingRateCode_USB520_HexValueAsKey_Dict[self.ActualSamplingRate_HexValue]

            ##############################################
            if self.SamplingRateInHz != self.ActualSamplingRate_HzValue:
                Set_ADC_Configuration_TempReturnedValue = self.FUTEK_USB_DLL_Object.Set_ADC_Configuration(self.DeviceHandle, self.SamplingRateCode_USB520_SamplingRateInHzAsKey_Dict[self.SamplingRateInHz], self.DeviceChannel)

                time.sleep(4.0) #Reader needs time to reset the ADC.

                self.ActualSamplingRate_HexValue = int(self.FUTEK_USB_DLL_Object.Get_ADC_Sampling_Rate_Setting(self.DeviceHandle, self.DeviceChannel)) #https://media.futek.com/docs/dotnet/api/SamplingRateCodes.html
                self.ActualSamplingRate_HzValue = self.SamplingRateCode_USB520_HexValueAsKey_Dict[self.ActualSamplingRate_HexValue]
            ##############################################

            ######################################################################################################

            ######################################################################################################
            if self.ResetAngleOnInitializationFlag == 1:
                self.FUTEK_USB_DLL_Object.Reset_Angle(self.DeviceHandle, self.DeviceChannel)
                print("@@@@@@@@@@@ InitializeDevice, self.FUTEK_USB_DLL_Object.Reset_Angle event fired! @@@@@@@@@@@")
                time.sleep(4.0)
            ######################################################################################################

            ######################################################################################################
            return 1
            ######################################################################################################

            ######################################################################################################
            ######################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("InitializeDevice: Exceptions: %s" % exceptions)
            return 0
            #traceback.print_exc()
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
    def ConvertAngleFromEncoderTicksToAllUnits(self, InputAngle_EncoderCounts):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ConvertedValuesDict =  dict([("EncoderTicks", -11111.0),
                                        ("Deg", -11111.0),
                                        ("Rad", -11111.0),
                                        ("Rev", -11111.0)])

            InputAngle_EncoderCounts = float(InputAngle_EncoderCounts)
            ##########################################################################################################

            ##########################################################################################################
            ConvertedValue_Deg = InputAngle_EncoderCounts*(360./(10.0*4.0*self.Rotation_PulsesPerRotation_ActualValue)) #FUTEK puts a random x10

            ConvertedValue_Rad = ConvertedValue_Deg*(math.pi/180.0)
            ConvertedValue_Rev = ConvertedValue_Deg*(1.0/360.0)
            ##########################################################################################################

            ##########################################################################################################
            ConvertedValuesDict = dict([("EncoderTicks", InputAngle_EncoderCounts),
                                        ("Deg", ConvertedValue_Deg),
                                        ("Rad", ConvertedValue_Rad),
                                        ("Rev", ConvertedValue_Rev)])
            ##########################################################################################################'

            ##########################################################################################################
            return ConvertedValuesDict
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("ConvertPositionToAllUnits InputAngle_EncoderCounts: " + str(InputAngle_EncoderCounts) + ", exceptions: %s" % exceptions)
            #traceback.print_exc()
            return ConvertedValuesDict
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
    def ConvertAngularSpeedFromRPMtoAllUnits(self, InputAngularSpeed_RPM):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ConvertedValuesDict =  dict([("EncoderTicksPerSec", -11111.0),
                                        ("DegPerSec", -11111.0),
                                        ("RadPerSec", -11111.0),
                                        ("RevPerSec", -11111.0),
                                        ("RevPerMin", -11111.0)])

            InputAngularSpeed_RPM = float(InputAngularSpeed_RPM)
            ##########################################################################################################

            ##########################################################################################################
            ConvertedValue_RevPerSec = InputAngularSpeed_RPM*(1.0/60.0)
            ConvertedValue_DegPerSec = ConvertedValue_RevPerSec*(360.0)
            ConvertedValue_RadPerSec = ConvertedValue_RevPerSec*(2.0*math.pi)
            ConvertedValue_EncoderTicksPerSec = ConvertedValue_RevPerSec*(4.0*self.Rotation_PulsesPerRotation_ActualValue)
            ##########################################################################################################

            ##########################################################################################################
            ConvertedValuesDict =  dict([("EncoderTicksPerSec", ConvertedValue_EncoderTicksPerSec),
                                        ("DegPerSec", ConvertedValue_DegPerSec),
                                        ("RadPerSec", ConvertedValue_RadPerSec),
                                        ("RevPerSec", ConvertedValue_RevPerSec),
                                        ("RevPerMin", InputAngularSpeed_RPM)])
            ##########################################################################################################'

            ##########################################################################################################
            return ConvertedValuesDict
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("ConvertAngularSpeedFromRPMtoAllUnits InputAngle_EncoderCounts: " + str(InputAngularSpeed_RPM) + ", exceptions: %s" % exceptions)
            #traceback.print_exc()
            return ConvertedValuesDict
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    '''
    ##########################################################################################################
    ##########################################################################################################
    def SetEncoderOffset_ExternalProgram(self, EncoderOffset_ToBeSet, PrintDebugFlag=0):
        try:

            self.EncoderOffset_ToBeSet = EncoderOffset_ToBeSet

            self.EncoderOffset_NeedsToBeSetFlag = 1

            if PrintDebugFlag == 1:
                print("SetEncoderOffset_ExternalProgram event fired.")

        except:
            exceptions = sys.exc_info()[0]
            print("SetEncoderOffset_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetEncoderOffset(self, EncoderOffset_ToBeSet, PrintDebugFlag=0):
    
        try:
            if self.AllowEncoderToBeZeroedFlag == 1:

                ##########################################################################################################
                
                #Do the work here.

                if PrintDebugFlag == 1:
                    print("__SetEncoderOffset event fired.")
                ##########################################################################################################

            else:
                print("__SetEncoderOffset event CANNOT be fired because AllowEncoderToBeZeroedFlag = 0.")

        except:
            exceptions = sys.exc_info()[0]
            print("__SetEncoderOffset, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    '''

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def DedicatedRxThread(self):

        self.MyPrint_WithoutLogFile("Started DedicatedRxThread for FutekForceTorqueReaderUSB520_ReubenPython3Class object.")
        self.DedicatedRxThread_StillRunningFlag = 1

        self.StartingTime_CalculatedFromDedicatedRxThread = self.getPreciseSecondsTimeStampString()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.CurrentTime_CalculatedFromDedicatedRxThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromDedicatedRxThread
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
            try:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ADC_RawValue = float(self.FUTEK_USB_DLL_Object.Normal_Data_Request(self.DeviceHandle, self.DeviceChannel))
                ForceOrTorque_CalibratedValue = (ADC_RawValue - self.Offset_Value) * ((self.Fullscale_Load - self.Offset_Load) / (self.Fullscale_Value - self.Offset_Value)) / self.DecimalPoint_ConversionFactor
                # Linear interpolation between two points (from https://media.futek.com/content/futek/files/pdf/Manuals_and_Technical_Documents/USBLabVIEWExampleGuide.pdf)
                # Note that there is also an interpolation that involves the 5-point calibration that isn't included here.
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.PrintForceTorqueValuesFlag == 1:
                    print("ADC_RawValue: " + str(ADC_RawValue) + ", ForceOrTorque_CalibratedValue: " + str(ForceOrTorque_CalibratedValue))
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("FTmeasurement", ForceOrTorque_CalibratedValue)]))

                self.CurrentFTmeasurement_Raw = ResultsDict["FTmeasurement"]["Raw_MostRecentValuesList"][0]
                self.CurrentFTmeasurement_Filtered = ResultsDict["FTmeasurement"]["Filtered_MostRecentValuesList"][0]
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.ZeroAndSnapshotData_OPEN_FLAG == 1:

                    if self.ResetTare_EventNeedsToBeFiredFlag == 1:

                        ##########################################################################################################
                        if self.ResetTare_EventIsCurrentlyBeingExecutedFlag == 0:

                            ################################################### START the tare process
                            self.ResetTare_TimeOfLastEvent = self.CurrentTime_CalculatedFromDedicatedRxThread

                            self.ResetTare_EventHasHappenedFlag = 0
                            self.ResetTare_EventIsCurrentlyBeingExecutedFlag = 1

                            self.ZeroAndSnapshotData_Object.ZeroAllVariables()
                            print("FutekForceTorqueReaderUSB520_ReubenPython3Class: Started tare process.")
                            ###################################################

                        ##########################################################################################################

                        ##########################################################################################################
                        else:

                            if self.CurrentTime_CalculatedFromDedicatedRxThread - self.ResetTare_TimeOfLastEvent >= 1.1*self.DataCollectionDurationInSecondsForSnapshottingAndZeroing:

                                ###################################################
                                self.ResetTare_EventHasHappenedFlag = 1
                                self.ResetTare_EventIsCurrentlyBeingExecutedFlag = 0

                                self.ResetTare_EventNeedsToBeFiredFlag = 0
                                print("FutekForceTorqueReaderUSB520_ReubenPython3Class: Ended tare process.")
                                ###################################################

                        ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.ZeroAndSnapshotData_OPEN_FLAG == 1:

                    ##########################################################################################################
                    self.ZeroAndSnapshotData_Object.CheckStateMachine()
                    ##########################################################################################################

                    ##########################################################################################################
                    FTmeasurement_ListOfDictsAsInputToZeroingObject = [dict([("Variable_Name", "CurrentFTmeasurement"),
                                                                             ("Raw_CurrentValue", self.CurrentFTmeasurement_Raw),
                                                                             ("Filtered_CurrentValue", self.CurrentFTmeasurement_Filtered)])]

                    self.ZeroAndSnapshotData_MostRecentDict = self.ZeroAndSnapshotData_Object.UpdateData(FTmeasurement_ListOfDictsAsInputToZeroingObject)

                    if "DataUpdateNumber" in self.ZeroAndSnapshotData_MostRecentDict:
                        self.ZeroAndSnapshotData_MostRecentDict_DataUpdateNumber = self.ZeroAndSnapshotData_MostRecentDict["DataUpdateNumber"]
                        self.ZeroAndSnapshotData_MostRecentDict_LoopFrequencyHz = self.ZeroAndSnapshotData_MostRecentDict["LoopFrequencyHz"]
                        self.ZeroAndSnapshotData_MostRecentDict_OnlyVariablesAndValuesDictOfDicts = self.ZeroAndSnapshotData_MostRecentDict["OnlyVariablesAndValuesDictOfDicts"]

                        self.CurrentFTmeasurement_Raw = self.ZeroAndSnapshotData_MostRecentDict_OnlyVariablesAndValuesDictOfDicts["CurrentFTmeasurement"]["Raw_CurrentValue_Zeroed"]
                        self.CurrentFTmeasurement_Filtered = self.ZeroAndSnapshotData_MostRecentDict_OnlyVariablesAndValuesDictOfDicts["CurrentFTmeasurement"]["Filtered_CurrentValue_Zeroed"]
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ########################################################################################################## Calculate derivative
                ##########################################################################################################
                try: #in case there's a division-by-zero.

                    ##########################################################################################################
                    FTmeasurementDerivative_Raw_TEMP = (self.CurrentFTmeasurement_Filtered - self.LastFTmeasurement_Filtered)/(1.0/self.DataStreamingFrequency_CalculatedFromDedicatedRxThread) #We also filter DataStreamingFrequency_CalculatedFromDedicatedRxThread

                    ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("FTmeasurementDerivative", FTmeasurementDerivative_Raw_TEMP)]))

                    self.CurrentFTmeasurementDerivative_Raw = ResultsDict["FTmeasurementDerivative"]["Raw_MostRecentValuesList"][0]
                    self.CurrentFTmeasurementDerivative_Filtered = ResultsDict["FTmeasurementDerivative"]["Filtered_MostRecentValuesList"][0]
                    ##########################################################################################################

                except:
                    pass
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.LoopCounter_CalculatedFromDedicatedRxThread_EnocderQueriesOnly >= round(self.SamplingRateInHz / 10.0):  # Max of 10Hz for new angular FTmeasurements

                    RotationValue_SuccessFlag = float(self.FUTEK_USB_DLL_Object.Get_Rotation_Values(self.DeviceHandle))  # This is what tells the reader to update its self.FUTEK_USB_DLL_Object.AngleValue and self.FUTEK_USB_DLL_Object.RPMValue
                    self.AngleValue_EncoderCounts = float(self.FUTEK_USB_DLL_Object.AngleValue)  # The value must be between -8,388,608 and +8,388,607. We're expecting a 0.25deg resolution (1/(360.0*4))
                    self.AngularSpeedValue_RevPerMin = float(self.FUTEK_USB_DLL_Object.RPMValue) * self.AngularResolution_ActualValue_Deg  # The value must be between -8,388,608 and +8,388,607.

                    self.AngleValue_AllUnitsDict = self.ConvertAngleFromEncoderTicksToAllUnits(self.AngleValue_EncoderCounts)
                    self.AngularSpeedValue_AllUnitsDict = self.ConvertAngularSpeedFromRPMtoAllUnits(self.AngularSpeedValue_RevPerMin)

                    if self.PrintAngleValuesFlag == 1: print("AngleValue_EncoderCounts: " + str(self.AngleValue_EncoderCounts) + ", AngularSpeedValue_RevPerMin: " + str(self.AngularSpeedValue_RevPerMin))

                    self.LoopCounter_CalculatedFromDedicatedRxThread_EnocderQueriesOnly = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                self.MostRecentDataDict["Time"] = self.CurrentTime_CalculatedFromDedicatedRxThread

                self.MostRecentDataDict["CurrentTime_CalculatedFromDedicatedRxThread"] = self.CurrentTime_CalculatedFromDedicatedRxThread
                self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromDedicatedRxThread"] = self.DataStreamingFrequency_CalculatedFromDedicatedRxThread

                self.MostRecentDataDict["FTmeasurement_ExponentialSmoothingFilterLambda"] = self.FTmeasurement_ExponentialSmoothingFilterLambda
                self.MostRecentDataDict["FTmeasurementDerivative_ExponentialSmoothingFilterLambda"] = self.FTmeasurementDerivative_ExponentialSmoothingFilterLambda

                self.MostRecentDataDict["FTmeasurement_Raw"] = self.CurrentFTmeasurement_Raw
                self.MostRecentDataDict["FTmeasurement_Filtered"] = self.CurrentFTmeasurement_Filtered

                self.MostRecentDataDict["FTmeasurementDerivative_Raw"] = self.CurrentFTmeasurementDerivative_Raw
                self.MostRecentDataDict["FTmeasurementDerivative_Filtered"] = self.CurrentFTmeasurementDerivative_Filtered

                self.MostRecentDataDict["AngleValue_AllUnitsDict"] = self.AngleValue_AllUnitsDict
                self.MostRecentDataDict["AngularSpeedValue_AllUnitsDict"] = self.AngularSpeedValue_AllUnitsDict

                self.LastFTmeasurement_Raw = self.CurrentFTmeasurement_Raw
                self.LastFTmeasurement_Filtered = self.CurrentFTmeasurement_Filtered
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
                self.LoopCounter_CalculatedFromDedicatedRxThread_EnocderQueriesOnly = self.LoopCounter_CalculatedFromDedicatedRxThread_EnocderQueriesOnly + 1

                self.UpdateFrequencyCalculation_DedicatedRxThread_Filtered()

                if self.DedicatedRxThread_TimeToSleepEachLoop > 0.0:
                    if self.DedicatedRxThread_TimeToSleepEachLoop > 0.001:
                        time.sleep(self.DedicatedRxThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                    else:
                        time.sleep(self.DedicatedRxThread_TimeToSleepEachLoop)
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("DedicatedRxThread, exceptions: %s" % exceptions)
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
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            self.CloseDevice()
            self.ZeroAndSnapshotData_Object.ExitProgram_Callback()

        except:
            pass

        self.MyPrint_WithoutLogFile("Finished DedicatedRxThread for FutekForceTorqueReaderUSB520_ReubenPython3Class object.")
        self.DedicatedRxThread_StillRunningFlag = 0
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
    ##########################################################################################################
    def CloseDevice(self):

        try:

            self.FUTEK_USB_DLL_Object.Reset_Board(self.DeviceHandle)  # Without this call, the board gets into a bad state
            print("FutekForceTorqueReaderUSB520_ReubenPython3Class: CloseDevice, event fired!")

        except:
            exceptions = sys.exc_info()[0]
            print("FutekForceTorqueReaderUSB520_ReubenPython3Class: CloseDevice, Exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for FutekForceTorqueReaderUSB520_ReubenPython3Class object")

        self.EXIT_PROGRAM_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent):

        self.GUI_Thread(GuiParent)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for FutekForceTorqueReaderUSB520_ReubenPython3Class object.")

        #################################################
        #################################################
        #################################################
        self.root = parent
        self.parent = parent
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.TkinterScaleLabelWidth = 30
        self.TkinterScaleWidth = 10
        self.TkinterScaleLength = 250
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=50)
        self.DeviceInfo_Label["text"] = (self.NameToDisplay_UserSet)
        self.DeviceInfo_Label.grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        self.ResetTare_Button = Button(self.myFrame, text="Reset Tare", state="normal", width=20, command=lambda: self.ResetTare())
        self.ResetTare_Button.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=120)
        self.Data_Label.grid(row=2, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=10, rowspan=1)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=3, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=10, rowspan=10)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################
        #################################################
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ResetTare(self):

        self.ResetTare_EventNeedsToBeFiredFlag = 1

        #print("ResetTare_Button_Response: Event fired!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                #######################################################
                #######################################################
                try:

                    #######################################################
                    #######################################################
                    #######################################################
                    self.Data_Label["text"] = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict)
                    #######################################################
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    #######################################################
                    if self.ZeroAndSnapshotData_OPEN_FLAG == 1 and self.ZeroAndSnapshotData___USE_GUI_FLAG == 1:
                        self.ZeroAndSnapshotData_Object.GUI_update_clock()
                    #######################################################
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    #######################################################
                    self.UpdateFrequencyCalculation_GUIthread_Filtered()
                    #######################################################
                    #######################################################
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("FutekForceTorqueReaderUSB520_ReubenPython3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

        number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

        ListOfStringsToJoin = []

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if isinstance(input, str) == 1:
            ListOfStringsToJoin.append(input)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
            element = float(input)
            prefix_string = "{:." + str(number_of_decimal_places) + "f}"
            element_as_string = prefix_string.format(element)

            ##########################################################################################################
            ##########################################################################################################
            if element >= 0:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
                element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
            else:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
            ##########################################################################################################
            ##########################################################################################################

            ListOfStringsToJoin.append(element_as_string)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, list) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, tuple) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, dict) == 1:

            if len(input) > 0:
                for Key in input: #RECURSION
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a dict()
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        else:
            ListOfStringsToJoin.append(str(input))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if len(ListOfStringsToJoin) > 1:

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            StringToReturn = ""
            for Index, StringToProcess in enumerate(ListOfStringsToJoin):

                ################################################
                if Index == 0: #The first element
                    if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                        StringToReturn = "{"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                        StringToReturn = "("
                    else:
                        StringToReturn = "["

                    StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
                ################################################

                ################################################
                elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                    StringToReturn = StringToReturn + StringToProcess + ", "
                ################################################

                ################################################
                else: #The last element
                    StringToReturn = StringToReturn + StringToProcess

                    if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                        StringToReturn = StringToReturn + "}"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                        StringToReturn = StringToReturn + ")"
                    else:
                        StringToReturn = StringToReturn + "]"

                ################################################

            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        elif len(ListOfStringsToJoin) == 1:
            StringToReturn = ListOfStringsToJoin[0]

        else:
            StringToReturn = ListOfStringsToJoin

        return StringToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertDictToProperlyFormattedStringForPrinting(self, DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

        try:
            ProperlyFormattedStringForPrinting = ""
            ItemsPerLineCounter = 0

            for Key in DictToPrint:

                ##########################################################################################################
                if isinstance(DictToPrint[Key], dict): #RECURSION
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ":\n" + \
                                                         self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key],
                                                                                                              NumberOfDecimalsPlaceToUse,
                                                                                                              NumberOfEntriesPerLine,
                                                                                                              NumberOfTabsBetweenItems)

                else:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ": " + \
                                                         self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key],
                                                                                                                                               0,
                                                                                                                                               NumberOfDecimalsPlaceToUse)
                ##########################################################################################################

                ##########################################################################################################
                if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                    ItemsPerLineCounter = ItemsPerLineCounter + 1
                else:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                    ItemsPerLineCounter = 0
                ##########################################################################################################

            return ProperlyFormattedStringForPrinting

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertDictToProperlyFormattedStringForPrinting, Exceptions: %s" % exceptions)
            return ""
            #traceback.print_exc()
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