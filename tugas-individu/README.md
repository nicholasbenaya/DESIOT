# Panduan Praktikum Tugas Individu: ESP32 + Modul LDR Digital (D0) + Blynk + ThingSpeak

**Mata Kuliah:** Desain dan Aplikasi IoT (DESIOT) - **Institut Teknologi Sepuluh Nopember (ITS)**

---

## 📌 Karakteristik Modul LDR 3-Pin (D0, VCC, GND)
Modul LDR jenis ini menggunakan IC komparator tegangan (umumnya LM393) dan sebuah potensiometer (trimpot biru kecil):
* **Pin D0 (Digital Output):** Mengeluarkan sinyal digital logika **`0` (LOW)** saat mendeteksi cahaya terang (di atas batas ambang), dan logika **`1` (HIGH)** saat kondisi gelap / cahaya terhalang.
* **Trimpot Biru:** Dapat diputar menggunakan obeng kecil untuk mengatur ambang batas sensitivitas cahaya terang/gelap.

---

## 🔌 1. Skema Pengkabelan (Wiring 3-Pin LDR ke ESP32)

| Pin Modul LDR | Pin ESP32 DevKit | Keterangan & Warna Jumper |
| :--- | :--- | :--- |
| **VCC** | **3V3** | Sumber tegangan 3.3V (Kabel Merah) |
| **GND** | **GND** | Ground bersama (Kabel Hitam) |
| **D0 (Digital Out)** | **GPIO 4** | Input pin digital membaca level logika cahaya (Kabel Biru/Kuning) |

*(Catatan: Gunakan tegangan **3V3** agar sinyal logika D0 yang keluar dari modul LDR memiliki level tegangan 3.3V yang aman 100% untuk pin GPIO ESP32).*

---

## 📱 2. Konfigurasi di Blynk IoT (blynk.cloud & Mobile App)

1. **Buat Template di Web [blynk.cloud](https://blynk.cloud):**
   * Masuk ke **Developer Zone** ➔ **Templates** ➔ **+ New Template**
   * **Name:** `Monitoring Cahaya LDR` | **Hardware:** `ESP32` | **Connection:** `WiFi`
2. **Buat Datastreams (Virtual Pins):**
   * **V0:** Name: `Status Terang (1/0)`, Type: `Integer`, Min: `0`, Max: `1`
   * **V1:** Name: `Kondisi Cahaya`, Type: `String` (Menampilkan `"TERANG"` atau `"GELAP"`)
   * **V2:** Name: `LED Alarm Gelap`, Type: `Integer`, Min: `0`, Max: `255`
3. **Salin Kredensial Template Device:**
   * Masuk ke menu **Search** ➔ **+ New Device** ➔ Pilih template yang baru dibuat.
   * Di tab **Device Info**, salin 3 baris kredensial:
     ```cpp
     #define BLYNK_TEMPLATE_ID "TMPLxxxxxx"
     #define BLYNK_TEMPLATE_NAME "Monitoring Cahaya LDR"
     #define BLYNK_AUTH_TOKEN "xxxxxxxxxxxx"
     ```
   * Tempelkan di baris 11–13 file `src/main.cpp`.
4. **Desain Widget di Aplikasi HP (Blynk App):**
   * **Value Display:** Hubungkan ke Datastream `V1` (Menampilkan teks `"TERANG"` atau `"GELAP"` secara realtime).
   * **LED Widget:** Hubungkan ke Datastream `V2` (Otomatis menyala merah/kuning saat kondisi **GELAP** sebagai simulasi lampu penerangan malam otomatis).

---

## 📈 3. Konfigurasi di ThingSpeak (thingspeak.com)

1. Buka [thingspeak.com](https://thingspeak.com), login, dan klik **New Channel**:
   * **Name:** `Monitoring Cahaya LDR DESIOT`
   * Centang **Field 1:** `Status Cahaya (1=Terang, 0=Gelap)`
   * Centang **Field 2:** `Raw Pin Level D0 (0=LOW, 1=HIGH)`
2. Klik **Save Channel**, lalu buka tab **API Keys**:
   * Salin **Channel ID** ke variabel `myChannelNumber` di `main.cpp`.
   * Salin **Write API Key** ke variabel `myWriteAPIKey` di `main.cpp`.

---

## 🚀 4. Upload Program via PlatformIO

Buka terminal di folder `tugas-individu`, lalu jalankan:
```bash
pio run -t upload
pio device monitor -b 115200
```

---

## 🧪 5. Kalibrasi Trimpot & Pengujian Praktikum

1. **Kalibrasi Sensitivitas Trimpot:**
   * Di modul LDR terdapat 2 buah LED kecil (LED Power dan LED Indikator D0).
   * Dalam kondisi cahaya ruangan normal, putar perlahan baut trimpot biru menggunakan obeng kecil hingga LED indikator D0 pas berada di batas antara menyala dan padam.
2. **Uji Kondisi Gelap (Tutup Sensor):**
   * Tutup sensor LDR dengan jari Anda.
   * LED indikator D0 padam (Pin D0 menjadi `HIGH`), Serial Monitor menampilkan `Status: GELAP`.
   * Di aplikasi Blynk, teks berubah menjadi `GELAP` dan widget LED otomatis menyala.
3. **Uji Kondisi Terang (Beri Cahaya):**
   * Sorot LDR dengan senter HP.
   * LED indikator D0 menyala (Pin D0 menjadi `LOW`), Serial Monitor menampilkan `Status: TERANG`.
   * Di aplikasi Blynk, teks berubah menjadi `TERANG` dan widget LED padam.
4. **Grafik ThingSpeak:**
   * Buka tab *Private View* ThingSpeak. Setiap **20 detik**, grafik time-series akan mencatat transisi status logika cahaya (1 saat terang dan 0 saat gelap).
