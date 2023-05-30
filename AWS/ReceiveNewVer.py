# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import threading
import serial
import serial.tools.list_ports

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a3i34psezogwo0-ats.iot.ap-southeast-2.amazonaws.com"
CLIENT_ID = "basicPubSub2"
PATH_TO_CERTIFICATE = "certs/Cert2/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certs/Cert2/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs/Cert2/AmazonRootCA1.pem"
MESSAGE = "Hello World"
TOPIC = "sdk/test/python"
RANGE = 20

max_wait_count = 100
received_count = 0
received_all_event = threading.Event()

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

received_count = 0

# Serial connection part

def initSerialPort():
  global ser
  ser = serial.Serial()
  ser.baudrate = 9600
  ser.port = "COM1"
  ser.timeout = 5
  ser.open()

# def inputPort():
#   ports = list(serial.tools.list_ports.comports())
#   for port in ports:
#     print(port.device)
#   print("Введите номер порта: ")
#   portN = input()
#   try:
#     initSerialPort(portN)
#   except:
#     print("хз че, но что то не так, попробуй снова")
#     inputPort()
    

def serialSend(data):
    data = data.decode('utf-8')
    data = data[10:14]
    data = data.replace(':', '').replace(',', '').replace(' ', '')
    print(data)
    txs = ""
    for val in data:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'
    txs += '\n' #Временная мера
    ser.write(txs.encode())
    print(txs.encode(), "encoded message")

initSerialPort()


# end serial connection part

def on_message_received(topic, payload, **kwargs):
    print(payload)
    serialSend(payload)
    global received_count
    received_count += 1
    if received_count == max_wait_count:
        received_all_event.set()

subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=TOPIC,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received
)
subscribe_result = subscribe_future.result()
print("Subscribed with {}".format(str(subscribe_result['qos'])))


# Wait for all messages to be received.
# This waits forever if count was set to 0.
#if not received_all_event.is_set():
#    print("Waiting for all messages to be received...")

received_all_event.wait()
print("{} message(s) received.".format(received_count))

# Disconnect
print("Disconnecting...")
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print("Disconnected!")




