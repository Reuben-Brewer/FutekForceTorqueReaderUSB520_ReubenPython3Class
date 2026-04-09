# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision H, 04/09/2026

Verified working on: Python 3.11/12/13 for Windows 10/11 64-bit, Ubuntu 24.04-LTS,and Raspberry Pi Bookworm.
'''

__author__ = 'reuben.brewer'

#########################################################
import os
import sys
import time
import traceback

#Needed for GetHostIPaddressViaSocketModuleCall_FAILS and GetHostIPaddressViaDummySocket_LinuxAndWindows
import socket

#Needed for GetHostIPaddressViaNetifaces_LinuxAndLimitedWindows and GetHostIPaddressViaScapy_WindowsOnly
import netifaces #'pip install netifaces' works right-away on Raspberry Pi, but there's a prereq in Windows to install "VCForPython27.msi" from http://aka.ms/vcpython27" BEFORE netifaces

#ON 08/30/21, DISCOVERED THAT "from scapy.all import *" CRASHES PYTHON, NOT SURE WHY. version downgrading to 2.4.0 and upgrading to 2.4.5 didn't help. Had to reinstall 2.4.3
#Needed for GetHostIPaddressViaScapy_WindowsOnly
if sys.platform == "win32": #If this is included on Raspberry Pi, then whatever imports this file will fail to launch on startup (not sure why). Since this is a windows-only function, just don't import it on Raspberry Pi.
    from scapy.all import * #"pip install scapy==2.4.3" works on both Windows 8.1 and Raspian Jessie
    from scapy.arch.windows import get_windows_if_list
    #Note: In Scapy v2 use from scapy.all import * instead of from scapy import *.
#########################################################

##########################################################################################################
##########################################################################################################
def GetHostIPaddressViaSocketModuleCall_FAILS():
    host_name = socket.gethostname()
    host_ip_address = socket.gethostbyname(host_name) #GIVES YOU THE INCORRECT IP ADDRESS (NOT THE ONE PHYSICALLY TRANSMITTING THE DATA)
    print("host_name: " + host_name + ", host_ip_address: " + host_ip_address)

    return [host_name, host_ip_address]
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GetHostIPaddressViaDummySocket_LinuxAndWindows():

    host_ip_address = ""

    try:
        dummy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dummy_socket.connect(("8.8.8.8", 80))
        host_ip_address = dummy_socket.getsockname()[0]
        #print("GetHostIPaddressViaDummySocket_LinuxAndWindows, host_ip_address: " + host_ip_address)
        dummy_socket.close()

    except:
        exceptions = sys.exc_info()[0]
        print("GetHostIPaddressViaDummySocket_LinuxAndWindows, exceptions: %s" % exceptions)
        traceback.print_exc()

    return host_ip_address
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GetHostIPaddressViaNetifaces_LinuxAndLimitedWindows():

    NetworkInterfacesDictToReturn = dict([("ethernet", []),
                                           ("wireless", [])])

    host_IP_address_eth0 = ""
    host_IP_address_wlan0 = ""

    try:

        ##########################################################################################################
        if sys.platform == "linux" or sys.platform == "linux2":

            try:
                netifaces.ifaddresses('eth0') #ethernet hardwired connection
                host_IP_address_eth0 = str(netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'])
                #print("host_IP_address_eth0: " + str(host_IP_address_eth0))

            except:
                pass

            try:
                netifaces.ifaddresses('wlan0') #wireless connection
                host_IP_address_wlan0 = str(netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr'])
                #print("host_IP_address_wlan0: " + str(host_IP_address_wlan0))

            except:
                pass

            NetworkInterfacesDictToReturn["ethernet"].append(dict([("ConnectionType", "ethernet"),
                                                                   ("IPv4", host_IP_address_eth0),
                                                                   ("DeviceDescription", "")]))

            NetworkInterfacesDictToReturn["wireless"].append(dict([("ConnectionType", "wireless"),
                                                                   ("IPv4", host_IP_address_wlan0),
                                                                   ("DeviceDescription", "")]))
        ##########################################################################################################

        ##########################################################################################################
        elif sys.platform == "win32":

            NetworkInterfacesFromNetifacesList = netifaces.interfaces()

            for NetworkInterface in NetworkInterfacesFromNetifacesList:

                try:
                    #print("NetworkInterface: " + str(NetworkInterface))
                    NetworkInterfaceIPv4 = str(netifaces.ifaddresses(NetworkInterface)[netifaces.AF_INET][0]["addr"])
                    #print("GetHostIPaddressViaNetifaces_LinuxAndLimitedWindows: " + str(NetworkInterfaceIPv4) + "  " + str(NetworkInterface))

                    #########################################################
                    if "unknown" not in NetworkInterfacesDictToReturn:
                        NetworkInterfacesDictToReturn["unknown"] = []
                    #########################################################

                    NetworkInterfacesDictToReturn["wireless"].append(dict([("ConnectionType", "unknown"),
                                                                           ("IPv4", NetworkInterfaceIPv4),
                                                                           ("DeviceDescription", "")]))

                    '''
                    if NetworkInterfaceIPv4.find("10.") != -1:
                        NetworkInterfacesDictToReturn["wireless"]["IPv4"] = NetworkInterfaceIPv4

                    elif NetworkInterfaceIPv4.find("169.") != -1:
                        NetworkInterfacesDictToReturn["ethernet"]["IPv4"] = NetworkInterfaceIPv4
                    '''

                except:
                    pass
        ##########################################################################################################

    except:
        exceptions = sys.exc_info()[0]
        print("GetHostIPaddressViaNetifaces_LinuxAndLimitedWindows, exceptions: %s" % exceptions)
        traceback.print_exc()

    return NetworkInterfacesDictToReturn
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GetHostIPaddressViaScapy_WindowsOnly():

    NetworkInterfacesDictToReturn = dict([("ethernet", []),
                                           ("wireless", [])])

    try:
        ##########################################################################################################
        if sys.platform == "win32":

            NetworkInterfacesListOfDicts = get_windows_if_list() #Function from 'from scapy.all import *'. New call is scapy.interfaces.
            host_ethernet_info =["-1", "-1"]
            host_wifi_info = ["-1", "-1"]

            for NetworkInterfaceDict in NetworkInterfacesListOfDicts:
                #print("NetworkInterfaceDict: " + str(NetworkInterfaceDict))
                NetworkInterfaceName = NetworkInterfaceDict["name"]

                if "ips" in NetworkInterfaceDict:
                    NetworkInterfaceIPv4 = NetworkInterfaceDict["ips"]#[-1]
                else:
                    NetworkInterfaceIPv4 = []

                NetworkInterfaceDescription = NetworkInterfaceDict["description"]
                NetworkInterfaceMACaddress = NetworkInterfaceDict["mac"]

                if NetworkInterfaceName.lower().find("wi") !=-1:
                    NetworkInterfacesDictToReturn["wireless"].append(dict([("ConnectionType", "wireless"),
                                                                      ("IPv4", NetworkInterfaceIPv4),
                                                                      ("DeviceDescription", NetworkInterfaceDescription),
                                                                      ("MACaddress", NetworkInterfaceMACaddress)]))

                elif NetworkInterfaceName.lower().find("eth") != -1:

                    if NetworkInterfaceDescription.lower().find("eth") != -1: #This gets rid of the Checkpoint VPN ethernet connection
                        NetworkInterfacesDictToReturn["ethernet"].append(dict([("ConnectionType", "ethernet"),
                                                                               ("IPv4", NetworkInterfaceIPv4),
                                                                               ("DeviceDescription", NetworkInterfaceDescription),
                                                                               ("MACaddress", NetworkInterfaceMACaddress)]))

        ##########################################################################################################

    except:
        exceptions = sys.exc_info()[0]
        print("GetHostIPaddressViaScapy_WindowsOnly, exceptions: %s" % exceptions)
        traceback.print_exc()

    return NetworkInterfacesDictToReturn
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    #'''
    ##########################################################################################################
    host_ip_address = GetHostIPaddressViaDummySocket_LinuxAndWindows()
    print("GetHostIPaddressViaDummySocket_LinuxAndWindows: " + host_ip_address)
    ##########################################################################################################
    #'''

    #'''
    ##########################################################################################################
    NetworkInterfaces = GetHostIPaddressViaNetifaces_LinuxAndLimitedWindows()

    #########################################################
    for interface in NetworkInterfaces["ethernet"]:
        print("ethernet interface" + str(interface))
    #########################################################

    #########################################################
    for interface in NetworkInterfaces["wireless"]:
        print("wireless interface" + str(interface))
    #########################################################

    ##########################################################################################################
    #'''

    '''
    ##########################################################################################################
    if sys.platform == "win32":
        NetworkInterfaces = GetHostIPaddressViaScapy_WindowsOnly()

        #########################################################
        for interface in NetworkInterfaces["ethernet"]:
            print("ethernet interface" + str(interface))
        #########################################################

        #########################################################
        for interface in NetworkInterfaces["wireless"]:
            print("wireless interface" + str(interface))
        #########################################################

    ##########################################################################################################
    '''

##########################################################################################################
##########################################################################################################