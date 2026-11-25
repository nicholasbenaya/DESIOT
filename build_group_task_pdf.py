import os
import subprocess
import base64
import re

# Load circuit diagram image as base64
img_path = r'c:\Users\kegz\Desktop\Folder iko\Projects Local\DESIOT\rangkaian_tugas_kelompok.png'
with open(img_path, 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode('utf-8')

html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Panduan Lengkap Implementasi & Rangkaian Tugas Kelompok DESIOT (ESP32-S3)</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 12mm 14mm 12mm 14mm;
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
    font-size: 8.8pt;
    line-height: 1.42;
    color: #1e293b;
    background: #ffffff;
  }}

  /* Header */
  .doc-header {{
    border-bottom: 2.5px solid #0284c7;
    padding-bottom: 8px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}
  .doc-header .title-area h1 {{
    font-size: 14pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.3px;
    text-transform: uppercase;
  }}
  .doc-header .title-area .subtitle {{
    font-size: 9pt;
    color: #0284c7;
    font-weight: 600;
    margin-top: 2px;
  }}
  .doc-header .meta-badge {{
    background: #e0f2fe;
    color: #0369a1;
    border: 1px solid #bae6fd;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 7.8pt;
    font-weight: 700;
    text-align: right;
    line-height: 1.3;
  }}

  /* Section Styling */
  .section {{
    margin-bottom: 12px;
    page-break-inside: avoid;
  }}
  .section-title {{
    font-size: 10.2pt;
    font-weight: 700;
    color: #0f172a;
    border-left: 3.5px solid #0284c7;
    padding-left: 8px;
    margin-bottom: 6px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
  }}

  /* Callout Boxes */
  .callout {{
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 10px;
    font-size: 8.5pt;
    line-height: 1.4;
  }}
  .callout-warning {{
    background: #fffbeb;
    border-left: 4px solid #d97706;
    color: #92400e;
  }}
  .callout-danger {{
    background: #fef2f2;
    border-left: 4px solid #ef4444;
    color: #991b1b;
  }}
  .callout-info {{
    background: #f0f9ff;
    border-left: 4px solid #0284c7;
    color: #0369a1;
  }}
  .callout-success {{
    background: #f0fdf4;
    border-left: 4px solid #16a34a;
    color: #166534;
  }}
  .callout strong {{
    font-weight: 700;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 8px;
    font-size: 8.2pt;
  }}
  th {{
    background: #f1f5f9;
    color: #334155;
    font-weight: 700;
    text-align: left;
    padding: 5px 8px;
    border: 1px solid #cbd5e1;
    font-size: 8pt;
    text-transform: uppercase;
  }}
  td {{
    padding: 5px 8px;
    border: 1px solid #e2e8f0;
    vertical-align: middle;
  }}
  tr:nth-child(even) {{
    background: #f8fafc;
  }}

  /* Badges */
  .badge {{
    display: inline-block;
    padding: 1.5px 5.5px;
    border-radius: 4px;
    font-size: 7.5pt;
    font-weight: 700;
    font-family: Consolas, monospace;
  }}
  .badge-pin {{
    background: #dbeafe;
    color: #1e40af;
    border: 1px solid #bfdbfe;
  }}
  .badge-pwr {{
    background: #fee2e2;
    color: #991b1b;
    border: 1px solid #fecaca;
  }}
  .badge-gnd {{
    background: #f1f5f9;
    color: #334155;
    border: 1px solid #cbd5e1;
  }}
  .badge-sig {{
    background: #dcfce7;
    color: #166534;
    border: 1px solid #bbf7d0;
  }}

  /* Diagram Image */
  .diagram-container {{
    text-align: center;
    margin: 8px 0 12px 0;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 6px;
    page-break-inside: avoid;
  }}
  .diagram-container img {{
    max-width: 100%;
    height: auto;
    border-radius: 4px;
  }}
  .diagram-caption {{
    font-size: 7.8pt;
    color: #64748b;
    font-style: italic;
    margin-top: 4px;
  }}

  /* Hanzi Box */
  .hanzi-card {{
    background: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-around;
    text-align: center;
  }}
  .hanzi-item {{
    flex: 1;
    padding: 4px 6px;
    border-right: 1px solid #e2e8f0;
  }}
  .hanzi-item:last-child {{
    border-right: none;
  }}
  .hanzi-char {{
    font-size: 16pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.1;
  }}
  .hanzi-label {{
    font-size: 8.2pt;
    font-weight: 700;
    margin-top: 2px;
  }}
  .hanzi-desc {{
    font-size: 7.2pt;
    color: #475569;
    margin-top: 2px;
  }}

  .page-break {{
    page-break-before: always;
  }}

  .footer-note {{
    border-top: 1px solid #e2e8f0;
    padding-top: 6px;
    font-size: 7.5pt;
    color: #64748b;
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
  }}
</style>
</head>
<body>

  <!-- ==================== HALAMAN 1 ==================== -->
  <div class="doc-header">
    <div class="title-area">
      <h1>SOP Rangkaian & Implementasi Tugas Kelompok</h1>
      <div class="subtitle">Sistem Irigasi Otomatis Berbasis ESP32-S3 BLE Mesh & Wi-Fi MQTT Gateway</div>
    </div>
    <div class="meta-badge">
      Mata Kuliah: DESIOT (ITS)<br>
      Target Board: ESP32-S3 DevKit<br>
      Kelompok 4 Orang (Max 5 Menit)
    </div>
  </div>

  <div class="callout callout-danger">
    <strong>PRINSIP KELISTRIKAN KRUSIAL (PENTING DIBACA SEBELUM MERANGKAI):</strong><br>
    <strong>Pin VIN adalah Jalur Input Daya Regulator LDO Internal, BUKAN Output Catu Daya Beban!</strong>
    Jangan mengambil daya motor pompa air DC 5V atau coil relay langsung dari pin VIN ESP32-S3. Motor pompa adalah beban induktif yang menyedot arus lonjakan (<em>inrush current</em>) 500mA–1A. Menarik arus beban motor melalui jalur PCB ESP32-S3 akan memicu <em>voltage sag</em> yang menyebabkan <strong>ESP32-S3 Brownout Reset (restart berulang kali)</strong> atau terbakar bila ditenagai baterai 9V. <strong>Solusi Wajib:</strong> Gunakan adaptor 5V eksternal mandiri untuk relay & pompa dengan skema <strong>Common Ground</strong>.
  </div>

  <div class="section">
    <div class="section-title">1. Skema Visual Rangkaian Elektronika 4-Node (ESP32-S3)</div>
    <div class="diagram-container">
      <img src="data:image/png;base64,{img_b64}" alt="Skema Rangkaian Tugas Kelompok DESIOT ESP32-S3">
      <div class="diagram-caption">Gambar 1: Skema Pengkabelan Lengkap Node 1 (Pompa DC), Node 2 (Sensor LPN), Node 3 (Relay/Friend), dan Node 4 (Gateway Wi-Fi MQTT).</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">2. Identifikasi Terminal Modul Relay Berbahasa Mandarin (Hanzi)</div>
    <p style="margin-bottom: 6px; font-size: 8.2pt; color: #475569;">
      Pada modul relay biru (Songle / generic), silkscreen PCB terminal 3 sekrup output umumnya bertuliskan karakter Mandarin. Berikut panduan pencocokannya:
    </p>
    <div class="hanzi-card">
      <div class="hanzi-item">
        <div class="hanzi-char" style="color: #ea580c;">常开 / 开</div>
        <div class="hanzi-label" style="color: #ea580c;">NO (Normally Open)</div>
        <div class="hanzi-desc"><strong>HUBUNGKAN KE POMPA (+)</strong><br>Arus baru mengalir saat relay ON (bunyi klik).</div>
      </div>
      <div class="hanzi-item">
        <div class="hanzi-char" style="color: #0284c7;">公 / 公共端</div>
        <div class="hanzi-label" style="color: #0284c7;">COM (Common)</div>
        <div class="hanzi-desc"><strong>HUBUNGKAN KE +5V ADAPTOR</strong><br>Terminal bersama sumber daya arus listrik.</div>
      </div>
      <div class="hanzi-item">
        <div class="hanzi-char" style="color: #64748b;">常闭 / 闭</div>
        <div class="hanzi-label" style="color: #64748b;">NC (Normally Closed)</div>
        <div class="hanzi-desc"><strong>KOSONGKAN / JANGAN DIPAKAI</strong><br>Terhubung saat relay OFF, terputus saat ON.</div>
      </div>
    </div>
    <div class="callout callout-info" style="margin-bottom: 4px; padding: 5px 10px;">
      <strong>Trik Multimeter (Buzzer Mode):</strong> Saat relay mati tanpa listrik, tempelkan probe di terminal tengah (COM) dan salah satu terminal samping. Terminal yang <em>berbunyi "BEEP"</em> adalah <strong>NC (常闭)</strong>, sedangkan terminal yang <em>diam (tidak bunyi)</em> pasti adalah <strong>NO (常开)</strong>.
    </div>
  </div>

  <!-- ==================== HALAMAN 2 ==================== -->
  <div class="page-break"></div>

  <div class="doc-header">
    <div class="title-area">
      <h1>Tabel Pengkabelan Fisik & Alur Pengerjaan</h1>
      <div class="subtitle">Daftar Koneksi Pin ESP32-S3 & Panduan Demo 5 Menit</div>
    </div>
    <div class="meta-badge">
      Halaman 2 dari 2<br>Dokumen Resmi DESIOT
    </div>
  </div>

  <div class="section">
    <div class="section-title">3. Tabel Pengkabelan Fisik Lengkap (ESP32-S3 DevKit)</div>

    <strong style="color: #92400e; font-size: 8.5pt;">A. Node 1: Aktuator Pompa Air DC (Generic OnOff Server)</strong>
    <table>
      <thead>
        <tr>
          <th style="width: 28%;">Dari Komponen / Pin</th>
          <th style="width: 28%;">Terhubung Ke</th>
          <th style="width: 44%;">Fungsi & Catatan Teknis</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Relay: Pin IN</strong></td>
          <td><span class="badge badge-sig">GPIO 10</span> ESP32-S3</td>
          <td>Sinyal kontrol digital aktuasi pompa</td>
        </tr>
        <tr>
          <td><strong>Relay: Pin VCC</strong></td>
          <td><span class="badge badge-pwr">+5V</span> Adaptor Eksternal</td>
          <td>Daya coil relay elektromagnetik (terpisah dari ESP32)</td>
        </tr>
        <tr>
          <td><strong>Relay: Terminal COM (公)</strong></td>
          <td><span class="badge badge-pwr">+5V</span> Adaptor Eksternal</td>
          <td>Sumber tegangan penggerak motor pompa</td>
        </tr>
        <tr>
          <td><strong>Relay: Terminal NO (常开)</strong></td>
          <td><strong>Kabel Positif (+)</strong> Pompa DC</td>
          <td>Menghubungkan arus ke motor saat relay dipicu ON</td>
        </tr>
        <tr>
          <td><strong>Relay: Pin GND</strong></td>
          <td><span class="badge badge-gnd">GND</span> Common Ground</td>
          <td>Ground referensi modul relay</td>
        </tr>
        <tr>
          <td><strong>Pompa DC: Kabel Negatif (-)</strong></td>
          <td><span class="badge badge-gnd">GND</span> Common Ground</td>
          <td>Menutup sirkuit daya motor pompa</td>
        </tr>
        <tr>
          <td><strong>ESP32-S3: Pin GND</strong></td>
          <td><span class="badge badge-gnd">GND</span> Common Ground</td>
          <td><strong>Wajib Common Ground</strong> menyamakan level logika sinyal IN</td>
        </tr>
        <tr>
          <td><strong>ESP32-S3: Port USB</strong></td>
          <td>Charger USB 5V Mandiri</td>
          <td>Daya mikrokontroler bebas noise motor</td>
        </tr>
      </tbody>
    </table>

    <strong style="color: #15803d; font-size: 8.5pt;">B. Node 2: Sensor Kelembapan Tanah (Low Power Node - Baterai Mandiri)</strong>
    <table>
      <thead>
        <tr>
          <th style="width: 28%;">Dari Komponen / Pin</th>
          <th style="width: 28%;">Terhubung Ke</th>
          <th style="width: 44%;">Fungsi & Catatan Teknis</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Sensor: Pin AOUT</strong></td>
          <td><span class="badge badge-pin">GPIO 4</span> ESP32-S3</td>
          <td>Output analog kadar air (ADC1_CH3 pada ESP32-S3)</td>
        </tr>
        <tr>
          <td><strong>Sensor: Pin VCC</strong></td>
          <td><span class="badge badge-pwr">3V3</span> ESP32-S3</td>
          <td><strong>Wajib 3.3V</strong> agar output ADC aman (0–3.0V). <em>Jangan ke VIN!</em></td>
        </tr>
        <tr>
          <td><strong>Sensor: Pin GND</strong></td>
          <td><span class="badge badge-gnd">GND</span> ESP32-S3</td>
          <td>Ground sensor kapasitif</td>
        </tr>
        <tr>
          <td><strong>Baterai: Kutub Positif (+)</strong></td>
          <td><span class="badge badge-pwr">VIN</span> ESP32-S3</td>
          <td>Input ke regulator internal LDO (Baterai 18650 x 2 / 7.4V / 9V)</td>
        </tr>
        <tr>
          <td><strong>Baterai: Kutub Negatif (-)</strong></td>
          <td><span class="badge badge-gnd">GND</span> ESP32-S3</td>
          <td>Ground baterai mandiri</td>
        </tr>
      </tbody>
    </table>

    <strong style="color: #0369a1; font-size: 8.5pt;">C. Node 3 & Node 4: Jaringan Mesh & Gateway MQTT</strong>
    <table>
      <thead>
        <tr>
          <th style="width: 20%;">Simpul</th>
          <th style="width: 36%;">Koneksi Daya & Data</th>
          <th style="width: 44%;">Peran dalam Jaringan</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Node 3 (Relay/Friend)</strong></td>
          <td>Port USB ke Charger HP 5V (Tanpa sensor luar)</td>
          <td>Radio RX siaga 100% menyimpan antrean pesan LPN & merelai paket</td>
        </tr>
        <tr>
          <td><strong>Node 4 (Gateway Wi-Fi)</strong></td>
          <td>Port USB ke Laptop Host (CH343 / COM6)</td>
          <td>Menangkap paket mesh & mem-publish data JSON ke Mosquitto (1883)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="section">
    <div class="section-title">4. Skenario Demo Video 5 Menit & Matriks Klaim Pekerjaan</div>
    <div style="display: flex; gap: 10px;">
      <div style="flex: 1;">
        <strong style="font-size: 8pt; color: #0f172a;">Alur Waktu Video Demo (Maks. 5 Menit):</strong>
        <ul style="padding-left: 14px; font-size: 7.8pt; line-height: 1.35; margin-top: 3px; color: #334155;">
          <li><strong>0:00 - 0:45:</strong> Perkenalan 4 anggota & arsitektur sistem 4-Node.</li>
          <li><strong>0:45 - 2:00:</strong> Tunjukkan fisik hardware Node 1, 2, 3, dan 4.</li>
          <li><strong>2:00 - 3:30:</strong> <em>Uji Kering:</em> Angkat sensor Node 2 ke udara &rarr; pompa Node 1 aktif &rarr; data masuk di Mosquitto laptop.</li>
          <li><strong>3:30 - 4:30:</strong> <em>Uji Basah:</em> Celupkan sensor ke air &rarr; pompa otomatis mati &rarr; status update di laptop.</li>
          <li><strong>4:30 - 5:00:</strong> Kesimpulan efisiensi daya LPN & penutup.</li>
        </ul>
      </div>
      <div style="flex: 1.2;">
        <strong style="font-size: 8pt; color: #0f172a;">Matriks Tanggung Jawab Anggota (Wajib di Makalah & PPT):</strong>
        <table style="margin-top: 3px; font-size: 7.5pt;">
          <thead>
            <tr>
              <th>Anggota</th>
              <th>Peran Utama</th>
              <th>Kontribusi</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Anggota 1</strong></td>
              <td>Node 1: Pompa DC, Relay 5V, Common Ground</td>
              <td>25%</td>
            </tr>
            <tr>
              <td><strong>Anggota 2</strong></td>
              <td>Node 2: Sensor Kapasitif (GPIO 4), Deep-Sleep LPN</td>
              <td>25%</td>
            </tr>
            <tr>
              <td><strong>Anggota 3</strong></td>
              <td>Node 3: Relay + Friend Node, Buffer Antrean</td>
              <td>25%</td>
            </tr>
            <tr>
              <td><strong>Anggota 4</strong></td>
              <td>Node 4: Gateway Wi-Fi MQTT, Mosquitto Host PC</td>
              <td>25%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <div class="footer-note">
    <span>Dokumen Resmi Praktikum DESIOT - Departemen Teknik Komputer / Teknik Elektro ITS Surabaya</span>
    <span>Berkas Pendukung: Makalah (GDocs) | Presentasi (GSlides) | Repositori GitHub: nicholasbenaya/desiot-ble-mesh-nodes</span>
  </div>

</body>
</html>
"""

html_file = r'c:\Users\kegz\Desktop\Folder iko\Projects Local\DESIOT\Panduan_Implementasi_Tugas_Kelompok_DESIOT_ESP32S3.html'
pdf_file = r'c:\Users\kegz\Desktop\Folder iko\Projects Local\DESIOT\Panduan_Implementasi_Tugas_Kelompok_DESIOT_ESP32S3.pdf'

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

cmd = [
    chrome_path,
    '--headless=new',
    '--disable-gpu',
    '--no-pdf-header-footer',
    f'--print-to-pdf={pdf_file}',
    html_file
]

print("Menjalankan headless Chrome untuk generate PDF...")
res = subprocess.run(cmd, capture_output=True, text=True)

with open(pdf_file, 'rb') as f:
    pdf_bytes = f.read()

pages = re.findall(rb'/Type\s*/Page\b', pdf_bytes)
print(f"Hasil Ekspor PDF:")
print(f"- Jumlah Halaman: {len(pages)}")
print(f"- Ukuran File   : {len(pdf_bytes):,} bytes")
print(f"- Lokasi File   : {pdf_file}")
