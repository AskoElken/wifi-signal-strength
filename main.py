import re
import subprocess
import time

def get_wifi_signal_strength(interface='en0'):
    try:
        # Run the airport command to get Wi-Fi info
        airport_output = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I', f'{interface}']).decode('utf-8')

        # Use regular expressions to extract signal strength and SSID
        signal_strength_match = re.search(r'agrCtlRSSI: (-\d+)', airport_output)
        ssid_match = re.search(r'SSID:\s+(.+)', airport_output)


        if signal_strength_match and ssid_match:
            signal_strength = signal_strength_match.group(1)
            ssid = ssid_match.group(1)
            return signal_strength, ssid
        else:
            return None

    except subprocess.CalledProcessError as e:
        return None

if __name__ == "__main__":
    interface = 'en0'  # Change this to your Wi-Fi interface name (typically 'en0' on macOS)

    while True:
        signal_strength, ssid = get_wifi_signal_strength(interface)
        if signal_strength is not None and ssid is not None:
            print(f'{ssid[6:]}: {signal_strength} dBm')
        else:
            print('Unable to retrieve signal strength.')

        time.sleep(1)  # Sleep for 1 second before the next measurement
