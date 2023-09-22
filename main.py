import subprocess
import time
import curses
import re

def get_connected_ssid_by_channel():
    try:
        # Run the airport command to get Wi-Fi info
        airport_output = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I']).decode('utf-8')

        # Use regular expressions to extract the connected channel
        channel_match = re.search(r'channel: (\d+)', airport_output)

        if channel_match:
            connected_channel = channel_match.group(1)
            # Run the airport command to get the SSID on the connected channel
            airport_output = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s', '-c', connected_channel, '-I']).decode('utf-8')
            # Use regular expressions to extract the connected SSID
            ssid_match = re.search(r'SSID: (.+)', airport_output)
            if ssid_match:
                return connected_channel, ssid_match.group(1)
        return ''
    except subprocess.CalledProcessError as e:
        return ''

def get_wifi_signal_strength(stdscr):
    while True:
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        connected_channel, connected_ssid = get_connected_ssid_by_channel()

        try:
            # Run the airport command to get Wi-Fi info
            airport_output = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s','-I']).decode('utf-8')

            # Split the output into lines and skip the header line
            lines = airport_output.strip().split('\n')[1:]

            wifi_info = []

            # Extract and store SSID, signal strength, and channel of each detected network
            for line in lines:
                columns = line.split()

                if len(columns) >= 4:
                    ssid = columns[0]
                    signal_strength = columns[1]
                    channel = columns[2]

                    if channel != 'RSSI':
                        wifi_info.append((ssid, signal_strength, channel))

            wifi_info.sort(key=lambda x: str(x[2]))  # Sort the list by channel

            # Clear the screen
            stdscr.clear()

            # Display SSID, signal strength, and channel in sorted order
            row = 0
            for ssid, signal_strength, channel in wifi_info:
                display_text = "SSID: {:<20} Signal Strength: {:<10} Channel: {:<5}".format(ssid, signal_strength, channel)

                if ssid == connected_ssid and channel == connected_channel:
                    stdscr.addstr(row, 0, display_text, curses.color_pair(1))
                else:
                    stdscr.addstr(row, 0, display_text)

                row += 1

            stdscr.refresh()

            time.sleep(1)  # Sleep for 1 seconds before the next update

        except subprocess.CalledProcessError as e:
            stdscr.addstr(0, 0, f"Error: {e}")
            stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(get_wifi_signal_strength)
