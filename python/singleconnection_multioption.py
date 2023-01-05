#!/usr/bin/env python
# encoding: utf-8

"""
singleconnection_multioption.py

This program lets the user choose between TCP mode or OSC mode.

Default TCP Connection Host: 127.0.0.1
Default TCP Connection Port: 15010

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
        """Execute the singleconnection mode for acquiring data from AcqKnowledge, and enables server to connect to external application. 
        Alternatively, it receives the data sent via TCP and then sends the data via OSC protocol if -osc | --oscActivated flag is True.
        """

        help_message = """usage: python singleconnection_multioption.py [-h | --help] [-ch | --controlHost <hostname>] [-cp | --controlPort  <port>] \
[-ah | --AcqHost <hostname>] [-ap | --AcqPort <port>] 
[-osc | --oscActivated] [-oh | --OSCHost <hostname>] [-op | --OSCport <port>]       

Options and arguments:
-h   | --help: display this message
-ch  | --controlHost <hostname>: Hostname for Control AcqAcqKnowledge Server (XML-RPC).
-cp  | --controlPort <port>: Port for Control AcqAcqKnowledge Server (XML-RPC).
-ah  | --AcqHost <hostname>: Hostname for Acquisition Server.
-ap  | --AcqPort <port>: Port for Acquisition Server.
-osc | --oscActivated: Activates stream data via OSC.
-oh  | --OSCHost <hostname>: OSC Server Hostname (no effect if -osc flag is not activated).
-op  | --OSCport <port>: OSC Server Port (no effect if -osc flag is not activated).
        """
        parser = argparse.ArgumentParser(usage=help_message,add_help=False)
        parser.add_argument("-h","--help",action='store_true',help=argparse.SUPPRESS)
        parser.add_argument("-ch","--controlHost",default="127.0.0.1",help=argparse.SUPPRESS)
        parser.add_argument("-cp","--controlPort",default=15010,help=argparse.SUPPRESS)
        
        parser.add_argument("-ah","--AcqHost",default="127.0.0.1",help=argparse.SUPPRESS)
        parser.add_argument("-ap","--AcqPort",default=15020,help=argparse.SUPPRESS)

        parser.add_argument("-osc","--oscActivated",action="store_true",help=argparse.SUPPRESS)

        parser.add_argument("-oh","--OSCHost",default="127.0.0.1",help=argparse.SUPPRESS)
        parser.add_argument("-op","--OSCPort",default=5005,help=argparse.SUPPRESS)

        
        args = parser.parse_args()

        if args.help:
                print(help_message)
                sys.exit()

        try:
                #Trying to connect to specified server. QuickConnect option is not used due security reasons.
                print("Intentando conectar al servidor AcqKnowledge a través de la conexión de control en la dirección %s y puerto %s..." \
                         % (args.controlHost, args.controlPort))        
                acqServer = biopacndt.AcqNdtServer(args.controlHost, args.controlPort)
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

                if args.oscActivated:
                        print("Se intentará enviar información via OSC")
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

                        dataServer = biopacndt.AcqNdtDataServer(singleConnectPort, enabledChannels,OSCHostname = args.OSCHost,OSCport=int(args.OSCPort))

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
                        print("El servidor está listo para enviar la información. Enviando a través del puerto OSC  %i" % (dataServer.GetOSCPort()))
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
                else:
                        print("Se intentará enviar información via TCP")
                        if acqServer.changeDataConnectionHostname(args.AcqHost) != 0:
                                print("No se puede realizar conexión al hostname %s" % (args.AcqHost))
                                sys.exit()

                        if acqServer.changeSingleConnectionModePort(args.AcqPort) != 0:
                                print("No se puede realizar conexión al puerto %s" % (args.AcqPort))
                                sys.exit()

                        print('Servidor TCP disponible en hostname %s port %i' % (args.AcqHost, args.AcqPort))

                while True:
                        time.sleep(1)
                        
        except KeyboardInterrupt:
                print("Proceso Interrumpido")
                print("Desconenctando servidor AcqKnowledge...")
                
                try:
                        
                        if acqServer.getAcquisitionInProgress():
                                acqServer.toggleAcquisition()
                                # acqServer.__RPC.__close()
                                print("La adquisición de datos ha sido detenida.")
                        else:
                                print("La adquisición ya fue detenida previamente, por lo que no se hará nada.")
                        if args.oscActivated:
                                dataServer.Stop()
                        print("Servidor desconectado.")
                         
                except ConnectionRefusedError:
                        print("No se puede establecer una conexión ya que el equipo de destino denegó expresamente dicha conexión.")

def SendOSCData(index, frame, channelsInSlice,OSCClient):
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
                
                msg = str(index)
                for data in frame:
                        msg += " " + str(data)
                OSCClient.send_message("/BioHarness", msg)
                
if __name__ == '__main__':
        main()