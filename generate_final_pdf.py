import os
import subprocess
import re

html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Panduan Pengadaan & Skema Rangkaian IoT - ITS</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 10mm 13mm 10mm 13mm;
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  body {{
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    font-size: 8.2pt;
    line-height: 1.38;
    color: #1e293b;
    background: #ffffff;
  }}

  /* Header */
  .doc-header {{
    border-bottom: 2.5px solid #0284c7;
    padding-bottom: 6px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}
  .doc-header .title-area h1 {{
    font-size: 13.5pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.3px;
    text-transform: uppercase;
  }}
  .doc-header .title-area .subtitle {{
    font-size: 8.8pt;
    color: #0284c7;
    font-weight: 600;
    margin-top: 1px;
  }}
  .doc-header .meta-area {{
    text-align: right;
    font-size: 7.6pt;
    color: #64748b;
    line-height: 1.3;
  }}

  /* Section Styles */
  .section-title {{
    font-size: 9.5pt;
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
  }}

  p {{
    margin-bottom: 5px;
    color: #334155;
    font-size: 8pt;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 7px;
    font-size: 7.8pt;
  }}
  th {{
    background-color: #e2e8f0;
    color: #0f172a;
    font-weight: 700;
    text-align: left;
    padding: 4px 6px;
    border: 1px solid #cbd5e1;
  }}
  td {{
    padding: 4px 6px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }}
  tr:nth-child(even) td {{
    background-color: #f8fafc;
  }}

  /* Badges & Tags */
  .badge {{
    display: inline-block;
    padding: 1.5px 5px;
    border-radius: 3px;
    font-size: 6.8pt;
    font-weight: 700;
    white-space: nowrap;
  }}
  .badge-ready {{ background: #dcfce7; color: #15803d; border: 1px solid #86efac; }}
  .badge-pending {{ background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }}

  /* Callout box */
  .callout {{
    background-color: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 3.5px solid #22c55e;
    border-radius: 5px;
    padding: 7px 9px;
    margin-bottom: 7px;
  }}
  .callout-title {{
    font-weight: 700;
    color: #166534;
    font-size: 8.3pt;
    margin-bottom: 2px;
  }}
  .callout ul {{
    margin-left: 15px;
    color: #1e293b;
    font-size: 7.7pt;
  }}
  .callout li {{
    margin-bottom: 2px;
  }}

  /* Offline Store Card */
  .store-box {{
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 3.5px solid #0284c7;
    border-radius: 5px;
    padding: 6px 9px;
    margin-bottom: 7px;
  }}
  .store-title {{
    font-weight: 700;
    color: #0369a1;
    font-size: 8.2pt;
    margin-bottom: 2px;
  }}

  .page-break {{
    page-break-before: always;
    break-before: page;
  }}

  a {{
    color: #0284c7;
    text-decoration: underline;
    font-weight: 600;
  }}

  .circuit-img {{
    width: 100%;
    max-height: 220mm;
    object-fit: contain;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    margin-top: 6px;
    margin-bottom: 6px;
  }}

  .footer-note {{
    font-size: 7pt;
    color: #94a3b8;
    text-align: center;
    margin-top: 8px;
    border-top: 1px solid #f1f5f9;
    padding-top: 4px;
  }}
</style>
</head>
<body>

  <!-- ==================== HALAMAN 1 ==================== -->
  <div class="doc-header">
    <div class="title-area">
      <h1>Panduan Pengadaan & Skema Rangkaian IoT</h1>
      <div class="subtitle">Desain dan Aplikasi IoT - Institut Teknologi Sepuluh Nopember (ITS) Surabaya</div>
    </div>
    <div class="meta-area">
      <div><strong>Fokus:</strong> Link Shopee, Alternatif Offline & Skema Wiring</div>
      <div><strong>Status:</strong> Dokumen Siap Cetak / Referensi Praktikum</div>
    </div>
  </div>

  <div class="section-title">1. Status Checklist Inventaris Alat dan Bahan</div>
  <table>
    <thead>
      <tr>
        <th style="width: 32%;">Nama Komponen / Alat</th>
        <th style="width: 12%;">Status</th>
        <th style="width: 36%;">Peruntukan & Alokasi Sistem</th>
        <th style="width: 20%;">Catatan Tindak Lanjut</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>4x ESP32 Dev Board</strong></td>
        <td><span class="badge badge-ready">READY ✅</span></td>
        <td>Node 1 (Pompa), Node 2 (Sensor), Node 3 (Relay/Friend), Node 4 (Gateway).</td>
        <td>Gabungan board tugas individu anggota.</td>
      </tr>
      <tr>
        <td><strong>Kabel Jumper + Breadboard 1-2 set</strong></td>
        <td><span class="badge badge-ready">READY ✅</span></td>
        <td>Wiring prototipe modul dan antarmuka sensor/aktuator.</td>
        <td>Cukup dibagi pakai antar anggota.</td>
      </tr>
      <tr>
        <td><strong>PC / Laptop</strong></td>
        <td><span class="badge badge-ready">READY ✅</span></td>
        <td>Host Broker Mosquitto MQTT, visualisasi grafik, dan upload code.</td>
        <td>Gunakan satu laptop kelompok saat demo.</td>
      </tr>
      <tr>
        <td><strong>1x Capacitive Soil Moisture Sensor</strong></td>
        <td><span class="badge badge-pending">BELUM ⏳</span></td>
        <td>Node 2: Sensor pembaca kelembapan tanah (Low Power Node).</td>
        <td>Perlu dibeli (Online / Offline).</td>
      </tr>
      <tr>
        <td><strong>1x Pompa Air DC Mini (3-5V)</strong></td>
        <td><span class="badge badge-pending">BELUM ⏳</span></td>
        <td>Node 1: Aktuator penyiram air otomatis (OnOff Server).</td>
        <td>Perlu dibeli (Patungan Kelompok).</td>
      </tr>
      <tr>
        <td><strong>1x Modul Relay 1-CH / MOSFET</strong></td>
        <td><span class="badge badge-pending">BELUM ⏳</span></td>
        <td>Node 1: Saklar penggerak motor DC pompa dari pin GPIO ESP32.</td>
        <td>Perlu dibeli (Patungan Kelompok).</td>
      </tr>
      <tr>
        <td><strong>1x Baterai + Holder (Opsional LPN)</strong></td>
        <td><span class="badge badge-pending">BELUM ⏳</span></td>
        <td>Node 2: Catu daya portabel mandiri saat mode deep sleep.</td>
        <td>Perlu dibeli / Pakai alternatif.</td>
      </tr>
    </tbody>
  </table>

  <div class="section-title">2. Detail Komponen yang Perlu Dibeli (Link Shopee & Alternatifnya)</div>
  <table>
    <thead>
      <tr>
        <th style="width: 24%;">Komponen Target</th>
        <th style="width: 28%;">Tautan Shopee & Estimasi</th>
        <th style="width: 32%;">Opsi Alternatif Toko Offline / Lebih Murah</th>
        <th style="width: 16%;">Cara Pasang / Catatan</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          <strong>Capacitive Soil Moisture Sensor v1.2</strong><br>
          <span style="font-size:7pt; color:#64748b;">Sensor kelembapan tanah</span>
        </td>
        <td>
          🛒 <a href="https://shopee.co.id/search?keyword=capacitive%20soil%20moisture%20sensor%20v1.2" target="_blank">Link Shopee: Capacitive Sensor</a><br>
          <strong>Kisaran:</strong> Rp12.000 - Rp18.000
        </td>
        <td>
          <strong>1. Sensor Kelembapan Resistif (YL-69 / FC-28):</strong> Banyak di toko offline, harga ~Rp7.000.<br>
          <strong>2. Sensor Suhu & Kelembapan DHT11/22:</strong> Jika diizinkan kelembapan udara.
        </td>
        <td>
          VCC ke 3.3V, GND ke GND, AOUT ke GPIO 34 (ADC1 ESP32).
        </td>
      </tr>
      <tr>
        <td>
          <strong>Pompa Air DC Mini 5V Submersible</strong><br>
          <span style="font-size:7pt; color:#64748b;">Pompa celup air mini</span>
        </td>
        <td>
          🛒 <a href="https://shopee.co.id/search?keyword=pompa%20air%20dc%20mini%20submersible%205v" target="_blank">Link Shopee: Pompa DC Mini 5V</a><br>
          <strong>Kisaran:</strong> Rp15.000 - Rp22.000
        </td>
        <td>
          <strong>1. Pompa DC 5V USB:</strong> Kabel USB tinggal dipotong/colok.<br>
          <strong>2. Pompa DC 12V:</strong> Bekas dispenser/akuarium (+ catu 12V).<br>
          <strong>3. LED / Buzzer:</strong> Uji coba logika On/Off awal.
        </td>
        <td>
          Wajib celup air. Kutub (+) ke Output Relay, (-) ke GND.
        </td>
      </tr>
      <tr>
        <td>
          <strong>Modul Relay 1-Channel 5V / MOSFET</strong><br>
          <span style="font-size:7pt; color:#64748b;">Driver isolasi beban induktif</span>
        </td>
        <td>
          🛒 <a href="https://shopee.co.id/search?keyword=modul%20relay%201%20channel%205v" target="_blank">Link Shopee: Relay 1-CH 5V</a><br>
          🛒 <a href="https://shopee.co.id/search?keyword=modul%20mosfet%20dc" target="_blank">Link Shopee: Modul MOSFET</a><br>
          <strong>Kisaran:</strong> Rp7.000 - Rp14.000
        </td>
        <td>
          <strong>Rangkaian Transistor NPN (~Rp4.000):</strong><br>
          • 1x Transistor NPN (TIP120 / BD139 / 2N2222)<br>
          • 1x Dioda 1N4007 (Flyback diode)<br>
          • 1x Resistor 1kΩ
        </td>
        <td>
          Pin IN ke GPIO 23. NO/COM memutus kutub (+) pompa. Dioda membuang tegangan back-EMF.
        </td>
      </tr>
      <tr>
        <td>
          <strong>Baterai 18650 + Holder</strong><br>
          <span style="font-size:7pt; color:#64748b;">Power portabel Node 2 LPN</span>
        </td>
        <td>
          🛒 <a href="https://shopee.co.id/search?keyword=baterai%2018650%20dan%20holder%201%20slot" target="_blank">Link Shopee: Baterai 18650 + Holder</a><br>
          <strong>Kisaran:</strong> Rp18.000 - Rp30.000 total
        </td>
        <td>
          <strong>1. Baterai Kotak 9V + Kancing (Rp15.000):</strong> Di Indomaret/Alfamart.<br>
          <strong>2. Holder 3x Baterai AA (4.5V):</strong> Toko mainan/listrik.<br>
          <strong>3. Power Bank via Port USB:</strong> Milik pribadi.
        </td>
        <td>
          Kutub (+) baterai ke **VIN** ESP32, (-) ke **GND**. IC AMS1117 ESP32 aman meregulasi tegangan.
        </td>
      </tr>
    </tbody>
  </table>

  <!-- ==================== HALAMAN 2 ==================== -->
  <div class="page-break"></div>

  <div class="section-title">3. Rekomendasi Toko Elektronika Offline Terdekat (Area Kampus ITS Surabaya)</div>
  <p>Untuk kebutuhan komponen mendesak tanpa menunggu pengiriman online:</p>

  <div class="store-box">
    <div class="store-title">📍 1. Robotech Shop Surabaya (Paling Dekat Kampus ITS)</div>
    <div style="font-size:7.6pt; color:#334155; line-height:1.35;">
      <strong>Lokasi:</strong> Jl. Gebang Wetan No. 24, Sukolilo, Surabaya (Tepat di samping barat kampus ITS, bisa jalan kaki).<br>
      <strong>Stok:</strong> Modul relay, sensor kelembapan tanah, pompa DC mini 5V, kancing baterai 9V, kabel jumper, resistor, dan aneka sensor IoT.
    </div>
  </div>

  <div class="store-box">
    <div class="store-title">📍 2. CNC Store Surabaya / Toko CNC</div>
    <div style="font-size:7.6pt; color:#334155; line-height:1.35;">
      <strong>Lokasi:</strong> Wilayah Nginden Semolo / Jl. Semolowaru (Sekitar 10-15 menit berkendara dari kampus ITS).<br>
      <strong>Stok:</strong> Modul ESP32 lengkap, sensor kapasitif v1.2, modul MOSFET switch, step-down, dan baterai holder.
    </div>
  </div>

  <div class="store-box">
    <div class="store-title">📍 3. Pasar Genteng Besar Surabaya (Lantai 2 - Pusat Grosir Komponen)</div>
    <div style="font-size:7.6pt; color:#334155; line-height:1.35;">
      <strong>Lokasi:</strong> Jl. Genteng Besar, Surabaya Pusat.<br>
      <strong>Stok:</strong> Toko komponen elektronik satuan terlengkap (transistor TIP120, dioda 1N4007, baterai, relay, selang mini) dengan harga grosir.
    </div>
  </div>

  <div class="section-title">4. Alokasi Pembagian Biaya Pengadaan (Checklist Efisiensi)</div>
  <div class="callout">
    <div class="callout-title">💡 STRATEGI PENGHEMATAN BIAYA ANGGARAN:</div>
    <ul>
      <li><strong>ESP32 (4 Unit):</strong> Masing-masing anggota kelompok cukup membeli 1 ESP32 untuk tugas individu mereka. Saat tugas kelompok dimulai, ke-4 ESP32 tersebut digabungkan menjadi 4 Node. Kelompok hemat hingga <strong>Rp 240.000</strong>.</li>
      <li><strong>Sensor:</strong> 1 anggota memilih sensor kelembapan untuk tugas individunya, sehingga sensor tersebut langsung menjadi Node 2 di tugas kelompok tanpa membeli ulang.</li>
      <li><strong>Komponen Patungan:</strong> Kelompok hanya perlu membiayai pompa air DC mini, modul relay, dan selang air mini dengan total patungan hanya sekitar <strong>Rp 35.000 - Rp 45.000 per kelompok</strong> (± Rp 10.000 / orang).</li>
    </ul>
  </div>

  <!-- ==================== HALAMAN 3 ==================== -->
  <div class="page-break"></div>

  <div class="section-title">5. Skema Rangkaian Elektronika & Topologi: Tugas Kelompok</div>
  <p>Diagram visual di bawah ini mengilustrasikan wiring pinout hardware untuk masing-masing Node (Node 1 Pompa, Node 2 Sensor, Node 3 Relay/Friend, dan Node 4 Gateway MQTT) serta topologi interkoneksi BLE Mesh:</p>
  
  <img class="circuit-img" src="rangkaian_tugas_kelompok.png" alt="Skema Rangkaian Tugas Kelompok">

  <div class="footer-note">
    Gambar 1: Wiring Pinout dan Arsitektur Jaringan BLE Mesh 4-Node terhubung ke Komputer Host (Mosquitto MQTT Broker).
  </div>

  <!-- ==================== HALAMAN 4 ==================== -->
  <div class="page-break"></div>

  <div class="section-title">6. Skema Rangkaian Elektronika & Alur Data: Tugas Individu</div>
  <p>Diagram visual di bawah ini mengilustrasikan perkabelan antara Node ESP32 dengan sensor, serta aliran data nirkabel menuju dashboard mobile Blynk dan analitik cloud ThingSpeak:</p>

  <img class="circuit-img" src="rangkaian_tugas_individu.png" alt="Skema Rangkaian Tugas Individu">

  <table style="margin-top: 10px;">
    <thead>
      <tr>
        <th style="width: 25%;">Pin Sensor (DHT / Soil)</th>
        <th style="width: 25%;">Pin ESP32 Target</th>
        <th style="width: 50%;">Fungsi & Catatan Teknis</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>VCC</strong></td>
        <td><strong>3V3</strong></td>
        <td>Catu daya logika sensor (3.3V aman untuk input ADC ESP32).</td>
      </tr>
      <tr>
        <td><strong>GND</strong></td>
        <td><strong>GND</strong></td>
        <td>Common ground referensi tegangan.</td>
      </tr>
      <tr>
        <td><strong>DATA / AOUT</strong></td>
        <td><strong>GPIO 4 / GPIO 34</strong></td>
        <td>Jika sensor DHT11/22: Gunakan pin digital GPIO 4.<br>Jika sensor Soil Moisture analog: Gunakan pin ADC1 GPIO 34.</td>
      </tr>
      <tr>
        <td><strong>USB Port</strong></td>
        <td><strong>Laptop / PC</strong></td>
        <td>Serial monitor debug (Baud rate 115200) & power supply saat pengujian.</td>
      </tr>
    </tbody>
  </table>

  <div class="footer-note">
    Gambar 2: Wiring Sensor ke ESP32 dan Alur Pelaporan Nilai Sensor ke Blynk Mobile App & ThingSpeak Channel.
  </div>

</body>
</html>
"""

html_file = 'panduan_pengadaan_alat_dan_bahan_iot.html'
pdf_file = 'Panduan_Pengadaan_Alat_dan_Bahan_IoT.pdf'

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
