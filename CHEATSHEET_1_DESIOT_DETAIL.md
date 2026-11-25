# CHEATSHEET 1: DESAIN & APLIKASI INTERNET OF THINGS (DESIOT)
## Panduan Komprehensif, Terstruktur, dan Ramah Pemula Berdasarkan Materi Perkuliahan Resmi Teknik Komputer ITS

---

## DAFTAR ISI
1. [Modul 1: Fondasi, Filosofi, dan Arsitektur Sistem IoT](#modul-1-fondasi-filosofi-dan-arsitektur-sistem-iot)
2. [Modul 2: Metodologi Desain Sistem IoT (10 Langkah Bahga & Madisetti)](#modul-2-metodologi-desain-sistem-iot-10-langkah-bahga--madisetti)
3. [Modul 3: Node IoT, Manajemen Energi, dan Karakteristik Sensor](#modul-3-node-iot-manajemen-energi-dan-karakteristik-sensor)
4. [Modul 4: Konektivitas Jarak Pendek (Wi-Fi, Bluetooth LE, dan Zigbee)](#modul-4-konektivitas-jarak-pendek-wi-fi-bluetooth-le-dan-zigbee)
5. [Modul 5: Konektivitas Jarak Jauh (LoRa, LoRaWAN, NB-IoT, dan Seluler)](#modul-5-konektivitas-jarak-jauh-lora-lorawan-nb-iot-dan-seluler)
6. [Matriks Perbandingan & Panduan Keputusan Praktis](#matriks-perbandingan--panduan-keputusan-praktis)

---

## MODUL 1: FONDASI, FILOSOFI, DAN ARSITEKTUR SISTEM IOT

### 1.1 Apa Itu IoT Sebenarnya? (Bukan Sekadar "Benda + Internet")
Banyak orang salah kaprah mengira bahwa memasang modul Wi-Fi pada colokan listrik atau lampu otomatis langsung menjadikannya IoT. Di dunia keteknikan:
* **IoT adalah sistem siklus tertutup (closed-loop system)** berskala besar yang mengumpulkan data dunia fisik, mengirimkannya, menganalisisnya, dan mengambil keputusan atau tindakan aksi nyata secara otomatis tanpa membutuhkan campur tangan manusia setiap saat.
* **Perbedaan Sistem Tertanam (Embedded Systems) vs IoT:**
  * *Sistem Tertanam* melatih Anda merancang **satu perangkat mandiri** (misal: mikrokontroler pengatur suhu AC di kamar).
  * *Desain & Aplikasi IoT* melatih Anda merancang **orkestrasinya**: bagaimana ratusan hingga ribuan perangkat di berbagai tempat berbicara satu sama lain, mengalirkan data ke awan (cloud), dan menjaga sistem tetap hidup selama bertahun-tahun di lingkungan nyata.

### 1.2 Evolusi dari RFID, M2M, hingga AIoT
1. **RFID (1999, Kevin Ashton):** Gagasan awal pelacakan barang manufaktur menggunakan tag nirkabel pasif.
2. **M2M (Machine-to-Machine, era 2000-an):** Komunikasi tertutup antar dua mesin, biasanya menggunakan jaringan kabel industri atau SMS seluler. Sifatnya terisolasi (silo), tidak terintegrasi ke internet terbuka.
3. **IoT (2010-an ke atas):** Komunikasi berbasis standar internet terbuka (IP), perangkat terhubung ke platform cloud, memungkinkan pemantauan masif dan pertukaran data lintas platform.
4. **AIoT (Artificial Intelligence of Things):** Komputasi kecerdasan buatan digeser mendekati fisik (edge computing) sehingga perangkat pintar mampu mengenali anomali atau membuat keputusan cerdas lokal tanpa selalu bergantung pada server cloud.

### 1.3 Empat Sumbu Kompromi Mutlak (Trade-off Matrix)
Di dunia nirkabel, tidak ada satu pun teknologi yang merajai semua keunggulan. Setiap perancang IoT selalu diikat oleh empat sumbu:
1. **Jangkauan (Range):** Seberapa jauh sinyal dapat merambat (meter hingga puluhan kilometer).
2. **Kecepatan Data (Data Rate / Throughput):** Berapa banyak bit yang dapat dikirim per detik.
3. **Konsumsi Daya (Power Consumption):** Seberapa rakus perangkat memakan baterai.
4. **Biaya (Cost):** Biaya komponen perangkat keras serta biaya operasional (seperti langganan pulsa / paket data).

> **Hukum Alam:** Jika Anda ingin jarak tempuh puluhan kilometer dengan baterai kecil yang tahan bertahun-tahun, Anda **wajib merelakan** kecepatan data (hanya bisa mengirim beberapa belas byte per menit, bukan streaming video).

---

### 1.4 Model Arsitektur IoT

#### A. Model 3 Lapis (Arsitektur Klasik)
* **Lapis Persepsi (Perception Layer):** Bagian ujung tombak fisik (sensor suhu, arus listrik, getaran, GPS) dan aktuator (relay, motor, katup).
* **Lapis Jaringan (Network Layer):** Jalur transportasi data (Wi-Fi, Zigbee, LoRa, 4G, kabel Ethernet, router, gateway).
* **Lapis Aplikasi (Application Layer):** Antarmuka visual yang dilihat pengguna (dashboard web, aplikasi Android/iOS, sistem notifikasi).

#### B. Model 5 Lapis (Arsitektur Industri Komprehensif)
Model ini menambahkan dua lapisan krusial yang menjembatani jaringan mentah dengan aplikasi bisnis:
1. **Lapis 1 (Perception):** Penginderaan data fisik dan eksekusi aktuasi mekanik.
2. **Lapis 2 (Network):** Transmisi data nirkabel/kabel dan translasi protokol lokal ke internet.
3. **Lapis 3 (Middleware / Processing):** Jantung pengolahan data di cloud atau server lokal. Bertugas menyimpan basis data berkala (time-series), otentikasi keamanan, komputasi analitik, dan *rule engine* (misal: "jika suhu > 40°C selama 3 menit, kirim alarm").
4. **Lapis 4 (Application):** Antarmuka pengguna (UI/UX), pemantauan visual grafik, dan kontrol jarak jauh.
5. **Lapis 5 (Business Layer):** Analisis nilai ekonomi, manajemen siklus hidup armada perangkat (fleet management), pembaruan firmware jarak jauh (FOTA), kepatuhan privasi (UU PDP / GDPR), dan model monetisasi.

---

### 1.5 Empat Model Komunikasi Data pada IoT

```
1. Request-Response (REST)        2. Publish-Subscribe (MQTT)
   [Klien] ---> Permintaan ---> [Server]   [Penerbit] ---> [Broker] ---> [Pelanggan]
           <---  Jawaban  <---                             (Topik: sensor/suhu)

3. Push-Pull (Antrean Pesan)      4. Exclusive Pair (WebSocket)
   [Produsen] ---> [Antrean Antara]        [Klien] <=================> [Server]
                   ---> [Konsumen 1]            (Koneksi Dua Arah Terbuka Penuh)
                   ---> [Konsumen 2]
```

1. **Request-Response (Contoh: REST API via HTTP/HTTPS):**
   * *Analogi:* Seperti Anda memesan makanan ke pelayan restoran. Anda bertanya/meminta, pelayan menjawab.
   * *Karakteristik:* Klien yang harus selalu berinisiatif. Server bersifat pasif menunggu panggilan. Kurang cocok untuk sensor baterai kecil karena beban pembukaan koneksi (header HTTP) sangat besar.
2. **Publish-Subscribe (Contoh: MQTT):**
   * *Analogi:* Seperti berlangganan majalah melalui kantor pos. Pengirim (publisher) mengirim berita bertopik tertentu ke kantor pos (broker). Pelanggan (subscriber) yang mendaftar pada topik tersebut akan langsung menerima kiriman secara instan.
   * *Karakteristik:* Sangat ringan (overhead header hanya 2 byte), hemat bandwidth, dan memisahkan pengirim dan penerima secara ruang dan waktu.
3. **Push-Pull (Contoh: AMQP, ZeroMQ, Apache Kafka):**
   * *Analogi:* Seperti antrean tiket bioskop. Pengirim memasukkan pesan ke dalam antrean (buffer), dan pekerja di sisi lain mengambil antrean tersebut satu per satu.
   * *Karakteristik:* Menjamin tidak ada data yang hilang saat lalu lintas data mendadak melonjak tinggi (load balancing).
4. **Exclusive Pair (Contoh: WebSocket):**
   * *Analogi:* Seperti panggilan telepon yang terus terhubung. Sekali sambungan terangkat, kedua belah pihak bisa saling bicara kapan saja tanpa perlu memanggil ulang nomor telepon.
   * *Karakteristik:* Komunikasi dua arah (full-duplex) dengan latensi sangat rendah, cocok untuk dashboard pemantauan visual langsung.

---

### 1.6 Enam Tingkatan Sistem IoT (IoT Levels Bahga & Madisetti)

| Tingkatan | Jumlah Node | Lokasi Penyimpanan Data | Lokasi Analisis Komputasi | Lokasi Aplikasi Kontrol | Ketergantungan Awan (Cloud) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Level 1** | Tunggal (1) | Lokal di perangkat | Lokal di perangkat | Lokal di perangkat | **Nol** (Mandiri sepenuhnya) |
| **Level 2** | Tunggal (1) | Cloud (Awan) | Lokal di perangkat | Cloud (Awan) | Rendah (Hanya untuk simpanan) |
| **Level 3** | Tunggal (1) | Cloud (Awan) | Cloud (Awan) | Cloud (Awan) | **Tinggi** (Koma jika internet putus) |
| **Level 4** | Banyak (Multi) | Cloud (Awan) | Cloud (Awan) | Cloud (+ Observer Lokal) | Tinggi |
| **Level 5** | Banyak (Multi) | Cloud (Awan) | Cloud (Awan) | Cloud (+ Koordinator Lokal) | Sedang (Koordinator mengelola lokal) |
| **Level 6** | Banyak (Multi) | Terdistribusi (Cloud + Lokal) | Terdistribusi (Edge + Cloud) | Terdistribusi (Lokal + Cloud) | **Aman** (Kendali kritis jalan mandiri) |

> **Pelajaran Penting (Jebakan Sistem Kendali):** Untuk sistem kritis (seperti pompa air banjir atau rem mesin pabrik), **jangan pernah** memakai Level 3 murni! Jika koneksi internet putus, keputusan mematikan pompa tidak akan pernah sampai dan tangki bisa jebol. Gunakan arsitektur kendali lokal (Level 6 dengan loop keselamatan tertutup) agar saat internet mati, sistem mekanik tetap beroperasi normal.

---

## MODUL 2: METODOLOGI DESAIN SISTEM IOT (10 LANGKAH BAHGA & MADISETTI)

Mengapa metodologi diperlukan? Karena kesalahan paling mahal dalam proyek rekayasa adalah **langsung terburu-buru membeli papan mikrokontroler (hardware)** sebelum memahami apa sebenarnya masalah yang ingin dipecahkan.

```
LANGKAH 1 s.d. 5: ZONA "APA & MENGAPA" (Bebas Merek & Bebas Teknologi)
Langkah 1: Purpose & Requirements   --> Menentukan tujuan dan batasan terukur
Langkah 2: Process Specification     --> Menggambar alur proses kerja sistem
Langkah 3: Domain Model             --> Mengenali benda nyata, alat, dan perannya
Langkah 4: Information Model        --> Menyusun rincian data dan atribut
Langkah 5: Service Specification    --> Menentukan menu layanan data

LANGKAH 6 s.d. 8: ZONA "BAGAIMANA" (Arsitektur Mengikat & Pemilihan Teknologi)
Langkah 6: IoT Level Specification  --> Memilih tingkat kompleksitas (Level 1-6)
Langkah 7: Functional View          --> Mengelompokkan fungsi-fungsi sistem
Langkah 8: Operational View         --> MEMILIH PERANGKAT & PROTOKOL NYATA

LANGKAH 9 & 10: ZONA "PEMBUATAN & IMPLEMENTASI"
Langkah 9: Integration              --> Merakit perangkat keras dan pengkabelan
Langkah 10: Application Dev         --> Menulis kode antarmuka dan aplikasi akhir
```

### Rincian Langkah Kunci:

#### Langkah 1: Kebutuhan Fungsional vs Nonfungsional
* **Kebutuhan Fungsional (Sistem melakukan apa):** "Sistem mendeteksi ketinggian air tangki dan menyalakan pompa saat air surut."
* **Kebutuhan Nonfungsional (Sistem melakukannya sebaik apa):** Inilah yang menentukan proyek Anda berhasil atau gagal di lapangan. Wajib dinyatakan dalam **angka terukur** dan **cara mengujinya**:
  1. *Energi:* Node sensor atap wajib bertahan minimal 12 bulan dengan 1 baterai koin atau panel surya mini.
  2. *Latensi:* Pemutusan darurat pompa saat sumur kering (*dry-run protection*) wajib aktif dalam waktu kurang dari 2 detik.
  3. *Ketersediaan (Availability):* Mode pengisian otomatis wajib tetap berjalan normal minimal 72 jam meskipun koneksi internet kampus mati total.
  4. *Biaya:* Biaya produksi per node tidak boleh melebihi Rp 750.000.

#### Langkah 3: Domain Model (Membedakan Benda Nyata dan Alat)
* **Physical Entity (Entitas Fisik):** Benda nyata di dunia nyata yang kita pedulikan keadaannya (contoh: Air di dalam Tangki Atap Gedung).
* **Virtual Entity:** Data kembaran digital dari tangki tersebut di dalam sistem basis data.
* **Device:** Alat perantara yang dipasang untuk mengetahui kondisi fisik (contoh: Sensor ultrasonik kedap air).
* **Resource:** Potongan kode perangkat lunak di dalam mikrokontroler yang membaca nilai tegangan sensor.
* **Service:** Pintu layanan komunikasi (misal: pengiriman data telemetri lewat topik MQTT).

> **Peringatan Desain:** Tangki adalah *Physical Entity*, sedangkan sensor ultrasonik adalah *Device*. Jangan pernah tertukar!

#### Tiga Anggaran Wajib Sebelum Merakit Perangkat
1. **Anggaran Energi:** Menghitung konsumsi muatan listrik harian ($Q = \sum I \times t$) untuk memastikan baterai sanggup bertahan sesuai target.
2. **Anggaran Latensi:** Memastikan waktu tunda pengiriman pesan tidak membahayakan sistem fisik.
3. **Anggaran Biaya:** Menghitung total biaya perangkat keras ditambah biaya berlangganan cloud/seluler selama siklus hidup perangkat.

---

## MODUL 3: NODE IOT, MANAJEMEN ENERGI, DAN KARAKTERISTIK SENSOR

### 3.1 Profil Arus Kerja Node IoT: Siklus Bangun dan Tidur
Perangkat sensor bertenaga baterai tidak boleh hidup terus-menerus. Ia menerapkan strategi hidup berkala (*duty cycle*):

```
Arus (mA)
  ^
  |        [TX Radio: 120 mA, durasi 0.5 dtk]
  |              +---+
  |   [Ukur:     |   |
  |    10 mA]    |   |
  |     +-+      |   |
  |     | |      |   |
  +-----+ +------+   +--------------------------------------------+  [Deep Sleep: 20 uA, durasi 15 menit]
  +--------------------------------------------------------------------> Waktu
```

1. **Fasa Tidur Lelap (Deep Sleep):** Hampir seluruh sirkuit (CPU, radio nirkabel, sensor) dimatikan total. Hanya ada pewaktu (RTC timer) yang tetap berdetik dengan konsumsi arus sangat mikro (sekitar 10 hingga 20 mikroampere).
2. **Fasa Bangun (Wake-up):** Osilator kristal stabil, CPU kembali mendapat daya listrik.
3. **Fasa Penginderaan (Sensing):** Sensor dinyalakan sesaat, membaca kondisi fisik, lalu mematikan sensor kembali.
4. **Fasa Pemrosesan (Processing):** CPU mengemas data angka ke dalam format biner yang padat.
5. **Fasa Pengiriman Radio (RF Transmission):** Radio nirkabel menyala, mengirim paket data ke udara, lalu segera masuk kembali ke mode tidur lelap.

### 3.2 Rumus Perhitungan Anggaran Energi dan Umur Baterai
1. **Muatan per Siklus ($Q_{\text{siklus}}$):**
   $$Q = (I_{\text{tidur}} \times t_{\text{tidur}}) + (I_{\text{ukur}} \times t_{\text{ukur}}) + (I_{\text{proses}} \times t_{\text{proses}}) + (I_{\text{kirim}} \times t_{\text{kirim}})$$
2. **Arus Rata-Rata ($I_{\text{avg}}$):**
   $$I_{\text{avg}} = \frac{Q_{\text{siklus}}}{t_{\text{total\_siklus}}}$$
3. **Estimasi Umur Baterai ($T$):**
   $$T = \frac{\text{Kapasitas Baterai Terpakai (mAh)}}{I_{\text{avg}} \text{ (mA)} \times 24 \text{ jam} \times 365 \text{ hari}}$$

### 3.3 Jebakan Papan Development vs Papan Produksi Nyata
Banyak mahasiswa terkejut saat membaca datasheet mikrokontroler (misal: ESP32 tertulis memiliki arus *deep sleep* hanya 10-15 µA), namun saat menguji papan modul *NodeMCU* atau *DevKit* dengan baterai, baterainya habis hanya dalam beberapa hari!
* **Penyebab Kebocoran:**
  1. *Regulator Tegangan LDO Murah (misal AMS1117):* Memiliki arus bocor pasif (*quiescent current*) sebesar 5 hingga 10 mA terus-menerus meskipun ESP32 sedang tertidur lelap!
  2. *Chip Jembatan USB-ke-Serial (CP2102 / CH340):* Tetap mendapat aliran daya dari jalur rel 3.3V dan terus memakan daya 10-15 mA.
  3. *Lampu LED Indikator Daya:* Sebuah LED merah kecil yang menyala terus menyedot arus 2 hingga 5 mA tanpa henti.
* **Solusi Industri:** Gunakan papan produksi kustom dengan regulator berefisiensi tinggi (*ultra-low quiescent LDO* < 1 µA), copot chip konverter USB, dan matikan LED daya.

### 3.4 Baterai Bukan Tangki Air (Fakta Fisik Kimia Baterai)
* **Resistansi Internal ($R_{\text{int}}$):** Begitu radio nirkabel menyala dan mendadak menarik arus besar (misal 150 mA), terjadi lonjakan penurunan tegangan internal ($\Delta V = I \times R_{\text{int}}$). Jika tegangan jatuh di bawah ambang batas kerja mikrokontroler (*brownout reset*), perangkat akan langsung restart sebelum sempat mengirim data.
* **Penuaan dan Suhu Panas:** Suhu lingkungan yang panas (seperti sensor di atap seng) meningkatkan laju *self-discharge* (kehilangan energi sendiri) dan mempercepat degradasi kimia baterai.

### 3.5 Karakteristik Sensor, Kalibrasi, dan Fusi Data
* **Akurasi vs Presisi:** Akurasi adalah seberapa dekat nilai ukur ke nilai kebenaran acuan. Presisi adalah seberapa konsisten nilai ukur saat diulang berkali-kali.
* **Penyimpangan Nilai (Drift):** Pergeseran nilai bacaan akibat penuaan komponen atau fluktuasi suhu lingkungan.
* **Metode Kalibrasi:**
  * *1 Titik (Zero Offset):* Menggeser garis ke atas atau ke bawah agar titik nol pas.
  * *2 Titik (Offset + Span/Gain):* Mengatur titik nol dan titik skala penuh (kemiringan garis).
  * *Multi-Titik:* Mengompensasi ketidaklinearan kurva respons sensor.
* **Metadata Wajib:** Sebuah angka sensor tanpa label konteks adalah data yang tidak berguna atau bahkan membahayakan. Setiap paket data wajib menyertakan: ID Perangkat, Tanda Waktu (Timestamp UTC), Satuan Ukur, dan Status Kesehatan Baterai/Sensor.

### 3.6 Prinsip Emas: "Mencuplik Murah, Mengirim Radio Itu Sangat Mahal"
Daya listrik yang dihabiskan untuk satu kali memancarkan gelombang radio setara dengan daya untuk membaca sensor sebanyak **208 kali lipat**. Karena itu, strategi cerdas menghemat daya adalah:
1. **Deadband Reporting:** Sensor hanya mengirim data jika perubahannya melebihi ambang batas tertentu (misal: suhu naik lebih dari 0.5°C). Jika kondisi stabil, jangan memancar!
2. **Local Edge Aggregation:** Mengambil sampel tiap detik, menghitung rata-rata dan nilai ekstrem secara lokal di memori RAM, lalu hanya mengirim ringkasan tiap 10 menit sekali.
3. **Adaptive Sampling:** Saat kondisi normal, cuplik tiap 15 menit. Saat terdeteksi laju perubahan cepat (anomali), tingkatkan frekuensi cuplikan secara otomatis.

---

## MODUL 4: KONEKTIVITAS JARAK PENDEK (WI-FI, BLUETOOTH LE, DAN ZIGBEE)

### 4.1 Teorema Shannon-Hartley & Anggaran Daya Tautan (Link Budget)
Mengapa sinyal melemah saat merambat di udara?
* **Teorema Shannon:** Kapasitas informasi maksimal ($C$) berbanding lurus dengan lebar pita frekuensi ($B$) dan rasio daya sinyal terhadap derau ($SNR$):
  $$C = B \log_2 (1 + \text{SNR})$$
* **Link Budget (Kekuatan Sinyal Penerima):**
  $$P_{\text{rx}} = P_{\text{tx}} + G_{\text{tx}} + G_{\text{rx}} - \text{PathLoss} - \text{Margin}$$
  Agar data dapat dibaca oleh penerima, daya sinyal yang sampai ($P_{\text{rx}}$) **wajib lebih besar** daripada batas kepekaan penerima (*receiver sensitivity*).
* **Frekuensi 2.4 GHz vs Sub-GHz (misal 920 MHz):**
  * Frekuensi tinggi (2.4 GHz) membawa data lebih banyak dan cepat, tetapi sangat mudah diredam oleh dinding beton, kaca, dan dedaunan pohon.
  * Frekuensi rendah (Sub-GHz) memiliki panjang gelombang lebih besar, mampu membelok di sekitar rintangan (difraksi), dan memiliki daya tembus material fisik yang jauh lebih unggul.

---

### 4.2 Wi-Fi (IEEE 802.11)
* **Kelebihan:** Kecepatan transfer data sangat tinggi (puluhan hingga ratusan Mbps), infrastruktur Access Point (AP) sudah ada di mana-mana, langsung terhubung ke jaringan internet IP tanpa perlu penerjemah protokol khusus.
* **Kelemahan:** Sangat boros daya listrik (arus aktif 100-300 mA), proses asosiasi dan jabat tangan (*handshake DHCP/WPA2*) memakan waktu lama (beberapa detik), sehingga mustahil beroperasi bertahun-tahun hanya dengan baterai koin kecil.

---

### 4.3 Bluetooth Low Energy (BLE)
* **Konsep:** Dirancang bukan untuk memutar audio musik berjam-jam (itu tugas Bluetooth Classic), melainkan untuk menyemburkan paket data kecil secara kilat lalu segera kembali tidur.
* **Mekanisme Advertising (Kanal 37, 38, 39):**
  BLE menyiarkan paket data kecil pada tiga kanal frekuensi khusus yang diletakkan di antara celah frekuensi Wi-Fi untuk menghindari tabrakan sinyal. Ponsel pintar atau gateway dapat membaca data suhu ruangan langsung dari paket siaran (*beacon frame*) tanpa perlu repot melakukan proses *pairing* yang rumit!
* **GATT (Generic Attribute Profile):** Struktur data hierarkis di dalam perangkat BLE yang terdiri atas *Profile*, *Service*, dan *Characteristic* (tempat nilai data disimpan).

---

### 4.4 Zigbee (IEEE 802.15.4) & Jaringan Mesh
Jika jarak jangkauan Wi-Fi dan Bluetooth terbatas hanya 10 hingga 30 meter dalam ruangan, bagaimana menghubungkan sensor di gedung 4 lantai? Jawabannya adalah **Jaringan Jala (Mesh Network)**.

```
                  [Coordinator (ZC)]
                   (Pusat Jaringan)
                         |
           +-------------+-------------+
           |                           |
      [Router 1 (ZR)]             [Router 2 (ZR)]
      (Wajib Colok Listrik)       (Wajib Colok Listrik)
           |                           |
     +-----+-----+                     |
     |           |                     |
[End Device] [End Device]        [End Device (ZED)]
(Tidur, Baterai) (Tidur, Baterai)  (Tidur, Baterai)
```

* **Tiga Peran Node dalam Zigbee:**
  1. **Zigbee Coordinator (ZC):** Sangat cerdas, bertugas membuka jaringan pertama kali, menyimpan kunci keamanan, hanya ada 1 per jaringan, dan **wajib dicolok listrik terus-menerus**.
  2. **Zigbee Router (ZR):** Bertindak sebagai estafet pesan yang meneruskan paket data dari tetangganya ke koordinator. Karena harus siap mendengar kapan saja ada paket yang lewat, router **tidak boleh tidur dan wajib dicolok listrik AC**.
  3. **Zigbee End Device (ZED):** Node ujung berupa sensor bertenaga baterai. Boleh tidur lelap sepanjang hari dan hanya bangun saat ingin menitipkan data ke router induknya.

---

## MODUL 5: KONEKTIVITAS JARAK JAUH (LORA, LORAWAN, NB-IOT, DAN SELULER)

### 5.1 Rahasia Teknologi LoRa: Membaca Sinyal di Bawah Derau (Noise)
LoRa (Long Range) adalah modulasi radio fisik yang menggunakan teknik **Chirp Spread Spectrum (CSS)**: frekuensi sinyal disapu secara bertahap dari rendah ke tinggi (seperti suara kicauan burung).
* **Processing Gain:** Melalui penyebaran kode simbol, penerima LoRa sanggup mendeteksi dan mendekode sinyal radio yang kekuatannya **20 dB di bawah derau lingkungan** (daya sinyal hanya seperseratus dari derau latar belakang!).
* **Spreading Factor (SF7 hingga SF12):**
  Spreading Factor adalah tuas kompromi matematis yang bisa diatur oleh perancang sistem:

| Spreading Factor (SF) | Kecepatan Bit | Waktu Pancar di Udara (Airtime 50 B) | Sensitivitas Penerima | Jangkauan Sinyal | Konsumsi Energi Baterai |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **SF7** | Tertinggi (~5.5 kbps) | Sangat Cepat (~0.098 detik) | Standar (-123 dBm) | Sedang (2 - 4 km) | **Paling Hemat** |
| **SF8** | Sedang (~3.1 kbps) | 2x lipat dari SF7 | Lebih Sensitif | Menengah | Sedang |
| **SF10** | Rendah (~0.98 kbps) | Lambat (~0.616 detik) | Sangat Kuat | Jauh | Boros |
| **SF12** | **Paling Rendah (~0.25 kbps)** | **Sangat Lambat (~2.302 detik)** | **Ekstrem (-137 dBm)** | **Paling Jauh (hingga >10 km)** | **Paling Boros (23x lipat SF7)** |

> **Pelajaran Penting:** LoRa bukanlah teknologi yang hemat energi karena fisika radionya (pada SF12, energi satu kali kirim LoRa memakan 371 kali energi pengiriman Zigbee!). Yang membuat LoRaWAN hemat energi adalah arsitekturnya: sensor hanya memancar sangat jarang dan tidur sepanjang sisa waktu.

---

### 5.2 LoRa vs LoRaWAN & Arsitektur Star-of-Stars
* **LoRa:** Lapisan fisik perangkat keras radio (modulasi gelombang di udara).
* **LoRaWAN:** Protokol jaringan dan kontrol akses media (MAC) yang mengatur alamat perangkat, enkripsi data dua lapis (Network Key dan App Key), serta manajemen server.
* **Topologi Jaringan:** LoRaWAN tidak menggunakan jala (mesh), melainkan **Bintang-ke-Bintang (Star-of-Stars)**. Semua node sensor langsung menyemburkan paket data ke udara, dan seluruh gateway di sekitar yang menangkap paket tersebut akan meneruskannya lewat kabel internet IP ke Server Jaringan terpusat (*Network Server*).

```
[Node Sensor 1] \
[Node Sensor 2] ---> (( [Gateway LoRaWAN] )) ---> [Internet / IP] ---> [Network Server] ---> [App Server]
[Node Sensor 3] /
```

---

### 5.3 Tiga Kelas Perangkat LoRaWAN
1. **Kelas A (All / Paling Hemat Daya):**
   * Perangkat hanya mendengarkan jika ia baru saja selesai memancarkan data (uplink). Setelah memancar, ia membuka 2 jendela penerimaan (*receive windows* RX1 dan RX2) selama beberapa milidetik, lalu tidur lelap. Server tidak bisa menghubungi node jika node tidak bangun sendiri. **Wajib didukung oleh semua perangkat LoRaWAN.**
2. **Kelas B (Beacon / Terjadwal):**
   * Gateway memancarkan sinyal penanda waktu (*beacon*) secara berkala. Node bangun pada jadwal slot waktu yang telah disepakati untuk membuka jendela dengar. Cocok untuk meteran air pintar yang butuh diperintah sekali sehari.
3. **Kelas C (Continuous / Selalu Mendengarkan):**
   * Jendela penerima radio dibuka terus-menerus tanpa henti (hanya mati saat sedang memancar). Sangat boros listrik, sehingga **wajib dicolok ke sumber listrik PLN** (contoh: lampu penerangan jalan umum pintar).

---

### 5.4 Regulasi Hukum Frekuensi di Indonesia (SDPPI Kominfo)
Di Indonesia, penggunaan frekuensi radio diatur secara ketat oleh regulasi resmi:
* **Alokasi Frekuensi Legal:** **920 hingga 923 MHz** (Standar wilayah LoRaWAN AS923-2).
* **Peringatan Keras:** Toko daring sering menjual modul murah varian 868 MHz (standar Eropa) dan 915 MHz (standar Amerika). Mengoperasikan kedua frekuensi ini di Indonesia adalah **ilegal** dan dapat mengganggu frekuensi operator telekomunikasi seluler resmi.
* **Batasan Siklus Kerja (Duty Cycle 1%):**
  Untuk pita frekuensi tanpa izin (*unlicensed band*), hukum menetapkan batas penggunaan pemancar maksimal 1%. Artinya, jika modul Anda memancar selama 1 detik, modul Anda **wajib diam mematikan radio selama minimal 99 detik**!
  * *Dampak Nyata:* Mengirim data tiap 30 detik pada SF12 adalah tindakan yang **melanggar hukum**, karena waktu pancar 50 byte pada SF12 membutuhkan 2.3 detik (sehingga jeda wajibnya adalah 228 detik atau hampir 4 menit).

---

### 5.5 Jaringan Seluler IoT (NB-IoT & LTE-M) vs Sigfox
* **NB-IoT (Narrowband IoT):** Menumpang pada pita frekuensi berlisensi milik operator seluler (Telkomsel, Indosat, XL). Keunggulannya: daya tembus ke dalam ruang bawah tanah (basement) sangat baik (+20 dB) dan tidak perlu repot merawat gateway sendiri. Menggunakan fitur hemat daya khusus:
  * *PSM (Power Saving Mode):* Node sensor "menghilang" dari jaringan operator selama berjam-jam/hari tanpa perlu registrasi ulang.
  * *eDRX (extended Discontinuous Reception):* Node hanya memeriksa panggilan jaringan pada jeda waktu yang jauh lebih renggang dibanding ponsel biasa.
* **LTE-M (eMTC):** Bandwidth lebih besar (hingga 1 Mbps), mendukung kecepatan gerak tinggi (*handover* antar menara BTS tanpa putus) dan panggilan suara, cocok untuk pelacak kontainer logistik atau ambulans.
* **Sigfox:** Teknologi *Ultra-Narrowband (UNB)* yang sangat kikir (hanya 140 pesan per hari, masing-masing maksimal 12 byte). Infrastrukturnya tertutup milik perusahaan operator tunggal Sigfox.

---

## MATRIKS PERBANDINGAN & PANDUAN KEPUTUSAN PRAKTIS

### Matriks Perbandingan 7 Teknologi Konektivitas IoT

| Teknologi | Jangkauan Khas | Laju Data | Konsumsi Energi per Laporan | Kebutuhan Infrastruktur | Biaya Operasional Berjalan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Wi-Fi** | ~30 - 50 m | Sangat Tinggi (>10 Mbps) | Sangat Boros (~100 µAh) | Access Point (AP) Lokal | Gratis (Infrastruktur lokal) |
| **BLE** | ~10 - 30 m | Cepat (~1 Mbps) | Sangat Hemat (~0.008 µAh) | Smartphone / Gateway BLE | Gratis |
| **Zigbee** | 30 m per hop (Mesh) | Cukup (~250 kbps) | Sangat Hemat (~0.083 µAh) | Node Router Berlistrik AC | Gratis |
| **LoRa (P2P)** | 2 - 10 km | Sangat Kikir (<5 kbps) | Sedang (~1.6 - 31 µAh) | Cukup 2 Modul Radio | Gratis |
| **LoRaWAN** | 2 - 15 km | Sangat Kikir (<5 kbps) | Sedang (~1.6 - 31 µAh) | Gateway LoRaWAN + Server | Gratis (Jika bangun gateway sendiri) |
| **NB-IoT** | Nasional (BTS) | Rendah (~26 - 127 kbps) | Sedang-Hemat | Menara Operator Seluler | Berbayar (Langganan SIM Card per bulan) |
| **LTE-M** | Nasional (BTS) | Cukup (~1 Mbps) | Cukup Boros | Menara Operator Seluler | Berbayar (Langganan SIM Card per bulan) |

---

### Alur 6 Pertanyaan Penentu Pemilihan Teknologi (Decision Flowchart)
Jawablah enam pertanyaan ini secara berurutan saat merancang proyek:
1. **Berapa jarak titik sensor terjauh ke titik berlistrik/internet terdekat?**
   * Jika $> 100\text{ meter}$ tanpa ada dinding perantara, maka seluruh teknologi jarak pendek (Wi-Fi, BLE, Zigbee) **gugur**. Anda wajib beralih ke LPWAN atau Seluler.
2. **Apakah ada bangunan atau colokan listrik di antara titik-titik sensor?**
   * Jika tidak ada, teknologi jaringan jala (*Zigbee Mesh*) **gugur** karena router tidak memiliki sumber listrik konstan.
3. **Berapa ukuran paket data dan seberapa sering data harus dikirim?**
   * Jika data $> 1\text{ kB}$ per laporan atau interval kirim $< 1\text{ menit}$, seluruh teknologi LPWAN (LoRaWAN, Sigfox) **gugur** karena menabrak aturan hukum *Duty Cycle 1%*.
4. **Apakah perangkat harus bisa diperintah dari server sewaktu-waktu secara instan?**
   * Jika ya, maka LoRaWAN Kelas A **gugur**. Anda harus memakai LoRaWAN Kelas C (wajib colok listrik) atau modul seluler.
5. **Berapa banyak node sensor dan berapa lama sistem direncanakan hidup?**
   * Jika jumlah node ratusan dan digunakan bertahun-tahun di area privat (kebun/kampus), membangun gateway LoRaWAN sendiri jauh lebih hemat daripada membayar biaya langganan kartu SIM seluler bulanan untuk tiap perangkat.
6. **Siapa yang akan memelihara perangkat setelah diserahkan?**
   * Jika dirawat oleh masyarakat awam (bukan insinyur), hindari sistem yang membutuhkan perawatan server lokal yang rumit. Gunakan teknologi yang transparan dan andal.

---
*Dibuat khusus untuk penguasaan materi mata kuliah Desain dan Aplikasi IoT (DESIOT) Departemen Teknik Komputer FTEIC ITS.*
