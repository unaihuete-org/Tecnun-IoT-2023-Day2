# Tecnun-IoT-2023-Day2

## Challenges

1. Create App in IOT Central
2. Define Device Template for Raspberry Pi "simulated" sensors.
![image](https://user-images.githubusercontent.com/64772417/219130238-c95c3244-cd64-45e5-9107-8cf460cf5e59.png)
![image](https://user-images.githubusercontent.com/64772417/219130372-2b2a2f80-43a8-4c6a-b93c-94b1a785f88e.png)


4. Connect Raspberry Pi to Azure IOT Central using Python SDK. **Base python file is given to you**. The App should: 
    1. Provision Device. 
    2. Connect Device (create Device client, to have authenticated connection to communicate)
    3. Set "DeviceLocation" Property
    4. Define command(method) handler
    5. While loop sending telemetry and receiving engine control command to switch engine off/on 
6. Control the "engine" status from Azure IoT central , using commands (method).
7. Define a Job in Azure IoT Central that will schedule the engine switch ON/OFF.
8. Define a Rule in Azure IoT Central that will send you an email based on either temperatura or engineRPM sensor value.
9. Create a Dashboard with collected data in Azure IoT Central.
![image](https://user-images.githubusercontent.com/64772417/219142285-b3ea1b65-ef86-4c9d-a8fd-76c1b670d294.png)
11. Export the data from Azure IoT central to Azure Storage account.
12. (TO BE DECIDED) Upload picture from device to Azure IOT Central 

## Reference docs 
- Lab PDFs used with Yuemin (connecting to rapsberry, connecting raspberry to internet, reading sensors,...)
- Create Device Template https://learn.microsoft.com/en-us/azure/iot-central/core/howto-set-up-template
- Lab from Azure IoT Day 1 https://github.com/unaihuete-org/Tecnun-IoT-2023
- Send Telemetry from device to Azure IoT Central https://learn.microsoft.com/en-us/azure/iot-develop/quickstart-send-telemetry-central?pivots=programming-language-python
    - **Check Sample! (only some of the lines will be needed, check steps in challenge description)**: https://github.com/Azure/azure-iot-sdk-python/blob/main/samples/pnp/simple_thermostat.py 
- Upload file to Azure IoT Hub (also used for Azure IoT Central): https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-python-python-file-upload
- Command handlers https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-python-python-device-management-get-started#create-a-device-app-with-a-direct-method
