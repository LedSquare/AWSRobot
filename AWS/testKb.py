import keyboard as kb
import time 
import threading


wasd = [0,0]

def forBack():
  while True:
    if (kb.is_pressed('w')):
      wasd[0]=1
    if (kb.is_pressed('s')):
      wasd[0]=2
    if (kb.is_pressed('s') and kb.is_pressed('w')): 
      wasd[0]=0
    else:
      time.sleep(0.1)
      wasd[0]=0

def lefRight():
  while True: 
    
    if (kb.is_pressed('a')):
      wasd[1]=1 
    if (kb.is_pressed('d')):
      wasd[1]=2      
    if (kb.is_pressed('a') and kb.is_pressed('d')):
      wasd[1]=0
    else:
      time.sleep(0.1)
      wasd[1]=0
