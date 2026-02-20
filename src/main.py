import network
import urequests
import ujson
import utime
import machine
from machine import I2C, Pin
import lcd

i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
LCD = lcd.Lcd_i2c(i2c, cols=16, rows=2)
LCD.clear()
def load_config():
    with open("CONFIGURATION.txt", "r") as f:
        return ujson.load(f)


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        
        # Timeout pro připojení (cca 10s)
        attempt = 0
        while not wlan.isconnected() and attempt < 20:
            utime.sleep(0.5)
            attempt += 1
    
    if wlan.isconnected():
        return True
    else:
        return False
    
def get_location():
    try:
        # IP-API nevyžaduje klíč
        res = urequests.get("http://ip-api.com/json/")
        data = res.json()
        res.close()
        return data['lat'], data['lon'], data['city']
    except Exception:
        return None, None, "error"
    
def get_weather(lat, lon, api_key):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric".format(lat, lon, api_key)
        res = urequests.get(url)
        if res.status_code == 200:
            data = res.json()
            res.close()
            return data
        res.close()
    except:
        pass
    return None

def update_display(city, weather_data):
    LCD.clear()
    if weather_data:
        temp = weather_data['main']['temp']
        desc = weather_data['weather'][0]['main']
        hum = weather_data['main']['humidity']
        LCD.write("{}: {}C".format(city, temp))
        LCD.set_cursor(0, 1)
        LCD.write("{} Hum:{}%".format(desc, hum))
    else:
        LCD.write("Weather Data\nError")

config = load_config()
last_update = -60000
lat, lon, city = None, None, None

if config:
    while True:
        wlan = network.WLAN(network.STA_IF)

        if not wlan.isconnected():
            if not connect_wifi(config['ssid'], config['password']):
                utime.sleep(5)
                continue
        
        current_time = utime.ticks_ms()
        if utime.ticks_diff(current_time, last_update) >= 600000:
            if lat is None:
                lat, lon, city = get_location()
                if lat:
                    LCD.clear()
                    LCD.write("Loc: {},{}\n{}".format(lat, lon, city))
                    utime.sleep(3)