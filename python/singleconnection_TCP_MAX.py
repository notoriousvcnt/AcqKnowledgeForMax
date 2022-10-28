#!/usr/bin/env python
# encoding: utf-8

"""
singleconnection.py

Illustrates data streaming from AcqKnowledge to Python client code
using the single TCP connection mode.  This also illustrates using
variable sampling rates and how the AcqNdtDataServer class delivers
variable sampling rate data through its varying frames.

Note that in this example, all of the channels are downsampled, so
the actual hardware frame count is skipped on every odd hardware sample
index.

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

# Send a template to AcqKnowledge.  We will send the template file
# 'var-sample-no-base-rate.gtl' within the "resources" subdirectory.
#
# First construct a full path to this file on disk.

resourcePath = os.getcwd() + os.sep + "resources"
templateName = "BioHarnessTemplate.gtl"

# Send the template to AcqKnowledge.  We will use the LoadTemplate()
# member of the AcqNdtServer class.  This helper function will
# read the file into local memory, encode it appropriately, and
# transfer the data to AcqKnowledge.
#
# Note that capitalization is important!  The member function starts
# with a capital "L".

# print("Loading template %s" % templateName) 

# acqServer.LoadTemplate(templateName)


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
print('Servidor TCP conectado en el puerto %i' % (singleConnectPort))

acqServer.changeDataConnectionHostname('127.0.0.1')        




