import network
import urequests
import ujson
import utime
from machine import I2C, Pin
import lcd

# LCD setup
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
display = lcd.Lcd_i2c(i2c, cols=16, rows=2)
display.clear()

# ---------------- CONFIG ---------------- #

def load_config():
    try:
        with open("credentials.txt", "r") as f:
            return ujson.load(f)
    except Exception as e:
        print("Config error:", e)
        display.write("Config Error")
        return None


# ---------------- WIFI ---------------- #

def connect_wifi(ssid, password=None):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid)

    timeout = 15
    while not wlan.isconnected() and timeout > 0:
        display.clear()
        display.write("Connecting WiFi")
        print("Connecting WiFi...")
        utime.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        display.clear()
        display.write("WiFi OK\n" + ip)
        print("Connected:", ip)
        utime.sleep(2)
        return wlan
    else:
        display.clear()
        display.write("WiFi Failed!")
        print("WiFi failed")
        return None


# ---------------- LOCATION ---------------- #

def get_location():
    try:
        res = urequests.get("http://ip-api.com/json/")
        data = res.json()
        res.close()
        return data["lat"], data["lon"], data["city"]
    except:
        return None, None, "LOC ERR"


# ---------------- WEATHER ---------------- #
# Use HTTP to avoid SSL memory crashes

def get_weather(lat, lon, api_key):
    try:
        url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric".format(lat, lon, api_key)
        res = urequests.get(url)
        if res.status_code == 200:
            data = res.json()
            res.close()
            return data
        res.close()
    except Exception as e:
        print("Weather error:", e)
    return None


# ---------------- LCD UPDATE ---------------- #

def update_display(city, weather_data):
    display.clear()

    if weather_data:
        temp = weather_data["main"]["temp"]
        hum = weather_data["main"]["humidity"]
        desc = weather_data["weather"][0]["main"]

        # Trim text for 16x2 LCD
        city = city[:8]
        desc = desc[:8]

        display.write("{} {}C".format(city, temp))
        display.set_cursor(0, 1)
        display.write("{} {}%".format(desc, hum))
    else:
        display.write("Weather Error")


# ---------------- MAIN ---------------- #

config = load_config()
if not config:
    raise SystemExit

ssid = config["ssid"]
password = config["password"]
api_key = config["api_key"]

wlan = connect_wifi(ssid, password)
if not wlan:
    raise SystemExit

# Get location once
lat, lon, city = get_location()
if lat is None:
    display.clear()
    display.write("Loc Failed")
    city = "Unknown"
else:
    display.clear()
    display.write("Loc OK\n" + city)
    utime.sleep(2)

last_update = 0

# Main loop
while True:
    now = utime.ticks_ms()

    # Update every 10 minutes
    if utime.ticks_diff(now, last_update) > 600000:
        print("Updating weather...")
        data = get_weather(lat, lon, api_key)
        update_display(city, data)
        last_update = now

    # Auto reconnect WiFi
    if not wlan.isconnected():
        connect_wifi(ssid, password)

    utime.sleep(1)