import os
import subprocess
import re

html_content = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Cheatsheet & Latihan Soal Sistem Tertanam</title>
<style>
  @page {
    size: 215mm 330mm; /* Standar Folio / F4 */
    margin: 4.5mm 5.5mm;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 6.9pt;
    line-height: 1.22;
    color: #0f172a;
    background: #ffffff;
  }

  /* Header */
  .header {
    border-bottom: 2px solid #0f172a;
    padding-bottom: 2.5px;
    margin-bottom: 3.5px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .header h1 {
    font-size: 10.5pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    color: #0f172a;
  }
  .header .meta {
    font-size: 6.5pt;
    color: #475569;
    font-weight: 600;
  }

  /* Layout Grid: 3 Columns */
  .grid-container {
    display: grid;
    grid-template-columns: 1.05fr 1.05fr 1.15fr;
    gap: 3.8mm;
  }

  /* Section Styling */
  .section-title {
    font-size: 7.2pt;
    font-weight: 800;
    text-transform: uppercase;
    background: #0f172a;
    color: #ffffff;
    padding: 1.8px 4px;
    border-radius: 2px;
    margin-bottom: 2.5px;
    letter-spacing: 0.2px;
  }
  .section-title.alt {
    background: #1e3a8a;
  }
  .section-title.accent {
    background: #047857;
  }

  .card {
    border: 1px solid #cbd5e1;
    border-radius: 2.5px;
    padding: 2.5px 3.5px;
    margin-bottom: 2.5px;
    background: #ffffff;
  }
  .card-header {
    font-weight: 700;
    font-size: 6.9pt;
    color: #1e293b;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 1px;
    margin-bottom: 2px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .card-header .badge {
    font-size: 5.5pt;
    padding: 0.5px 3px;
    border-radius: 2px;
    background: #f1f5f9;
    color: #334155;
    font-weight: 700;
    border: 1px solid #cbd5e1;
  }

  /* Content typography */
  p, ul {
    margin-bottom: 1.5px;
  }
  ul {
    padding-left: 9px;
  }
  li {
    margin-bottom: 1px;
  }
  strong {
    color: #0f172a;
  }
  .code {
    font-family: Consolas, monospace;
    font-size: 6.5pt;
    background: #f1f5f9;
    padding: 0.5px 2px;
    border-radius: 2px;
    border: 1px solid #e2e8f0;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 6.2pt;
    margin-top: 1px;
    margin-bottom: 1.5px;
  }
  th, td {
    border: 1px solid #cbd5e1;
    padding: 1px 2.5px;
    text-align: left;
  }
  th {
    background: #f8fafc;
    font-weight: 700;
  }

  /* Questions column */
  .q-item {
    border: 1px solid #e2e8f0;
    border-left: 2.5px solid #0f172a;
    border-radius: 2px;
    padding: 2px 3px;
    margin-bottom: 2px;
    background: #fafafa;
  }
  .q-item.trivia { border-left-color: #6366f1; }
  .q-item.nontech { border-left-color: #0d9488; }
  .q-item.tech { border-left-color: #e11d48; }

  .q-header {
    font-weight: 700;
    font-size: 6.7pt;
    margin-bottom: 1px;
    display: flex;
    justify-content: space-between;
  }
  .q-type {
    font-size: 5.4pt;
    text-transform: uppercase;
    font-weight: 800;
    padding: 0.5px 2.5px;
    border-radius: 2px;
    color: #fff;
  }
  .type-triv { background: #6366f1; }
  .type-non { background: #0d9488; }
  .type-tech { background: #e11d48; }

  .q-text {
    font-size: 6.5pt;
    margin-bottom: 1px;
    line-height: 1.18;
  }
  .q-opts {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8px 3px;
    font-size: 6pt;
    color: #334155;
    margin-bottom: 1px;
    background: #fff;
    padding: 1px 2.5px;
    border-radius: 2px;
    border: 1px solid #f1f5f9;
  }
  .q-ans {
    font-size: 6.1pt;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    padding: 1px 2.5px;
    border-radius: 2px;
    line-height: 1.15;
    color: #14532d;
  }
  .q-ans strong {
    color: #15803d;
  }
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>Sistem Tertanam (Embedded Systems) - Master Cheatsheet</h1>
  </div>
  <div class="meta">
    Standar F4 (215 x 330 mm) | Rangkuman Materi & Pembahasan 10 Soal
  </div>
</div>

<div class="grid-container">
  <!-- KOLOM 1: HARDWARE & SIKLUS INTERUPSI -->
  <div class="col">
    <div class="section-title">Modul 1: I/O Hardware & Sirkuit Dasar</div>
    
    <div class="card">
      <div class="card-header">
        <span>Komponen Pasif vs Aktif</span>
        <span class="badge">Elektronika</span>
      </div>
      <ul>
        <li><strong>Pasif</strong>: Tidak butuh catu daya luar & tidak memperkuat daya (hanya serap/simpan/disipasi). Contoh: Resistor (panas), Kapasitor (medan listrik), Induktor (medan magnet).</li>
        <li><strong>Aktif</strong>: Butuh catu daya luar & mampu memberi penguatan sinyal/daya (gain) atau kontrol aliran elektron. Contoh: Op-Amp, Transistor (BJT, MOSFET), IC logic.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <span>Resistor Pull-Up vs Pull-Down</span>
        <span class="badge">Digital I/O</span>
      </div>
      <p>Mencegah pin berstatus <em>floating</em> (mengambang akibat interferensi noise):</p>
      <table>
        <tr>
          <th>Fitur</th>
          <th>Pull-Up</th>
          <th>Pull-Down</th>
        </tr>
        <tr>
          <td><strong>Hubungan R</strong></td>
          <td>Ke VCC (3,3V / 5V)</td>
          <td>Ke GND (0V)</td>
        </tr>
        <tr>
          <td><strong>Sakelar ke</strong></td>
          <td>Ground (GND)</td>
          <td>VCC</td>
        </tr>
        <tr>
          <td><strong>Status Lepas</strong></td>
          <td>HIGH (1)</td>
          <td>LOW (0)</td>
        </tr>
        <tr>
          <td><strong>Status Tekan</strong></td>
          <td>LOW (0)</td>
          <td>HIGH (1)</td>
        </tr>
        <tr>
          <td><strong>Tipe Logika</strong></td>
          <td><strong>Active-Low</strong></td>
          <td><strong>Active-High</strong></td>
        </tr>
      </table>
    </div>

    <div class="card">
      <div class="card-header">
        <span>Konvensi Active-Low & GPIO Trap</span>
        <span class="badge">Datasheet</span>
      </div>
      <ul>
        <li><strong>Tanda Active-Low</strong>: Ditulis /RESET, RESET#, RESET_N, atau garis atas (RESET). Artinya: fungsi terpicu saat tegangan <strong>LOW (0 V)</strong>; posisi diamnya HIGH.</li>
        <li><strong>Perangkap Pin ESP32-S3</strong>: Jalur <strong>GPIO26 s.d. GPIO32</strong> terhubung internal ke SPI Flash dan PSRAM. DILARANG dipakai untuk I/O bebas! Menggunakannya merusak bus memori dan memicu crash seketika.</li>
      </ul>
    </div>

    <div class="section-title">Modul 2: Penanganan Interupsi & CPU</div>

    <div class="card">
      <div class="card-header">
        <span>Polling vs Interupsi</span>
        <span class="badge">Mekanisme</span>
      </div>
      <ul>
        <li><strong>Polling</strong>: Mekanisme <strong>Software</strong>. CPU berulang-ulang mengecek status register. Boros komputasi, boros daya baterai, latensi lambat jika ada task lain.</li>
        <li><strong>Interupsi</strong>: Mekanisme <strong>Hardware</strong>. Periferal mengirim sinyal listrik fisik ke Interrupt Controller CPU. Asinkron, respons instan, CPU bisa tidur (hemat daya).</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <span>Siklus 5 Langkah Interupsi & Aktor</span>
        <span class="badge">Arsitektur</span>
      </div>
      <ul>
        <li><strong>1. Sinyal IRQ (Hardware)</strong>: Periferal picu sinyal, CPU selesaikan instruksi berjalan.</li>
        <li><strong>2. Simpan Status (Hardware)</strong>: CPU simpan PC & Flags ke stack, ambil alamat ISR dari Interrupt Vector Table (IVT).</li>
        <li><strong>3. Eksekusi ISR (Compiler + Developer)</strong>: Compiler buat Prologue (PUSH register); <em>Developer menulis kode logika inti ISR & clear flag register</em>.</li>
        <li><strong>4. Pemulihan Register (Compiler)</strong>: Compiler buat Epilogue (POP register dari stack).</li>
        <li><strong>5. Kembali (Hardware)</strong>: Eksekusi instruksi RETI/RTI, pulihkan PC & Flags, buka gerbang interupsi, lanjut program utama.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <span>Instruksi RETI / RTI vs RTS</span>
        <span class="badge">Assembly</span>
      </div>
      <ul>
        <li><strong>RTS</strong>: Hanya memulihkan Program Counter (PC) dari stack untuk subrutin fungsi biasa.</li>
        <li><strong>RETI / RTI</strong>: Memulihkan PC + memulihkan Status Register (Flags) + mengaktifkan kembali gerbang interupsi global.</li>
      </ul>
    </div>
  </div>

  <!-- KOLOM 2: FORMULA, MEMORI & INDUSTRI -->
  <div class="col">
    <div class="section-title alt">Modul 3: Kalkulasi & Formulasi Waktu</div>

    <div class="card">
      <div class="card-header">
        <span>Formulasi Hukum Ohm & Arus</span>
        <span class="badge">Rumus</span>
      </div>
      <p><strong>V = I x R</strong> &nbsp;|&nbsp; <strong>I = V / R</strong> &nbsp;|&nbsp; <strong>R = V / I</strong></p>
      <p><em>Peringatan Konversi</em>: Arus wajib dinyatakan dalam Ampere!</p>
      <ul>
        <li>20 mA = 0,02 A &rarr; V = 0,02 A x 220 &Omega; = <strong>4,4 V</strong></li>
        <li>10 mA = 0,01 A &rarr; V = 0,01 A x 330 &Omega; = <strong>3,3 V</strong></li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <span>Perhitungan Durasi ISR & Utilisasi CPU</span>
        <span class="badge">Timing</span>
      </div>
      <ul>
        <li><strong>Durasi 1 Siklus Clock</strong>: T = 1 / f_CPU<br>
        Pada 30 MHz: T = 1 / (30 x 10^6) s = 0,0333 &mu;s.</li>
        <li><strong>Total Waktu Eksekusi 1x ISR</strong>: t_ISR = Siklus_ISR / f_CPU<br>
        Contoh: Overhead 10 + (5 fungsi x 10) + 275 data = 335 siklus.<br>
        t_ISR = 335 / 30 &mu;s = 11,167 &mu;s &rarr; <strong>11 &mu;s</strong>.</li>
        <li><strong>Beban CPU (%)</strong>: (Siklus_ISR x Laju_Interupsi / f_CPU) x 100%<br>
        Pada laju audio 44.100 Hz:<br>
        Total siklus/s = 335 x 44.100 = 14.773.500 siklus/detik.<br>
        Kapasitas 30 MHz = 30.000.000 siklus/detik.<br>
        Beban CPU = (14.773.500 / 30.000.000) x 100% = 49,245% &rarr; <strong>49%</strong>.</li>
      </ul>
    </div>

    <div class="section-title alt">Modul 4: Konkurensi & Integritas Memori</div>

    <div class="card">
      <div class="card-header">
        <span>Kata Kunci volatile</span>
        <span class="badge">C / C++</span>
      </div>
      <ul>
        <li><strong>Fungsi Mutlak</strong>: Memaksa kompilator membaca/menulis langsung ke RAM fisik setiap saat; mencegah optimasi register caching.</li>
        <li><strong>Batas Kemampuan</strong>: volatile <em>TIDAK menjamin atomisitas</em> dan <em>TIDAK mematikan interupsi secara otomatis</em>.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <span>Operasi Non-Atomik 64-bit pada CPU 32-bit</span>
        <span class="badge">Race Condition</span>
      </div>
      <ul>
        <li>CPU 32-bit punya lebar bus & register 32-bit. Penulisan uint64_t dipecah kompilator jadi 2 instruksi (low-word lalu high-word).</li>
        <li><strong>Torn Write</strong>: Jika interupsi masuk persis di antara penulisan kata 1 dan kata 2, ISR akan membaca data korup/separuh basi.</li>
        <li><strong>Solusi</strong>: Wajib dibungkus <em>Critical Section</em> (menonaktifkan interupsi sementara saat membaca/menulis variabel bersama).</li>
      </ul>
    </div>

    <div class="section-title alt">Modul 5: Industri, Sejarah & Dokumen</div>

    <div class="card">
      <div class="card-header">
        <span>Pangsa Pasar & Dokumentasi Chip</span>
        <span class="badge">Fakta</span>
      </div>
      <ul>
        <li><strong>Pangsa Pasar Global</strong>: <strong>98%</strong> prosesor di dunia adalah Embedded Systems; hanya <strong>2%</strong> berakhir sebagai CPU PC/laptop pribadi.</li>
        <li><strong>Errata Sheet</strong>: Dokumen resmi pabrikan yang mencatat daftar cacat desain silikon chip (silicon bugs) serta ralat datasheet beserta cara penyelesaiannya (workarounds).</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-header">
        <span>Komparasi Arsitektur: AGC vs ESP32</span>
        <span class="badge">Komparatif</span>
      </div>
      <ul>
        <li><strong>2 Konsep AGC yang Diwarisi ESP32</strong>: Multitasking berbasis prioritas (RTOS FreeRTOS) & Penanganan Interupsi Hardware.</li>
        <li><strong>ESP32 Melampaui AGC</strong>: Clock 240 MHz vs 1,024 MHz (>200x lipat), Throughput ~600 MIPS vs ~40-85 kIPS, RAM 520 KB vs ~4 KB.</li>
      </ul>
    </div>
  </div>

  <!-- KOLOM 3: 10 SOAL LATIHAN & PEMBAHASAN -->
  <div class="col">
    <div class="section-title accent">Latihan 10 Soal, Kunci & Pembahasan</div>

    <!-- SOAL 1 -->
    <div class="q-item trivia">
      <div class="q-header">
        <span>1. Pangsa Pasar CPU Komputer Personal</span>
        <span class="q-type type-triv">Trivial</span>
      </div>
      <div class="q-text">Dari total prosesor dunia per tahun, bagian yang jadi CPU PC hanyalah:</div>
      <div class="q-opts">
        <div>a. 50%</div><div>b. 20%</div><div>c. 66%</div><div>d. 2%</div>
      </div>
      <div class="q-ans"><strong>Kunci: D (2%)</strong>. 98% dialokasikan untuk sistem tertanam (otomotif, IoT, medis, industri).</div>
    </div>

    <!-- SOAL 2 -->
    <div class="q-item trivia">
      <div class="q-header">
        <span>2. Dokumen Koreksi Cacat Desain Silikon</span>
        <span class="q-type type-triv">Trivial</span>
      </div>
      <div class="q-text">Dokumen resmi pabrikan pemuat daftar bug silikon chip & solusi workaround:</div>
      <div class="q-opts">
        <div>a. Application Note</div><div>b. Errata</div>
        <div>c. Timing Diagram</div><div>d. Reference Manual</div>
      </div>
      <div class="q-ans"><strong>Kunci: B (Errata)</strong>. Memuat ralat cetak dan catatan cacat logika silikon chip.</div>
    </div>

    <!-- SOAL 3 -->
    <div class="q-item trivia">
      <div class="q-header">
        <span>3. Perbandingan Clock AGC vs ESP32</span>
        <span class="q-type type-triv">Trivial</span>
      </div>
      <div class="q-text">AGC bekerja pada ~1,024 MHz, sedangkan clock maksimum ESP32 mencapai:</div>
      <div class="q-opts">
        <div>a. 16 MHz</div><div>b. 80 MHz</div><div>c. 240 MHz</div><div>d. 1,2 GHz</div>
      </div>
      <div class="q-ans"><strong>Kunci: C (240 MHz)</strong>. ESP32 Dual-Core Xtensa >200x lebih cepat dibanding AGC.</div>
    </div>

    <!-- SOAL 4 -->
    <div class="q-item nontech">
      <div class="q-header">
        <span>4. Hakikat Polling vs Interupsi</span>
        <span class="q-type type-non">Non-Teknikal</span>
      </div>
      <div class="q-text">Pernyataan paling tepat mengenai sifat mekanisme pelayanan kejadian:</div>
      <div class="q-opts">
        <div>a. Polling hw, interupsi sw</div><div>b. Polling sw, interupsi hw</div>
        <div>c. Polling selalu periodik</div><div>d. Interupsi tanpa prioritas</div>
      </div>
      <div class="q-ans"><strong>Kunci: B</strong>. Polling dikendalikan loop software; interupsi dipicu sinyal listrik hardware.</div>
    </div>

    <!-- SOAL 5 -->
    <div class="q-item nontech">
      <div class="q-header">
        <span>5. Pembagian Peran Siklus Interupsi</span>
        <span class="q-type type-non">Non-Teknikal</span>
      </div>
      <div class="q-text">Bagian dalam siklus penanganan interupsi yang kodenya ditulis oleh programmer:</div>
      <div class="q-opts">
        <div>a. Simpan PC ke stack</div><div>b. Ambil vektor IVT</div>
        <div>c. Isi logika fungsi ISR</div><div>d. Eksekusi RETI hardware</div>
      </div>
      <div class="q-ans"><strong>Kunci: C</strong>. Programmer menulis logika tugas ISR dan me-reset interrupt flag register.</div>
    </div>

    <!-- SOAL 6 -->
    <div class="q-item nontech">
      <div class="q-header">
        <span>6. Klasifikasi Komponen Sirkuit</span>
        <span class="q-type type-non">Non-Teknikal</span>
      </div>
      <div class="q-text">Komponen yang tergolong elemen aktif dalam rangkaian elektronika adalah:</div>
      <div class="q-opts">
        <div>a. Induktor</div><div>b. Kapasitor</div><div>c. Op-Amp</div><div>d. Resistor</div>
      </div>
      <div class="q-ans"><strong>Kunci: C (Op-Amp)</strong>. Membutuhkan daya eksternal dan mampu memperkuat sinyal.</div>
    </div>

    <!-- SOAL 7 -->
    <div class="q-item tech">
      <div class="q-header">
        <span>7. Perhitungan Hukum Ohm</span>
        <span class="q-type type-tech">Teknikal</span>
      </div>
      <div class="q-text">Resistor 220 &Omega; dialiri arus 20 mA. Tegangan jatuh pada resistor tersebut:</div>
      <div class="q-opts">
        <div>a. 3,3 V</div><div>b. 11 V</div><div>c. 4,4 V</div><div>d. 4400 V</div>
      </div>
      <div class="q-ans"><strong>Kunci: C (4,4 V)</strong>. V = I x R = 0,02 A x 220 &Omega; = 4,4 V.</div>
    </div>

    <!-- SOAL 8 -->
    <div class="q-item tech">
      <div class="q-header">
        <span>8. Persentase Beban CPU Audio ISR</span>
        <span class="q-type type-tech">Teknikal</span>
      </div>
      <div class="q-text">CPU 30 MHz, ISR butuh 335 siklus, frekuensi audio 44.100 Hz. Beban CPU:</div>
      <div class="q-opts">
        <div>a. 25%</div><div>b. 33%</div><div>c. 49%</div><div>d. 68%</div>
      </div>
      <div class="q-ans"><strong>Kunci: C (49%)</strong>. (335 x 44.100) / 30.000.000 = 14.773.500 / 30.000.000 = 49,25% &rarr; 49%.</div>
    </div>

    <!-- SOAL 9 -->
    <div class="q-item tech">
      <div class="q-header">
        <span>9. Variabel 64-bit pada CPU 32-bit</span>
        <span class="q-type type-tech">Teknikal</span>
      </div>
      <div class="q-text">Menulis uint64_t di CPU 32-bit berisiko race condition / torn write karena:</div>
      <div class="q-opts">
        <div>a. Lewat cache basi</div><div>b. Butuh 2 instruksi mesin</div>
        <div>c. Tak bisa volatile</div><div>d. Selalu di heap memori</div>
      </div>
      <div class="q-ans"><strong>Kunci: B</strong>. Penulisan dipecah 2 instruksi 32-bit; interupsi bisa masuk di antaranya.</div>
    </div>

    <!-- SOAL 10 -->
    <div class="q-item tech">
      <div class="q-header">
        <span>10. Pinout ESP32-S3 & Logika Active-Low</span>
        <span class="q-type type-tech">Teknikal</span>
      </div>
      <div class="q-text">Pin GPIO26-32 pada ESP32-S3 terlarang dipakai bebas karena:</div>
      <div class="q-opts">
        <div>a. Fisik tidak ada</div><div>b. Terhubung SPI Flash/PSRAM</div>
        <div>c. Khusus 1,8V</div><div>d. Tanpa dukungan RTC</div>
      </div>
      <div class="q-ans"><strong>Kunci: B</strong>. Terhubung ke bus Flash & PSRAM internal dalam modul mikrokontroler.</div>
    </div>

  </div>
</div>

</body>
</html>
"""

with open('cheatsheet_f4.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
html_path = os.path.abspath('cheatsheet_f4.html')
pdf_path = os.path.abspath('cheatsheet_f4.pdf')

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
print('Path:', pdf_path)
