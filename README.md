
# Audio Detection and Hue TRÅDFRI Plug Control Daemon

This project enables you to control a Philips Hue TRÅDFRI Smart Plug using audio detection on your MacOS device. When audio is detected, the plug will turn on; when no audio is detected for a set duration, the plug will turn off.

## **Requirements**

- **MacOS** (This script is developed for MacOS users.)
- **Python 3** (Make sure Python 3 is installed)
- **Requests** library: Install via `pip install requests`
- **CoreAudio**: This library allows interaction with audio devices on MacOS.

### **Hardware Requirements**
- **Philips Hue Bridge** (The central hub that connects all Hue devices, including the TRÅDFRI Smart Plug)
- **Philips Hue TRÅDFRI Smart Plug**
  
### **Steps to Setup**

#### 1. **Set Up Philips Hue Bridge**
   
To get started, you need to set up your **Philips Hue Bridge**. Here's how:

1. Unbox your Philips Hue Bridge and connect it to your Wi-Fi router using the provided Ethernet cable.
2. Plug the Hue Bridge into a power outlet using the supplied adapter.
3. Wait for the LED lights on the Hue Bridge to stabilize. The **first light** will turn blue, indicating that the Bridge is ready to connect.
4. Download the **Philips Hue app** on your smartphone (available on both iOS and Android).
5. Open the app and follow the in-app instructions to connect the Hue Bridge to your home network.
6. Once the Bridge is connected, the app will prompt you to **create an account** or log in with an existing one.

#### 2. **Add TRÅDFRI Smart Plug to Hue Bridge**

1. Plug in the **TRÅDFRI Smart Plug** to a power outlet.
2. Open the **Philips Hue app** on your phone.
3. Go to the **Settings** section, then tap **Light setup** and select **Add light**.
4. The Hue app will search for new devices. **Press the button** on your TRÅDFRI Smart Plug until the app detects it.
5. Once detected, the plug will be added to your Hue system. You can now control it from the app.

#### 3. **Obtain Hue Bridge API Username**

To control the Smart Plug programmatically, you need to obtain the **API username** for your Hue Bridge:

1. Open a web browser and navigate to: `http://<bridge-ip-address>/debug/clip.html`
2. Replace `<bridge-ip-address>` with the actual IP address of your Hue Bridge (you can find this in your router's connected devices list).
3. Under the **HTTP Request** section, enter the following:
   - **URL**: `/api`
   - **Body**: `{"devicetype":"your_username#audio_daemon"}`
   - **Method**: POST
4. Hit **POST** and the response will contain your **API username** (this is the value you need for the script).

#### 4. **Install Python Libraries**

Before running the script, you need to install the required Python libraries:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/audio-daemon-project.git
   cd audio-daemon-project
   ```

2. **Install the required libraries**:
   ```bash
   pip install requests
   ```

#### 5. **Configure the Python Script**

Before running the script, you need to update the **Hue Bridge** settings in the script:

1. Open the **`audio_daemon.py`** file.
2. Replace the following placeholders with your own data:
   - **HUE_BRIDGE_IP**: The IP address of your Hue Bridge.
   - **API_USERNAME**: The username you obtained from the previous step.
   - **GROUP_ID**: The group ID in which your TRÅDFRI Smart Plug is located (default is usually "0" for single-device setups).

```python
HUE_BRIDGE_IP = "192.168.1.100"  # Hue Bridge IP address
API_USERNAME = "your_api_username"  # Hue API key
GROUP_ID = "0"  # The group where TRÅDFRI plug is located
```

#### 6. **Create PLIST for LaunchDaemons**

To run the script automatically in the background (as a daemon), you'll need to create a **PLIST** file for `launchd` on macOS:

1. Open **Terminal**.
2. Create the following directory if it doesn't exist:
   ```bash
   sudo mkdir -p /Library/LaunchDaemons
   ```
3. Create the **PLIST file**:
   ```bash
   sudo nano /Library/LaunchDaemons/com.audio.daemon.plist
   ```
4. Add the following content to the PLIST file, adjusting paths as necessary:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
     <dict>
       <key>Label</key>
       <string>com.audio.daemon</string>
       <key>ProgramArguments</key>
       <array>
         <string>/usr/bin/python3</string>
         <string>/path/to/your/audio_daemon.py</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
       <key>KeepAlive</key>
       <true/>
     </dict>
   </plist>
   ```

5. Save and exit the editor (`Ctrl + O`, `Enter`, `Ctrl + X`).
6. Load the **PLIST** file using `launchctl`:
   ```bash
   sudo launchctl load /Library/LaunchDaemons/com.audio.daemon.plist
   ```

#### 7. **Run the Script**

Once the PLIST is created, the script will automatically start whenever your Mac boots up.

If you want to manually start it for testing, run the following in the terminal:
```bash
python3 audio_daemon.py
```

### **How It Works**

- **Audio Detection**: The script continuously checks whether any audio is being played on your system. Once it detects audio, it sends a request to the Hue Bridge to turn on the TRÅDFRI Smart Plug.
- **No Audio for Set Duration**: If no audio is detected for a defined period (e.g., 3 seconds), the script sends a request to turn off the plug.
- **Adjustable Parameters**: You can modify the sound threshold, duration, and check frequency by changing the script's parameters.

### **Troubleshooting**

- **Hue Bridge not detected**: Make sure the Hue Bridge is properly connected to your network and that the IP address is correct.
- **Plug not responding**: Check if the TRÅDFRI Smart Plug is correctly added to the Hue app. Make sure the Hue Bridge API username is correct.
