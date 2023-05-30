import serial
import serial.tools.list_ports
import keyboard
import time 
import threading

def initSerialPort(portNumber):
  global ser
  ser = serial.Serial()
  ser.baudrate = 9600
  ser.port = "COM" + str(portNumber)
  ser.timeout = 5
  ser.open()

def inputPort():
  ports = list(serial.tools.list_ports.comports())
  for port in ports:
    print(port.device)
  print("Введите номер порта: ")
  portN = input()
  try:
    initSerialPort(portN)
  except:
    print("хз че, но что то не так, попробуй снова")
    inputPort()
    

def serialSend(data):
  txs = ""
  for val in data:
    txs += str(val)
    txs += ','
  txs = txs[:-1]
  txs += ';'
  txs += '\n' #Временная мера
  ser.write(txs.encode())
  print(txs.encode())


def mainProg():
  inputPort()
  while True:
    data = subMess
    time.sleep(1)
    serialSend(data)

  
serialT1 = threading.Thread(target=mainProg)
receiveT2  = threading.Thread(target=receiveLoop)

serialT1.start()
receiveT2.start()

receiveT2.join()
serialT1.join()
