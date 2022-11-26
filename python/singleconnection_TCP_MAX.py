#!/usr/bin/env python
# encoding: utf-8

"""
singleconnection_TCP_MAX.py

This program ONLY prepares the AcqKnowledge server to send data via TCP in single connection mode. You need to configure an external server 
which will receive the incoming data from AcqKnowledge via NDT using TCP protocol. 

Default Connection Host: 127.0.0.1
Default Connection Port: 15020

Both Host and Port can be changed using the commands specified in the NDT Documentation, which is available in AcqKnowledge software or Usage Guide.

This program is an edited version from the original examples provided by BIOPAC.
Copyright (c) 2009-2010 BIOPAC Systems, Inc. All rights reserved.
"""

# import standard Python modules

from email.policy import default
import sys
import os

# import our biopacndt support module

import biopacndt

acqServer = biopacndt.AcqNdtQuickConnect()
if not acqServer:
        print("No AcqKnowledge servers found!") 
        sys.exit()

# Check if there is a data acquisition that is already running.
# In order to acquire data into a new template, we need to halt
# any previously running acquisition first.

if acqServer.getAcquisitionInProgress():
        acqServer.toggleAcquisition()
        print("Current data acquistion stopped") 

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

# instruct AcqKnowledge to send us data for all of the channels being
# acquired and retain the array of enabled channel objects.

enabledChannels = acqServer.DeliverAllEnabledChannels()

# ask AcqKnowledge which TCP port number will be used when it tries
# to establish its data connection

singleConnectPort = acqServer.getSingleConnectionModePort()
print('TCP Server connected on port %i' % (singleConnectPort))

acqServer.changeDataConnectionHostname('127.0.0.1')        




