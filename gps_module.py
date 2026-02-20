import serial
import pynmea2
import threading

latest_lat = "No Fix"
latest_lon = "No Fix"
fix_quality = 0

def gps_reader():
    global latest_lat, latest_lon, fix_quality

    try:
        gps = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
    except:
        return

    while True:
        try:
            line = gps.readline().decode('ascii', errors='replace')
            if line.startswith('$GPGGA'):
                msg = pynmea2.parse(line)
                fix_quality = msg.gps_qual

                if msg.latitude and msg.longitude and fix_quality > 0:
                    latest_lat = msg.latitude
                    latest_lon = msg.longitude
        except:
            pass

def start_gps():
    thread = threading.Thread(target=gps_reader, daemon=True)
    thread.start()

def get_location():
    return latest_lat, latest_lon
