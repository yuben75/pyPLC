# State machine for the car
#
#

#------------------------------------------------------------

import pyPlcTcpSocket
import time # for time.sleep()
from helpers import prettyHexMessage
from exiConnector import * # for EXI data handling/converting

stateInitialized = 0
stateWaitForSupportedApplicationProtocolResponse = 1
stateWaitForSessionSetupResponse = 2
stateWaitForServiceDiscoveryResponse = 3
stateWaitForServicePaymentSelectionResponse = 4
stateWaitForAuthorizationResponse = 5
stateWaitForChargeParameterDiscoveryResponse = 6
stateWaitForCableCheckResponse = 7
stateWaitForPreChargeResponse = 8
stateWaitForPowerDeliveryResponse = 9

class fsmPev():
    def enterState(self, n):
        print("from " + str(self.state) + " entering " + str(n))
        self.state = n
        self.cyclesInState = 0
        
    def isTooLong(self):
        # The timeout handling function.
        return (self.cyclesInState > 20)
        
    def stateFunctionInitialized(self):
        if (self.Tcp.isConnected):
            # we just use the initial request message from the Ioniq. It contains one entry: DIN.
            self.Tcp.transmit(addV2GTPHeader(exiHexToByteArray(exiHexDemoSupportedApplicationProtocolRequestIoniq)))
            self.enterState(stateWaitForSupportedApplicationProtocolResponse)
        
    def stateFunctionWaitForSupportedApplicationProtocolResponse(self):
        if (len(self.rxData)>0):
            print("In state WaitForSupportedApplicationProtocolResponse, received " + prettyHexMessage(self.rxData))
            exidata = removeV2GTPHeader(self.rxData)
            self.rxData = []
            strConverterResult = exiDecode(exidata, "Dh") # Decode Handshake-response
            print(strConverterResult)
            if (strConverterResult.find("supportedAppProtocolRes")>0):
                # todo: check the request content, and fill response parameters
                msg = addV2GTPHeader(exiEncode("EDA")) # EDA for Encode, Din, SessionSetupReq
                print("responding " + prettyHexMessage(msg))
                self.Tcp.transmit(msg)
                self.enterState(stateWaitForSessionSetupResponse)
        if (self.isTooLong()):
            self.enterState(0)
            
    def stateFunctionWaitForSessionSetupResponse(self):
        if (len(self.rxData)>0):
            print("In state WaitForSessionSetupResponse, received " + prettyHexMessage(self.rxData))
            exidata = removeV2GTPHeader(self.rxData)
            self.rxData = []
            strConverterResult = exiDecode(exidata, "DD") # Decode DIN
            print(strConverterResult)
            if (strConverterResult.find("SessionSetupRes")>0):
                # todo: check the request content, and fill response parameters
                msg = addV2GTPHeader(exiEncode("EDB")) # EDB for Encode, Din, ServiceDiscoveryRequest
                print("responding " + prettyHexMessage(msg))
                self.Tcp.transmit(msg)
                self.enterState(stateWaitForServiceDiscoveryResponse)
        if (self.isTooLong()):
            self.enterState(0)

    def stateFunctionWaitForServiceDiscoveryResponse(self):
        if (len(self.rxData)>0):
            print("In state WaitForServiceDiscoveryResponse, received " + prettyHexMessage(self.rxData))
            exidata = removeV2GTPHeader(self.rxData)
            self.rxData = []
            strConverterResult = exiDecode(exidata, "DD") # Decode DIN
            print(strConverterResult)
            if (strConverterResult.find("ServiceDiscoveryRes")>0):
                # todo: check the request content, and fill response parameters
                msg = addV2GTPHeader(exiEncode("EDC")) # EDC for Encode, Din, ServicePaymentSelection
                print("responding " + prettyHexMessage(msg))
                self.Tcp.transmit(msg)
                self.enterState(stateWaitForServicePaymentSelectionResponse)
        if (self.isTooLong()):
            self.enterState(0)

    def stateFunctionWaitForServicePaymentSelectionResponse(self):
        if (len(self.rxData)>0):
            print("In state WaitForServicePaymentSelectionResponse, received " + prettyHexMessage(self.rxData))
            exidata = removeV2GTPHeader(self.rxData)
            self.rxData = []
            strConverterResult = exiDecode(exidata, "DD") # Decode DIN
            print(strConverterResult)
            if (strConverterResult.find("ServicePaymentSelectionRes")>0):
                # todo: check the request content, and fill response parameters
                msg = addV2GTPHeader(exiEncode("EDE")) # EDE for Encode, Din, ChargeParameterDiscovery. We ignore Authorization, not specified in DIN.
                print("responding " + prettyHexMessage(msg))
                self.Tcp.transmit(msg)
                self.enterState(stateWaitForChargeParameterDiscoveryResponse)
        if (self.isTooLong()):
            self.enterState(0)
        
    def stateFunctionWaitForChargeParameterDiscoveryResponse(self):
        if (len(self.rxData)>0):
            print("In state WaitForChargeParameterDiscoveryResponse, received " + prettyHexMessage(self.rxData))
            exidata = removeV2GTPHeader(self.rxData)
            self.rxData = []
            strConverterResult = exiDecode(exidata, "DD") # Decode DIN
            print(strConverterResult)
            if (strConverterResult.find("ChargeParameterDiscoveryRes")>0):
                # todo: check the request content, and fill response parameters
                msg = addV2GTPHeader(exiEncode("EDF")) # EDF for Encode, Din, CableCheck
                print("responding " + prettyHexMessage(msg))
                self.Tcp.transmit(msg)
                self.enterState(stateWaitForCableCheckResponse)
        if (self.isTooLong()):
            self.enterState(0)

    def stateFunctionWaitForCableCheckResponse(self):
        if (len(self.rxData)>0):
            print("In state WaitForCableCheckResponse, received " + prettyHexMessage(self.rxData))
            exidata = removeV2GTPHeader(self.rxData)
            self.rxData = []
            strConverterResult = exiDecode(exidata, "DD") # Decode DIN
            print(strConverterResult)
            if (strConverterResult.find("CableCheckRes")>0):
                # todo: check the request content, and fill response parameters
                msg = addV2GTPHeader(exiEncode("EDG")) # EDG for Encode, Din, PreCharge
                print("responding " + prettyHexMessage(msg))
                self.Tcp.transmit(msg)
                self.enterState(stateWaitForPreChargeResponse)
        if (self.isTooLong()):
            self.enterState(0)

    def stateFunctionWaitForPreChargeResponse(self):
        if (len(self.rxData)>0):
            print("In state WaitForPreChargeResponse, received " + prettyHexMessage(self.rxData))
            exidata = removeV2GTPHeader(self.rxData)
            self.rxData = []
            strConverterResult = exiDecode(exidata, "DD") # Decode DIN
            print(strConverterResult)
            if (strConverterResult.find("PreChargeRes")>0):
                # todo: check the request content, and fill response parameters
                print("PreCharge aknowledge received.")
                print("As Demo, we stay in PreCharge until the timeout elapses.")
        if (self.isTooLong()):
            self.enterState(0)
       
    stateFunctions = { 
            stateInitialized: stateFunctionInitialized,
            stateWaitForSupportedApplicationProtocolResponse: stateFunctionWaitForSupportedApplicationProtocolResponse,
            stateWaitForSessionSetupResponse: stateFunctionWaitForSessionSetupResponse,
            stateWaitForServiceDiscoveryResponse: stateFunctionWaitForServiceDiscoveryResponse,
            stateWaitForServicePaymentSelectionResponse: stateFunctionWaitForServicePaymentSelectionResponse,
            stateWaitForChargeParameterDiscoveryResponse: stateFunctionWaitForChargeParameterDiscoveryResponse,
            stateWaitForCableCheckResponse: stateFunctionWaitForCableCheckResponse,
            stateWaitForPreChargeResponse: stateFunctionWaitForPreChargeResponse,
        }

    def reInit(self):
        print("re-initializing fsmPev") 
        self.state = stateInitialized
        self.cyclesInState = 0
        self.rxData = []
        if (not self.Tcp.isConnected):
            self.Tcp.connect('fe80::e0ad:99ac:52eb:85d3', 15118)
            if (not self.Tcp.isConnected):
                print("connection failed")
            else:
                print("connected")
        
    def __init__(self):
        print("initializing fsmPev") 
        self.Tcp = pyPlcTcpSocket.pyPlcTcpClientSocket()
        self.reInit()
                
    def mainfunction(self):
        #self.Tcp.mainfunction() # call the lower-level worker
        if (self.Tcp.isRxDataAvailable()):
                self.rxData = self.Tcp.getRxData()
                #print("received " + prettyHexMessage(self.rxData))
        # run the state machine:
        self.cyclesInState += 1 # for timeout handling, count how long we are in a state
        self.stateFunctions[self.state](self)
                
                
if __name__ == "__main__":
    print("Testing the pev state machine")
    pev = fsmPev()
    print("Press Ctrl-Break for aborting")
    while (True):
        time.sleep(0.1)
        pev.mainfunction()
        
