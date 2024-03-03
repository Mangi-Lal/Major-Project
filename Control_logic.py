import RPi.GPIO as GPIO
import pyrebase
from time import sleep
config = {
    "apiKey": "API_KEY",
    "authDomain": "major-project-19641",
    "databaseURL": "https://major-project-19641-default-rtdb.firebaseio.com/",
    "storageBucket": "project-680659596396"
}
firebase = pyrebase.initialize_app(config)

red = 3
yellow=7 # Terminal by number, el 22 es el GPIO25.
green = 11 # Terminal by number, el 18 es el GPIO24.
# El otro terminal a GND.


GPIO.setmode(GPIO.BOARD) # Terminal by number.
GPIO.setwarnings(False)
GPIO.setup(red,GPIO.OUT)
GPIO.setup(yellow,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)

print("Inicio. (CTRL + C para salir.")
#initialize the variable globally
ambulance = 9

def detectAmbulance():
    database = firebase.database()
    ProjectBucket = database.child("project-680659596396")
    print(ProjectBucket.get())
    ambulance = ProjectBucket.get().val()['Ambulance']
    print("value ",ambulance)
    print("ambulance detected ",ambulance)
    if ambulance == 1:
        return True
    else:
        return False
def handleAmbulance():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD) # Terminal by number.
    GPIO.setwarnings(False)
    GPIO.setup(red,GPIO.OUT)
    GPIO.setup(yellow,GPIO.OUT)
    GPIO.setup(green,GPIO.OUT)
    GPIO.output(red, GPIO.LOW)
    GPIO.output(yellow,GPIO.LOW)
    GPIO.output(green, GPIO.HIGH)
    sleep(5)


def handle_red_state(ttime):
    for interval in range(ttime):
        if detectAmbulance():
            handleAmbulance()
        else:
            GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD) # Terminal by number.
            GPIO.setwarnings(False)
            GPIO.setup(red,GPIO.OUT)
            GPIO.setup(yellow,GPIO.OUT)
            GPIO.setup(green,GPIO.OUT)
            GPIO.output(red, GPIO.HIGH)
            GPIO.output(yellow,GPIO.LOW)
            GPIO.output(green, GPIO.LOW)
            sleep(1)


def handle_yellow_state(ttime):
    for interval in range(ttime):
        if detectAmbulance():
            handleAmbulance()
        else:
            GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD) # Terminal by number.
            GPIO.setwarnings(False)
            GPIO.setup(red,GPIO.OUT)
            GPIO.setup(yellow,GPIO.OUT)
            GPIO.setup(green,GPIO.OUT)
            GPIO.output(red, GPIO.LOW)
            GPIO.output(yellow,GPIO.HIGH)
            GPIO.output(green, GPIO.LOW)
            sleep(1)


def handle_green_state(ttime):
    for interval in range(ttime):
        if detectAmbulance():
            handleAmbulance()
        else:
            GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD) # Terminal by number.
            GPIO.setwarnings(False)
            GPIO.setup(red,GPIO.OUT)
            GPIO.setup(yellow,GPIO.OUT)
            GPIO.setup(green,GPIO.OUT)
            GPIO.output(red, GPIO.LOW)
            GPIO.output(yellow,GPIO.LOW)
            GPIO.output(green, GPIO.HIGH)
            sleep(1)


def handle_yellow_state_short(ttime):
    for interval in range(ttime):
        if detectAmbulance():
            handleAmbulance()
        else:
            GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD) # Terminal by number.
            GPIO.setwarnings(False)
            GPIO.setup(red,GPIO.OUT)
            GPIO.setup(yellow,GPIO.OUT)
            GPIO.setup(green,GPIO.OUT)
            GPIO.output(red, GPIO.LOW)
            GPIO.output(yellow,GPIO.HIGH)
            GPIO.output(green, GPIO.LOW)
            sleep(1)

# State handlers list
state_handlers = [
# (state function, time in milliseconds)
(handle_red_state, 5), # Red LED, on for 5 seconds
(handle_yellow_state, 3), # Yellow LED, on for 3 seconds
(handle_green_state, 5), # Green LED, on for 5 seconds
(handle_yellow_state_short, 2) # Short Yellow LED, on for 2 seconds
]
def traffic_light():
    state = 0
    while True:
        # Get the current state tuple (handler function and sleep time)
        current_handler_and_time = state_handlers[state]
        handler_func = current_handler_and_time[0]
        sleep_duration_ms = current_handler_and_time[1]
        # Execute the handler function and sleep for the specified time
        handler_func(sleep_duration_ms)
        #usleep_ms(sleep_duration_ms)
        # Update the state index
        state = (state + 1) % len(state_handlers)
# Run the traffic light sequence
GPIO.cleanup()
traffic_light()