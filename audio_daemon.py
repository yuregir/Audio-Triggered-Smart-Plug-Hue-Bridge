
import time
import requests
from CoreAudio import AudioObjectGetPropertyData, kAudioObjectSystemObject, kAudioDevicePropertyDeviceIsRunning
from CoreAudio import kAudioObjectPropertyElementMaster
import threading

# Philips Hue API info
HUE_BRIDGE_IP = "192.168.1.100"  # Hue Bridge IP address
API_USERNAME = "your_api_username"  # Hue API key
GROUP_ID = "0"  # The group where TRÅDFRI plug is located

# Parameters (Adjustable)
SOUND_THRESHOLD = 1000  # Audio detection threshold
SOUND_DURATION = 3  # Duration to keep sound playing before turning plug on
CHECK_INTERVAL = 1  # How often to check audio (in seconds)

# Audio detection service
def check_audio():
    audio_is_playing = False
    sound_duration = 0  # Keep track of how long sound is playing
    while True:
        try:
            # Check audio status via Core Audio
            device_running = AudioObjectGetPropertyData(kAudioObjectSystemObject,
                kAudioDevicePropertyDeviceIsRunning,
                kAudioObjectPropertyElementMaster)
            
            if device_running:
                if not audio_is_playing:
                    audio_is_playing = True
                    sound_duration = 0  # Reset duration when sound starts
                    print("Audio detected.")
                sound_duration += CHECK_INTERVAL  # Increase sound duration
                if sound_duration >= SOUND_DURATION:
                    turn_on_plug()
            else:
                if audio_is_playing:
                    audio_is_playing = False
                    sound_duration = 0  # Reset duration when sound stops
                    print("Audio stopped. Turning off plug.")
                    turn_off_plug()

            if audio_is_playing and sound_duration < SOUND_DURATION:
                time.sleep(CHECK_INTERVAL)
            else:
                time.sleep(1)
                
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

# Hue API to turn on TRÅDFRI plug
def turn_on_plug():
    url = f"http://{HUE_BRIDGE_IP}/api/{API_USERNAME}/groups/{GROUP_ID}/action"
    payload = {"on": True}
    response = requests.put(url, json=payload)
    if response.status_code == 200:
        print("Ikea TRÅDFRI Smart Plug turned on.")
    else:
        print("Error turning on plug.")

# Hue API to turn off TRÅDFRI plug
def turn_off_plug():
    url = f"http://{HUE_BRIDGE_IP}/api/{API_USERNAME}/groups/{GROUP_ID}/action"
    payload = {"on": False}
    response = requests.put(url, json=payload)
    if response.status_code == 200:
        print("Ikea TRÅDFRI Smart Plug turned off.")
    else:
        print("Error turning off plug.")

# Main function
def main():
    audio_thread = threading.Thread(target=check_audio)
    audio_thread.daemon = True
    audio_thread.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
