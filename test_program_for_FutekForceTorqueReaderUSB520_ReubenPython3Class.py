# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision D, 08/08/2025

Verified working on: Python 3.11/3.12 for Windows 10, 11 64-bit.
'''

__author__ = 'reuben.brewer'

##########################################
from CSVdataLogger_ReubenPython3Class import *
from EntryListWithBlinking_ReubenPython2and3Class import *
from FutekForceTorqueReaderUSB520_ReubenPython3Class import *
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
##########################################

##########################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
import signal #for CTRLc_HandlerFunction
import keyboard
##########################################

##########################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
##########################################

##########################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
##########################################

###########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def CTRLc_RegisterHandlerFunction():

    CurrentHandlerRegisteredForSIGINT = signal.getsignal(signal.SIGINT)
    #print("CurrentHandlerRegisteredForSIGINT: " + str(CurrentHandlerRegisteredForSIGINT))

    defaultish = (signal.SIG_DFL, signal.SIG_IGN, None, getattr(signal, "default_int_handler", None)) #Treat Python's built-in default handler as "unregistered"

    if CurrentHandlerRegisteredForSIGINT in defaultish: # Only install if it's default/ignored (i.e., nobody set it yet)
        signal.signal(signal.SIGINT, CTRLc_HandlerFunction)
        print("test_program_for_FutekForceTorqueReaderUSB520_ReubenPython3Class.py, CTRLc_RegisterHandlerFunction event fired!")

    else:
        print("test_program_for_FutekForceTorqueReaderUSB520_ReubenPython3Class.py, could not register CTRLc_RegisterHandlerFunction (already registered previously)")
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def CTRLc_HandlerFunction(signum, frame):

    print("test_program_for_FutekForceTorqueReaderUSB520_ReubenPython3Class.py, CTRLc_HandlerFunction event firing!")

    ExitProgram_Callback()

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

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
                ListOfStringsToJoin.append(ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                ListOfStringsToJoin.append("TUPLE" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                ListOfStringsToJoin.append(str(Key) + ": " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

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

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

    try:
        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ":\n" + \
                                                     ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ": " + \
                                                     ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

            if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                ItemsPerLineCounter = ItemsPerLineCounter + 1
            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                ItemsPerLineCounter = 0

        return ProperlyFormattedStringForPrinting

    except:
        exceptions = sys.exc_info()[0]
        print("ConvertDictToProperlyFormattedStringForPrinting, Exceptions: %s" % exceptions)
        return ""
        # traceback.print_exc()
#######################################################################################################################
#######################################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global LoopCounter_CalculatedFromGUIthread
    global CurrentTime_CalculatedFromGUIthread
    global StartingTime_CalculatedFromGUIthread
    global LastTime_CalculatedFromGUIthread
    global DataStreamingFrequency_CalculatedFromGUIthread
    global DataStreamingDeltaT_CalculatedFromGUIthread

    global FutekForceTorqueReaderUSB520_Object
    global FutekForceTorqueReaderUSB520_OPEN_FLAG
    global SHOW_IN_GUI_FutekForceTorqueReaderUSB520_FLAG
    global FutekForceTorqueReaderUSB520_MostRecentDict
    global FutekForceTorqueReaderUSB520_MostRecentDict_Label

    global EntryListWithBlinking_Object
    global EntryListWithBlinking_OPEN_FLAG

    global CSVdataLogger_Object
    global CSVdataLogger_OPEN_FLAG
    global SHOW_IN_GUI_CSVdataLogger_FLAG

    global MyPrint_Object
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################
        #########################################################

            #########################################################
            #########################################################
            try:
                #########################################################
                CurrentTime_CalculatedFromGUIthread = getPreciseSecondsTimeStampString() - StartingTime_CalculatedFromGUIthread
                [LoopCounter_CalculatedFromGUIthread, LastTime_CalculatedFromGUIthread, DataStreamingFrequency_CalculatedFromGUIthread, DataStreamingDeltaT_CalculatedFromGUIthread] = UpdateFrequencyCalculation(LoopCounter_CalculatedFromGUIthread, CurrentTime_CalculatedFromGUIthread,
                                                                                                                                                                                                                  LastTime_CalculatedFromGUIthread, DataStreamingFrequency_CalculatedFromGUIthread,
                                                                                                                                                                                                                  DataStreamingDeltaT_CalculatedFromGUIthread)
                #########################################################

                #########################################################
                FutekForceTorqueReaderUSB520_MostRecentDict_Label["text"] = ConvertDictToProperlyFormattedStringForPrinting(FutekForceTorqueReaderUSB520_MostRecentDict, NumberOfDecimalsPlaceToUse=3, NumberOfEntriesPerLine=3, NumberOfTabsBetweenItems=1)
                #########################################################

                #########################################################
                if FutekForceTorqueReaderUSB520_OPEN_FLAG == 1 and SHOW_IN_GUI_FutekForceTorqueReaderUSB520_FLAG == 1:
                    FutekForceTorqueReaderUSB520_Object.GUI_update_clock()
                #########################################################

                #########################################################
                if EntryListWithBlinking_OPEN_FLAG == 1:
                    EntryListWithBlinking_Object.GUI_update_clock()
                #########################################################

                #########################################################
                if CSVdataLogger_OPEN_FLAG == 1 and SHOW_IN_GUI_CSVdataLogger_FLAG == 1:
                    CSVdataLogger_Object.GUI_update_clock()
                #########################################################

                #########################################################
                if MyPrint_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPrint_FLAG == 1:
                    MyPrint_Object.GUI_update_clock()
                #########################################################

                #########################################################
                root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
                #########################################################

            #########################################################
            #########################################################

            #########################################################
            #########################################################
            except:
                exceptions = sys.exc_info()[0]
                print("GUI_update_clock(), Exceptions: %s" % exceptions)
                traceback.print_exc()
            #########################################################
            #########################################################

        #########################################################
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG

    print("ExitProgram_Callback event fired!")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def UpdateFrequencyCalculation(LoopCounter, CurrentTime, LastTime, DataStreamingFrequency, DataStreamingDeltaT):

    try:

        DataStreamingDeltaT = CurrentTime - LastTime

        ##########################
        if DataStreamingDeltaT != 0.0:
            DataStreamingFrequency = 1.0/DataStreamingDeltaT
        ##########################

        LastTime = CurrentTime

        LoopCounter = LoopCounter + 1

        return [LoopCounter, LastTime, DataStreamingFrequency, DataStreamingDeltaT]

    except:
        exceptions = sys.exc_info()[0]
        print("UpdateFrequencyCalculation, exceptions: %s" % exceptions)
        return [-11111.0]*4
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_FutekForceTorqueReaderUSB520
    global Tab_MyPrint
    global Tab_CSVdataLogger

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_FutekForceTorqueReaderUSB520 = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_FutekForceTorqueReaderUSB520, text='   FutekForceTorqueReaderUSB520   ')

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        Tab_MyPrint = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        Tab_CSVdataLogger = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_CSVdataLogger, text='   CSVdataLogger   ')

        TabControlObject.grid(row=0, column=0, sticky='nsew')

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############
        #################################################
    else:
        #################################################
        Tab_MainControls = root
        Tab_FutekForceTorqueReaderUSB520 = root
        Tab_MyPrint = root
        Tab_CSVdataLogger = root
        #################################################

    ##########################################################################################################

    #################################################
    #################################################
    global MainFrame
    MainFrame = Frame(Tab_MainControls)
    MainFrame.grid(row=0, column=0, padx=1, pady=1, rowspan=1, columnspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    global FutekForceTorqueReaderUSB520_MostRecentDict_Label
    FutekForceTorqueReaderUSB520_MostRecentDict_Label = Label(MainFrame, text="FutekForceTorqueReaderUSB520_MostRecentDict_Label", width=120, font=("Helvetica", 10))
    FutekForceTorqueReaderUSB520_MostRecentDict_Label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    global ButtonsFrame
    ButtonsFrame = Frame(MainFrame)
    ButtonsFrame.grid(row = 1, column = 0, padx = 1, pady = 1, rowspan = 1, columnspan = 1)
    #################################################
    #################################################

    #################################################
    #################################################
    global ResetTare_Button
    ResetTare_Button = Button(ButtonsFrame, text=" TestProgram: Reset Tare", state="normal", width=20, command=lambda: ResetTare_Button_Response())
    ResetTare_Button.grid(row=0, column=0, padx=10, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    ##########################################################################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_FutekForceTorqueReaderUSB520_ReubenPython3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ResetTare_Button_Response():
    global FutekForceTorqueReaderUSB520_ResetTare_EventNeedsToBeFiredFlag

    FutekForceTorqueReaderUSB520_ResetTare_EventNeedsToBeFiredFlag = 1

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    #CTRLc_RegisterHandlerFunction()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    #################################################
    #################################################

    ################################################# unicorn
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_FutekForceTorqueReaderUSB520_FLAG
    USE_FutekForceTorqueReaderUSB520_FLAG = 1

    global USE_EntryListWithBlinking_FLAG
    USE_EntryListWithBlinking_FLAG = 1

    global USE_MyPrint_FLAG
    USE_MyPrint_FLAG = 0

    global USE_MyPlotterPureTkinterStandAloneProcess0_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess0_FLAG = 1

    global USE_MyPlotterPureTkinterStandAloneProcess1_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess1_FLAG = 1

    global USE_CSVdataLogger_FLAG
    USE_CSVdataLogger_FLAG = 1

    global USE_KEYBOARD_FLAG
    USE_KEYBOARD_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_FutekForceTorqueReaderUSB520_FLAG
    SHOW_IN_GUI_FutekForceTorqueReaderUSB520_FLAG = 1

    global SHOW_IN_GUI_MyPrint_FLAG
    SHOW_IN_GUI_MyPrint_FLAG = 1

    global SHOW_IN_GUI_CSVdataLogger_FLAG
    SHOW_IN_GUI_CSVdataLogger_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_FutekForceTorqueReaderUSB520
    global GUI_COLUMN_FutekForceTorqueReaderUSB520
    global GUI_PADX_FutekForceTorqueReaderUSB520
    global GUI_PADY_FutekForceTorqueReaderUSB520
    global GUI_ROWSPAN_FutekForceTorqueReaderUSB520
    global GUI_COLUMNSPAN_FutekForceTorqueReaderUSB520
    GUI_ROW_FutekForceTorqueReaderUSB520 = 1

    GUI_COLUMN_FutekForceTorqueReaderUSB520 = 0
    GUI_PADX_FutekForceTorqueReaderUSB520 = 1
    GUI_PADY_FutekForceTorqueReaderUSB520 = 1
    GUI_ROWSPAN_FutekForceTorqueReaderUSB520 = 1
    GUI_COLUMNSPAN_FutekForceTorqueReaderUSB520 = 2

    global GUI_ROW_EntryListWithBlinking
    global GUI_COLUMN_EntryListWithBlinking
    global GUI_PADX_EntryListWithBlinking
    global GUI_PADY_EntryListWithBlinking
    global GUI_ROWSPAN_EntryListWithBlinking
    global GUI_COLUMNSPAN_EntryListWithBlinking
    GUI_ROW_EntryListWithBlinking = 2

    GUI_COLUMN_EntryListWithBlinking = 0
    GUI_PADX_EntryListWithBlinking = 1
    GUI_PADY_EntryListWithBlinking = 1
    GUI_ROWSPAN_EntryListWithBlinking = 1
    GUI_COLUMNSPAN_EntryListWithBlinking = 1

    global GUI_ROW_CSVdataLogger
    global GUI_COLUMN_CSVdataLogger
    global GUI_PADX_CSVdataLogger
    global GUI_PADY_CSVdataLogger
    global GUI_ROWSPAN_CSVdataLogger
    global GUI_COLUMNSPAN_CSVdataLogger
    GUI_ROW_CSVdataLogger = 3

    GUI_COLUMN_CSVdataLogger = 0
    GUI_PADX_CSVdataLogger = 1
    GUI_PADY_CSVdataLogger = 1
    GUI_ROWSPAN_CSVdataLogger = 1
    GUI_COLUMNSPAN_CSVdataLogger = 1

    global GUI_ROW_MyPrint
    global GUI_COLUMN_MyPrint
    global GUI_PADX_MyPrint
    global GUI_PADY_MyPrint
    global GUI_ROWSPAN_MyPrint
    global GUI_COLUMNSPAN_MyPrint
    GUI_ROW_MyPrint = 4

    GUI_COLUMN_MyPrint = 0
    GUI_PADX_MyPrint = 1
    GUI_PADY_MyPrint = 1
    GUI_ROWSPAN_MyPrint = 1
    GUI_COLUMNSPAN_MyPrint = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    #################################################
    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0
    #################################################

    #################################################
    global LoopCounter_CalculatedFromGUIthread
    LoopCounter_CalculatedFromGUIthread = 0

    global CurrentTime_CalculatedFromGUIthread
    CurrentTime_CalculatedFromGUIthread = -11111.0

    global StartingTime_CalculatedFromGUIthread
    StartingTime_CalculatedFromGUIthread = -11111.0

    global LastTime_CalculatedFromGUIthread
    LastTime_CalculatedFromGUIthread = -11111.0

    global DataStreamingFrequency_CalculatedFromGUIthread
    DataStreamingFrequency_CalculatedFromGUIthread = -1

    global DataStreamingDeltaT_CalculatedFromGUIthread
    DataStreamingDeltaT_CalculatedFromGUIthread = -1
    #################################################

    global root

    global root_Xpos
    root_Xpos = 870

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1600

    global root_height
    root_height = 1300

    global TabControlObject
    global Tab_MainControls
    global Tab_FutekForceTorqueReaderUSB520
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30
    #################################################
    #################################################

    #################################################
    #################################################
    global FutekForceTorqueReaderUSB520_Object

    global FutekForceTorqueReaderUSB520_OPEN_FLAG
    FutekForceTorqueReaderUSB520_OPEN_FLAG = 0

    global FutekForceTorqueReaderUSB520_MostRecentDict
    FutekForceTorqueReaderUSB520_MostRecentDict = dict()

    global FutekForceTorqueReaderUSB520_MostRecentDict_Time
    FutekForceTorqueReaderUSB520_MostRecentDict_Time = 0.0

    global FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurement_Raw
    FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurement_Raw = 0.0

    global FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurement_Filtered
    FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurement_Filtered = 0.0

    global FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurementDerivative_Raw
    FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurementDerivative_Raw = 0.0

    global FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurementDerivative_Filtered
    FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurementDerivative_Filtered = 0.0

    global FutekForceTorqueReaderUSB520_MostRecentDict_AngleValue_AllUnitsDict
    FutekForceTorqueReaderUSB520_MostRecentDict_AngleValue_AllUnitsDict = dict()

    global FutekForceTorqueReaderUSB520_MostRecentDict_AngleValue_Deg
    FutekForceTorqueReaderUSB520_MostRecentDict_AngleValue_Deg = 0.0

    global FutekForceTorqueReaderUSB520_MostRecentDict_AngularSpeedValue_DegPerSec
    FutekForceTorqueReaderUSB520_MostRecentDict_AngularSpeedValue_DegPerSec = 0.0

    global FutekForceTorqueReaderUSB520_MostRecentDict_AngularSpeedValue_AllUnitsDict
    FutekForceTorqueReaderUSB520_MostRecentDict_AngularSpeedValue_AllUnitsDict = dict()

    global FutekForceTorqueReaderUSB520_ResetTare_EventNeedsToBeFiredFlag
    FutekForceTorqueReaderUSB520_ResetTare_EventNeedsToBeFiredFlag = 0

    global FutekForceTorqueReaderUSB520_SamplingRateInHz
    FutekForceTorqueReaderUSB520_SamplingRateInHz = 100.0

    global FutekForceTorqueReaderUSB520_DataCollectionDurationInSecondsForSnapshottingAndZeroing
    FutekForceTorqueReaderUSB520_DataCollectionDurationInSecondsForSnapshottingAndZeroing = 4.0

    global FutekForceTorqueReaderUSB520_FTmeasurement_ExponentialSmoothingFilterLambda
    FutekForceTorqueReaderUSB520_FTmeasurement_ExponentialSmoothingFilterLambda = 0.95

    global FutekForceTorqueReaderUSB520_FTmeasurementDerivative_ExponentialSmoothingFilterLambda
    FutekForceTorqueReaderUSB520_FTmeasurementDerivative_ExponentialSmoothingFilterLambda = 0.5
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_Object

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
    #################################################
    #################################################

    #################################################
    #################################################
    global CSVdataLogger_Object

    global CSVdataLogger_OPEN_FLAG
    CSVdataLogger_OPEN_FLAG = -1

    global CSVdataLogger_MostRecentDict
    CSVdataLogger_MostRecentDict = dict()

    global CSVdataLogger_MostRecentDict_Time
    CSVdataLogger_MostRecentDict_Time = -11111.0

    global CSVdataLogger_Object_SetupDict_VariableNamesForHeaderList
    CSVdataLogger_Object_SetupDict_VariableNamesForHeaderList = ["CurrentTime_MainLoopThread",
                                                                "FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurement_Raw",
                                                                "FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurement_Filtered",
                                                                "FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurementDerivative_Raw",
                                                                "FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurementDerivative_Filtered",
                                                                "FutekForceTorqueReaderUSB520_MostRecentDict_AngleValue_Deg",
                                                                "FutekForceTorqueReaderUSB520_MostRecentDict_AngularSpeedValue_DegPerSec"]
    #################################################
    #################################################

    #################################################
    #################################################
    global EntryListWithBlinking_Object

    global EntryListWithBlinking_OPEN_FLAG
    EntryListWithBlinking_OPEN_FLAG = -1

    global EntryListWithBlinking_MostRecentDict
    EntryListWithBlinking_MostRecentDict = dict()

    global EntryListWithBlinking_MostRecentDict_DataUpdateNumber
    EntryListWithBlinking_MostRecentDict_DataUpdateNumber = 0

    global EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last
    EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last = -1

    EntryWidth = 10
    LabelWidth = 80
    FontSize = 8
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess0_Object

    global MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG = -1

    global MyPlotterPureTkinterStandAloneProcess0_MostRecentDict
    MyPlotterPureTkinterStandAloneProcess0_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess0_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess0_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = -1

    global LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess0
    LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess0 = -11111.0
    #################################################
    #################################################
    
    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess1_Object

    global MyPlotterPureTkinterStandAloneProcess1_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess1_OPEN_FLAG = -1

    global MyPlotterPureTkinterStandAloneProcess1_MostRecentDict
    MyPlotterPureTkinterStandAloneProcess1_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess1_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess1_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = -1

    global LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess1
    LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess1 = -11111.0
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## KEY GUI LINE
    ##########################################################################################################
    ##########################################################################################################
    if USE_GUI_FLAG == 1:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  #Allow enough time for 'root' to be created that we can then pass it into other classes.
    else:
        root = None
        Tab_MainControls = None
        Tab_FutekForceTorqueReaderUSB520 = None
        Tab_MyPrint = None
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global FutekForceTorqueReaderUSB520_GUIparametersDict
    FutekForceTorqueReaderUSB520_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_FutekForceTorqueReaderUSB520_FLAG),
                                                            ("root", Tab_FutekForceTorqueReaderUSB520),
                                                            ("EnableInternal_MyPrint_Flag", 0),
                                                            ("NumberOfPrintLines", 10),
                                                            ("UseBorderAroundThisGuiObjectFlag", 0),
                                                            ("GUI_ROW", GUI_ROW_FutekForceTorqueReaderUSB520),
                                                            ("GUI_COLUMN", GUI_COLUMN_FutekForceTorqueReaderUSB520),
                                                            ("GUI_PADX", GUI_PADX_FutekForceTorqueReaderUSB520),
                                                            ("GUI_PADY", GUI_PADY_FutekForceTorqueReaderUSB520),
                                                            ("GUI_ROWSPAN", GUI_ROWSPAN_FutekForceTorqueReaderUSB520),
                                                            ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_FutekForceTorqueReaderUSB520)])

    global FutekForceTorqueReaderUSB520_SetupDict
    FutekForceTorqueReaderUSB520_SetupDict = dict([("GUIparametersDict", FutekForceTorqueReaderUSB520_GUIparametersDict),
                                                    ("ZeroAndSnapshotData___USE_GUI_FLAG", 0),
                                                    ("NameToDisplay_UserSet", "FutekForceTorqueReaderUSB520"),
                                                    ("SerialNumber_Desired", "1132494"),
                                                    ("TypeOfBoard_EnglishNameString", "USB520"),
                                                    ("SamplingRateInHz", FutekForceTorqueReaderUSB520_SamplingRateInHz), #[5, 10, 15, 20, 25, 30, 50, 60, 100, 600, 960, 1200, 2400, 4800]
                                                    ("ResetAngleOnInitializationFlag", 0),
                                                    ("DedicatedRxThread_TimeToSleepEachLoop", 0.002),
                                                    ("DataCollectionDurationInSecondsForSnapshottingAndZeroing", FutekForceTorqueReaderUSB520_DataCollectionDurationInSecondsForSnapshottingAndZeroing),
                                                    ("FTmeasurement_ExponentialSmoothingFilterLambda", FutekForceTorqueReaderUSB520_FTmeasurement_ExponentialSmoothingFilterLambda),
                                                    ("FTmeasurementDerivative_ExponentialSmoothingFilterLambda", FutekForceTorqueReaderUSB520_FTmeasurementDerivative_ExponentialSmoothingFilterLambda)])

    if USE_FutekForceTorqueReaderUSB520_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            FutekForceTorqueReaderUSB520_Object = FutekForceTorqueReaderUSB520_ReubenPython3Class(FutekForceTorqueReaderUSB520_SetupDict)
            FutekForceTorqueReaderUSB520_OPEN_FLAG = FutekForceTorqueReaderUSB520_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("FutekForceTorqueReaderUSB520_ReubenPython3ClassObject __init__, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_FutekForceTorqueReaderUSB520_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if FutekForceTorqueReaderUSB520_OPEN_FLAG != 1:
                print("Failed to open FutekForceTorqueReaderUSB520_ReubenPython3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global CSVdataLogger_Object_GUIparametersDict
    CSVdataLogger_Object_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_CSVdataLogger_FLAG),
                                                                    ("root", Tab_CSVdataLogger), #Tab_MainControls
                                                                    ("EnableInternal_MyPrint_Flag", 1),
                                                                    ("NumberOfPrintLines", 10),
                                                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                    ("GUI_ROW", GUI_ROW_CSVdataLogger),
                                                                    ("GUI_COLUMN", GUI_COLUMN_CSVdataLogger),
                                                                    ("GUI_PADX", GUI_PADX_CSVdataLogger),
                                                                    ("GUI_PADY", GUI_PADY_CSVdataLogger),
                                                                    ("GUI_ROWSPAN", GUI_ROWSPAN_CSVdataLogger),
                                                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_CSVdataLogger)])

    global CSVdataLogger_Object_SetupDict
    CSVdataLogger_Object_SetupDict = dict([("GUIparametersDict", CSVdataLogger_Object_GUIparametersDict),
                                                            ("NameToDisplay_UserSet", "CSVdataLogger"),
                                                            ("CSVfile_DirectoryPath", "C:\\CSVfiles"),
                                                            ("FileNamePrefix", "CSV_file_"),
                                                            ("VariableNamesForHeaderList", CSVdataLogger_Object_SetupDict_VariableNamesForHeaderList),
                                                            ("MainThread_TimeToSleepEachLoop", 0.002),
                                                            ("SaveOnStartupFlag", 0)])

    if USE_CSVdataLogger_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            CSVdataLogger_Object = CSVdataLogger_ReubenPython3Class(CSVdataLogger_Object_SetupDict)
            CSVdataLogger_OPEN_FLAG = CSVdataLogger_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("CSVdataLogger_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_CSVdataLogger_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if CSVdataLogger_OPEN_FLAG != 1:
                print("Failed to open CSVdataLogger_ReubenPython3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global EntryListWithBlinking_Object_GUIparametersDict
    EntryListWithBlinking_Object_GUIparametersDict = dict([("root", Tab_MainControls),
                                                                                ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                ("GUI_ROW", GUI_ROW_EntryListWithBlinking),
                                                                                ("GUI_COLUMN", GUI_COLUMN_EntryListWithBlinking),
                                                                                ("GUI_PADX", GUI_PADX_EntryListWithBlinking),
                                                                                ("GUI_PADY", GUI_PADY_EntryListWithBlinking),
                                                                                ("GUI_ROWSPAN", GUI_ROWSPAN_EntryListWithBlinking),
                                                                                ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_EntryListWithBlinking)])

    global EntryListWithBlinking_Variables_ListOfDicts
    EntryListWithBlinking_Variables_ListOfDicts = [dict([("Name", "FutekForceTorqueReaderUSB520_FTmeasurement_ExponentialSmoothingFilterLambda"),("Type", "float"),("StartingVal", FutekForceTorqueReaderUSB520_FTmeasurement_ExponentialSmoothingFilterLambda),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                   dict([("Name", "FutekForceTorqueReaderUSB520_FTmeasurementDerivative_ExponentialSmoothingFilterLambda"),("Type", "float"),("StartingVal", FutekForceTorqueReaderUSB520_FTmeasurementDerivative_ExponentialSmoothingFilterLambda),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)])]

    global EntryListWithBlinking_Object_SetupDict
    EntryListWithBlinking_Object_SetupDict = dict([("GUIparametersDict", EntryListWithBlinking_Object_GUIparametersDict),
                                                                          ("EntryListWithBlinking_Variables_ListOfDicts", EntryListWithBlinking_Variables_ListOfDicts),
                                                                          ("DebugByPrintingVariablesFlag", 0),
                                                                          ("LoseFocusIfMouseLeavesEntryFlag", 0)])
    if USE_EntryListWithBlinking_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            EntryListWithBlinking_Object = EntryListWithBlinking_ReubenPython2and3Class(EntryListWithBlinking_Object_SetupDict)
            EntryListWithBlinking_OPEN_FLAG = EntryListWithBlinking_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("EntryListWithBlinking_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_EntryListWithBlinking_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if EntryListWithBlinking_OPEN_FLAG != 1:
                print("Failed to open EntryListWithBlinking_ReubenPython2and3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:

        global MyPrint_Object_GUIparametersDict
        MyPrint_Object_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MyPrint_FLAG),
                                                                        ("root", Tab_MyPrint),
                                                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                        ("GUI_ROW", GUI_ROW_MyPrint),
                                                                        ("GUI_COLUMN", GUI_COLUMN_MyPrint),
                                                                        ("GUI_PADX", GUI_PADX_MyPrint),
                                                                        ("GUI_PADY", GUI_PADY_MyPrint),
                                                                        ("GUI_ROWSPAN", GUI_ROWSPAN_MyPrint),
                                                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MyPrint)])

        global MyPrint_Object_SetupDict
        MyPrint_Object_SetupDict = dict([("NumberOfPrintLines", 10),
                                                                ("WidthOfPrintingLabel", 200),
                                                                ("PrintToConsoleFlag", 1),
                                                                ("LogFileNameFullPath", os.getcwd() + "//TestLog.txt"),
                                                                ("GUIparametersDict", MyPrint_Object_GUIparametersDict)])

        if USE_MyPrint_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
            try:
                MyPrint_Object = MyPrint_ReubenPython2and3Class(MyPrint_Object_SetupDict)
                MyPrint_OPEN_FLAG = MyPrint_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

            except:
                exceptions = sys.exc_info()[0]
                print("MyPrint_Object __init__: Exceptions: %s" % exceptions)
                traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPrint_OPEN_FLAG != 1:
                print("Failed to open MyPrint_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess0_NameList
    MyPlotterPureTkinterStandAloneProcess0_NameList = ["Torque", "TorqueDotT"]

    global MyPlotterPureTkinterStandAloneProcess0_MarkerSizeList
    MyPlotterPureTkinterStandAloneProcess0_MarkerSizeList = [0]*2

    global MyPlotterPureTkinterStandAloneProcess0_LineWidthList
    MyPlotterPureTkinterStandAloneProcess0_LineWidthList = [2]*2

    global MyPlotterPureTkinterStandAloneProcess0_IncludeInXaxisAutoscaleCalculationList
    MyPlotterPureTkinterStandAloneProcess0_IncludeInXaxisAutoscaleCalculationList = [1, 1]

    global MyPlotterPureTkinterStandAloneProcess0_IncludeInYaxisAutoscaleCalculationList
    MyPlotterPureTkinterStandAloneProcess0_IncludeInYaxisAutoscaleCalculationList = [1, 1]

    global MyPlotterPureTkinterStandAloneProcess0_ColorList
    MyPlotterPureTkinterStandAloneProcess0_ColorList = ["Green", "Red"]

    global MyPlotterPureTkinterStandAloneProcess0_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess0_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                    ("NumberOfPrintLines", 10),
                                                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                    ("GraphCanvasWidth", 800),
                                                                    ("GraphCanvasHeight", 550),
                                                                    ("GraphCanvasWindowStartingX", 0),
                                                                    ("GraphCanvasWindowStartingY", 0),
                                                                    ("GraphCanvasWindowTitle", "FUTEK Torque"),
                                                                    ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 20)])

    global MyPlotterPureTkinterStandAloneProcess0_SetupDict
    MyPlotterPureTkinterStandAloneProcess0_SetupDict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess0_GUIparametersDict),
                                                            ("ParentPID", os.getpid()),
                                                            ("WatchdogTimerExpirationDurationSeconds_StandAlonePlottingProcess", 5.0),
                                                            ("CurvesToPlotNamesAndColorsDictOfLists",
                                                                dict([("NameList", MyPlotterPureTkinterStandAloneProcess0_NameList),
                                                                      ("MarkerSizeList", MyPlotterPureTkinterStandAloneProcess0_MarkerSizeList),
                                                                      ("LineWidthList", MyPlotterPureTkinterStandAloneProcess0_LineWidthList),
                                                                      ("IncludeInXaxisAutoscaleCalculationList", MyPlotterPureTkinterStandAloneProcess0_IncludeInXaxisAutoscaleCalculationList),
                                                                      ("IncludeInYaxisAutoscaleCalculationList", MyPlotterPureTkinterStandAloneProcess0_IncludeInYaxisAutoscaleCalculationList),
                                                                      ("ColorList", MyPlotterPureTkinterStandAloneProcess0_ColorList)])),
                                                            ("SmallTextSize", 7),
                                                            ("LargeTextSize", 12),
                                                            ("NumberOfDataPointToPlot", 50),
                                                            ("XaxisNumberOfTickMarks", 10),
                                                            ("YaxisNumberOfTickMarks", 10),
                                                            ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("XaxisAutoscaleFlag", 1),
                                                            ("YaxisAutoscaleFlag", 1),
                                                            ("X_min", 0.0),
                                                            ("X_max", 20.0),
                                                            ("Y_min", -10.00),
                                                            ("Y_max", 10.00),
                                                            ("XaxisDrawnAtBottomOfGraph", 0),
                                                            ("XaxisLabelString", "Time (sec)"),
                                                            ("YaxisLabelString", "Y-units (units)"),
                                                            ("ShowLegendFlag", 1),
                                                            ("SavePlot_DirectoryPath", os.path.join(os.getcwd(), "SavedImagesFolder"))])

    if USE_MyPlotterPureTkinterStandAloneProcess0_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPlotterPureTkinterStandAloneProcess0_Object = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess0_SetupDict)
            MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess0_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess0_Object, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPlotterPureTkinterStandAloneProcess0_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterClass_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess1_NameList
    MyPlotterPureTkinterStandAloneProcess1_NameList = ["Deg", "DegPerSec"]

    global MyPlotterPureTkinterStandAloneProcess1_MarkerSizeList
    MyPlotterPureTkinterStandAloneProcess1_MarkerSizeList = [0]*2

    global MyPlotterPureTkinterStandAloneProcess1_LineWidthList
    MyPlotterPureTkinterStandAloneProcess1_LineWidthList = [2]*2

    global MyPlotterPureTkinterStandAloneProcess1_IncludeInXaxisAutoscaleCalculationList
    MyPlotterPureTkinterStandAloneProcess1_IncludeInXaxisAutoscaleCalculationList = [1, 1]

    global MyPlotterPureTkinterStandAloneProcess1_IncludeInYaxisAutoscaleCalculationList
    MyPlotterPureTkinterStandAloneProcess1_IncludeInYaxisAutoscaleCalculationList = [1, 1]

    global MyPlotterPureTkinterStandAloneProcess1_ColorList
    MyPlotterPureTkinterStandAloneProcess1_ColorList = ["Green", "Red"]

    global MyPlotterPureTkinterStandAloneProcess1_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess1_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                    ("NumberOfPrintLines", 10),
                                                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                    ("GraphCanvasWidth", 800),
                                                                    ("GraphCanvasHeight", 550),
                                                                    ("GraphCanvasWindowStartingX", 0),
                                                                    ("GraphCanvasWindowStartingY", 600),
                                                                    ("GraphCanvasWindowTitle", "FUTEK Angle"),
                                                                    ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 20)])

    global MyPlotterPureTkinterStandAloneProcess1_SetupDict
    MyPlotterPureTkinterStandAloneProcess1_SetupDict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess1_GUIparametersDict),
                                                            ("ParentPID", os.getpid()),
                                                            ("WatchdogTimerExpirationDurationSeconds_StandAlonePlottingProcess", 5.0),
                                                            ("CurvesToPlotNamesAndColorsDictOfLists",
                                                                dict([("NameList", MyPlotterPureTkinterStandAloneProcess1_NameList),
                                                                      ("MarkerSizeList", MyPlotterPureTkinterStandAloneProcess1_MarkerSizeList),
                                                                      ("LineWidthList", MyPlotterPureTkinterStandAloneProcess1_LineWidthList),
                                                                      ("IncludeInXaxisAutoscaleCalculationList", MyPlotterPureTkinterStandAloneProcess1_IncludeInXaxisAutoscaleCalculationList),
                                                                      ("IncludeInYaxisAutoscaleCalculationList", MyPlotterPureTkinterStandAloneProcess1_IncludeInYaxisAutoscaleCalculationList),
                                                                      ("ColorList", MyPlotterPureTkinterStandAloneProcess1_ColorList)])),
                                                            ("SmallTextSize", 7),
                                                            ("LargeTextSize", 12),
                                                            ("NumberOfDataPointToPlot", 50),
                                                            ("XaxisNumberOfTickMarks", 10),
                                                            ("YaxisNumberOfTickMarks", 10),
                                                            ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("XaxisAutoscaleFlag", 1),
                                                            ("YaxisAutoscaleFlag", 1),
                                                            ("X_min", 0.0),
                                                            ("X_max", 20.0),
                                                            ("Y_min", -10.00),
                                                            ("Y_max", 10.00),
                                                            ("XaxisDrawnAtBottomOfGraph", 0),
                                                            ("XaxisLabelString", "Time (sec)"),
                                                            ("YaxisLabelString", "Y-units (units)"),
                                                            ("ShowLegendFlag", 1),
                                                            ("SavePlot_DirectoryPath", os.path.join(os.getcwd(), "SavedImagesFolder"))])

    if USE_MyPlotterPureTkinterStandAloneProcess1_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPlotterPureTkinterStandAloneProcess1_Object = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess1_SetupDict)
            MyPlotterPureTkinterStandAloneProcess1_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess1_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess1_Object, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPlotterPureTkinterStandAloneProcess1_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPlotterPureTkinterStandAloneProcess1_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterClass_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if EXIT_PROGRAM_FLAG == 0:
        print("Starting main loop 'test_program_for_FutekForceTorqueReaderUSB520_ReubenPython3Class.")
        StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    while(EXIT_PROGRAM_FLAG == 0):

        ##########################################################################################################
        ##########################################################################################################

        ###################################################
        ###################################################
        ###################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        ###################################################
        ###################################################
        ###################################################

        ####################################################
        ###################################################
        ####################################################

        ################################################### GET's
        ###################################################
        if EntryListWithBlinking_OPEN_FLAG == 1:

            EntryListWithBlinking_MostRecentDict = EntryListWithBlinking_Object.GetMostRecentDataDict()

            if "DataUpdateNumber" in EntryListWithBlinking_MostRecentDict and EntryListWithBlinking_MostRecentDict["DataUpdateNumber"] != EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last:
                EntryListWithBlinking_MostRecentDict_DataUpdateNumber = EntryListWithBlinking_MostRecentDict["DataUpdateNumber"]
                #print("DataUpdateNumber = " + str(EntryListWithBlinking_MostRecentDict_DataUpdateNumber) + ", EntryListWithBlinking_MostRecentDict: " + str(EntryListWithBlinking_MostRecentDict))

                ###################################################
                if EntryListWithBlinking_MostRecentDict_DataUpdateNumber > 1:
                    FutekForceTorqueReaderUSB520_FTmeasurement_ExponentialSmoothingFilterLambda = float(EntryListWithBlinking_MostRecentDict["FutekForceTorqueReaderUSB520_FTmeasurement_ExponentialSmoothingFilterLambda"])
                    FutekForceTorqueReaderUSB520_FTmeasurementDerivative_ExponentialSmoothingFilterLambda = float(EntryListWithBlinking_MostRecentDict["FutekForceTorqueReaderUSB520_FTmeasurementDerivative_ExponentialSmoothingFilterLambda"])

                    if FutekForceTorqueReaderUSB520_OPEN_FLAG == 1:

                        FutekForceTorqueReaderUSB520_Object.UpdateVariableFilterSettingsFromExternalProgram("FTmeasurement",
                                                                                                            UseMedianFilterFlag=1,
                                                                                                            UseExponentialSmoothingFilterFlag=1,
                                                                                                            ExponentialSmoothingFilterLambda=FutekForceTorqueReaderUSB520_FTmeasurement_ExponentialSmoothingFilterLambda)

                        FutekForceTorqueReaderUSB520_Object.UpdateVariableFilterSettingsFromExternalProgram("FTmeasurementDerivative",
                                                                                                            UseMedianFilterFlag=1,
                                                                                                            UseExponentialSmoothingFilterFlag=1,
                                                                                                            ExponentialSmoothingFilterLambda=FutekForceTorqueReaderUSB520_FTmeasurementDerivative_ExponentialSmoothingFilterLambda)
                ###################################################

        ###################################################
        ###################################################

        ###################################################
        ###################################################
        EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last = EntryListWithBlinking_MostRecentDict_DataUpdateNumber
        ###################################################
        ###################################################

        ####################################################
        ###################################################
        ####################################################

        ################################################### GET's
        ###################################################
        ###################################################
        if FutekForceTorqueReaderUSB520_OPEN_FLAG == 1:

            FutekForceTorqueReaderUSB520_MostRecentDict = FutekForceTorqueReaderUSB520_Object.GetMostRecentDataDict()
            #print("FutekForceTorqueReaderUSB520_MostRecentDict: " + str(FutekForceTorqueReaderUSB520_MostRecentDict))

            if "Time" in FutekForceTorqueReaderUSB520_MostRecentDict:
                FutekForceTorqueReaderUSB520_MostRecentDict_Time = FutekForceTorqueReaderUSB520_MostRecentDict["Time"]
                FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurement_Raw = FutekForceTorqueReaderUSB520_MostRecentDict["FTmeasurement_Raw"]
                FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurement_Filtered = FutekForceTorqueReaderUSB520_MostRecentDict["FTmeasurement_Filtered"]
                FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurementDerivative_Raw = FutekForceTorqueReaderUSB520_MostRecentDict["FTmeasurementDerivative_Raw"]
                FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurementDerivative_Filtered = FutekForceTorqueReaderUSB520_MostRecentDict["FTmeasurementDerivative_Filtered"]

                FutekForceTorqueReaderUSB520_MostRecentDict_AngleValue_AllUnitsDict = FutekForceTorqueReaderUSB520_MostRecentDict["AngleValue_AllUnitsDict"]
                FutekForceTorqueReaderUSB520_MostRecentDict_AngleValue_Deg = FutekForceTorqueReaderUSB520_MostRecentDict_AngleValue_AllUnitsDict["Deg"]

                FutekForceTorqueReaderUSB520_MostRecentDict_AngularSpeedValue_AllUnitsDict = FutekForceTorqueReaderUSB520_MostRecentDict["AngularSpeedValue_AllUnitsDict"]
                FutekForceTorqueReaderUSB520_MostRecentDict_AngularSpeedValue_DegPerSec = FutekForceTorqueReaderUSB520_MostRecentDict_AngularSpeedValue_AllUnitsDict["DegPerSec"]
        ###################################################
        ###################################################
        ###################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ################################################### SET's
        ###################################################
        ###################################################
        if FutekForceTorqueReaderUSB520_OPEN_FLAG == 1:

            ###################################################
            ###################################################
            if FutekForceTorqueReaderUSB520_ResetTare_EventNeedsToBeFiredFlag == 1:
                FutekForceTorqueReaderUSB520_Object.ResetTare()

                FutekForceTorqueReaderUSB520_ResetTare_EventNeedsToBeFiredFlag = 0
            ###################################################
            ###################################################

        ###################################################
        ###################################################
        ###################################################

        #################################################### SET's
        ####################################################
        ####################################################
        if FutekForceTorqueReaderUSB520_OPEN_FLAG == 1 and CSVdataLogger_OPEN_FLAG == 1:

            ####################################################
            ####################################################
            ListToWrite = []

            ListToWrite.append(CurrentTime_MainLoopThread)

            ListToWrite.append(FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurement_Raw)
            ListToWrite.append(FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurement_Filtered)

            ListToWrite.append(FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurementDerivative_Raw)
            ListToWrite.append(FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurementDerivative_Filtered)

            ListToWrite.append(FutekForceTorqueReaderUSB520_MostRecentDict_AngleValue_Deg)
            ListToWrite.append(FutekForceTorqueReaderUSB520_MostRecentDict_AngularSpeedValue_DegPerSec)
            
            #print("ListToWrite: " + str(ListToWrite))
            ####################################################
            ####################################################

            CSVdataLogger_Object.AddDataToCSVfile_ExternalFunctionCall(ListToWrite)
        ####################################################
        ####################################################
        ####################################################

        #################################################### SET's
        ####################################################
        ####################################################
        if MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG == 1:
            try:
                ####################################################
                ####################################################
                MyPlotterPureTkinterStandAloneProcess0_MostRecentDict = MyPlotterPureTkinterStandAloneProcess0_Object.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess0_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess0_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess0_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess0_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                        if CurrentTime_MainLoopThread - LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess0 >= 0.030:

                            ####################################################
                            ListOfValuesToPlot = []
                            #ListOfValuesToPlot.append(FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurement_Raw)
                            ListOfValuesToPlot.append(FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurement_Filtered)
                            #ListOfValuesToPlot.append(FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurementDerivative_Raw)
                            ListOfValuesToPlot.append(FutekForceTorqueReaderUSB520_MostRecentDict_FTmeasurementDerivative_Filtered)
                            ####################################################

                            ####################################################
                            MyPlotterPureTkinterStandAloneProcess0_Object.ExternalAddPointOrListOfPointsToPlot(MyPlotterPureTkinterStandAloneProcess0_NameList[0:len(ListOfValuesToPlot)],
                                                                                                                                    [CurrentTime_MainLoopThread]*len(ListOfValuesToPlot),
                                                                                                                                    ListOfValuesToPlot)
                            ####################################################

                            ####################################################
                            LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess0 = CurrentTime_MainLoopThread
                            ####################################################

                ####################################################
                ####################################################

            except:
                exceptions = sys.exc_info()[0]
                print("test_program_for_FutekForceTorqueReaderUSB520_ReubenPython3Class, if MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG == 1: SET's, Exceptions: %s" % exceptions)
                traceback.print_exc()
        ####################################################
        ####################################################
        ####################################################

        #################################################### SET's
        ####################################################
        ####################################################
        if MyPlotterPureTkinterStandAloneProcess1_OPEN_FLAG == 1:
            try:
                ####################################################
                ####################################################
                MyPlotterPureTkinterStandAloneProcess1_MostRecentDict = MyPlotterPureTkinterStandAloneProcess1_Object.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess1_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess1_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess1_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess1_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                        if CurrentTime_MainLoopThread - LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess1 >= 0.030:

                            ####################################################
                            ListOfValuesToPlot = []
                            ListOfValuesToPlot.append(FutekForceTorqueReaderUSB520_MostRecentDict_AngleValue_Deg)
                            ListOfValuesToPlot.append(FutekForceTorqueReaderUSB520_MostRecentDict_AngularSpeedValue_DegPerSec)
                            ####################################################

                            ####################################################
                            MyPlotterPureTkinterStandAloneProcess1_Object.ExternalAddPointOrListOfPointsToPlot(MyPlotterPureTkinterStandAloneProcess1_NameList[0:len(ListOfValuesToPlot)],
                                                                                                                                    [CurrentTime_MainLoopThread]*len(ListOfValuesToPlot),
                                                                                                                                    ListOfValuesToPlot)
                            ####################################################

                            ####################################################
                            LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess1 = CurrentTime_MainLoopThread
                            ####################################################

                ####################################################
                ####################################################

            except:
                exceptions = sys.exc_info()[0]
                print("test_program_for_FutekForceTorqueReaderUSB520_ReubenPython3Class, if MyPlotterPureTkinterStandAloneProcess1_OPEN_FLAG == 1: SET's, Exceptions: %s" % exceptions)
                traceback.print_exc()
        ####################################################
        ####################################################
        ####################################################

        ##########################################################################################################
        ##########################################################################################################

        time.sleep(0.002)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## THIS IS THE EXIT ROUTINE!
    ##########################################################################################################
    ##########################################################################################################
    print("Exiting main program 'test_program_for_FutekForceTorqueReaderUSB520_ReubenPython3Class.")

    #################################################
    if FutekForceTorqueReaderUSB520_OPEN_FLAG == 1:
        FutekForceTorqueReaderUSB520_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if EntryListWithBlinking_OPEN_FLAG == 1:
        EntryListWithBlinking_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPlotterPureTkinterStandAloneProcess0_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess0_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPlotterPureTkinterStandAloneProcess1_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess1_Object.ExitProgram_Callback()
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################