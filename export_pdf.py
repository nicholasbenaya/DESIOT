import os
import subprocess
import re

html_content = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Rencana Kebutuhan Alat dan Bahan - Desain dan Aplikasi IoT</title>
<style>
  @page {
    size: A4 portrait;
    margin: 10mm 14mm 10mm 14mm;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    font-size: 8.5pt;
    line-height: 1.38;
    color: #1e293b;
    background: #ffffff;
  }

  /* Header */
  .doc-header {
    border-bottom: 2px solid #0284c7;
    padding-bottom: 6px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .doc-header .title-area h1 {
    font-size: 13.5pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.3px;
    text-transform: uppercase;
  }
  .doc-header .title-area .subtitle {
    font-size: 8.8pt;
    color: #0284c7;
    font-weight: 600;
    margin-top: 1px;
  }
  .doc-header .meta-area {
    text-align: right;
    font-size: 7.8pt;
    color: #64748b;
    line-height: 1.3;
  }

  /* Section Styles */
  .section-title {
    font-size: 9.8pt;
    font-weight: 700;
    color: #0f172a;
    margin-top: 8px;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    border-left: 3.5px solid #0284c7;
    padding-left: 7px;
    background: #f1f5f9;
    padding-top: 3px;
    padding-bottom: 3px;
    border-radius: 0 4px 4px 0;
  }

  p {
    margin-bottom: 5px;
    color: #334155;
    font-size: 8.2pt;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 7px;
    font-size: 7.9pt;
  }
  th {
    background-color: #e2e8f0;
    color: #0f172a;
    font-weight: 700;
    text-align: left;
    padding: 4.5px 7px;
    border: 1px solid #cbd5e1;
  }
  td {
    padding: 4px 7px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }
  tr:nth-child(even) td {
    background-color: #f8fafc;
  }

  /* Badges & Tags */
  .badge {
    display: inline-block;
    padding: 1.5px 5px;
    border-radius: 3px;
    font-size: 6.8pt;
    font-weight: 700;
    white-space: nowrap;
  }
  .badge-blue { background: #e0f2fe; color: #0369a1; }
  .badge-green { background: #dcfce7; color: #15803d; }
  .badge-amber { background: #fef3c7; color: #b45309; }
  .badge-purple { background: #f3e8ff; color: #7e22ce; }

  /* Callout box */
  .callout {
    background-color: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 3.5px solid #22c55e;
    border-radius: 5px;
    padding: 8px 10px;
    margin-bottom: 8px;
  }
  .callout-title {
    font-weight: 700;
    color: #166534;
    font-size: 8.5pt;
    margin-bottom: 3px;
  }
  .callout ul {
    margin-left: 16px;
    color: #1e293b;
    font-size: 7.9pt;
  }
  .callout li {
    margin-bottom: 3px;
  }

  .page-break {
    page-break-before: always;
    break-before: page;
  }

  /* Node Card Grid */
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    margin-bottom: 6px;
  }
  .card {
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 6px 8px;
    background: #ffffff;
  }
  .card-title {
    font-weight: 700;
    font-size: 8.2pt;
    color: #0f172a;
    margin-bottom: 2px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .card-desc {
    font-size: 7.4pt;
    color: #475569;
    line-height: 1.25;
  }
  .card-items {
    margin-top: 4px;
    font-size: 7.4pt;
    color: #0f172a;
    border-top: 1px dashed #e2e8f0;
    padding-top: 3px;
  }

  .footer-note {
    font-size: 7.2pt;
    color: #94a3b8;
    text-align: center;
    margin-top: 10px;
    border-top: 1px solid #f1f5f9;
    padding-top: 5px;
  }
</style>
</head>
<body>

  <!-- HEADER -->
  <div class="doc-header">
    <div class="title-area">
      <h1>Rencana Kebutuhan Alat dan Bahan</h1>
      <div class="subtitle">Mata Kuliah: Desain dan Aplikasi IoT - Institut Teknologi Sepuluh Nopember (ITS)</div>
    </div>
    <div class="meta-area">
      <div><strong>Topik:</strong> BLE Mesh & Cloud IoT</div>
      <div><strong>Fokus:</strong> Analisis Anti-Redundansi Komponen</div>
    </div>
  </div>

  <p>
    Dokumen ini menyajikan rincian alat, bahan, dan perangkat lunak untuk menyelesaikan dua penugasan praktikum IoT: 
    <strong>Tugas Kelompok</strong> (Arsitektur 4-Node BLE Mesh terintegrasi Gateway Wi-Fi MQTT) dan <strong>Tugas Individu</strong> 
    (Telemetri Sensor ESP32 ke Blynk & ThingSpeak), dilengkapi strategi pembagian belanja agar tidak terjadi pemborosan komponen.
  </p>

  <!-- BAGIAN 1: TUGAS KELOMPOK -->
  <div class="section-title">1. Kebutuhan Tugas Kelompok (Arsitektur BLE Mesh & Gateway MQTT)</div>
  <p>
    Sistem tugas kelompok terdiri dari 4 simpul berbasis <strong>ESP32</strong> dalam jaringan <strong>Bluetooth Mesh (BLE Mesh)</strong>, 
    di mana Node 4 berfungsi sebagai gateway Wi-Fi menuju broker MQTT (Mosquitto) pada komputer lokal:
  </p>

  <div class="grid-2">
    <div class="card">
      <div class="card-title">
        <span>Node 1: Pompa DC</span>
        <span class="badge badge-amber">OnOff Server</span>
      </div>
      <div class="card-desc">Wajib siaga menerima perintah On/Off. Menyalakan pompa air DC saat ada instruksi mesh.</div>
      <div class="card-items">
        <strong>Komponen:</strong> ESP32, Mini Submersible Water Pump DC 3-5V, Driver (Modul Relay 5V / MOSFET), Selang mini.
      </div>
    </div>

    <div class="card">
      <div class="card-title">
        <span>Node 2: Sensor Kelembapan</span>
        <span class="badge badge-green">Low Power Node</span>
      </div>
      <div class="card-desc">Membaca kelembapan secara berkala (tidur & bangun berkala). Bergantung pada Friend Node saat sleep.</div>
      <div class="card-items">
        <strong>Komponen:</strong> ESP32, Capacitive Soil Moisture Sensor v1.2 (atau DHT11/22), Baterai (18650 / Li-Po) + Holder.
      </div>
    </div>

    <div class="card">
      <div class="card-title">
        <span>Node 3: Relay + Friend</span>
        <span class="badge badge-blue">Relay & Friend Node</span>
      </div>
      <div class="card-desc">Jembatan komunikasi mesh yang wajib berlistrik terus-menerus untuk melayani LPN dan meneruskan paket.</div>
      <div class="card-items">
        <strong>Komponen:</strong> ESP32, Kabel USB + Adaptor 5V (wajib selalu aktif/standby).
      </div>
    </div>

    <div class="card">
      <div class="card-title">
        <span>Node 4: Provisioner & Proxy</span>
        <span class="badge badge-purple">Gateway Wi-Fi</span>
      </div>
      <div class="card-desc">Mengatur provisi jaringan mesh, bertindak sebagai Proxy BLE, serta jembatan protokol ke Wi-Fi MQTT.</div>
      <div class="card-items">
        <strong>Komponen:</strong> ESP32, Kabel USB, Akses Wi-Fi Access Point / Hotspot lokal.
      </div>
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Komponen / Alat</th>
        <th style="width: 10%;">Jumlah</th>
        <th style="width: 42%;">Spesifikasi & Fungsi</th>
        <th style="width: 23%;">Estimasi Harga</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>ESP32 DevKit Board</strong></td>
        <td>4 Unit</td>
        <td>ESP32 30/38 pin (Node 1, Node 2, Node 3, Node 4). Mendukung BLE Mesh & Wi-Fi.</td>
        <td>Rp 50.000 - Rp 65.000 / unit</td>
      </tr>
      <tr>
        <td><strong>Capacitive Soil Moisture Sensor</strong></td>
        <td>1 Unit</td>
        <td>Sensor kelembapan tanah analog v1.2 (Node 2). Anti-korosi dibanding resistif.</td>
        <td>Rp 10.000 - Rp 18.000</td>
      </tr>
      <tr>
        <td><strong>Pompa Air DC Mini</strong></td>
        <td>1 Unit</td>
        <td>Mini Submersible DC Pump 3V - 5V (Node 1) untuk demonstrasi penyiram.</td>
        <td>Rp 15.000 - Rp 25.000</td>
      </tr>
      <tr>
        <td><strong>Modul Relay 1-Channel / MOSFET</strong></td>
        <td>1 Unit</td>
        <td>Relay 5V optocoupler / Modul Switch MOSFET (Penggerak pompa dari GPIO ESP32).</td>
        <td>Rp 8.000 - Rp 15.000</td>
      </tr>
      <tr>
        <td><strong>Baterai + Holder (Opsional LPN)</strong></td>
        <td>1 Set</td>
        <td>Baterai 18650 3.7V + holder (Demonstrasi portabel Low Power Node 2).</td>
        <td>Rp 20.000 - Rp 35.000</td>
      </tr>
      <tr>
        <td><strong>Kabel Jumper & Breadboard</strong></td>
        <td>1-2 Set</td>
        <td>Kabel Jumper Male-Female, Male-Male, Breadboard 400 titik untuk perakitan.</td>
        <td>Rp 20.000 - Rp 30.000</td>
      </tr>
      <tr>
        <td><strong>PC / Komputer Host</strong></td>
        <td>1 Unit</td>
        <td>Menjalankan Mosquitto MQTT Broker dan Dashboard grafik (Node-RED/Grafana).</td>
        <td>- (Milik Pribadi)</td>
      </tr>
    </tbody>
  </table>

  <!-- BAGIAN 2: TUGAS INDIVIDU -->
  <div class="section-title">2. Kebutuhan Tugas Individu (ESP32 + Blynk + ThingSpeak)</div>
  <p>
    Tugas individu mensyaratkan 1 simpul ESP32 membaca sensor, mengirim telemetry ke Blynk Mobile App, 
    dan mencatat data historis ke platform cloud ThingSpeak.
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Komponen / Alat</th>
        <th style="width: 10%;">Jumlah</th>
        <th style="width: 42%;">Spesifikasi & Fungsi</th>
        <th style="width: 23%;">Estimasi Harga</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>ESP32 DevKit Board</strong></td>
        <td>1 Unit</td>
        <td>Mikrokontroler utama terhubung ke sensor dan Wi-Fi internet.</td>
        <td>Rp 50.000 - Rp 65.000</td>
      </tr>
      <tr>
        <td><strong>Sensor</strong></td>
        <td>1 Unit</td>
        <td>Bebas. Disarankan: DHT11/DHT22 (suhu/kelembapan) atau Soil Moisture Sensor.</td>
        <td>Rp 12.000 - Rp 25.000</td>
      </tr>
      <tr>
        <td><strong>Kabel Data USB</strong></td>
        <td>1 Unit</td>
        <td>Micro-USB / Type-C (untuk upload program dari laptop & power).</td>
        <td>- (Bawaan HP / Rp 10.000)</td>
      </tr>
      <tr>
        <td><strong>Breadboard Mini & Jumper</strong></td>
        <td>Secukupnya</td>
        <td>Breadboard 170/400 titik + kabel jumper Female-to-Male (3-4 kabel).</td>
        <td>Rp 10.000 - Rp 15.000</td>
      </tr>
      <tr>
        <td><strong>Aplikasi Blynk & ThingSpeak</strong></td>
        <td>Akun Free</td>
        <td>Blynk IoT Mobile App (Android/iOS) + MathWorks ThingSpeak Channel.</td>
        <td>Gratis (Free Tier)</td>
      </tr>
    </tbody>
  </table>

  <!-- PAGE BREAK -->
  <div class="page-break"></div>

  <!-- BAGIAN 3: ANALISIS ANTI-REDUNDANSI -->
  <div class="section-title">3. Analisis Komponen Sama & Strategi Anti-Redundansi</div>
  <p>
    Untuk menghemat pengeluaran secara maksimal dan menghindari pembelian ganda, manfaatkan irisan kebutuhan antara tugas individu dan tugas kelompok berikut:
  </p>

  <div class="callout">
    <div class="callout-title">💡 STRATEGI PENGHEMATAN BIAYA ANGGARAN KELOMPOK:</div>
    <ul>
      <li>
        <strong>ESP32 Tidak Perlu Dibeli Terpisah untuk Kelompok:</strong> Tugas kelompok membutuhkan 4 ESP32. Jika 1 kelompok beranggotakan 4 mahasiswa, 
        setiap anggota cukup membeli 1 ESP32 untuk tugas individunya masing-masing. Saat tugas kelompok, gabungkan ke-4 ESP32 tersebut! 
        <em>(Menghemat anggaran kelompok sebesar Rp 200.000 - Rp 260.000).</em>
      </li>
      <li>
        <strong>Gunakan Sensor Kelembapan untuk Tugas Individu:</strong> Tugas individu membebaskan jenis sensor. Jika anggota kelompok memilih 
        sensor kelembapan (Soil Moisture atau DHT11/22), sensor tersebut dapat langsung dipasang ke Node 2 saat pengerjaan tugas kelompok tanpa perlu membeli sensor baru lagi.
      </li>
      <li>
        <strong>Kabel Jumper dan Breadboard Dibagi Pakai:</strong> 1 paket kabel jumper isi 40 helai sudah sangat mencukupi kebutuhan 4 anggota individu 
        sekaligus perakitan tugas kelompok.
      </li>
      <li>
        <strong>Infrastruktur Komputer & Internet:</strong> Hotspot HP 2.4 GHz dan laptop yang dipakai untuk menguji Blynk/ThingSpeak dapat langsung 
        berperan sebagai host broker MQTT (Mosquitto) dan penampil grafik di tugas kelompok.
      </li>
    </ul>
  </div>

  <!-- BAGIAN 4: CHECKLIST PEMBAGIAN BELANJA -->
  <div class="section-title">4. Checklist Pembagian Pengadaan (Individu vs Patungan)</div>
  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Kategori</th>
        <th style="width: 45%;">Item yang Harus Dibeli</th>
        <th style="width: 30%;">Penanggung Jawab Biaya</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Beli Mandiri (Individu)</strong></td>
        <td>
          • 1x ESP32 Dev Board<br>
          • 1x Sensor (Disarankan Sensor Kelembapan / DHT)<br>
          • 1x Kabel USB Data
        </td>
        <td>Masing-masing mahasiswa (digunakan untuk tugas individu, lalu digabungkan ke kelompok).</td>
      </tr>
      <tr>
        <td><strong>Patungan Bersama (Kelompok)</strong></td>
        <td>
          • 1x Pompa Air DC 5V Mini<br>
          • 1x Modul Relay 1-Channel 5V / Modul MOSFET<br>
          • 1x Pack Kabel Jumper campur (M-M, M-F)<br>
          • 1m Selang Air kecil & baterai holder (jika diperlukan)
        </td>
        <td>Kas / Patungan seluruh anggota kelompok (Estimasi total: ± Rp 40.000 - Rp 60.000 / kelompok).</td>
      </tr>
    </tbody>
  </table>

  <!-- BAGIAN 5: CATATAN TEKNIS -->
  <div class="section-title">5. Catatan Teknis Penting untuk Praktikum</div>
  <ul style="margin-left: 20px; font-size: 8.1pt; color: #334155; line-height: 1.55;">
    <li>
      <strong>Isolasi Daya Motor Pompa (Node 1):</strong> Motor DC induktif menghasilkan <em>back-EMF</em> (lonjakan arus balik) saat mati mendadak. 
      Gunakan modul relay yang dilengkapi optocoupler atau pasang dioda flyback (1N4007) jika merangkai driver transistor sendiri agar ESP32 tidak mudah restart / rusak.
    </li>
    <li>
      <strong>Konfigurasi Low Power Node (Node 2):</strong> ESP-BLE-MESH mendukung fitur LPN (Low Power Node). Node 2 harus diprogram menjalin 
      relasi persahabatan (<em>Friendship</em>) dengan Node 3 (Friend Node). Dengan begitu, Node 2 dapat masuk mode deep-sleep tanpa kehilangan pesan jaringan.
    </li>
    <li>
      <strong>Konektivitas Node 4 (Gateway):</strong> Node 4 mengoperasikan BLE Mesh dan Wi-Fi secara simultan. Pastikan alokasi memori heap ESP32 
      mencukupi karena stack BLE Mesh + Wi-Fi MQTT membutuhkan RAM yang cukup besar pada ESP-IDF/Arduino-ESP32.
    </li>
    <li>
      <strong>Frekuensi Wi-Fi:</strong> ESP32 hanya mendukung pita Wi-Fi <strong>2.4 GHz</strong>. Pastikan hotspot laptop atau smartphone Anda tidak disetel hanya pada pita 5 GHz saat pengujian Blynk, ThingSpeak, dan MQTT.
    </li>
  </ul>

  <div class="footer-note">
    Dokumen dibuat secara otomatis untuk referensi praktikum Desain dan Aplikasi IoT - Departemen Teknik Komputer / Teknik Elektro ITS.
  </div>

</body>
</html>
"""

html_file = 'kebutuhan_alat_dan_bahan_iot.html'
pdf_file = 'Kebutuhan_Alat_dan_Bahan_IoT.pdf'

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
html_path = os.path.abspath(html_file)
pdf_path = os.path.abspath(pdf_file)

cmd = [
    chrome_path,
    '--headless=new',
    '--disable-gpu',
    '--no-pdf-header-footer',
    f'--print-to-pdf={pdf_path}',
    html_path
]

res = subprocess.run(cmd, capture_output=True, text=True)

with open(pdf_path, 'rb') as f:
    pdf_bytes = f.read()

pages = re.findall(rb'/Type\s*/Page\b', pdf_bytes)
print('PDF Generation Result:')
print('Page count:', len(pages))
print('File size:', len(pdf_bytes), 'bytes')
print('PDF Path:', pdf_path)
