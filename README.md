###########################

FutekForceTorqueReaderUSB520_ReubenPython3Class

Control class (including ability to hook to Tkinter GUI) to control/read load-cell data from the Futek USB520 Force/Torque Reader.

https://www.futek.com/store/instruments/usb/mv-v-amplified-and-encoder-input-usb-solution-USB520/FSH03944

DotNET API Documentation: https://media.futek.com/docs/dotnet/api/FUTEK_USB_DLL~FUTEK_USB_DLL.USB_DLL_methods.html

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision I, 02/11/2026

Verified working on:

Python 3.11/12/13

Windows 10/11 64-bit in DLL or USB-Serial mode (limited to 10Hz).

Raspberry Pi Bookworm in USB-Serial mode (limited to 10Hz).

IMPORTANT NOTE 0:

Although ASCII-output is available, it's limited to 10Hz. As such, you'll get MUCH faster sampling using the Windows-DLL method of communicating with the reader.
Unfortunately, you're stuck at 10Hz on Ubuntu and Raspberry Pi as they can't load the DLL.

IMPORTANT NOTE 1:

In the folder "\InstallFiles_and_SupportDocuments\futek-usb-dll", there are DLL files for both 32 and 64-bit Python. 99% of users will want the 64-bit version,
but you can always use the 32-bit version if you need to pair with 32-bit Python.

IMPORTANT NOTE 2:

Once your DLL file is downloaded and extracted, right-click the DLL file and click "Unblock" from the bottom of the tab (Windows' default is to block it for security reasons).
Alternatively, you can enter into the DLL-containing-folder from ADMIN PowerShell and enter the command:

Get-ChildItem -Path . -Filter *.dll | Unblock-File

IMPORTANT NOTE 3:

As long as the DLL is in some subfolder within the parent code's same directory, the FutekForceTorqueReaderUSB520_ReubenPython3Class will find and load it.

IMPORTANT NOTE 4:

To debug the serial stream in Ubuntu/RaspberryPi, issue:

sudo stty -F /dev/ttyUSB0 115200 raw -echo

sudo cat /dev/ttyUSBO0

###########################

########################### Python module installation instructions, all OS's

############

BareBones___FutekForceTorqueReaderUSB520_ReubenPython3Class.py, ListOfModuleDependencies_All:['pythonnet', 'FUTEK_USB_DLL', 'keyboard']

pip install pythonnet (this is where clr is imported from).

NOTE: For loading the DLL via the clr module, it's critical to use the clr *from the pythonnet module ("pip install pythonnet"), not from a stand-alone clr module.

############

############

FutekForceTorqueReaderUSB520_ReubenPython3Class, ListOfModuleDependencies: ['clr', 'ftd2xx', 'FUTEK_USB_DLL', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'ReubenGithubCodeModulePaths', 'serial', 'serial.tools', 'ZeroAndSnapshotData_ReubenPython2and3Class']

FutekForceTorqueReaderUSB520_ReubenPython3Class, ListOfModuleDependencies_TestProgram: ['CSVdataLogger_ReubenPython3Class', 'EntryListWithBlinking_ReubenPython2and3Class', 'keyboard', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'ReubenGithubCodeModulePaths']

FutekForceTorqueReaderUSB520_ReubenPython3Class, ListOfModuleDependencies_NestedLayers: ['EntryListWithBlinking_ReubenPython2and3Class', 'GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class', 'LowPassFilter_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil', 'pyautogui', 'ReubenGithubCodeModulePaths']

FutekForceTorqueReaderUSB520_ReubenPython3Class, ListOfModuleDependencies_All:['clr', 'CSVdataLogger_ReubenPython3Class', 'EntryListWithBlinking_ReubenPython2and3Class', 'ftd2xx', 'FUTEK_USB_DLL', 'GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class', 'keyboard', 'LowPassFilter_ReubenPython2and3Class', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil', 'pyautogui', 'ReubenGithubCodeModulePaths', 'serial', 'serial.tools', 'ZeroAndSnapshotData_ReubenPython2and3Class']

############

###########################
