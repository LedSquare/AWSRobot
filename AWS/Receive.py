# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import keyboard

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a3i34psezogwo0-ats.iot.ap-southeast-2.amazonaws.com"
CLIENT_ID = "basicPubSub2"
PATH_TO_CERTIFICATE = "certs/RaspberryPI.cert.pem"
PATH_TO_PRIVATE_KEY = "certs/RaspberryPI.private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs/root-CA.crt"
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
def receiveLoop():  
    while True:
        t.sleep(1)
        def on_message_received(topic, payload, **kwargs):
            print(topic, payload)
            global subMess
            subMess = payload
            #if received_count == args.count:
            #    received_all_event.set()
        subscribe_future, packet_id = mqtt_connection.subscribe(
            topic=TOPIC,
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=on_message_received
        )
        subscribe_result = subscribe_future.result()
    
    
