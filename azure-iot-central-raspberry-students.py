# In this python program, we will connect to Azure IoT Central and send telemetry data from a Raspberry Pi.
# Telemetry data will be send to Azure IoT Central every 5 seconds.
# Mock sensors will be used to generate random data.


#import libraries
import json
import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device import Message, MethodResponse
from random import random
from datetime import timedelta, datetime
from azure.core.exceptions import AzureError
from azure.storage.blob import BlobClient
engine=False
   

######### PROVISION DEVICE DEF FUNCTION ################
async def provision_device(provisioning_host, id_scope, registration_id, symmetric_key, model_id):

MISSING CODE

############# MAIN ##################
async def main():
    #Global variable to control engine status (on/off)(TRUE/FALSE)
    global engine

    #-----PROVISION DEVICE TO AZURE IOT CENTRAL USING DPS-------#

    #ID Scope
    id_scope=""
    #Registration ID == Device ID
    registration_id=""
    #Symmetric Key == Primary Key
    symmetric_key=""
    #Provisioning Host is a global endpoint
    provisioning_host="global.azure-devices-provisioning.net"
    # model id --> taken from the device template in IoT Central DTDL file
    model_id=""

    # Provision the device
    

    MISSING CODE




    #------- CONNECT DEVICE TO AZURE IOT CENTRAL-------#
    
    MISSING CODE

    #--------- SET PROPERTY----------#
    # Set device DeviceLocation property
    

    MISSING CODE




    print("Device location property sent")

    #--------- RECEIVE COMMANDS/METHODS----------#
    
    # Define method listener to receive commands from Azure IoT Central and change engine status
    # use  on_method_request_received property to receive commands
    async def method_request_handler(method_request):
        global engine
       

        MISSING CODE
        

    # Attach the handler to the client
    device_client.on_method_request_received = method_request_handler

    #--------- SEND FILE TO IOT CENTRAL----------#

    #full path to file tecnun.jpg in same directory as this python file

    
    MISSING CODE

    #--------- SEND TELEMETRY WHILE LOOP----------#
    # Send telemetry data to Azure IoT Central every 10 seconds 
    while True:
        
        # Generate random data temperature 30 to 100 celsius
        MISSING CODE
        # Define Engine RPM if engine is on (1000 to 2000)
        MISSING CODE
    
        # Create message
        msg = Message(
            json.dumps(
                {
                    "Temperature": temperature,
                    "Engine": engine,
                    "EngineRPM": engineRPM
                }
            )
        )

        # Send message
        
        MISSING CODE
        print("Message successfully sent")

        # Wait 10 seconds
        await asyncio.sleep(10)


#--------- RUN MAIN FUNCTION----------#
if __name__ == "__main__":
    asyncio.run(main())


