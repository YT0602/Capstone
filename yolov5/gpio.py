import Jetson.GPIO as GPIO
import threading
import torch
import time




ENA = 33
IN1 = 35
IN2 = 37

# set pin numbers to the board's
GPIO.setmode(GPIO.BOARD)

# initialize EnA, In1 and In2
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)

def forward():
    time.sleep(3.5)
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    time.sleep(7)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

def backward():
    time.sleep(2)
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(7)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)



                    if save_img or save_crop or view_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                        annotator.box_label(xyxy, label, color=colors(c, True))
                        accNum = float(f'{conf:.2f}')
                        if names[c] == 'Good apple' and accNum > 0.30:
                            print(names[c] + ': ' + f'{conf:.2f}')
                            thread = threading.Thread(target=forward)
                            thread.start()
                        elif names[c] == 'damaged apple' and accNum > 0.30:
                            print(names[c] + ': ' + f'{conf:.2f}')
                            time.sleep(1.5)
                            thread = threading.Thread(target=backward)
                            thread.start()