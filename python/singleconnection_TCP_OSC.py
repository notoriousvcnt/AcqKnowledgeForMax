#!/usr/bin/env python
# encoding: utf-8

"""
singleconnection_TCP_OSC.py

This program receives data streaming from AcqKnowledge to Python client code
using the single TCP connection mode and then sends the data via OSC protocol.

Default TCP Connection Host: 127.0.0.1
Default TCP Connection Port: 15020

Default OSC Connection Host: 127.0.0.1
Default OSC Connection Port: 5005

This program is an edited version from the original examples provided by BIOPAC.
Copyright (c) 2009-2010 BIOPAC Systems, Inc. All rights reserved.
"""

# import standard Python modules

import sys
import time

# import our biopacndt support module

import biopacndt

#import osc and parse modules
import argparse
from pythonosc import udp_client

def main():     
    """Execute the singleconnection mode for acquiring data from AcqKnowledge. It receives the data sent via TCP 
    and then sends the data via OSC protocol.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-host","--hostname",help="AcqKnowledge Server Hostname",default="127.0.0.1")
    parser.add_argument("-p","--port",help="AcqKnowledge Server Port",default=15020)
    args = parser.parse_args()

    try:
        #Trying to connect to specified server. QuickConnect option is not used due security reasons.
        print("Intentando conectar al servidor AcqKnowledge en la dirección %s y puerto %s..." % (args.hostname,args.port))        
        acqServer = biopacndt.AcqNdtServer(args.hostname, args.port)
    except ConnectionRefusedError:
        print("No se puede conectar al servidor especificado.")
        sys.exit()

    try: 
            # Check if there is a data acquisition that is already running.
            # In order to acquire data into a new template, we need to halt
            # any previously running acquisition first.
            
            if acqServer.getAcquisitionInProgress():
                    acqServer.toggleAcquisition()
                    print("Current data acquistion stopped")
            
            
            # instruct AcqKnowledge to send us data for all of the channels being
            # acquired and retain the array of enabled channel objects.

            enabledChannels = acqServer.DeliverAllEnabledChannels()

            # change data connection method to single.  The single data connection
            # mode means that AcqKnowledge will make a single TCP network connection
            # to our client code to deliver the data, all channels being
            # delivered over that same connection.
            #
            # When in 'single' mode, we only need one AcqNdtDataServer object
            # which will process all channels.
            
            if acqServer.getDataConnectionMethod() != "single":
                    acqServer.changeDataConnectionMethod("single")
                    print("Data Connection Method Changed to: single")
            
            # ask AcqKnowledge which TCP port number will be used when it tries
            # to establish its data connection
            
            singleConnectPort = acqServer.getSingleConnectionModePort()
            
            # construct our AcqNdtDataServer object which receives data from
            # AcqKnowledge.  Since we're using 'single' connection mode, we only
            # need one AcqNdtDataServer object which will handle all of our channels.
            #
            # The constructor takes the TCP port for the data connection and a list
            # of AcqNdtChannel objects correpsonding to the channels whose data is
            # being sent from AcqKnowledge.
            #
            # We got our TCP port above in the singleConnectionPort variable.
            #
            # The DeliverAllEnabledChannels() function returns a list of AcqNdtChannel
            # objects that ar enabled for acquisition, so we will pass in that
            # list from above.

            dataServer = biopacndt.AcqNdtDataServer(singleConnectPort, enabledChannels,OSCport=5005)
            print('Sending data to OSC port %i' % (dataServer.GetOSCPort()))

            # add our callback functions to the AcqNdtDataServer to process
            # channel data as it is being received.
    

            dataServer.RegisterCallback("SendOSCData",SendOSCData)
            
            
            # start the data server.  The data server will start listening for
            # AcqKnowledge to make its data connection and, once data starts
            # coming in, invoking our callbacks to process it.
            #
            # The AcqNdtDataServer must be started prior to initiating our
            # data acquisition.
            
            dataServer.Start()
            
            # tell AcqKnowledge to begin acquiring data.
            
            if acqServer.toggleAcquisition() != 0 and acqServer.getAcquisitionInProgress() == 0:
                print("no se puede iniciar la adquisición de datos. Se cerrará el programa")
                sys.exit()

            # wait for AcqKnowledge to finish acquiring all of the data in the graph.
            
            acqServer.WaitForAcquisitionEnd()
            
            # give ourselves an additional 10 seconds to process any data that
            # may have been sent at the end of the acquisition or is waiting
            # in our data server queue.
            time.sleep(10)
            # stop the AcqNdtDataServer after all of our incoming data has been
            # processed.             
            dataServer.Stop()
            
            
    except KeyboardInterrupt:
            print("Proceso Interrumpido")
            print("Desconenctando servidor AcqKnowledge...")
            dataServer.Stop()
            print("Servidor desconectado.")   
              
                     

def outputToScreen(index, frame, channelsInSlice):
        """Callback for use with an AcqNdtDataServer to display incoming channel data in the console.
        
        index:  hardware sample index of the frame passed to the callback.
                        to convert to channel samples, divide by the SampleDivider out
                        of the channel structure.
        frame:  a tuple of doubles representing the amplitude of each channel
                        at the hardware sample position in index.  The index of the
                        amplitude in this tuple matches the index of the corresponding
                        AcqNdtChannel structure in channelsInSlice
        channelsInSlice:        a tuple of AcqNdtChannel objects indicating which
                        channels were acquired in this frame of data.  The amplitude
                        of the sample of the channel is at the corresponding location
                        in the frame tuple.
        """
        
        # NOTE:  'index' is set to a hardware acquisition sample index.
    
        print("%s | %s" % (index, frame)) 


def SendOSCData(self,index, frame, channelsInSlice,OSCClient):
                """Callback for use with an AcqNdtDataServer to send incoming channel data via OSC protocol.
                
                index:  hardware sample index of the frame passed to the callback.
                                to convert to channel samples, divide by the SampleDivider out
                                of the channel structure.
                frame:  a tuple of doubles representing the amplitude of each channel
                                at the hardware sample position in index.  The index of the
                                amplitude in this tuple matches the index of the corresponding
                                AcqNdtChannel structure in channelsInSlice
                channelsInSlice:        a tuple of AcqNdtChannel objects indicating which
                                channels were acquired in this frame of data.  The amplitude
                                of the sample of the channel is at the corresponding location
                                in the frame tuple.
                OSCClient: OSC client object from which the data will be sent to remote server.
                """
                
                # NOTE:  'index' is set to a hardware acquisition sample index.
                
                msg = "%s %s %s %s %s %s %s" % (index, frame[0], frame[1], frame[2], frame[3], frame[4], frame[5])
                OSCClient.send_message("/BioHarness", msg)
                
if __name__ == '__main__':
        main()