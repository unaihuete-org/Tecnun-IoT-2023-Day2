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
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=registration_id,
        id_scope=id_scope,
        symmetric_key=symmetric_key,
    )
    provisioning_device_client.provisioning_payload = {"modelId": model_id}
    return await provisioning_device_client.register()


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
    registration_result = await provision_device(
        provisioning_host, id_scope, registration_id, symmetric_key, model_id
    )

    if registration_result.status == "assigned":
        print("Device was assigned")
        print(registration_result.registration_state.assigned_hub)
        print(registration_result.registration_state.device_id)

        # Create device client
        device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=symmetric_key,
            hostname=registration_result.registration_state.assigned_hub,
            device_id=registration_result.registration_state.device_id,
            product_info=model_id,
        )
    else:
        raise RuntimeError(
            "Could not provision device. Aborting Plug and Play device connection."
        )
  
    #------- CONNECT DEVICE TO AZURE IOT CENTRAL-------#
    await device_client.connect()

    #--------- SET PROPERTY----------#
    # Set device DeviceLocation property
    await device_client.patch_twin_reported_properties({
      "DeviceLocation": {
        "lat": 43.304677,
        "lon": -2.009697,
        "alt": 5
      }
    })
    print("Device location property sent")

    #--------- RECEIVE COMMANDS/METHODS----------#
    
    # Define method listener to receive commands from Azure IoT Central and change engine status
    # use  on_method_request_received property to receive commands
    async def method_request_handler(method_request):
        global engine
        if method_request.name == "EngineControl":
            # Act on the method by rebooting the device
            print("Command received to change engine status")
        
            
        
            # Change engine status
            if method_request.payload == True:
                engine = True
            else:
                engine = False
            print ("Changed engine status to",method_request.payload)

            # Create a method response indicating the method request was resolved
            resp_status = 200
            resp_payload = {"Response": "This is the response from the device"}
            method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)

        else:
            # Create a method response indicating the method request was for an unknown method
            resp_status = 404
            resp_payload = {"Response": "Unknown method"}
            method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)

        # Send the method response
        await device_client.send_method_response(method_response)
        

    # Attach the handler to the client
    device_client.on_method_request_received = method_request_handler

    #--------- SEND FILE TO IOT CENTRAL----------#

    #full path to file tecnun.jpg in same directory as this python file

    
    PATH_TO_FILE =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "tecnun.jpg") 
    blob_name = os.path.basename(PATH_TO_FILE)
    storage_info = await device_client.get_storage_info_for_blob(blob_name)

    print(storage_info)
    sas_url = "https://{}/{}/{}{}".format(
        storage_info["hostName"],
        storage_info["containerName"],
        storage_info["blobName"],
        storage_info["sasToken"]
    )

    # Upload the specified file
    print("Uploading file to Azure IoT Central")
    with BlobClient.from_blob_url(sas_url) as blob_client:
        with open(PATH_TO_FILE, "rb") as f:
            blob_client.upload_blob(f, overwrite=True)
            

    #print("File uploaded to Azure IoT Central")
    await device_client.notify_blob_upload_status(
    storage_info["correlationId"], True, 200, "OK: {}".format(PATH_TO_FILE)
    )

    #--------- SEND TELEMETRY WHILE LOOP----------#
    # Send telemetry data to Azure IoT Central every 10 seconds 
    while True:
        
        # Generate random data temperature 30 to 100 celsius
        temperature = random() * 70 + 30
        # Define Engine RPM if engine is on (1000 to 2000)
        if engine:
            engineRPM = random() * 1000 + 1000
        else:
            engineRPM = 0
    
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
        print("Sending message: {}".format(msg))
        await device_client.send_message(msg)
        print("Message successfully sent")

        # Wait 10 seconds
        await asyncio.sleep(10)



#--------- RUN MAIN FUNCTION----------#
if __name__ == "__main__":
    asyncio.run(main())


