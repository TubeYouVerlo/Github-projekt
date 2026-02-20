# 🌦️ MicroPython Meteostanice s 16x2 I2C LCD

Jednoduchý IoT projekt, který se připojí k WiFi, automaticky zjistí polohu podle IP adresy, stáhne aktuální počasí a zobrazí ho na 16x2 I2C LCD displeji.

Funguje na:
- Raspberry Pi Pico W  
- ESP32 / ESP8266 (s MicroPythonem)

---

## 📦 Funkce projektu

- 📡 Připojení k WiFi (otevřená i zabezpečená síť)  
- 🌍 Automatické zjištění polohy (IP geolokace)  
- 🌡️ Stažení aktuálního počasí z OpenWeatherMap  
- 📟 Zobrazení teploty, vlhkosti a stavu počasí na LCD  
- 🔄 Automatická aktualizace každých 10 minut  
- 🔁 Automatické znovupřipojení k WiFi  
- 🧠 Optimalizované pro zařízení s malou RAM (MicroPython)

---

## 🧰 Požadovaný hardware

- Mikrořadič (Pico W / ESP32 / ESP8266)  
- 16x2 I2C LCD displej (HD44780 + PCF8574 převodník)  
- Propojovací vodiče  
- Připojení k internetu přes WiFi  

### Zapojení I2C (příklad pro Pico W)

| LCD Pin | Pico W Pin |
|----------|--------------|
| SDA | GP0 |
| SCL | GP1 |
| VCC | 3.3V / 5V |
| GND | GND |

