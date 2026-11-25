# DESIOT - Smart Irrigation BLE Mesh & Edge Autonomy System

> **Tugas Kelompok Mata Kuliah Desain dan Aplikasi IoT (DESIOT)**  
> **Laboratorium A108 • Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC)**  
> **Institut Teknologi Sepuluh Nopember (ITS) Surabaya**

---

## 📌 Ringkasan Proyek

Sistem irigasi pertanian pintar (*Smart Irrigation System*) berbasis **BLE Mesh (Bluetooth Low Energy Mesh)** dan **Gateway Wi-Fi / MQTT** menggunakan 4 unit mikrokontroler **ESP32-S3 DevKit** dengan framework **pure ESP-IDF (ESP-BLE-MESH)**.

Sistem dirancang dengan arsitektur **Industrial Edge Autonomy**:
- Node Gateway mengevaluasi telemetri kelembapan tanah secara lokal dan langsung memerintahkan aktuator pompa melalui BLE Mesh.
- Jaringan mesh tetap beroperasi secara mandiri (*fail-safe*) tanpa ketergantungan pada server komputer atau dashboard web (*no single point of failure*).
- Web Dashboard berbasis Flask + MQTT + Chart.js berfungsi murni sebagai **Human-Machine Interface (HMI)** untuk monitoring visual *real-time* dan *manual override*.

---

## 🏗️ Arsitektur & Topologi 4-Node BLE Mesh

```text
[ Node 2: Sensor Kelembapan ] (LPN / Low Power Node, Unicast: 0x0004)
        | (Capacitive Moisture v1.2, GPIO 4 ADC1_CH3)
        | [Vendor Model 0x0002 Telemetry setiap 5s]
        v
[ Node 3: Relay + Friend ] (Unicast: 0x0005)
        | (Backbone Router & Friend Cache, Always Listening)
        v
[ Node 4: Gateway & Provisioner ] (Unicast: 0x0001, Dual-Radio: BLE Mesh + Wi-Fi)
        |
        +--- [Edge Autonomy Decision: ADC >= 2100 -> ON, ADC <= 1800 -> OFF]
        |        | (Generic OnOff Client via BLE Mesh)
        |        v
        |    [ Node 1: Pompa DC ] (Generic OnOff Server, Unicast: 0x0002/0x0003)
        |         (Relay Active-LOW, GPIO 10)
        |
        +---> (Wi-Fi STA + MQTT: desiot/kebun/#)
                 |
                 v
        [ Komputer Host: Eclipse Mosquitto Broker ]
                 |
                 v
        [ Web Dashboard (Flask + Chart.js HMI) : http://localhost:5000 ]
```

---

## 🔌 Detail Spesifikasi & Peran Node

| Node | Peran Mesh | Hardware Utama | Pinout ESP32-S3 | Status Daya | Unicast Addr |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **Node 1** | Generic OnOff Server | Relay 5V Active-LOW, Pompa DC 5V | `GPIO 10` ➔ IN Relay<br>`GND` ➔ Common Ground<br>`Adaptor 5V Eksternal` ➔ VCC & COM Relay<br>`NO Relay` ➔ (+) Pompa | Wajib Siaga (Adaptor USB 5V Mandiri) | `0x0002` / `0x0003` |
| **Node 2** | Low Power Node (LPN) | Capacitive Soil Moisture Sensor v1.2 | `GPIO 4 (ADC1_CH3)` ➔ AOUT Sensor<br>`3V3` ➔ VCC Sensor (Wajib 3.3V)<br>`GND` ➔ Ground Sensor | Baterai / USB (Vendor Model Telemetri 5s) | `0x0004` |
| **Node 3** | Relay + Friend Node | ESP32-S3 DevKit | Radio RX Scanning 100% Siaga | Wajib Berlistrik (Adaptor USB 5V) | `0x0005` |
| **Node 4** | Provisioner, Gateway & OnOff Client | ESP32-S3 DevKit | Dual Radio (BLE Mesh + Wi-Fi STA) | Wajib Berlistrik (USB Host PC) | `0x0001` |

---

## 📂 Struktur Direktori Repositori

```text
DESIOT/
├── firmware_idf/                     # Source Code Utama Firmware ESP-IDF (Pure C)
│   ├── include/
│   │   └── mesh_common.h             # Konfigurasi Bersama (NetKey, AppKey, Pin, Topik MQTT, Threshold)
│   ├── src/
│   │   ├── node1_pump.c              # Firmware Node 1: Generic OnOff Server Pompa
│   │   ├── node2_sensor.c            # Firmware Node 2: Sensor Kelembapan & Vendor Model
│   │   ├── node3_relay_friend.c      # Firmware Node 3: Relay Mesh Router & Friend Node
│   │   └── node4_gateway.c           # Firmware Node 4: Gateway Wi-Fi, MQTT & Edge Autonomy
│   ├── tools/
│   │   └── web_dashboard.py          # Server HMI Web Dashboard (Flask + MQTT + Chart.js)
│   ├── CMakeLists.txt                # Build configuration ESP-IDF
│   ├── partitions.csv                # Custom 4MB partition table
│   └── platformio.ini                # Konfigurasi multi-environment PlatformIO
├── Makalah_Tugas_Kelompok_DESIOT.md  # Laporan Akademik Lengkap Proyek
├── Panduan_Implementasi_Tugas_Kelompok_DESIOT_ESP32S3.pdf # Panduan Implementasi & Wiring
├── Presentasi_Tugas_Kelompok_DESIOT.pptx # Slide Presentasi Proyek
├── rangkaian_tugas_kelompok.png      # Skema Rangkaian Hardware Kelompok
├── mosquitto.conf                    # Konfigurasi Broker MQTT Lokal (Listener 0.0.0.0:1883)
├── .gitignore                        # Filter file build & cache
└── README.md                         # Dokumentasi Resmi Repositori
```

---

## 🚀 Panduan Kompilasi & Flash Firmware (PlatformIO)

Pastikan telah menginstal **PlatformIO Core (CLI)** atau extension PlatformIO di VS Code.

Buka terminal di direktori proyek, lalu jalankan perintah upload sesuai node yang terhubung via kabel USB:

### 1. Flash Node 3 (Relay + Friend Node)
```bash
pio run -d firmware_idf -e node3_relay_friend -t upload
pio device monitor -d firmware_idf -b 115200
```

### 2. Flash Node 1 (Aktuator Pompa DC)
```bash
pio run -d firmware_idf -e node1_pump -t upload
pio device monitor -d firmware_idf -b 115200
```

### 3. Flash Node 2 (Sensor Kelembapan Tanah)
```bash
pio run -d firmware_idf -e node2_sensor_lpn -t upload
pio device monitor -d firmware_idf -b 115200
```

### 4. Flash Node 4 (Gateway Wi-Fi & Provisioner)
> Sebelum flash Node 4, pastikan kredensial Wi-Fi dan IP Broker MQTT pada `firmware_idf/include/mesh_common.h` sudah disesuaikan dengan jaringan yang aktif.
```bash
pio run -d firmware_idf -e node4_gateway -t upload
pio device monitor -d firmware_idf -b 115200
```

---

## 🖥️ Menjalankan Broker MQTT & Web Dashboard HMI

### 1. Jalankan Eclipse Mosquitto Broker
Pastikan file konfigurasi mengizinkan koneksi dari jaringan lokal (`listener 1883 0.0.0.0` dan `allow_anonymous true`):
```bash
mosquitto -c mosquitto.conf -v
```

### 2. Jalankan Server Web Dashboard
Pastikan dependensi Python terpasang (`flask`, `paho-mqtt`):
```bash
pip install flask paho-mqtt
python firmware_idf/tools/web_dashboard.py
```
Akses dashboard visual melalui browser pada: **`http://localhost:5000`**

---

## ⚙️ Logika Edge Autonomy

Node 4 mengevaluasi nilai telemetri ADC dari Node 2 secara instan di sisi *firmware* (`node4_gateway.c`):
- **Kondisi Tanah Kering (`ADC >= 2100`)**:
  Node 4 otomatis mengirimkan perintah `Generic OnOff Set = 1` ke Node 1 melalui BLE Mesh untuk menyalakan pompa.
- **Kondisi Tanah Basah (`ADC <= 1800`)**:
  Node 4 otomatis mengirimkan perintah `Generic OnOff Set = 0` ke Node 1 melalui BLE Mesh untuk memadamkan pompa.
- **HMI Manual Override**:
  Jika tombol **NYALAKAN** atau **PADAMKAN** ditekan pada Web Dashboard, Node 4 beralih ke Mode Manual dan mengesampingkan otomasi sampai mode dikembalikan ke Otomatis.

---

## 👥 Tim Pengembang (Lab A108 • FTEIC ITS)

* **Nicholas Benaya (5024241050)** & Anggota Kelompok Proyek DESIOT  
* Departemen Teknik Elektro / Teknik Komputer  
* Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC)  
* Institut Teknologi Sepuluh Nopember (ITS) Surabaya
