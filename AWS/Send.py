# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
from testKb import forBack, lefRight, wasd
import threading
import keyboard

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a3i34psezogwo0-ats.iot.ap-southeast-2.amazonaws.com"
CLIENT_ID = "basicPubSub2"
PATH_TO_CERTIFICATE = "certs/RaspberryPI.cert.pem"
PATH_TO_PRIVATE_KEY = "certs/RaspberryPI.private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs/root-CA.crt"
MESSAGE = wasd
TOPIC = "sdk/test/python"
# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")
# Publish message to server desired number of times.
print('Begin Publish')

def ending():
    print('Publish End')
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    
def mainSendProg():
    whileOn = True
    while whileOn:
        data = "{}".format(MESSAGE)
        message = {"mes" : data}
        mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
        print("Published: '" + json.dumps(message) + "' to the topic: " + TOPIC)
        t.sleep(1)
        if keyboard.is_pressed("="):
            whileOn = False
    ending()
        
    

mainSendProgT1 = threading.Thread(target=mainSendProg)
forbackT2 = threading.Thread(target=forBack)
lefRightT3 = threading.Thread(target=lefRight)

mainSendProgT1.start()  
forbackT2.start()
lefRightT3.start()



