#!/usr/bin/env python3
"""
=========================================================================
DESIOT ITS SURABAYA - MQTT DASHBOARD & CONTROLLER HOST
Mata Kuliah : Desain dan Aplikasi IoT - ITS Surabaya
Fungsi      : 
  1. Menerima data telemetri kelembapan tanah dari Node 4 via MQTT
  2. Mengevaluasi kondisi tanah secara terpusat (Opsi B):
     - Jika ADC >= 2100 (Kering) -> Kirim MQTT Pompa ON
     - Jika ADC <= 1800 (Basah)  -> Kirim MQTT Pompa OFF
  3. Menampilkan grafik / tabel status real-time di terminal
=========================================================================
"""

import sys
import time
import json

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("[ERROR] Library 'paho-mqtt' belum terinstall.")
    print("Silakan jalankan: pip install paho-mqtt")
    sys.exit(1)

BROKER_HOST = "10.3.74.219"
BROKER_PORT = 1883

TOPIC_SENSOR = "desiot/kebun/sensor"
TOPIC_PUMP_STATE = "desiot/kebun/pompa"
TOPIC_PUMP_SET = "desiot/kebun/pompa/set"
TOPIC_GATEWAY = "desiot/kebun/gateway"

SOIL_DRY_THRESHOLD = 2100
SOIL_WET_THRESHOLD = 1800

current_pump_state = None

def on_connect(client, userdata, flags, rc, *args):
    # Kompatibel dengan paho-mqtt v1 dan v2 (ReasonCode)
    code = getattr(rc, "value", rc)
    if code == 0:
        print("==================================================")
        print("  DESIOT ITS SURABAYA - MQTT CONTROLLER & MONITOR ")
        print(f"  Terhubung ke Broker: {BROKER_HOST}:{BROKER_PORT}")
        print("==================================================")
        client.subscribe(TOPIC_SENSOR)
        client.subscribe(TOPIC_PUMP_STATE)
        client.subscribe(TOPIC_GATEWAY)
        print(f"[SUB] Berlangganan ke topik: {TOPIC_SENSOR}")
        print(f"[SUB] Berlangganan ke topik: {TOPIC_PUMP_STATE}")
        print(f"[SUB] Berlangganan ke topik: {TOPIC_GATEWAY}")
        print("Siaga menerima data telemetri dari Node 4...\n")
    else:
        print(f"[ERROR] Gagal terhubung ke broker, kode: {rc}")

def on_message(client, userdata, msg):
    global current_pump_state
    topic = msg.topic
    payload_str = msg.payload.decode('utf-8', errors='ignore')

    timestamp = time.strftime("%H:%M:%S")

    try:
        data = json.loads(payload_str)
    except Exception:
        data = {"raw": payload_str}

    if topic == TOPIC_SENSOR:
        adc = data.get("raw_adc", 0)
        status = data.get("status", "UNKNOWN")
        bar_len = min(40, max(0, int((adc / 4095.0) * 40)))
        bar = "█" * bar_len + "-" * (40 - bar_len)

        print(f"[{timestamp}] [SENSOR LPN Node 2]")
        print(f"  ADC: {adc} | Status: {status}")
        print(f"  Grafik: [{bar}] ({adc}/4095)")

        # Logika Pengambilan Keputusan Otomatis Terpusat (Opsi B)
        if adc >= SOIL_DRY_THRESHOLD and current_pump_state != 1:
            print("  >>> KONDISI: TANAH KERING! Mengirim perintah ON ke Pompa Node 1 via MQTT...")
            client.publish(TOPIC_PUMP_SET, json.dumps({"state": 1}))
            current_pump_state = 1
        elif adc <= SOIL_WET_THRESHOLD and current_pump_state != 0:
            print("  >>> KONDISI: TANAH BASAH! Mengirim perintah OFF ke Pompa Node 1 via MQTT...")
            client.publish(TOPIC_PUMP_SET, json.dumps({"state": 0}))
            current_pump_state = 0
        print("-" * 50)

    elif topic == TOPIC_PUMP_STATE:
        state = data.get("pump_state", 0)
        current_pump_state = state
        print(f"[{timestamp}] [KONFIRMASI POMPA Node 1] Status Fisik: {'>>> MENYALA (ON) <<<' if state else '>>> PADAM (OFF) <<<'}")
        print("-" * 50)

    elif topic == TOPIC_GATEWAY:
        print(f"[{timestamp}] [GATEWAY Node 4] Status: {data}")
        print("-" * 50)

def main():
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Menghubungkan ke broker Mosquitto di {BROKER_HOST}:{BROKER_PORT}...")
    try:
        client.connect(BROKER_HOST, BROKER_PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
        client.disconnect()
    except Exception as e:
        print(f"[ERROR] Koneksi error: {e}")

if __name__ == "__main__":
    main()
