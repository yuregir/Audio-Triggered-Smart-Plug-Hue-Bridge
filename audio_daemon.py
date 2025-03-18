import time
import requests
import numpy as np
import threading
import CoreAudio
from scipy import signal

# Hue Bridge Information
HUE_BRIDGE_IP = "192.168.1.100"  # Hue Bridge IP address
API_USERNAME = "your_api_username"  # Hue API key
GROUP_ID = "0"  # The group where TRÅDFRI plug is located

# Adjustable Parameters
AUDIO_THRESHOLD = 0.02  # Audio detection threshold (value between 0 and 1)
AUDIO_DETECTED_DURATION = 3  # Time (in seconds) to keep the plug on after detecting sound
AUDIO_SILENCE_DURATION = 5  # Time (in seconds) to keep the plug off after silence
CHECK_INTERVAL = 1  # Interval to check audio levels (in seconds)

# Hue API URLs
HUE_URL = f"http://{HUE_BRIDGE_IP}/api/{API_USERNAME}/groups/{GROUP_ID}/action"

# Function to detect audio using Core Audio
def detect_audio():
    # Get default input device using Core Audio API
    input_device = CoreAudio.CoreAudioGetDefaultInputDevice()
    input_stream = CoreAudio.CoreAudioOpenStream(input_device)

    audio_data = input_stream.read(1024)
    volume_norm = np.linalg.norm(audio_data) * 10  # Normalize the audio volume
    return volume_norm

# Function to turn on the Hue Plug
def turn_on_plug():
    data = {"on": True}
    response = requests.put(HUE_URL, json=data)
    return response.status_code == 200

# Function to turn off the Hue Plug
def turn_off_plug():
    data = {"on": False}
    response = requests.put(HUE_URL, json=data)
    return response.status_code == 200

# Main function to handle audio detection and control plug
def audio_detection_loop():
    plug_status = False  # Start with the plug turned off
    last_audio_time = time.time()  # Track the last time sound was detected
    last_silence_time = time.time()  # Track the last time silence was detected

    while True:
        audio_level = detect_audio()
        current_time = time.time()

        # If sound is detected
        if audio_level > AUDIO_THRESHOLD:
            last_audio_time = current_time  # Update the last audio detection time
            if not plug_status:
                # If the plug is off and the audio is detected for enough time, turn it on
                if current_time - last_silence_time >= AUDIO_DETECTED_DURATION:
                    turn_on_plug()
                    plug_status = True
                    print("Plug turned ON due to audio")

        # If silence is detected (audio level is below threshold)
        elif audio_level < AUDIO_THRESHOLD:
            last_silence_time = current_time  # Update the silence detection time
            if plug_status:
                # If the plug is on and there's silence for enough time, turn it off
                if current_time - last_audio_time >= AUDIO_SILENCE_DURATION:
                    turn_off_plug()
                    plug_status = False
                    print("Plug turned OFF due to silence")

        time.sleep(CHECK_INTERVAL)

# Function to run the audio detection as a background daemon
def run_as_daemon():
    detection_thread = threading.Thread(target=audio_detection_loop)
    detection_thread.daemon = True  # Run the thread as a daemon so it runs in the background
    detection_thread.start()

# Start the daemon
if __name__ == "__main__":
    run_as_daemon()

    # The main program will keep running while the daemon thread works in the background
    while True:
        time.sleep(60)  # Main program stays idle while the background thread runs
