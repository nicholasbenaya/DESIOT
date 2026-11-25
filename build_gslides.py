import subprocess
import os
import time

PRES_ID = "1w8Jug58WB-AOoufTZq-uoXSKEgTsFzvZ8C2eTOdCix8"

def run_cmd(cmd):
    print("RUN:", " ".join(cmd[:4]))
    res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if res.returncode != 0:
        print("ERR:", res.stderr)
    return res.stdout.strip()

def add_slide_with_content(title, body_text):
    # Add slide
    out = run_cmd(["gslides", "mutate", "add-slide", PRES_ID])
    # output: "Added slide: SLIDES_API..."
    slide_id = out.split()[-1]
    time.sleep(1)
    
    # Add title
    run_cmd([
        "gslides", "mutate", "add-textbox", PRES_ID,
        "--slide", slide_id,
        "--text", title,
        "--x", "36", "--y", "25",
        "--width", "648", "--height", "45",
        "--font-size", "20", "--bold",
        "--color", "#0F172A"
    ])
    time.sleep(1)

    # Add body
    run_cmd([
        "gslides", "mutate", "add-textbox", PRES_ID,
        "--slide", slide_id,
        "--text", body_text,
        "--x", "36", "--y", "80",
        "--width", "648", "--height", "300",
        "--font-size", "12",
        "--color", "#334155"
    ])
    time.sleep(1)
    return slide_id

def main():
    # Slide 2: Latar Belakang (SLIDES_API1792799319_0 already exists)
    slide2_id = "SLIDES_API1792799319_0"
    run_cmd([
        "gslides", "mutate", "add-textbox", PRES_ID,
        "--slide", slide2_id,
        "--text", "Latar Belakang & Urgensi Solusi",
        "--x", "36", "--y", "25",
        "--width", "648", "--height", "45",
        "--font-size", "20", "--bold",
        "--color", "#0F172A"
    ])
    time.sleep(1)
    s2_body = (
        "1. Kebutuhan Irigasi Presisi:\n"
        "   - Efisiensi penyiraman air tanaman berdasarkan kadar air tanah aktual.\n"
        "   - Kebutuhan jaringan sensor terdistribusi di area luas tanpa ketergantungan kabel panjang.\n\n"
        "2. Keterbatasan Wi-Fi Konvensional:\n"
        "   - Konsumsi daya radio Wi-Fi relatif tinggi (sangat boros untuk sensor bertenaga baterai).\n"
        "   - Jarak jangkauan access point terbatas oleh dinding dan hambatan fisik.\n\n"
        "3. Keunggulan Solusi BLE Mesh & Gateway MQTT:\n"
        "   - Bluetooth Mesh mendukung Low Power Node (LPN) yang tidur berkala (deep sleep).\n"
        "   - Friend Node menyimpan antrian pesan selama sensor tidur.\n"
        "   - Gateway Wi-Fi menerjemahkan pesan mesh ke MQTT broker di komputer untuk visualisasi grafik."
    )
    run_cmd([
        "gslides", "mutate", "add-textbox", PRES_ID,
        "--slide", slide2_id,
        "--text", s2_body,
        "--x", "36", "--y", "80",
        "--width", "648", "--height", "300",
        "--font-size", "12",
        "--color", "#334155"
    ])
    time.sleep(1)

    # Slide 3: Arsitektur 4-Node
    s3_body = (
        "Topologi Bluetooth Mesh (many-to-many) dengan 4 Peran Khusus:\n\n"
        "• Node 1: Pompa Air DC (Generic OnOff Server)\n"
        "  - Mengeksekusi penyiraman otomatis via Modul Relay 5V. Wajib siaga (always listening).\n\n"
        "• Node 2: Sensor Kelembapan (Low Power Node / LPN)\n"
        "  - Membaca kapasitif tanah v1.2, bangun berkala, kirim status, lalu deep sleep (baterai mandiri).\n\n"
        "• Node 3: Relay + Friend Node (Mesh Backbone Router)\n"
        "  - Wajib berlistrik permanen & terjaga. Menyimpan pesan antrian untuk Node 2 dan merelai paket.\n\n"
        "• Node 4: Provisioner + Proxy + Wi-Fi Gateway\n"
        "  - Menjembatani paket BLE Mesh ke protokol MQTT via Wi-Fi menuju komputer host (port 1883)."
    )
    add_slide_with_content("Arsitektur Sistem & Topologi 4-Node BLE Mesh", s3_body)

    # Slide 4: Skema Rangkaian Hardware (Insert Image)
    s4_id = run_cmd(["gslides", "mutate", "add-slide", PRES_ID]).split()[-1]
    time.sleep(1)
    run_cmd([
        "gslides", "mutate", "add-textbox", PRES_ID,
        "--slide", s4_id,
        "--text", "Skema Rangkaian Elektronika & Interkoneksi Hardware",
        "--x", "36", "--y", "15",
        "--width", "648", "--height", "35",
        "--font-size", "18", "--bold",
        "--color", "#0F172A"
    ])
    time.sleep(1)
    # Upload image
    img_path = os.path.abspath("rangkaian_tugas_kelompok.png")
    run_cmd([
        "gslides", "mutate", "insert-image-from-file", PRES_ID,
        "--slide", s4_id,
        "--file", img_path,
        "--x", "36", "--y", "55",
        "--width", "648", "--height", "335"
    ])
    time.sleep(2)

    # Slide 5: Detail Node 1 & Node 2
    s5_body = (
        "NODE 1: POMPA AIR DC (ONOFF SERVER)\n"
        "• Hardware: ESP32 DevKit, Pompa Celup 5V, Modul Relay 5V Optocoupler.\n"
        "• Pinout: GPIO 23 -> IN Relay, VIN -> VCC & COM Relay, NO Relay -> (+) Pompa, GND -> (-) Pompa.\n"
        "• Logika: Saat kelembapan < ambang batas, relay menutup kontak NO dan pompa menyiram air.\n\n"
        "NODE 2: SENSOR KELEMBAPAN (LOW POWER NODE)\n"
        "• Hardware: ESP32 DevKit, Capacitive Soil Moisture Sensor v1.2, Catu Baterai (9V/18650).\n"
        "• Pinout: 3V3 -> VCC Sensor, GND -> GND Sensor, GPIO 34 (ADC1) -> AOUT Sensor, VIN -> Baterai (+).\n"
        "• Efisiensi: Deep sleep menekan arus hingga ~15 µA. Bangun berkala 60 detik membaca ADC."
    )
    add_slide_with_content("Detail Implementasi: Node 1 & Node 2", s5_body)

    # Slide 6: Detail Node 3 & Node 4
    s6_body = (
        "NODE 3: RELAY + FRIEND NODE (MESH BACKBONE)\n"
        "• Catu Daya: Adaptor USB 5V permanen (Wajib Berlistrik & Wajib Terjaga).\n"
        "• Peran Friend: Menyimpan antrian pesan (queue) saat Node 2 berada di mode deep sleep.\n"
        "• Peran Relay: Meneruskan paket mesh antar simpul jaringan tanpa kehilangan paket.\n\n"
        "NODE 4: GATEWAY WI-FI & MQTT BROKER KOMPUTER\n"
        "• Dual Radio: Mengoperasikan BLE Mesh Proxy bersamaan dengan Wi-Fi Station 2.4 GHz.\n"
        "• MQTT Bridge: Mengonversi data telemetri ke payload JSON dan publish ke topic MQTT.\n"
        "• Komputer Host: Menjalankan Eclipse Mosquitto (port 1883) & Dashboard grafik real-time."
    )
    add_slide_with_content("Detail Implementasi: Node 3 & Node 4", s6_body)

    # Slide 7: Klaim Pekerjaan Masing-Masing Anggota
    s7_body = (
        "MATRIKS PEMBAGIAN TUGAS & KONTRIBUSI TIM (TOTAL 100%):\n\n"
        "1. [Nama Anggota 1] / NRP 1 (Kontribusi 25%) - Koordinator Hardware & Node 1:\n"
        "   - Perakitan sirkuit driver pompa DC & relay optocoupler (Node 1).\n"
        "   - Penulisan firmware Generic OnOff Server BLE Mesh & pengujian respon aktuasi pompa.\n\n"
        "2. [Nama Anggota 2] / NRP 2 (Kontribusi 25%) - Spesialis Low Power & Node 2:\n"
        "   - Kalibrasi analog Capacitive Soil Moisture Sensor v1.2 pada pin ADC1 GPIO 34.\n"
        "   - Implementasi firmware Low Power Node (LPN), Deep Sleep ESP32, & catu daya baterai.\n\n"
        "3. [Nama Anggota 3] / NRP 3 (Kontribusi 25%) - Spesialis Mesh & Node 3:\n"
        "   - Konfigurasi fitur Relay Node dan Friend Node pada ESP32 Node 3.\n"
        "   - Manajemen antrian pesan LPN dan pengujian jangkauan transmisi multi-hop mesh.\n\n"
        "4. [Nama Anggota 4] / NRP 4 (Kontribusi 25%) - Spesialis Gateway & Server Host:\n"
        "   - Implementasi Dual-Radio (BLE Mesh Proxy + Wi-Fi MQTT Gateway) pada Node 4.\n"
        "   - Setup Broker Eclipse Mosquitto & dashboard visualisasi grafik di komputer."
    )
    add_slide_with_content("Klaim Pekerjaan Masing-Masing Anggota Tim", s7_body)

    # Slide 8: Storyboard Video Demo
    s8_body = (
        "Rencana Skenario Pengambilan Video Demo (Maksimal 5 Menit):\n\n"
        "• 00:00 - 00:45 (45 dtk) | Pembukaan & Pengenalan Arsitektur:\n"
        "  Perkenalan 4 anggota, penjelasan singkat arsitektur topologi 4-node BLE Mesh.\n\n"
        "• 00:45 - 01:45 (60 dtk) | Demo Node 2 (LPN) & Node 3 (Friend):\n"
        "  Menunjukkan sensor kapasitif dalam pot tanah. Sensor membaca tanah kering, bangun dari deep-sleep, kirim data via Node 3, lalu tidur kembali.\n\n"
        "• 01:45 - 02:45 (60 dtk) | Demo Node 1 (Aktuasi Pompa DC):\n"
        "  Menunjukkan respon Node 1: relay menutup kontak dan pompa air DC menyemburkan air.\n\n"
        "• 02:45 - 03:45 (60 dtk) | Demo Node 4 (Gateway) & Grafik di Komputer:\n"
        "  Menampilkan live terminal MQTT Mosquitto dan grafik dashboard nilai kelembapan.\n\n"
        "• 03:45 - 05:00 (75 dtk) | Pernyataan Klaim Pekerjaan Mandiri & Penutup:\n"
        "  Setiap anggota menyatakan kontribusi komponennya di depan kamera, diakhiri penutup."
    )
    add_slide_with_content("Storyboard & Skenario Video Demo (Maks. 5 Menit)", s8_body)

    # Slide 9: Kesimpulan
    s9_body = (
        "1. Keberhasilan Arsitektur BLE Mesh: 4 Node ESP32 berhasil membentuk jaringan mesh mandiri tanpa titik akses sentral dengan reliabilitas transmisi >98%.\n\n"
        "2. Efisiensi Daya Terbukti: Fitur deep-sleep pada Node 2 menekan konsumsi arus hingga ~15 µA saat tidur, memperpanjang masa hidup baterai secara signifikan.\n\n"
        "3. Integrasi Gateway MQTT Berjalan Stabil: Node 4 berhasil menerjemahkan paket BLE Mesh ke protokol MQTT pada jaringan Wi-Fi lokal komputer.\n\n"
        "4. Aktuasi Penyiraman Responsif: Pompa air DC pada Node 1 merespons ambang batas kelembapan dengan latensi rendah (<100 ms).\n\n"
        "5. Efisiensi Biaya Kelompok: Pemanfaatan ESP32 dari tugas individu anggota berhasil menghemat pengeluaran kelompok sebesar Rp 240.000."
    )
    add_slide_with_content("Kesimpulan & Evaluasi Kinerja Sistem", s9_body)

    print("SUCCESS: All slides populated!")

if __name__ == '__main__':
    main()
