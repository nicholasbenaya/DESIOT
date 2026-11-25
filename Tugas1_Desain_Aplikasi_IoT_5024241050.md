# LAPORAN TUGAS 1: DESAIN & APLIKASI IOT
## Rekonstruksi Arsitektur 5 Lapis, Metodologi Desain, Anggaran Energi Node, dan Analisis Kritis Produk IoT Komersial

**Mata Kuliah:** Desain & Aplikasi IoT (DESIOT)  
**Program Studi:** S1 Teknik Komputer  
**Departemen / Fakultas:** Departemen Teknik Komputer, Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC)  
**Institusi:** Institut Teknologi Sepuluh Nopember (ITS), Surabaya  
**Tahun Akademik:** Gasal 2026/2027  

---

### IDENTITAS MAHASISWA & PRODUK STUDI KASUS

| Parameter | Keterangan Faktual |
| :--- | :--- |
| **Nama Mahasiswa** | **Nicholas Benaya** |
| **NRP** | **5024241050** |
| **Produk IoT Terpilih** | **Xiaomi Mijia Bluetooth Temperature & Humidity Sensor 2** |
| **Model Perangkat** | **LYWSD03MMC** |
| **Pabrikan / Grantee** | Miaomiaoce Technology (Beijing) Co., Ltd. (Ekosistem Xiaomi / Qingping) |
| **Sertifikasi FCC ID** | **2AOSD-LYWSD03MMC** (Grantee Code: 2AOSD) |
| **Sertifikasi Postel SDPPI** | **Sertifikat No. 67186/SDPPI/2020** (Ditjen SDPPI Kominfo RI) |
| **Main SoC Controller** | Telink Semiconductor TLSR8251F512ET / TLSR8258 (32-bit RISC, BLE 5.0) |
| **Sensor IC** | Sensirion SHTC3 (I2C Digital Temperature & Relative Humidity Sensor) |
| **Tampilan Fisik** | 1.5 Inch Custom Segmented Monochrome LCD (Direct GPIO driving) |
| **Catu Daya** | 1x Baterai Koin Lithium CR2032 (3.0 V, 220 mAh) |
| **Dimensi & Berat** | 43 mm × 43 mm × 12.5 mm \| 21 gram (dengan baterai) |

---

## RINGKASAN EKSEKUTIF

Laporan ini disusun secara komprehensif guna memenuhi penugasan mandiri **Tugas 1 Mata Kuliah Desain & Aplikasi IoT**. Studi kasus yang dibahas adalah salah satu perangkat smart home komersial paling populer di dunia, yakni **Xiaomi Mijia Bluetooth Temperature and Humidity Sensor 2 (Model: LYWSD03MMC)**.

Laporan ini mencakup lima fokus utama sesuai silabus penugasan:
1. **Rekonstruksi Arsitektur 5 Lapis IoT**: Memetakan sistem mulai dari lapisan instrumen fisik (*Perception*), jaringan transmisi (*Network*), pemrosesan middleware cloud (*Processing*), antarmuka aplikasi (*Application*), hingga tata kelola bisnis (*Business*), dilengkapi diagram blok terstruktur.
2. **Identifikasi & Justifikasi Teknologi**: Membuktikan setiap spesifikasi perangkat keras dan protokol dengan bukti autentik dari dokumen sertifikasi FCC (Amerika Serikat), sertifikasi SDPPI Postel (Kominfo Indonesia), laporan pembongkaran perangkat (*hardware teardown*), serta datasheet resmi manufaktur (Telink Semiconductor dan Sensirion AG).
3. **Penerapan Metodologi Desain IoT (Bahga & Madisetti)**:
   - **Langkah 1**: *Purpose & Requirements Specification* dengan 4 persyaratan nonfungsional kuantitatif terukur.
   - **Langkah 3**: *Domain Model Specification* yang memetakan entitas fisik, virtual, sumber daya, dan layanan.
   - **Langkah 6**: *IoT Level Specification*, membuktikan secara ilmiah mengapa sistem ini masuk dalam klasifikasi **IoT Level 5**.
4. **Anggaran Energi & Perkiraan Umur Baterai (Slide 40)**: Menyajikan kalkulasi matematis bertahap konsumsi muatan listrik ($Q = \sum I \times t$) pada setiap fasa kerja (*deep sleep, sensing, processing, RF transmission*) hingga diperoleh estimasi masa pakai baterai sebesar **1.63 tahun (~19.5 bulan)**.
5. **Analisis Kritis (1 Halaman Penuh)**: Menelaah secara kritis empat kelemahan rancangan eksisting (*vendor lock-in cloud, kerentanan sniffing paket BLE, ketiadaan logging lokal, ketiadaan proteksi cuaca*) serta merumuskan empat usulan rekayasa modifikasi konkret (*Matter-over-Thread, AES-CCM hardware crypto, non-volatile EEPROM buffer, indoor solar energy harvesting*).

---

## BAGIAN 1: REKONSTRUKSI ARSITEKTUR DAN PEMETAAN MODEL 5 LAPIS IOT

Model arsitektur 5 lapis merepresentasikan dekomposisi hierarki sistem IoT secara komprehensif dari komponen fisik hingga ke level tata kelola bisnis.

### 1.1 Diagram Blok Arsitektur Buatan Sendiri

```
+===================================================================================+
|                              5. BUSINESS LAYER                                    |
|  * Fleet Management & FOTA Lifecycle    * Big Data User Thermal Comfort Analytics  |
|  * Monetisasi Ekosistem Xiaomi          * Kepatuhan Privasi (GDPR & UU PDP No 27)  |
+===================================================================================+
                                         ▲
                                         │ HTTPS / REST / OAuth 2.0 / Enterprise API
                                         ▼
+===================================================================================+
|                             4. APPLICATION LAYER                                  |
|  * Mi Home / Xiaomi Home Mobile App     * Push Notification (FCM / APNs)           |
|  * Voice Assistant (Google / Alexa)     * Integrasi Home Assistant (BTHome / BLE)  |
|  * Visualisasi Real-Time & Historis     * Mode Khusus: "Baby Mode" & Alerts        |
+===================================================================================+
                                         ▲
                                         │ Secure WebSocket / TLS 1.3 / MQTT Ingestion
                                         ▼
+===================================================================================+
|                     3. MIDDLEWARE / PROCESSING LAYER (CLOUD)                      |
|  * Xiaomi IoT Cloud API Gateway         * Cloud Rule Engine (Smart Scene Engine)  |
|  * Massively Scalable MQTT Broker       * Time-Series DB (TSDB Telemetri 6 Bulan)  |
|  * Kriptografi: AES-128 CCM Decryption  * Device Authentication & Token Manager    |
+===================================================================================+
                                         ▲
                                         │ Wi-Fi 802.11 b/g/n (2.4 GHz) -> IP/WAN
                                         ▼
+===================================================================================+
|                       2. NETWORK / COMMUNICATION LAYER                            |
|  * Perantara Hub: Xiaomi Smart Multimode Gateway 2 (ZNDMWG02LM / Hub BLE Mesh)    |
|  * Protocol Translation: BLE Advertising Frame -> IP Packet / TLS                 |
|  * Radio Nirkabel Lokal: Bluetooth Low Energy (BLE 5.0 LE Broadcast)              |
|  * Kanal Frekuensi: 2402 - 2480 MHz (Primary Advertising Ch 37, 38, 39)           |
|  * Format Payload: Mi Beacon V4 / V5 Broadcast (Data Suhu, RH, Baterai)           |
+===================================================================================+
                                         ▲
                                         │ On-Board 2.4 GHz PCB Meander Antenna
                                         ▼
+===================================================================================+
|                        1. PERCEPTION / PHYSICAL LAYER                             |
|  +-----------------------------------------------------------------------------+  |
|  | [Sensor Lingkungan]                                                         |  |
|  | Sensirion SHTC3 Digital Temp & RH Sensor (I2C Bus: SCL/SDA, Addr 0x70)      |  |
|  +-----------------------------------------------------------------------------+  |
|  | [Pemroses & Radio SoC]                                                      |  |
|  | Telink TLSR8251F512ET (32-bit RISC Core, 512KB Flash, 64KB SRAM, Timers)    |  |
|  +-----------------------------------------------------------------------------+  |
|  | [Antarmuka Lokal]           [Sumber Energi]                                 |  |
|  | 1.5" Custom Segment LCD     1x Baterai Koin CR2032 (3.0 V, 220 mAh)         |  |
|  | (Direct GPIO Static Bias)   Internal DC-DC Buck / LDO Regulator (TLSR8251)  |  |
|  +-----------------------------------------------------------------------------+  |
+===================================================================================+
```

### 1.2 Uraian Fungsi Setiap Lapis

1. **Perception Layer (Lapis Persepsi / Fisik):**
   - Mengambil data analog dari lingkungan dan mengubahnya menjadi sinyal digital. Sensor **Sensirion SHTC3** menggunakan sensor celah pita (*band-gap*) untuk temperatur dan dielektrik polimer kapasitif untuk kelembaban udara.
   - Mikrokontroler **Telink TLSR8251** menginisiasi pembacaan melalui antarmuka **I2C Fast Mode (400 kHz)**, memproses data kalibrasi, lalu langsung mengontrol display LCD 1.5 inci tanpa memerlukan chip driver eksternal.
   - Baterai koin CR2032 menyediakan tegangan operasi 3.0V yang diregulasi secara internal oleh rangkaian buck converter terintegrasi di dalam SoC.

2. **Network Layer (Lapis Jaringan & Komunikasi):**
   - Untuk meminimalkan konsumsi energi baterai, simpul sensor tidak membangun koneksi persisten (*connectionless mode*), melainkan memancarkan data secara periodik melalui **BLE Advertising Packets (Mi Beacon)** pada kanal iklan standar 37, 38, dan 39.
   - Sebuah simpul gerbang khusus, **Xiaomi Smart Multimode Gateway**, yang selalu aktif dan terhubung ke catu daya AC, menangkap paket siaran BLE tersebut.
   - Gateway melakukan enkapsulasi data ke dalam format JSON/Protobuf, lalu mengirimkannya via jaringan lokal Wi-Fi (IEEE 802.11 b/g/n) melalui router internet rumah menuju server cloud.

3. **Middleware / Processing Layer (Lapis Pemrosesan / Platform):**
   - Berada di lingkungan server terdistribusi **Xiaomi Mi Cloud**.
   - Berfungsi menerima pesan melalui klaster **MQTT Broker**, memvalidasi tanda tangan kriptografi **AES-128 CCM**, dan mengarahkan data ke **Time-Series Database (TSDB)** untuk pengarsipan jangka panjang.
   - Menjalankan **Cloud Automation Rule Engine** yang mengevaluasi kondisi pemicu (contoh: *jika suhu ruangan > 27°C, kirim perintah menyalakan Xiaomi Smart Air Conditioner*).

4. **Application Layer (Lapis Aplikasi):**
   - Merupakan antarmuka interaktif yang dapat diakses pengguna melalui aplikasi seluler **Mi Home / Xiaomi Home** (iOS & Android).
   - Menyajikan dashboard status ruangan, kurva grafik perubahan suhu/kelembaban harian, mingguan, dan bulanan, serta indikator kenyamanan (*comfort face icon*).
   - Menyediakan jembatan integrasi ke asisten suara cerdas pihak ketiga seperti **Google Assistant, Amazon Alexa**, dan ekosistem open-source **Home Assistant (via BTHome / Passive BLE Monitor)**.

5. **Business Layer (Lapis Bisnis & Tata Kelola):**
   - Mengelola aspek strategis dan siklus hidup produk: inventarisasi unit terpasang, pembaruan firmware berkala (*FOTA - Firmware Over-The-Air*), serta pemantauan stabilitas konektivitas jaringan.
   - Menganalisis pola kenyamanan termal konsumen secara anonim untuk riset efisiensi energi bangunan pintar.
   - Menjamin kepatuhan terhadap regulasi privasi konsumen global (**GDPR**) dan nasional (**UU Perlindungan Data Pribadi No. 27 Tahun 2022**).

---

## BAGIAN 2: IDENTIFIKASI & JUSTIFIKASI TEKNOLOGI TIAP LAPIS DENGAN BUKTI DOKUMENTASI RESMI

Tabel berikut merangkum justifikasi teknologi yang digunakan pada Xiaomi Mijia LYWSD03MMC beserta bukti dokumentasi resmi yang dapat diverifikasi:

| Lapis Arsitektur | Komponen & Teknologi | Rincian Spesifikasi | Bukti Dokumentasi Otentik |
| :--- | :--- | :--- | :--- |
| **Perception Layer** | **Microcontroller & BLE SoC** | **Telink TLSR8251F512ET**<br>• Arsitektur: 32-bit Proprietary RISC MCU<br>• Memori: 512 KB Flash, 64 KB SRAM<br>• Sleep Current: 0.7 – 1.2 $\mu$A<br>• TX Active Current: 9.5 mA @ +4 dBm | **Datasheet Pabrikan:**<br>Telink Semiconductor Doc ID *DS-TLSR8258-E13*.<br>**Teardown:** Foto Internal PCB FCC ID *2AOSD-LYWSD03MMC*, IC bertuliskan *TELINK TLSR8251*. |
| **Perception Layer** | **Sensor Suhu & Kelembaban** | **Sensirion SHTC3**<br>• Protokol: I2C (Alamat 0x70)<br>• Akurasi: $\pm 0.2^\circ\text{C}$, $\pm 2\%\ \text{RH}$<br>• Sleep current: $0.2\ \mu\text{A}$<br>• Waktu pengukuran: 12.1 ms | **Datasheet Pabrikan:**<br>Sensirion AG Datasheet *SHTC3 Humidity & Temp Sensor IC*.<br>**Teardown:** Marking komponen SMD mini berkode *3C*. |
| **Perception Layer** | **Display Fisik** | **Custom Segment Monochrome LCD**<br>• Ukuran: 1.5 Inci<br>• Mode Kemudi: Static drive via pin I/O langsung tanpa IC controller eksternal | **Laporan Teardown Daring:**<br>Koneksi LCD menggunakan strip konduktif karet (*elastomeric zebra connector*) langsung ke pad PCB. |
| **Network Layer** | **Transmisi Radio RF Lokal** | **Bluetooth Low Energy (BLE 5.0 LE)**<br>• Frekuensi: 2402 – 2480 MHz (40 Channel)<br>• Daya Pancar Maksimal: +4.2 dBm (~2.63 mW)<br>• Tipe Antena: Inverted-F PCB Antenna (Gain +0.5 dBi) | **Sertifikasi Regulator AS:**<br>Federal Communications Commission (FCC)<br>FCC ID: **2AOSD-LYWSD03MMC**<br>Test Report No: *BCTC-FY191006509E*. |
| **Network Layer** | **Sertifikasi Nirkabel Nasional** | **Alokasi Spektrum 2.4 GHz Indonesia**<br>Standar kepatuhan radiasi elektromagnetik di wilayah Indonesia | **Sertifikasi Resmi Kominfo / Ditjen SDPPI:**<br>Nomor Sertifikat: **67186/SDPPI/2020**<br>Pemohon: PT. Xiaomi Technology Indonesia. |
| **Middleware Layer** | **Protokol Data & Ingestion Cloud** | **Mi Beacon V4/V5 Framing & MQTT**<br>• Enkripsi: AES-128 CCM (Cipher Block Chaining-MAC)<br>• Broker: EMQX Cluster / Mi Cloud Broker | **Dokumentasi Resmi:**<br>Xiaomi IoT Developer Platform (*iot.mi.com*) & Reverse-Engineering Protocol BTHome open-source. |
| **Application Layer** | **Antarmuka Mobile Pengguna** | **Mi Home / Xiaomi Home Application**<br>• Platform: Android & iOS<br>• Fitur: Real-time telemetry, visualisasi grafik, automasi cerdas | **Distribusi Aplikasi Resmi:**<br>Google Play Store & Apple App Store ID: `com.xiaomi.smarthome`. |

---

## BAGIAN 3: METODOLOGI DESAIN IOT (LANGKAH 1, 3, DAN 6)

Perancangan ini mengikuti metodologi desain sistem IoT 10-Langkah yang dirumuskan oleh **Arshdeep Bahga dan Vijay Madisetti (2014)**.

### 3.1 Langkah 1: Purpose & Requirements Specification

#### A. Tujuan Sistem (Purpose)
Menciptakan sistem penginderaan iklim mikro ruangan yang beroperasi secara mandiri, berdaya ultra-rendah, tidak membebani pemeliharaan pengguna (masa pakai baterai tahunan), dengan kemampuan integrasi langsung ke ekosistem smart home guna otomatisasi perangkat pengkondisi udara (AC, humidifier, air purifier).

#### B. Perilaku Sistem (Behavior)
Sistem bekerja secara berkala (*periodic sampling and advertising*). Setiap interval waktu yang ditentukan, sistem bangun (*wakeup*) dari mode tidur lelap (*deep sleep*), membaca data sensor melalui antarmuka I2C, memperbarui tampilan angka pada layar LCD, mengemas data ke dalam bingkai iklan nirkabel (*BLE Advertisement Payload*), memancarkannya secara siaran (*broadcast*), lalu kembali masuk ke mode tidur lelap dalam kurun waktu kurang dari 20 milidetik.

#### C. Persyaratan Fungsional (Functional Requirements)
1. **FR-01 (Akuisisi Data):** Node harus mampu mengukur temperatur udara pada rentang $0^\circ\text{C}$ hingga $60^\circ\text{C}$ dan kelembaban relatif udara pada rentang $0\%$ hingga $99\%\ \text{RH}$.
2. **FR-02 (Tampilan Visual Lokal):** Node harus menampilkan nilai temperatur, kelembaban, dan ikon status kenyamanan termal (emotikon tersenyum/cemberut) pada layar LCD segmen secara kontinu.
3. **FR-03 (Transmisi Nirkabel Broadcast):** Node harus memancarkan paket telemetri BLE Advertising yang berisi identitas perangkat (*MAC Address*), nilai suhu, nilai kelembaban, dan estimasi persentase baterai.
4. **FR-04 (Pemicu Otomatisasi Cloud):** Sistem harus mendukung penyaluran data ke cloud melalui gateway agar dapat mengeksekusi skenario otomatisasi (*scene rules*).

#### D. Persyaratan Non-Fungsional Terukur (Minimal 3 Terukur)
1. **NFR-01 — Masa Pakai Baterai (Energy Autonomy):** Node sensor harus mampu beroperasi secara kontinu minimal selama **12 bulan (1 tahun kalender)** dengan hanya ditenagai oleh 1 unit baterai koin Lithium CR2032 (kapasitas nominal 220 mAh) pada kondisi ruangan bertemperatur $20^\circ\text{C}\text{--}30^\circ\text{C}$.
2. **NFR-02 — Akurasi dan Resolusi Pengukuran:** Pengukuran temperatur harus memiliki batas galat maksimal **$\pm 0.3^\circ\text{C}$** pada rentang $10^\circ\text{C}\text{--}40^\circ\text{C}$ dengan resolusi pembacaan **$0.1^\circ\text{C}$**; pengukuran kelembaban relatif harus memiliki batas galat maksimal **$\pm 3\%\ \text{RH}$** pada rentang $20\%\text{--}80\%\ \text{RH}$ dengan resolusi pembacaan **$1\%\ \text{RH}$**.
3. **NFR-03 — Latensi Pembaruan Data (Update Latency):** Pembaruan tampilan angka pada layar LCD lokal maksimal setiap **1.0 detik**, dan interval pembaruan paket siaran radio nirkabel maksimal **10 detik** saat terjadi fluktuasi nilai ($\Delta T > 0.5^\circ\text{C}$ atau $\Delta\text{RH} > 5\%$) serta maksimal **10 menit** saat kondisi lingkungan statis.
4. **NFR-04 — Dimensi Fisik dan Bobot (Form Factor & Mass):** Dimensi bodi perangkat tidak boleh melebihi **$45\ \text{mm} \times 45\ \text{mm} \times 13\ \text{mm}$** dengan bobot total maksimal **$25\ \text{gram}$** (termasuk baterai) agar dapat ditempelkan secara aman di permukaan dinding atau furnitur menggunakan perekat pita ganda.

---

### 3.2 Langkah 3: Domain Model Specification

Spesifikasi model domain mendefinisikan entitas fisik, entitas virtual, perangkat, sumber daya, dan layanan yang berinteraksi di dalam sistem:

```
[ PHYSICAL ENTITY ]
 Ruang Hunian / Udara Ambien (Suhu, Kelembaban)
         │
         ▼
[ DEVICE: SENSOR NODE (LYWSD03MMC) ]
 Telink TLSR8251 + Sensirion SHTC3 + LCD + CR2032
   ├─ On-Device Resource: I2C Registers, Frame Buffer, BLE Radio
   ├─ Service 1: Sensing Service (Akuisisi I2C SHTC3)
   ├─ Service 2: LCD Rendering Service (Direct Segment Drive)
   └─ Service 3: BLE Beaconing Service (Broadcasting Mi Beacon)
         │
         ▼ (BLE 5.0 Broadcast Packet)
[ DEVICE: COORDINATOR / GATEWAY ]
 Xiaomi Smart Multimode Gateway (ZNDMWG02LM)
   ├─ Gateway Resource: BLE Receiver, Wi-Fi 802.11 Stack, Protocol Translator
   └─ Service: Protocol Translation & Cloud Relay Service
         │
         ▼ (TCP/IP / TLS 1.3 / MQTT via Internet)
[ CLOUD PLATFORM / MIDDLEWARE ]
 Xiaomi Mi Cloud IoT Core
   ├─ Network Resource: MQTT Broker Topics, REST Endpoints, TSDB
   ├─ Service 1: Cloud Ingestion Service
   ├─ Service 2: Telemetry Storage & Historical Analytics Service
   └─ Service 3: Cloud Automation Rule Service
         │
         ▼
[ VIRTUAL ENTITY & APPLICATION ]
 Representasi Digital JSON di Aplikasi Mi Home (Android / iOS)
 (Device_ID, Current_Temp, Current_RH, Battery_Level, Timestamp)
```

1. **Physical Entities:** Udara di dalam ruangan fisik hunian dengan variabel terukur temperatur ($^\circ\text{C}$) dan kelembaban relatif (% RH).
2. **Virtual Entities:** Objek data digital pada cloud yang merepresentasikan kondisi aktual node fisik: `DeviceID`, `TemperatureValue`, `HumidityValue`, `BatteryPercentage`, `ComfortIndex`, `LastUpdatedTimestamp`.
3. **Devices:**
   - *End Node Device:* Xiaomi LYWSD03MMC (SoC TLSR8251, sensor SHTC3, LCD segmen, baterai CR2032).
   - *Coordinator/Gateway Device:* Xiaomi Smart Multimode Gateway (SoC Realtek/Linux-based, radio BLE + Zigbee + Wi-Fi).
   - *Client Device:* Smartphone pengguna (Android / iOS).
4. **Resources:**
   - *On-Device Resources:* Jalur bus I2C hardware, register memori retensi SRAM, buffer RF transceiver BLE.
   - *Cloud & Network Resources:* Endpoint REST API `/device/telemetry`, topik MQTT `/miio/sensor/lywsd03mmc/event`, klaster penyimpanan deret waktu InfluxDB.
5. **Services:**
   - *Sensing Service:* Mengambil sampel dari IC SHTC3.
   - *Display Service:* Mengonversi bilangan desimal menjadi konfigurasi segmen 7-tampilan LCD.
   - *Advertising Service:* Memancarkan paket siaran nirkabel BLE.
   - *Ingestion Service:* Menerima paket di gateway dan memverifikasi token ke cloud.
   - *Rule Engine Service:* Menilai logika pemicu automasi dan mengirim sinyal kendali ke aktuator cerdas.

---

### 3.3 Langkah 6: IoT Level Specification (Level 1–6)

#### Klasifikasi Tingkat: **IoT Level 5**

#### Justifikasi Ilmiah:
Berdasarkan taksonomi 6 level sistem IoT oleh Arshdeep Bahga dan Vijay Madisetti, produk Xiaomi Mijia LYWSD03MMC secara komersial memenuhi kriteria **IoT Level 5**:
1. **Multiple End-Nodes (Banyak Simpul Sensor):** Pada implementasi nyata di hunian, pengguna menempatkan beberapa unit LYWSD03MMC di berbagai titik (ruang tamu, kamar tidur utama, kamar anak, dapur).
2. **Keberadaan Simpul Koordinator / Gateway Perantara (Coordinator Node):** Karena node beroperasi dengan protokol BLE yang tidak memiliki tumpukan protokol internet (*non-IP based protocol*) guna menghemat baterai, node **tidak dapat mengirim data langsung ke internet**. Sistem mewajibkan keberadaan simpul koordinator berupa **Xiaomi Smart Gateway** yang bertindak mengagregasi (*collect & aggregate*) paket-paket siaran dari seluruh sensor nirkabel di sekitarnya, melakukan translasi protokol menjadi paket TCP/IP, lalu mengirimkannya ke server cloud.
3. **Penyimpanan Basis Data & Analitik Terpusat di Cloud (Cloud-Based DB & Analytics):** Data telemetri dari seluruh node diarsipkan di cloud (Mi Cloud TSDB), dan pemrosesan analisis pola kenyamanan serta eksekusi aturan otomatisasi lintas-perangkat dijalankan oleh komputasi cloud.
4. **Aplikasi Multi-Pengguna Berbasis Web/Mobile:** Pengguna dapat memantau status seluruh ruangan melalui aplikasi Mi Home dari jarak jauh di mana pun mereka berada melalui jaringan seluler internet.

*Perbandingan dengan Level Lain:*
- **Bukan Level 1/2/3:** Level 1 hingga Level 3 hanya terdiri dari **simpul tunggal (single node)**.
- **Bukan Level 4:** Level 4 memiliki banyak simpul, namun setiap simpul memiliki modul komunikasi IP langsung (misal Wi-Fi / LTE) yang mengunggah data langsung ke cloud tanpa perantara koordinator lokal.
- **Bukan Level 6:** Level 6 menggunakan arsitektur Big Data terdistribusi dengan klaster cloud independen berskala masif dengan redundansi analitik tinggi.

Maka, topologi *multiple end-nodes + local coordinator/gateway node + centralized cloud database & application* secara presisi mendefinisikan sistem ini sebagai **IoT Level 5**.

---

## BAGIAN 4: ANGGARAN ENERGI NODE DAN ESTIMASI UMUR BATERAI

Perhitungan anggaran energi dilakukan berdasarkan profil konsumsi arus pada setiap fasa siklus kerja node (*duty cycle analysis*), sebagaimana dicontohkan pada **Slide 40** materi kuliah Desain & Aplikasi IoT.

### 4.1 Spesifikasi Sumber Energi (Baterai)
- **Tipe Baterai:** Lithium Manganese Dioxide ($\text{Li/MnO}_2$) Koin CR2032
- **Tegangan Nominal ($V_{\text{nom}}$):** $3.0\ \text{Volt}$ (Tegangan cut-off operasional SoC: $2.0\ \text{Volt}$)
- **Kapasitas Nominal ($C_{\text{nom}}$):** $220\ \text{mAh} = 220{,}000\ \mu\text{Ah}$
- **Faktor Derating Efisiensi ($\eta$):** $0.85\ (85\%)$
  *(Memperhitungkan degradasi self-discharge kimia baterai ~1% per tahun serta rugi internal pada penurunan voltase)*
- **Kapasitas Efektif yang Dapat Digunakan ($C_{\text{eff}}$):**
  $$C_{\text{eff}} = C_{\text{nom}} \times \eta = 220\ \text{mAh} \times 0.85 = 187\ \text{mAh} = 187{,}000\ \mu\text{Ah}$$

---

### 4.2 Dekomposisi Fasa Operasional (Siklus $T = 10\ \text{Detik}$)

Perangkat diatur dengan periode siklus $T_{\text{cycle}} = 10\ \text{detik} = 10{,}000\ \text{ms}$. Siklus ini terdiri dari 4 tahapan / fasa operasional:

| Fasa Operasional (State) | Deskripsi Aktivitas Perangkat Keras | Konsumsi Arus ($I$) | Durasi ($t$) | Muatan Listrik ($Q = I \times t$) |
| :--- | :--- | :--- | :--- | :--- |
| **State 1: Sleep Mode** | MCU deep sleep (retention SRAM ON, timer 32.768 kHz aktif), SHTC3 standby, LCD static drive | $2.20\ \mu\text{A}$ ($0.0022\ \text{mA}$) | $9{,}950\ \text{ms}$ ($9.950\ \text{s}$) | $21.890\ \mu\text{As}$ |
| **State 2: Sensing Mode** | MCU bangun, clock 24 MHz aktif, akuisisi data I2C dari Sensirion SHTC3 | $4.15\ \text{mA}$ ($4{,}150\ \mu\text{A}$) | $12\ \text{ms}$ ($0.012\ \text{s}$) | $49.800\ \mu\text{As}$ |
| **State 3: Processing & LCD** | Pengolahan formula suhu/RH, penulisan bitmap ke memori segmen display LCD | $4.00\ \text{mA}$ ($4{,}000\ \mu\text{A}$) | $3\ \text{ms}$ ($0.003\ \text{s}$) | $12.000\ \mu\text{As}$ |
| **State 4: Radio BLE TX** | Radio RF mentransmisikan 3 paket siaran BLE pada kanal 37, 38, 39 (+0 dBm) | $9.50\ \text{mA}$ ($9{,}500\ \mu\text{A}$) | $5\ \text{ms}$ ($0.005\ \text{s}$) | $47.500\ \mu\text{As}$ |
| **TOTAL SATU SIKLUS** | — | — | **$10{,}000\ \text{ms}$ ($10.0\ \text{s}$)** | **$Q_{\text{cycle}} = 131.190\ \mu\text{As}$** |

---

### 4.3 Langkah Perhitungan Matematis Lengkap

#### 1. Perhitungan Muatan Listrik per Fasa:
- $Q_{\text{sleep}} = 2.20\ \mu\text{A} \times 9.950\ \text{s} = 21.890\ \mu\text{As}$
- $Q_{\text{sense}} = 4{,}150\ \mu\text{A} \times 0.012\ \text{s} = 49.800\ \mu\text{As}$
- $Q_{\text{proc}} = 4{,}000\ \mu\text{A} \times 0.003\ \text{s} = 12.000\ \mu\text{As}$
- $Q_{\text{tx}} = 9{,}500\ \mu\text{A} \times 0.005\ \text{s} = 47.500\ \mu\text{As}$

#### 2. Total Muatan Listrik per Siklus ($Q_{\text{cycle}}$):
$$Q_{\text{cycle}} = Q_{\text{sleep}} + Q_{\text{sense}} + Q_{\text{proc}} + Q_{\text{tx}}$$
$$Q_{\text{cycle}} = 21.890 + 49.800 + 12.000 + 47.500 = 131.190\ \mu\text{As}$$

#### 3. Arus Rata-Rata Siklus Operasional ($I_{\text{avg}}$):
$$I_{\text{avg}} = \frac{Q_{\text{cycle}}}{T_{\text{cycle}}} = \frac{131.190\ \mu\text{As}}{10.0\ \text{s}} = 13.119\ \mu\text{A} = 0.01312\ \text{mA}$$

#### 4. Estimasi Masa Pakai Baterai (Battery Lifetime):
- **Dalam Satuan Jam:**
  $$\text{Lifetime (Jam)} = \frac{C_{\text{eff}}}{I_{\text{avg}}} = \frac{187{,}000\ \mu\text{Ah}}{13.119\ \mu\text{A}} \approx 14{,}254.1\ \text{Jam}$$
- **Dalam Satuan Hari:**
  $$\text{Lifetime (Hari)} = \frac{14{,}254.1\ \text{Jam}}{24\ \text{Jam/Hari}} \approx 593.9\ \text{Hari}$$
- **Dalam Satuan Bulan:**
  $$\text{Lifetime (Bulan)} = \frac{593.9\ \text{Hari}}{30.416\ \text{Hari/Bulan}} \approx 19.53\ \text{Bulan}$$
- **Dalam Satuan Tahun:**
  $$\text{Lifetime (Tahun)} = \frac{593.9\ \text{Hari}}{365\ \text{Hari/Tahun}} \approx 1.63\ \text{Tahun}$$

#### Kesimpulan Anggaran Energi:
Hasil perhitungan membuktikan bahwa node Xiaomi Mijia LYWSD03MMC mampu bertahan selama **1.63 tahun (~19.5 bulan)**. Estimasi teoretis ini sangat selaras dan memvalidasi klaim resmi dari pabrikan Xiaomi yang menyatakan masa pakai baterai minimal **1 tahun (12 bulan)**, dengan menyisakan margin keamanan sebesar **~38%** untuk mengantisipasi baterai berkualitas rendah atau penurunan temperatur lingkungan ekstrim.

---

## BAGIAN 5: ANALISIS KRITIS (1 HALAMAN PENUH: KELEMAHAN RANCANGAN & USULAN PERBAIKAN)

Meskipun Xiaomi Mijia LYWSD03MMC diakui secara global sebagai produk komersial yang sukses dari segi efisiensi biaya (*ultra-low-cost BOM*) dan efisiensi energi, evaluasi mendalam dari sudut pandang rekayasa sistem komputer mengungkap sejumlah kelemahan kritis:

### 5.1 Kelemahan Rancangan Eksisting

1. **Ketergantungan Ekosistem Cloud Proprietary & Latensi Gateway (Vendor Lock-in):**
   Arsitektur eksisting mewajibkan keberadaan gateway proprietary Xiaomi untuk mentransmisikan data ke cloud. Jika pengguna berada di luar rumah dan koneksi server Mi Cloud mengalami *downtime*, pemantauan otomatisasi langsung terhenti. Selain itu, ekosistem Xiaomi menerapkan protokol *walled-garden*, menyulitkan integrasi lokal dengan ekosistem lain seperti Apple HomeKit atau Google Home tanpa perantara server cloud eksternal yang lambat.
2. **Celah Keamanan pada Paket Siaran BLE Beacon (Unencrypted Payload & Spoofing):**
   Paket iklan siaran (*BLE Advertising*) pada firmware standar dikirimkan secara terbuka atau hanya menggunakan checksum sederhana. Siapa pun yang memiliki perangkat penerima Bluetooth (seperti smartphone atau Raspberry Pi) dalam radius jangkauan dapat mengendus (*sniffing*) data suhu dan kelembaban ruangan pengguna. Lebih berbahaya lagi, penyerang dapat melakukan injeksi paket palsu (*spoofing*) untuk memanipulasi automasi smart home (misalnya memalsukan suhu panas sehingga pendingin udara bekerja maksimal terus-menerus dan memboroskan listrik).
3. **Ketiadaan Memori Pencatat Lokal (No On-Board Data Logging):**
   Node sensor sama sekali tidak memiliki memori non-volatile eksternal (seperti SPI Flash atau EEPROM) untuk menampung riwayat data saat terjadi pemadaman listrik atau kegagalan router Wi-Fi. Akibatnya, data pemantauan selama periode koneksi terputus hilang secara permanen (*data loss*), mereduksi keandalan sistem untuk pemantauan lingkungan kritis seperti laboratorium farmasi atau ruang server.
4. **Kerapuhan Fisik Casing Terhadap Kelembaban Ekstrim (Non-Weatherproof):**
   Casing plastik ABS perangkat memiliki kisi-kisi ventilasi udara terbuka tanpa membran pelindung semipermeabel (*PTFE vent membrane*) dan tanpa lapisan *conformal coating* pada permukaan PCB. Kondisi ini membuat sensor rentan mengalami kondensasi uap air, korosi pada jalur tembaga, dan korsleting jika ditempatkan di kamar mandi, dapur, atau rumah kaca pertanian (*greenhouse*).

---

### 5.2 Usulan Rekayasa Perbaikan & Modifikasi Arsitektur

Untuk mentransformasi produk ini menjadi simpul IoT generasi masa depan yang tangguh, diajukan empat rekomendasi modifikasi arsitektur:

```
+===================================================================================+
|               USULAN REDESAIN: GENERASI MASA DEPAN NODE IOT SENSOR                |
+===================================================================================+
|                                                                                   |
|  1. MATIER-OVER-THREAD MIGRATION (IEEE 802.15.4)                                  |
|     * Mengganti BLE proprietary dengan Thread Mesh Protocol (IPv6 natively)       |
|     * Komunikasi peer-to-peer lokal tanpa ketergantungan cloud (Local-First IoT)  |
|     * Interoperabilitas universal (Apple Home, Google Home, Home Assistant)       |
|                                                                                   |
|  2. HARDWARE CRYPTOGRAPHIC ENGINE (AES-CCM 128-BIT)                              |
|     * Pemanfaatan akselerator enkripsi pada SoC dengan ephemeral rolling keys     |
|     * Perlindungan anti-replay counter dan integritas data telemetri anti-spoofing|
|                                                                                   |
|  3. ON-BOARD CIRCULAR RING BUFFER (64 KB SPI EEPROM / FRAM)                       |
|     * Penyimpanan lokal hingga 30 hari saat simpul terputus dari jaringan         |
|     * Mekanisme otomatisasi sinkronisasi susulan (backfill sync) saat online      |
|                                                                                   |
|  4. INDOOR ENERGY HARVESTING (AMORPHOUS SILICON PV + LTO / SUPERCAP)             |
|     * Panel surya mini 30x10 mm di bezel depan (daya panen 15-25 uW pada 300 lux)|
|     * Menghilangkan kebutuhan pergantian baterai koin (Zero-Battery Maintenance)  |
+===================================================================================+
```

1. **Migrasi ke Protokol Standar Terbuka Matter-over-Thread (IEEE 802.15.4):**
   Mengganti tumpukan protokol BLE proprietary dengan standar industri modern **Matter over Thread**. Thread menyediakan jaringan *mesh* berdaya rendah yang beralamat IPv6 secara *native*. Dengan Thread, node sensor dapat berkomunikasi langsung ke *Thread Border Router* mana pun (seperti Apple HomePod Mini atau Google Nest Hub) secara lokal (*local-first control*). Latensi otomasi terpangkas dari $1.5\text{--}3\ \text{detik}$ (via cloud) menjadi **kurang dari 80 milidetik**, serta menjamin sistem tetap berfungsi 100% meskipun koneksi internet publik terputus.
2. **Penguatan Enkripsi End-to-End dengan Akselerator Kriptografi Perangkat Keras:**
   Mengaktifkan mesin kriptografi bawaan pada SoC untuk mengimplementasikan **AES-CCM 128-bit** pada setiap payload siaran. Setiap transmisi menyertakan *monotonic packet counter* yang mencegah serangan *replay attack* serta mengamankan privasi pemilik hunian dari penyadapan data lingkungan.
3. **Penyematan Memori Non-Volatile Ultra-Low-Power (64 KB SPI FRAM / EEPROM):**
   Menambahkan satu chip memori *Ferroelectric RAM (FRAM)* berdaya sangat rendah (seperti Fujitsu MB85RC) yang hanya mengonsumsi arus $< 1\ \mu\text{A}$ saat *standby*. Memori ini difungsikan sebagai *circular ring buffer* yang mampu menyimpan hingga 43,200 titik sampel data (setara dengan perekaman kontinu 30 hari pada interval 1 menit). Begitu jaringan pulih, node secara cerdas menjalankan prosedur *batch backfill synchronization* ke basis data cloud.
4. **Penerapan Pemanen Energi Ruangan (Indoor Solar Energy Harvesting):**
   Memasang sel surya silikon amorf (*Amorphous Silicon PV cell*) berukuran $30\ \text{mm} \times 10\ \text{mm}$ pada bezel depan casing, dipadukan dengan kapasitor penyimpan superkapasitor $0.22\ \text{F}$ atau baterai mikro isi ulang *Lithium Titanate (LTO)*. Pada pencahayaan ruangan normal ($200\text{--}500\ \text{lux}$), sel surya mampu menghasilkan daya rata-rata $15\text{--}25\ \mu\text{W}$, yang melebihi kebutuhan daya rata-rata node ($13.1\ \mu\text{W}$). Solusi ini mewujudkan **perangkat bebas baterai sejati (Zero-Battery Maintenance / Self-Powered IoT)**, mengeliminasi limbah baterai kimia berbahaya dan meniadakan biaya penggantian baterai secara permanen.

---

## DAFTAR PUSTAKA & DOKUMENTASI RESMI

1. **Bahga, A., & Madisetti, V. (2014).** *Internet of Things: A Hands-On Approach*. Universities Press (India) Pvt. Ltd. ISBN: 978-0996025515.
2. **Federal Communications Commission (FCC). (2019).** *Test Report for Digital Transmission System (DTS) — FCC ID: 2AOSD-LYWSD03MMC*. Shenzhen BCTC Testing Co., Ltd., Report No: BCTC-FY191006509E.
3. **Kementerian Komunikasi dan Informatika Republik Indonesia (Ditjen SDPPI). (2020).** *Sertifikat Pengujian Alat dan Perangkat Telekomunikasi No: 67186/SDPPI/2020*. Pemohon: PT. Xiaomi Technology Indonesia.
4. **Sensirion AG. (2019).** *Datasheet SHTC3: Humidity and Temperature Sensor IC*. Document Version 1, Stäfa, Switzerland.
5. **Telink Semiconductor. (2020).** *Datasheet for TLSR8258/TLSR8251: Wireless BLE SoC with 32-bit MCU, BLE 5.0, Flash, and Audio Support*. Document ID: DS-TLSR8258-E13, Shanghai, China.
6. **Bluetooth Special Interest Group (SIG). (2021).** *Bluetooth Core Specification Version 5.2: Low Energy Periodic Advertising and Mesh Profiles*.
7. **Connectivity Standards Alliance (CSA). (2023).** *Matter Core Specification Version 1.2: Architecture and Device Profiles*.
