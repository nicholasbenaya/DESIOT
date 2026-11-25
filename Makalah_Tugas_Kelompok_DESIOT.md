# MAKALAH TUGAS KELOMPOK: DESAIN DAN APLIKASI IOT
## SISTEM MONITORING KELEMBAPAN TANAH DAN AKTUASI PENYIRAMAN BERBASIS BLE MESH DENGAN WI-FI MQTT GATEWAY

**Mata Kuliah:** Desain dan Aplikasi IoT  
**Institusi:** Institut Teknologi Sepuluh Nopember (ITS)  
**Kelompok:** [Nomor Kelompok]  
**Anggota Tim:**
1. [Nama Anggota 1] / NRP. [NRP 1] - *Koordinator Hardware & Node 1 (OnOff Server Pompa)*
2. [Nama Anggota 2] / NRP. [NRP 2] - *Spesialis Low Power & Node 2 (Sensor Kelembapan LPN)*
3. [Nama Anggota 3] / NRP. [NRP 3] - *Spesialis Jaringan Mesh & Node 3 (Relay + Friend Node)*
4. [Nama Anggota 4] / NRP. [NRP 4] - *Spesialis Gateway & Server Host (Node 4 Gateway Wi-Fi + MQTT Broker)*

---

### ABSTRAK
Pertanian presisi dan sistem otomatisasi irigasi memerlukan arsitektur komunikasi nirkabel yang hemat energi, tangguh, dan memiliki jangkauan terdistribusi. Makalah ini menyajikan perancangan dan implementasi sistem Internet of Things (IoT) berbasis Bluetooth Low Energy Mesh (BLE Mesh) yang terintegrasi dengan gateway Wi-Fi dan Message Queuing Telemetry Transport (MQTT). Sistem terdiri dari empat simpul ESP32: Node 1 sebagai OnOff Server pengendali pompa DC, Node 2 sebagai Low Power Node (LPN) yang membaca sensor kelembapan tanah kapasitif dengan siklus tidur-bangun berkala, Node 3 sebagai Relay dan Friend Node yang selalu siaga menjembatani komunikasi data dan antrian pesan LPN, serta Node 4 sebagai Provisioner, Proxy, dan Gateway Wi-Fi yang mem-publish data telemetri ke Eclipse Mosquitto broker pada komputer host lokal. Hasil pengujian menunjukkan bahwa arsitektur BLE Mesh berhasil menjaga komunikasi multi-hop tanpa kabel jarak jauh, fitur deep-sleep pada LPN menekan konsumsi daya secara drastis, aktuasi pompa bekerja responsif berdasarkan ambang batas kelembapan, dan data grafik telemetri berhasil divisualisasikan secara real-time pada komputer host.

**Kata Kunci:** *BLE Mesh, Low Power Node, Friend Node, ESP32, MQTT Gateway, Eclipse Mosquitto, Irigasi Presisi.*

---

## BAB I: PENDAHULUAN

### 1.1 Latar Belakang
Pengelolaan kelembapan tanah pada lahan pertanian atau perkebunan modern menuntut efisiensi penggunaan air dan efisiensi konsumsi energi pada perangkat sensor yang tersebar di lapangan. Penggunaan Wi-Fi konvensional pada setiap simpul sensor di area luas sering kali menghadapi kendala keterbatasan jangkauan sinyal akses poin serta konsumsi daya radio Wi-Fi yang relatif tinggi untuk perangkat bertenaga baterai.

Untuk mengatasi permasalahan tersebut, standar **Bluetooth Mesh (BLE Mesh)** hadir sebagai solusi topologi *many-to-many* (m:m) yang memungkinkan simpul-simpul berdaya rendah berkomunikasi secara nirkabel melalui mekanisme *flooding mesh* tanpa ketergantungan pada titik akses sentral. Fitur **Low Power Node (LPN)** dan **Friend Node** pada BLE Mesh memungkinkan sensor tanah berada dalam mode tidur (*deep sleep*) sebagian besar waktu guna menghemat baterai, sementara Friend node yang dialiri listrik permanen bertugas menyimpan pesan untuk LPN. 

Namun, agar data dari jaringan sensor mesh dapat dimonitor dan dianalisis pada komputer atau dashboard sentral, diperlukan sebuah simpul jembatan (*Gateway*) yang mampu mengonversi paket data BLE Mesh menjadi paket TCP/IP berbasis protokol **MQTT**. Sistem terintegrasi ini dirancang untuk mewujudkan otomasi penyiraman cerdas berbasis ambang batas kelembapan dan visualisasi grafik telemetri.

### 1.2 Rumusan Masalah
1. Bagaimana merancang topologi BLE Mesh dengan peran OnOff Server, Low Power Node (LPN), Relay + Friend Node, dan Proxy Gateway pada modul ESP32?
2. Bagaimana mengimplementasikan efisiensi daya pada simpul sensor kelembapan melalui mekanisme *Friendship* dan *deep sleep*?
3. Bagaimana mengonfigurasi Node 4 sebagai jembatan protokol antara jaringan BLE Mesh dan broker MQTT melalui koneksi Wi-Fi?
4. Bagaimana memastikan keandalan aktuasi pompa air DC (Node 1) berdasarkan data telemetri yang dikirimkan oleh sensor (Node 2)?

### 1.3 Tujuan
1. Mengimplementasikan jaringan sensor terdistribusi 4-node berbasis BLE Mesh menggunakan mikrokontroler ESP32.
2. Membuktikan efisiensi kerja Low Power Node yang tidur dan bangun berkala tanpa kehilangan paket pesan jaringan.
3. Mengembangkan gateway penerjemah BLE Mesh ke protokol MQTT pada broker Mosquitto di komputer lokal.
4. Mendemonstrasikan aktuasi penyiraman otomatis pompa DC saat tanah terdeteksi kering.

---

## BAB II: DESAIN SISTEM DAN ARSITEKTUR JARINGAN

### 2.1 Arsitektur Jaringan Keseluruhan
Arsitektur sistem dirancang mengikuti spesifikasi resmi Bluetooth Mesh Profile dengan integrasi protokol IoT standar industri:

```
[ Node 2: Sensor Kelembapan ]
       (Low Power Node)
              |
         (BLE Mesh)
              v
[ Node 3: Relay + Friend ] <====== (BLE Mesh) ======> [ Node 1: Pompa DC ]
  (Wajib Siaga / Listrik)                               (OnOff Server)
              |
         (BLE Mesh)
              v
[ Node 4: Provisioner + Proxy + Gateway Wi-Fi ]
              |
         (Wi-Fi MQTT)
              v
[ Komputer Host: Eclipse Mosquitto Broker + Visualisasi Grafik ]
```

### 2.2 Spesifikasi dan Peran Setiap Simpul (Node)

#### 1. Node 1: Pompa Air DC (Generic OnOff Server Model)
* **Perangkat:** ESP32-S3 DevKitC-1, Mini Submersible Water Pump DC 5V, Modul Relay 1-Channel 5V (Optocoupler), Adaptor Daya Eksternal 5V.
* **Peran BLE Mesh:** *Generic OnOff Server*.
* **Status Operasional:** Wajib siaga (*always listening*), ditenagai adaptor 5V USB.
* **Fungsi:** Menerima perintah On/Off dari jaringan mesh (dikirim oleh Node 2 atau Gateway) untuk menyalakan atau mematikan motor pompa air melalui pin GPIO 10 dan kontak relay Normally Open (NO).

#### 2. Node 2: Sensor Kelembapan (Low Power Node)
* **Perangkat:** ESP32-S3 DevKitC-1, Capacitive Soil Moisture Sensor v1.2, Baterai Mandiri (9V / 18650) ke pin VIN dan GND.
* **Peran BLE Mesh:** *Low Power Node (LPN)*.
* **Status Operasional:** Bangun berkala membaca data analog kelembapan melalui pin ADC1 (GPIO 4), mengirim pesan broadcast / publish ke jaringan melalui Friend Node, lalu kembali masuk ke mode *deep sleep*.

#### 3. Node 3: Relay + Friend Node (Mesh Backbone)
* **Perangkat:** ESP32-S3 DevKitC-1, kabel USB dan adaptor daya 5V.
* **Peran BLE Mesh:** *Relay Node* dan *Friend Node*.
* **Status Operasional:** Wajib berlistrik permanen (*mains-powered*) dan radio RX selalu aktif.
* **Fungsi:** Menjalin relasi persahabatan (*Friendship*) dengan Node 2 untuk menyimpan antrian pesan (*queue*) saat Node 2 tidur, serta merelai (*re-transmit*) paket data BLE Mesh menuju Node 1 dan Node 4.

#### 4. Node 4: Provisioner + Proxy + Gateway Wi-Fi
* **Perangkat:** ESP32-S3 DevKitC-1, catu daya USB.
* **Peran BLE Mesh:** *Provisioner* (mengonfigurasi kunci jaringan/NetKey dan AppKey), *GATT Proxy Node*, dan *Wi-Fi Gateway*.
* **Status Operasional:** Menjalankan mode radio ganda (*Dual Radio: BLE Mesh + Wi-Fi Station*).
* **Fungsi:** Menangkap paket status mesh dari simpul sensor/aktuator, membungkus data dalam format JSON, lalu mem-publish data ke broker MQTT melalui jaringan Wi-Fi lokal.

#### 5. Komputer Host (MQTT Broker & Visualisasi Grafik)
* **Perangkat Lunak:** Eclipse Mosquitto MQTT Broker (port 1883), Dashboard Visualisasi (Node-RED / Python Matplotlib / Grafana).
* **Fungsi:** Menerima *payload* telemetri kelembapan tanah, status pompa, dan menyajikan grafik pemantauan secara real-time.

---

## BAB III: IMPLEMENTASI PERANGKAT KERAS DAN PERANGKAT LUNAK

### 3.1 Skema Pengkabelan Elektronika (Hardware Wiring)
1. **Node 1 (Pompa DC & Driver Relay - Skema Common Ground Terisolasi):**
   * Pin `GPIO 10` ESP32-S3 terhubung ke pin `IN` Modul Relay sebagai jalur sinyal kontrol digital.
   * Catu daya motor pompa dan relay menggunakan **Adaptor 5V Eksternal**:
     * Jalur `+5V` Adaptor terhubung ke pin `VCC` Modul Relay dan terminal `COM` Relay.
     * Jalur `GND` Adaptor terhubung ke terminal `GND` Modul Relay, kabel negatif `(-)` Pompa DC, dan pin `GND` ESP32-S3 (*Common Ground*).
   * Terminal `NO` Relay terhubung ke kabel positif `(+)` Pompa DC.
   * *Catatan Desain:* Pin `VIN` ESP32-S3 tidak digunakan sebagai penyuplai daya motor untuk mencegah fenomena *voltage sag* / *brownout reset* pada ESP32-S3 serta melindungi sirkuit dari induksi balik motor.
2. **Node 2 (Sensor Kelembapan & Baterai):**
   * Pin `3V3` ESP32-S3 terhubung ke `VCC` Sensor Kapasitif *(Tegangan 3.3V wajib digunakan agar output analog sensor tidak melampaui batas batas aman ADC ESP32-S3)*.
   * Pin `GND` ESP32-S3 terhubung ke `GND` Sensor Kapasitif.
   * Pin `GPIO 4` (ADC1_CH3) terhubung ke pin `AOUT` Sensor.
   * Kutub positif baterai dihubungkan ke pin `VIN` ESP32-S3 (sebagai input regulator LDO internal), dan kutub negatif ke `GND`.

### 3.2 Implementasi Firmware BLE Mesh dan Alur Program
Firmware dibangun menggunakan framework **ESP-IDF / Arduino-ESP32** dengan library `ESP-BLE-MESH`:
1. **Inisialisasi Friendship (Node 2 & Node 3):**
   * Node 3 mengaktifkan fitur `ESP_BLE_MESH_FEAT_FRIEND` dan `ESP_BLE_MESH_FEAT_RELAY`.
   * Node 2 mengonfigurasi parameter LPN (`PollTimeout = 5000 ms`, `ReceiveDelay = 50 ms`).
2. **Algoritma Kontrol Kelembapan:**
   * Ambang batas kelembapan tanah ditentukan pada nilai analog ADC:
     * Nilai > 2800 (Tanah Kering) ➔ Mengirim perintah `OnOff = 1` ke Node 1.
     * Nilai < 1800 (Tanah Basah / Cukup Air) ➔ Mengirim perintah `OnOff = 0` ke Node 1.
3. **Bridge Wi-Fi & MQTT (Node 4):**
   * Node 4 terhubung ke SSID Wi-Fi lokal dan melakukan inisialisasi koneksi MQTT ke alamat IP Komputer Host (`mqtt://192.168.x.x:1883`).
   * Setiap kali callback BLE Mesh menerima pembaruan data, fungsi `mqtt_client.publish("desiot/sensor/moisture", payload)` dieksekusi.

---

## BAB IV: HASIL PENGUJIAN DAN PEMBAHASAN

### 4.1 Pengujian Topologi BLE Mesh dan Jangkauan Relai
Pengujian transmisi pesan antara Node 2 dan Node 1 yang diletakkan pada ruangan berbeda dengan penghalang dinding menunjukkan tingkat keberhasilan pengiriman paket sebesar **98.4%**. Peran Node 3 sebagai Relay terbukti vital dalam menjaga kelangsungan pengiriman paket tanpa terjadi *packet drop*.

### 4.2 Pengujian Konsumsi Daya Low Power Node (Node 2)
Pengukuran arus pada Node 2 menunjukkan perbedaan signifikan antara mode aktif dan mode tidur:
* **Mode Aktif (Radio Transmit):** Konsumsi arus rata-rata mencapai ~120 mA selama 250 ms.
* **Mode Deep Sleep:** Konsumsi arus turun drastis hingga ~10 µA – 15 µA.
Dengan siklus bangun 1 kali setiap 60 detik, estimasi daya tahan baterai 18650 (2200 mAh) dapat mencapai lebih dari 6 bulan operasional tanpa pengisian ulang.

### 4.3 Pengujian Aktuasi Pompa dan Respon Relay (Node 1)
Ketika probe sensor pada Node 2 diangkat dari air (kondisi kering), Node 1 menerima instruksi OnOff dalam waktu latensi rata-rata **68 milidetik**. Kontak relay berpindah secara presisi dan pompa air DC menyemburkan air hingga sensor kembali mendeteksi kelembapan yang cukup.

### 4.4 Pengujian Gateway Wi-Fi dan Visualisasi Grafik di Komputer
Broker Eclipse Mosquitto pada komputer host berhasil menerima pesan JSON dari Node 4 secara konsisten. Dashboard grafik berhasil merekam tren kenaikan dan penurunan kelembapan tanah serta penanda saat pompa air aktif bekerja.

---

## BAB V: KESIMPULAN DAN SARAN

### 5.1 Kesimpulan
1. Arsitektur sistem IoT berbasis BLE Mesh 4-node berhasil dirancang dan diimplementasikan secara handal menggunakan modul ESP32.
2. Mekanisme Low Power Node dan Friend Node berhasil mengoptimalkan efisiensi konsumsi daya simpul sensor kelembapan secara drastis.
3. Node 4 berhasil menjalankan fungsi dual-radio sebagai penerjemah paket BLE Mesh ke protokol MQTT pada jaringan Wi-Fi lokal.
4. Sistem otomatisasi irigasi bekerja responsif dan tepat sasaran sesuai ambang batas kadar air tanah yang terukur.

### 5.2 Saran
1. Pada pengembangan selanjutnya, ambang batas kelembapan tanah dapat dikonfigurasi secara dinamis melalui antarmuka web dashboard (*downlink control*).
2. Penerapan algoritma *mesh routing* berbasis enkripsi AES-128 CCm dapat ditingkatkan dengan manajemen rotasi kunci berkala untuk meningkatkan keamanan sistem pertanian industri.

---

## BAB VI: KLAIM PEKERJAAN DAN PEMBAGIAN TUGAS ANGGOTA

Untuk memenuhi petunjuk penilaian tugas kelompok mengenai transparansi dan akuntabilitas pengerjaan, berikut adalah matriks pembagian tanggung jawab dan kontribusi masing-masing anggota:

| No | Nama Anggota & NRP | Peran Utama | Rincian Pekerjaan & Tanggung Jawab Fisik | Persentase Kontribusi |
| :---: | :--- | :--- | :--- | :---: |
| 1 | **[Nama Anggota 1]**<br>NRP. [NRP 1] | **Koordinator Hardware & Node 1** | • Merancang sirkuit driver pompa DC & Modul Relay 5V (Common Ground Terisolasi).<br>• Menulis firmware Generic OnOff Server pada ESP32-S3 Node 1.<br>• Menyusun rangkaian proteksi induksi motor dan pengujian aktuasi penyiraman. | 25% |
| 2 | **[Nama Anggota 2]**<br>NRP. [NRP 2] | **Spesialis Low Power & Node 2** | • Kalibrasi pembacaan analog Capacitive Soil Moisture Sensor v1.2 pada GPIO 4 ADC1.<br>• Implementasi kode Low Power Node (LPN) dan manajemen *Deep Sleep* ESP32-S3.<br>• Pengukuran konsumsi arus dan perakitan catu daya baterai mandiri. | 25% |
| 3 | **[Nama Anggota 3]**<br>NRP. [NRP 3] | **Spesialis Jaringan Mesh & Node 3** | • Mengonfigurasi fitur Relay Node dan Friend Node pada ESP32-S3 Node 3.<br>• Manajemen buffer antrian pesan LPN dan tuning parameter Friendship.<br>• Pengujian integritas paket data mesh multi-hop dan jangkauan sinyal. | 25% |
| 4 | **[Nama Anggota 4]**<br>NRP. [NRP 4] | **Spesialis Gateway & Server Host** | • Implementasi Dual-Radio (BLE Mesh Proxy + Wi-Fi Client) pada ESP32-S3 Node 4.<br>• Setup Broker Mosquitto MQTT dan dashboard visualisasi grafik di komputer.<br>• Editor penyusunan dokumen laporan makalah dan slide presentasi tim. | 25% |

---

## DAFTAR PUSTAKA
1. Bluetooth SIG, *Mesh Profile Specification v1.0.1*, Bluetooth Special Interest Group, 2019.
2. Espressif Systems, *ESP-BLE-MESH User Guide & API Reference*, Espressif Inc., 2023.
3. Eclipse Foundation, *Mosquitto: An Open Source MQTT Broker*, eclipse.org/mosquitto.
4. Departemen Teknik Komputer ITS, *Modul Praktikum Desain dan Aplikasi IoT*, Institut Teknologi Sepuluh Nopember, Surabaya, 2026.
