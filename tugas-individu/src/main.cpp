/* =========================================================================
 * TUGAS INDIVIDU: DESAIN DAN APLIKASI IOT (ITS SURABAYA)
 * ESP32 + MODUL LDR DIGITAL (PIN D0, VCC, GND) + BLYNK + THINGSPEAK
 * -------------------------------------------------------------------------
 * Spesifikasi Tugas:
 * 1. Node ESP32 terhubung ke Modul LDR Digital (Pin D0)
 * 2. Aplikasi Blynk terhubung ke ESP32 (Status Terang/Gelap Real-Time)
 * 3. ESP32 melaporkan data status cahaya ke ThingSpeak (Logging Historis)
 * ========================================================================= */

// --- 1. KREDENSIAL BLYNK IOT (WAJIB DITARUH PALING ATAS SEBELUM INCLUDE) ---
#define BLYNK_TEMPLATE_ID "TMPL6MLJkVh6N"
#define BLYNK_TEMPLATE_NAME "LDRDESIOT" // Ganti dengan Template Name Anda
#define BLYNK_AUTH_TOKEN    "rUkMhyF58tRXyR34-OaMfiXhXWccPYfs"          // Ganti dengan Auth Token Device Anda

#define BLYNK_PRINT Serial

#include <WiFi.h>
#include <BlynkSimpleEsp32.h>
#include <ThingSpeak.h>

// --- 2. PINOUT SENSOR MODUL LDR DIGITAL ---
// Pin D0 (Digital Output) Modul LDR dihubungkan ke GPIO 4 ESP32
#define PIN_LDR_DO          4

// --- 3. KREDENSIAL WI-FI ---
char ssid[] = "iPhone";       // Nama Wi-Fi / Hotspot HP (Wajib pita 2.4 GHz)
char pass[] = "acikiwir";          // Password Wi-Fi

// --- 4. KREDENSIAL THINGSPEAK ---
unsigned long myChannelNumber = 3592378;          // Ganti dengan Channel ID Anda
const char * myWriteAPIKey = "HV1KWP8OX1SEBUW8";  // Ganti dengan Write API Key Anda

// Objek Client & Timer
WiFiClient client;
BlynkTimer timer;

// Variabel Penyimpan Data Sensor Digital
// Logika Modul LDR LM393 umum:
// - Terang (cahaya cukup) : D0 bernilai LOW (0), LED onboard modul menyala
// - Gelap (tertutup)      : D0 bernilai HIGH (1), LED onboard modul padam
int ldrDigitalVal = 1;
int lightStateNum = 0;       // 1 = Terang, 0 = Gelap
String lightCondition = "GELAP";

// =========================================================================
// FUNGSI MEMBACA SENSOR LDR DIGITAL (D0)
// =========================================================================
void readLDRSensor() {
    ldrDigitalVal = digitalRead(PIN_LDR_DO);

    // Evaluasi Logika Komparator LM393
    if (ldrDigitalVal == LOW) {
        // Cahaya terdeteksi di atas threshold trimpot
        lightStateNum = 1;
        lightCondition = "TERANG";
    } else {
        // Cahaya di bawah threshold (kondisi gelap / tertutup)
        lightStateNum = 0;
        lightCondition = "GELAP";
    }

    Serial.printf("[SENSOR LDR D0] Pin D0 Level: %d | Status Cahaya: %s | State: %d\n",
                  ldrDigitalVal, lightCondition.c_str(), lightStateNum);
}

// =========================================================================
// FUNGSI MENGIRIM DATA KE BLYNK IOT (Interval: Tiap 2 Detik)
// =========================================================================
void sendDataToBlynk() {
    readLDRSensor();

    if (Blynk.connected()) {
        // Virtual Pin V0: Nilai numerik status (1 = Terang, 0 = Gelap) -> Value Display / Gauge
        Blynk.virtualWrite(V0, lightStateNum);

        // Virtual Pin V1: Teks status ("TERANG" atau "GELAP")
        Blynk.virtualWrite(V1, lightCondition);

        // Virtual Pin V2: LED Indikator di Aplikasi Blynk (Otomatis menyala jika GELAP)
        if (lightStateNum == 0) {
            Blynk.virtualWrite(V2, 255); // LED Widget ON (Warna Merah/Kuning)
        } else {
            Blynk.virtualWrite(V2, 0);   // LED Widget OFF
        }

        Serial.println("[BLYNK] Berhasil mengirim data ke Blynk IoT (V0, V1, V2).");
    }
}

// =========================================================================
// FUNGSI MENGIRIM DATA KE THINGSPEAK (Interval: Tiap 20 Detik)
// Catatan: ThingSpeak akun gratis membatasi update minimal 15 detik sekali
// =========================================================================
void sendDataToThingSpeak() {
    if (WiFi.status() == WL_CONNECTED) {
        // Field 1: Status Numerik Cahaya (1 = Terang, 0 = Gelap)
        ThingSpeak.setField(1, lightStateNum);

        // Field 2: Raw Pin Level D0 (0 atau 1)
        ThingSpeak.setField(2, ldrDigitalVal);

        // Kirim data ke ThingSpeak
        int httpCode = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);

        if (httpCode == 200) {
            Serial.printf("[THINGSPEAK] Sukses mengirim data ke Channel %lu (HTTP 200 OK).\n", myChannelNumber);
        } else {
            Serial.printf("[THINGSPEAK ERROR] Gagal mengirim data. Kode HTTP: %d\n", httpCode);
            if (httpCode == -401) {
                Serial.println("  -> Periksa kembali Write API Key Anda di thingspeak.com!");
            }
        }
    } else {
        Serial.println("[THINGSPEAK] Gagal terhubung ke Wi-Fi.");
    }
}

// =========================================================================
// SETUP & LOOP UTAMA
// =========================================================================
void setup() {
    Serial.begin(115200);
    delay(1000);

    Serial.println("\n=======================================================");
    Serial.println("DESIOT ITS - TUGAS INDIVIDU (ESP32 + LDR D0 + BLYNK)");
    Serial.println("=======================================================");

    // Inisialisasi Pin Digital D0 Modul LDR
    pinMode(PIN_LDR_DO, INPUT_PULLUP);
    Serial.printf("[HARDWARE] Modul LDR terhubung ke GPIO %d (Input Digital D0)\n", PIN_LDR_DO);

    // 1. Hubungkan ke Wi-Fi & Blynk IoT
    Serial.printf("[WIFI] Menghubungkan ke SSID: %s...\n", ssid);
    Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);

    // 2. Inisialisasi ThingSpeak Client
    ThingSpeak.begin(client);
    Serial.println("[THINGSPEAK] ThingSpeak Client berhasil diinisialisasi.");

    // 3. Konfigurasi Timer Non-Blocking
    // Kirim ke Blynk setiap 2 detik (responsif di aplikasi smartphone)
    timer.setInterval(2000L, sendDataToBlynk);

    // Kirim ke ThingSpeak setiap 20 detik (mematuhi batas rate-limit 15 detik)
    timer.setInterval(20000L, sendDataToThingSpeak);

    Serial.println("[SYSTEM] Setup selesai! Loop monitoring cahaya dimulai...\n");
    Serial.println("[TIP] Putar trimpot biru kecil pada modul LDR menggunakan obeng");
    Serial.println("      untuk mengatur sensitivitas ambang batas terang/gelap.\n");
}

void loop() {
    Blynk.run(); // Menjaga koneksi socket Blynk
    timer.run(); // Menjalankan timer pembacaan LDR D0 dan kirim ke cloud
}
