const fs = require('fs');
const path = require('path');
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  HeadingLevel,
  AlignmentType,
  WidthType,
  BorderStyle,
  ShadingType,
  PageNumber,
  NumberFormat,
  Header,
  Footer
} = require('docx');

// Colors
const COLOR_PRIMARY = "003366";    // Deep Navy ITS Blue
const COLOR_SECONDARY = "1A365D";  // Slate Blue
const COLOR_ACCENT = "0D9488";     // Teal accent
const COLOR_DARK = "1A202C";       // Dark body text
const COLOR_MUTED = "4A5568";      // Gray
const COLOR_LIGHT_BG = "F7FAFC";   // Light table alt
const COLOR_BORDER = "CBD5E0";     // Table border gray
const COLOR_CALLOUT_BG = "EDF2F7"; // Callout background

function createCell(text, options = {}) {
  const {
    isHeader = false,
    bold = false,
    align = AlignmentType.LEFT,
    width = null,
    bgColor = null,
    fontSize = 10,
    textColor = null,
    colSpan = 1
  } = options;

  const borders = {
    top: { style: BorderStyle.SINGLE, size: 4, color: COLOR_BORDER },
    bottom: { style: BorderStyle.SINGLE, size: 4, color: COLOR_BORDER },
    left: { style: BorderStyle.SINGLE, size: 4, color: COLOR_BORDER },
    right: { style: BorderStyle.SINGLE, size: 4, color: COLOR_BORDER }
  };

  return new TableCell({
    columnSpan: colSpan,
    width: width ? { size: width, type: WidthType.DXA } : undefined,
    shading: bgColor ? { fill: bgColor, type: ShadingType.CLEAR } : (isHeader ? { fill: COLOR_PRIMARY, type: ShadingType.CLEAR } : undefined),
    margins: { top: 120, bottom: 120, left: 160, right: 160 },
    borders: borders,
    children: [
      new Paragraph({
        alignment: align,
        spacing: { before: 40, after: 40 },
        children: [
          new TextRun({
            text: text,
            bold: isHeader || bold,
            color: isHeader ? "FFFFFF" : (textColor || COLOR_DARK),
            size: fontSize * 2,
            font: "Calibri"
          })
        ]
      })
    ]
  });
}

function p(text, options = {}) {
  const {
    bold = false,
    italic = false,
    size = 11,
    color = COLOR_DARK,
    align = AlignmentType.LEFT,
    before = 60,
    after = 120,
    line = 276
  } = options;

  return new Paragraph({
    alignment: align,
    spacing: { before: before, after: after, line: line },
    children: [
      new TextRun({
        text: text,
        bold: bold,
        italics: italic,
        size: size * 2,
        color: color,
        font: "Calibri"
      })
    ]
  });
}

function pMulti(runs, options = {}) {
  const {
    align = AlignmentType.LEFT,
    before = 60,
    after = 120,
    line = 276
  } = options;

  return new Paragraph({
    alignment: align,
    spacing: { before: before, after: after, line: line },
    children: runs.map(r => new TextRun({
      text: r.text,
      bold: r.bold || false,
      italics: r.italic || false,
      size: (r.size || 11) * 2,
      color: r.color || COLOR_DARK,
      font: r.font || "Calibri"
    }))
  });
}

function bullet(text, options = {}) {
  const { boldPrefix = "", size = 11, after = 80 } = options;
  const runs = [];
  if (boldPrefix) {
    runs.push(new TextRun({ text: boldPrefix, bold: true, size: size * 2, color: COLOR_DARK, font: "Calibri" }));
  }
  runs.push(new TextRun({ text: text, size: size * 2, color: COLOR_DARK, font: "Calibri" }));

  return new Paragraph({
    bullet: { level: 0 },
    spacing: { before: 40, after: after, line: 276 },
    children: runs
  });
}

function bullet2(text, options = {}) {
  const { boldPrefix = "", size = 10.5, after = 60 } = options;
  const runs = [];
  if (boldPrefix) {
    runs.push(new TextRun({ text: boldPrefix, bold: true, size: size * 2, color: COLOR_DARK, font: "Calibri" }));
  }
  runs.push(new TextRun({ text: text, size: size * 2, color: COLOR_DARK, font: "Calibri" }));

  return new Paragraph({
    bullet: { level: 1 },
    spacing: { before: 30, after: after, line: 260 },
    children: runs
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 320, after: 140 },
    children: [
      new TextRun({
        text: text,
        bold: true,
        size: 15 * 2,
        color: COLOR_PRIMARY,
        font: "Calibri"
      })
    ]
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 100 },
    children: [
      new TextRun({
        text: text,
        bold: true,
        size: 13 * 2,
        color: COLOR_SECONDARY,
        font: "Calibri"
      })
    ]
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 180, after: 80 },
    children: [
      new TextRun({
        text: text,
        bold: true,
        size: 11.5 * 2,
        color: COLOR_MUTED,
        font: "Calibri"
      })
    ]
  });
}

function callout(title, text) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            width: { size: 9360, type: WidthType.DXA },
            shading: { fill: COLOR_CALLOUT_BG, type: ShadingType.CLEAR },
            borders: {
              top: { style: BorderStyle.NONE },
              bottom: { style: BorderStyle.NONE },
              right: { style: BorderStyle.NONE },
              left: { style: BorderStyle.SINGLE, size: 24, color: COLOR_PRIMARY }
            },
            margins: { top: 140, bottom: 140, left: 200, right: 180 },
            children: [
              new Paragraph({
                spacing: { before: 0, after: 60 },
                children: [
                  new TextRun({ text: title, bold: true, size: 10.5 * 2, color: COLOR_PRIMARY, font: "Calibri" })
                ]
              }),
              new Paragraph({
                spacing: { before: 0, after: 0, line: 260 },
                children: [
                  new TextRun({ text: text, size: 10 * 2, color: COLOR_DARK, font: "Calibri" })
                ]
              })
            ]
          })
        ]
      })
    ]
  });
}

async function buildDocx() {
  const doc = new Document({
    styles: {
      default: {
        document: {
          run: { font: "Calibri", size: 22, color: COLOR_DARK }
        }
      }
    },
    sections: [
      // COVER PAGE
      {
        properties: {
          page: {
            margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 }
          }
        },
        headers: {
          default: new Header({
            children: [
              new Paragraph({
                alignment: AlignmentType.RIGHT,
                children: [
                  new TextRun({
                    text: "TUGAS 1 — DESAIN & APLIKASI IOT (DTK FTEIC ITS)",
                    size: 9 * 2,
                    color: COLOR_MUTED,
                    font: "Calibri"
                  })
                ]
              })
            ]
          })
        },
        footers: {
          default: new Footer({
            children: [
              new Paragraph({
                alignment: AlignmentType.JUSTIFIED,
                children: [
                  new TextRun({
                    text: "Nicholas Benaya (NRP: 5024241050) | Teknik Komputer ITS",
                    size: 9 * 2,
                    color: COLOR_MUTED,
                    font: "Calibri"
                  }),
                  new TextRun({
                    text: "\tHalaman ",
                    size: 9 * 2,
                    color: COLOR_MUTED,
                    font: "Calibri"
                  }),
                  new TextRun({
                    children: [PageNumber.CURRENT],
                    size: 9 * 2,
                    color: COLOR_MUTED,
                    font: "Calibri"
                  })
                ]
              })
            ]
          })
        },
        children: [
          // Judul Utama
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 600, after: 200 },
            children: [
              new TextRun({
                text: "LAPORAN TUGAS 1: DESAIN & APLIKASI IOT",
                bold: true,
                size: 20 * 2,
                color: COLOR_PRIMARY,
                font: "Calibri"
              })
            ]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 0, after: 400 },
            children: [
              new TextRun({
                text: "Rekonstruksi Arsitektur 5 Lapis, Metodologi Desain, Anggaran Energi Node, dan Analisis Kritis Produk IoT Komersial",
                bold: true,
                size: 13 * 2,
                color: COLOR_SECONDARY,
                font: "Calibri"
              })
            ]
          }),

          // Box Studi Kasus
          new Table({
            width: { size: 9360, type: WidthType.DXA },
            rows: [
              new TableRow({
                children: [
                  new TableCell({
                    width: { size: 9360, type: WidthType.DXA },
                    shading: { fill: "F0F4F8", type: ShadingType.CLEAR },
                    borders: {
                      top: { style: BorderStyle.SINGLE, size: 12, color: COLOR_PRIMARY },
                      bottom: { style: BorderStyle.SINGLE, size: 12, color: COLOR_PRIMARY },
                      left: { style: BorderStyle.SINGLE, size: 12, color: COLOR_PRIMARY },
                      right: { style: BorderStyle.SINGLE, size: 12, color: COLOR_PRIMARY }
                    },
                    margins: { top: 180, bottom: 180, left: 240, right: 240 },
                    children: [
                      new Paragraph({
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 0, after: 80 },
                        children: [
                          new TextRun({ text: "STUDI KASUS PRODUK IOT KOMERSIAL:", bold: true, size: 11 * 2, color: COLOR_PRIMARY })
                        ]
                      }),
                      new Paragraph({
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 0, after: 80 },
                        children: [
                          new TextRun({ text: "Xiaomi Mijia Bluetooth Temperature & Humidity Sensor 2", bold: true, size: 14 * 2, color: COLOR_SECONDARY })
                        ]
                      }),
                      new Paragraph({
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 0, after: 0 },
                        children: [
                          new TextRun({ text: "Model Perangkat: LYWSD03MMC | FCC ID: 2AOSD-LYWSD03MMC | Sertifikat Postel SDPPI: 67186/SDPPI/2020", italic: true, size: 9.5 * 2, color: COLOR_MUTED })
                        ]
                      })
                    ]
                  })
                ]
              })
            ]
          }),

          // Info Mahasiswa & Kampus
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 900, after: 120 },
            children: [
              new TextRun({ text: "Disusun Oleh:", italic: true, size: 11 * 2, color: COLOR_MUTED })
            ]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 0, after: 60 },
            children: [
              new TextRun({ text: "NICHOLAS BENAYA", bold: true, size: 14 * 2, color: COLOR_PRIMARY })
            ]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 0, after: 900 },
            children: [
              new TextRun({ text: "NRP: 5024241050", bold: true, size: 12 * 2, color: COLOR_DARK })
            ]
          }),

          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 0, after: 60 },
            children: [
              new TextRun({ text: "Dosen Pengampu: Tim Dosen Desain & Aplikasi IoT", size: 11 * 2, color: COLOR_DARK })
            ]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 0, after: 60 },
            children: [
              new TextRun({ text: "DEPARTEMEN TEKNIK KOMPUTER", bold: true, size: 12 * 2, color: COLOR_PRIMARY })
            ]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 0, after: 60 },
            children: [
              new TextRun({ text: "FAKULTAS TEKNOLOGI ELEKTRO DAN INFORMATIKA CERDAS (FTEIC)", bold: true, size: 11 * 2, color: COLOR_SECONDARY })
            ]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 0, after: 0 },
            children: [
              new TextRun({ text: "INSTITUT TEKNOLOGI SEPULUH NOPEMBER (ITS) SURABAYA\n2026/2027", bold: true, size: 11 * 2, color: COLOR_DARK })
            ]
          }),

          // Page break
          new Paragraph({ pageBreakBefore: true }),

          // DAFTAR ISI & RINGKASAN
          h1("RINGKASAN EKSEKUTIF"),
          p("Laporan ini disusun guna memenuhi Tugas 1 mata kuliah Desain & Aplikasi IoT. Studi kasus yang dipilih adalah produk IoT komersial nirkabel global berdaya ultra-rendah: Xiaomi Mijia Bluetooth Temperature and Humidity Sensor 2 (Model: LYWSD03MMC). Perangkat ini merupakan sensor pemantau mikroklimat cerdas yang dirancang untuk beroperasi secara mandiri menggunakan satu baterai koin CR2032 selama lebih dari satu tahun."),
          p("Pada laporan ini dilakukan dekonstruksi dan analisis menyeluruh meliputi:"),
          bullet("Pemetaan ke model arsitektur 5 lapis IoT (Perception, Network, Middleware, Application, Business) dilengkapi diagram blok komprehensif.", { boldPrefix: "1. Rekonstruksi Arsitektur: " }),
          bullet("Validasi teknis setiap lapis berdasarkan bukti faktual dari sertifikasi FCC ID, sertifikasi Ditjen Postel/SDPPI, teardown perangkat keras, serta datasheet komponen resmi.", { boldPrefix: "2. Bukti & Justifikasi Teknologi: " }),
          bullet("Penerapan langkah 1 (Purpose & Requirements Specification, termasuk 4 syarat nonfungsional kuantitatif terukur), langkah 3 (Domain Model Specification), dan langkah 6 (IoT Level Specification).", { boldPrefix: "3. Metodologi Desain IoT: " }),
          bullet("Perhitungan matematis bertahap konsumsi muatan listrik siklus operasional (sleep, sensing, processing, RF TX) untuk memverifikasi ketahanan baterai.", { boldPrefix: "4. Anggaran Energi & Baterai: " }),
          bullet("Satu halaman tinjauan tajam mengenai kelemahan protokol, privasi, ketergantungan cloud, dan ketiadaan logging lokal, disertai 4 solusi rekayasa modern.", { boldPrefix: "5. Analisis Kritis & Usulan Redesain: " }),

          // Profil Singkat
          h2("Profil Produk Komersial Terpilih"),
          new Table({
            width: { size: 9360, type: WidthType.DXA },
            rows: [
              new TableRow({
                children: [
                  createCell("Parameter", { isHeader: true, width: 2800 }),
                  createCell("Spesifikasi & Rincian Faktual", { isHeader: true, width: 6560 })
                ]
              }),
              new TableRow({
                children: [
                  createCell("Nama Produk Komersial", { bold: true }),
                  createCell("Xiaomi Mijia Bluetooth Temperature and Humidity Sensor 2")
                ]
              }),
              new TableRow({
                children: [
                  createCell("Model Number", { bold: true, bgColor: COLOR_LIGHT_BG }),
                  createCell("LYWSD03MMC", { bgColor: COLOR_LIGHT_BG })
                ]
              }),
              new TableRow({
                children: [
                  createCell("Produsen / Grantee", { bold: true }),
                  createCell("Miaomiaoce Technology (Beijing) Co., Ltd. (Ekosistem Xiaomi / Qingping)")
                ]
              }),
              new TableRow({
                children: [
                  createCell("Sertifikasi FCC ID", { bold: true, bgColor: COLOR_LIGHT_BG }),
                  createCell("2AOSD-LYWSD03MMC (Lolos uji FCC Bagian 15C / DTS - Digital Transmission System)", { bgColor: COLOR_LIGHT_BG })
                ]
              }),
              new TableRow({
                children: [
                  createCell("Sertifikasi Postel / Kominfo", { bold: true }),
                  createCell("Sertifikat SDPPI No. 67186/SDPPI/2020 (Distributor: PT. Xiaomi Technology Indonesia)")
                ]
              }),
              new TableRow({
                children: [
                  createCell("Main Controller (SoC)", { bold: true, bgColor: COLOR_LIGHT_BG }),
                  createCell("Telink TLSR8251F512ET / TLSR8258 (32-bit Proprietary RISC MCU, 512KB Flash, 64KB SRAM)", { bgColor: COLOR_LIGHT_BG })
                ]
              }),
              new TableRow({
                children: [
                  createCell("Sensor Lingkungan", { bold: true }),
                  createCell("Sensirion SHTC3 Digital Sensor (Antarmuka I2C, Suhu -40..125°C, RH 0..100%)")
                ]
              }),
              new TableRow({
                children: [
                  createCell("Display Lokal", { bold: true, bgColor: COLOR_LIGHT_BG }),
                  createCell("1.5 Inch Custom Segmented Monochrome LCD (Direct GPIO driving, no external IC)", { bgColor: COLOR_LIGHT_BG })
                ]
              }),
              new TableRow({
                children: [
                  createCell("Protokol Nirkabel", { bold: true }),
                  createCell("Bluetooth Low Energy (BLE 4.2 / BLE 5.0 LE) – Mi Beacon Advertising Broadcast")
                ]
              }),
              new TableRow({
                children: [
                  createCell("Catu Daya", { bold: true, bgColor: COLOR_LIGHT_BG }),
                  createCell("1x Baterai Koin Lithium CR2032 (3.0 V, 220 mAh)", { bgColor: COLOR_LIGHT_BG })
                ]
              }),
              new TableRow({
                children: [
                  createCell("Dimensi & Bobot", { bold: true }),
                  createCell("43 mm x 43 mm x 12.5 mm | Berat bersih: 21 gram (dengan baterai)")
                ]
              })
            ]
          }),

          // Page break
          new Paragraph({ pageBreakBefore: true }),

          // BAGIAN 1
          h1("BAGIAN 1: REKONSTRUKSI ARSITEKTUR DAN PEMETAAN MODEL 5 LAPIS IOT"),
          p("Arsitektur Internet of Things (IoT) pada sistem skala komersial umumnya dipetakan ke dalam model referensi 5 lapis (5-Layer IoT Architecture) untuk menggambarkan aliran data secara berjenjang dari instrumen fisik ke pengambil keputusan bisnis: Perception Layer, Network/Communication Layer, Middleware/Processing Layer, Application Layer, dan Business Layer."),

          h2("1.1 Diagram Blok Arsitektur Buatan Sendiri"),
          p("Berikut adalah rekonstruksi diagram blok arsitektur end-to-end Xiaomi Mijia LYWSD03MMC dari level node fisik hingga cloud and enterprise business layer:"),

          // Table representing architecture diagram blocks
          new Table({
            width: { size: 9360, type: WidthType.DXA },
            rows: [
              new TableRow({
                children: [
                  createCell("LAPIS ARSITEKTUR", { isHeader: true, width: 2200, align: AlignmentType.CENTER }),
                  createCell("KOMPONEN, TEKNOLOGI & ENTITAS", { isHeader: true, width: 4360, align: AlignmentType.CENTER }),
                  createCell("PROTOKOL & INTERFACE", { isHeader: true, width: 2800, align: AlignmentType.CENTER })
                ]
              }),
              new TableRow({
                children: [
                  createCell("5. Business Layer\n(Lapis Bisnis)", { bold: true, bgColor: "EBF8FF", align: AlignmentType.CENTER }),
                  createCell("• Manajemen Armada Produk (FOTA & Lifecycle)\n• Big Data Analytics Kenyamanan Hunian\n• Integrasi Ekosistem & Monetisasi Produk Xiaomi\n• Kebijakan Privasi (GDPR & UU PDP No. 27/2022)"),
                  createCell("Enterprise BI Dashboard,\nERP Xiaomi Eco,\nCloud Billing / User Tier")
                ]
              }),
              new TableRow({
                children: [
                  createCell("4. Application Layer\n(Lapis Aplikasi)", { bold: true, bgColor: "EDFDFD", align: AlignmentType.CENTER }),
                  createCell("• Mi Home / Xiaomi Home Mobile App (Android/iOS)\n• Voice Assistant (Google Assistant, Alexa, XiaoAI)\n• Home Assistant (Integrasi BLE BTHome / Passive)\n• Visualisasi Grafik Suhu & Kelembaban Historis"),
                  createCell("Mobile GUI (Flutter/React Native),\nREST API, WebSocket,\nPush Notification (APNs, FCM)")
                ]
              }),
              new TableRow({
                children: [
                  createCell("3. Middleware / Processing Layer\n(Lapis Pemrosesan)", { bold: true, bgColor: "F0FFF4", align: AlignmentType.CENTER }),
                  createCell("• Xiaomi IoT Core / Cloud API Gateway\n• MQTT Broker (EMQX Cluster) & Ingestion Engine\n• Time-Series Database (TSDB / InfluxDB)\n• Automation Rule Engine (Otomasi Smart AC / Humidifier)\n• Kriptografi: AES-128 CCM Decryption & Device Auth"),
                  createCell("MQTT / TLS 1.3,\nCoAP, JSON Schema,\nKafka Stream Processor,\nRedis Cache / TSDB")
                ]
              }),
              new TableRow({
                children: [
                  createCell("2. Network Layer\n(Lapis Jaringan)", { bold: true, bgColor: "FEFCBF", align: AlignmentType.CENTER }),
                  createCell("• Transmisi Nirkabel Lokal: BLE 5.0 LE Beacon\n• Hub Perantara: Xiaomi Smart Multimode Gateway (ZNDMWG02LM)\n• Gateway Backhaul: Wi-Fi IEEE 802.11 b/g/n (2.4 GHz)\n• Jaringan Publik: Internet Router / WAN (IPv4/TCP)"),
                  createCell("BLE Advertising (Ch 37,38,39),\nMi Beacon V4/V5 Protocol,\nWi-Fi WPA2/WPA3,\nIP / TCP / TLS")
                ]
              }),
              new TableRow({
                children: [
                  createCell("1. Perception Layer\n(Lapis Fisik / Persepsi)", { bold: true, bgColor: "FFF5F5", align: AlignmentType.CENTER }),
                  createCell("• Sensor Suhu & RH Digital: Sensirion SHTC3\n• Unit Pengolah: Telink TLSR8251 32-bit RISC SoC\n• Layar Penampil: 1.5 Inch Monochrome Segment LCD\n• Antena: On-board Inverted-F PCB Meander Antenna\n• Sumber Daya: 1x Baterai Koin CR2032 (3V, 220 mAh)"),
                  createCell("Antarmuka I2C (Clock 400 kHz),\nGPIO Static Direct Bias (LCD),\nInternal ADC & Power Rail (2.0 - 3.6V)")
                ]
              })
            ]
          }),

          h2("1.2 Penjelasan Rinci Setiap Lapis"),
          pMulti([
            { text: "1. Perception Layer (Lapis Persepsi): ", bold: true, color: COLOR_PRIMARY },
            { text: "Berfungsi mengonversi besaran fisik lingkungan (suhu udara dan kadar air relatif) menjadi sinyal digital. Sensor Sensirion SHTC3 melakukan transduksi kapasitif dan celah pita silikon, kemudian mengirimkan frame data 16-bit nilai suhu dan kelembaban melalui bus I2C ke SoC Telink TLSR8251. SoC ini juga mengontrol segmen LCD untuk menampilkan data secara lokal kepada penghuni ruangan tanpa membutuhkan aktivasi radio." }
          ]),
          pMulti([
            { text: "2. Network Layer (Lapis Jaringan): ", bold: true, color: COLOR_PRIMARY },
            { text: "Bertanggung jawab mentransmisikan data dari simpul end-device. Mengingat baterai CR2032 memiliki kapasitas sangat terbatas, LYWSD03MMC tidak menggunakan Wi-Fi mandiri, melainkan memancarkan paket broadcast BLE Advertising (Mi Beacon frame) pada kanal 37, 38, dan 39. Paket ini ditangkap oleh Xiaomi Multimode Gateway yang berada dalam radius 10-15 meter. Gateway berfungsi sebagai jembatan protokol (protocol translation) yang membungkus payload BLE ke dalam paket TCP/IP terenkripsi TLS dan mengirimkannya melalui Wi-Fi router rumah ke internet." }
          ]),
          pMulti([
            { text: "3. Middleware / Processing Layer (Lapis Pemrosesan): ", bold: true, color: COLOR_PRIMARY },
            { text: "Berada pada infrastruktur server Xiaomi Mi Cloud. Terdiri dari Message Broker berbasis MQTT skala masif, parser paket biner Mi Beacon, verifikasi keaslian pesan menggunakan kunci simetris AES-128 (Token autentikasi), basis data deret waktu (TSDB) untuk merekam riwayat historis, serta mesin aturan (Rule Engine). Mesin aturan mengevaluasi kondisi logika secara terus-menerus, misalnya memicu perintah 'Nyalakan Smart Plug Dehumidifier jika kelembaban > 70%'." }
          ]),
          pMulti([
            { text: "4. Application Layer (Lapis Aplikasi): ", bold: true, color: COLOR_PRIMARY },
            { text: "Menyediakan antarmuka manusia-mesin bagi pengguna akhir melalui aplikasi seluler Mi Home / Xiaomi Home (tersedia di Google Play Store dan Apple App Store). Menampilkan gauge suhu/kelembaban dinamis, indikator kenyamanan (Baby Mode), kurva tren harian/bulanan, ekspor data, serta integrasi asisten suara (Google Home, Alexa, Siri Shortcuts)." }
          ]),
          pMulti([
            { text: "5. Business Layer (Lapis Bisnis): ", bold: true, color: COLOR_PRIMARY },
            { text: "Mengelola keseluruhan siklus hidup perangkat, pembaruan firmware berkala via FOTA (Firmware Over-The-Air) melalui gateway, analisis agregat data penggunaan energi pelanggan, kepatuhan terhadap regulasi privasi konsumen (GDPR dan UU PDP No. 27/2022), serta strategi cross-selling perangkat pintar lain dalam ekosistem Xiaomi." }
          ]),

          // Page break
          new Paragraph({ pageBreakBefore: true }),

          // BAGIAN 2
          h1("BAGIAN 2: IDENTIFIKASI & JUSTIFIKASI TEKNOLOGI DENGAN BUKTI DOKUMENTASI RESMI"),
          p("Setiap klaim komponen, protokol, dan teknologi pada setiap lapis wajib diverifikasi secara empiris melalui dokumen otentik yang dapat diakses publik, meliputi sertifikasi regulator nirkabel, laporan teardown daring, dan datasheet resmi pabrikan komponen."),

          new Table({
            width: { size: 9360, type: WidthType.DXA },
            rows: [
              new TableRow({
                children: [
                  createCell("Lapis", { isHeader: true, width: 1400 }),
                  createCell("Komponen / Modul", { isHeader: true, width: 2200 }),
                  createCell("Teknologi Spesifik", { isHeader: true, width: 2500 }),
                  createCell("Bukti Faktual & Sumber Rujukan", { isHeader: true, width: 3260 })
                ]
              }),
              new TableRow({
                children: [
                  createCell("Perception"),
                  createCell("Microcontroller & RF SoC", { bold: true }),
                  createCell("Telink TLSR8251F512ET (32-bit RISC, 512KB Flash, 64KB SRAM, BLE 5.0)"),
                  createCell("Datasheet Telink Doc ID: DS-TLSR8258-E13 & Foto Teardown FCC Internal PCB.")
                ]
              }),
              new TableRow({
                children: [
                  createCell("Perception", { bgColor: COLOR_LIGHT_BG }),
                  createCell("Sensor Suhu & Kelembaban", { bold: true, bgColor: COLOR_LIGHT_BG }),
                  createCell("Sensirion SHTC3 (CMOSens Tech, I2C, ±0.2°C, ±2% RH)", { bgColor: COLOR_LIGHT_BG }),
                  createCell("Datasheet Sensirion SHTC3 Rev. 1 & Marking IC '3C' pada PCB teardown.", { bgColor: COLOR_LIGHT_BG })
                ]
              }),
              new TableRow({
                children: [
                  createCell("Perception"),
                  createCell("Display Lokal", { bold: true }),
                  createCell("1.5” Custom Segment LCD (Static drive via GPIO langsung)"),
                  createCell("Dokumentasi Teardown Daring (Pogo-pin rubber connector ke LCD).")
                ]
              }),
              new TableRow({
                children: [
                  createCell("Network", { bgColor: COLOR_LIGHT_BG }),
                  createCell("Transmisi Radio Lokal", { bold: true, bgColor: COLOR_LIGHT_BG }),
                  createCell("BLE 5.0 (2402 - 2480 MHz, GFSK, daya pancar +4.2 dBm)", { bgColor: COLOR_LIGHT_BG }),
                  createCell("FCC Test Report Report No. BCTC-FY191006509E (FCC ID: 2AOSD-LYWSD03MMC).", { bgColor: COLOR_LIGHT_BG })
                ]
              }),
              new TableRow({
                children: [
                  createCell("Network"),
                  createCell("Legalitas Radio Nasional", { bold: true }),
                  createCell("Alokasi Frekuensi 2.4 GHz ISM Indonesia"),
                  createCell("Sertifikat SDPPI Ditjen Postel Kominfo No. 67186/SDPPI/2020.")
                ]
              }),
              new TableRow({
                children: [
                  createCell("Middleware", { bgColor: COLOR_LIGHT_BG }),
                  createCell("Protokol Payload & Broker", { bold: true, bgColor: COLOR_LIGHT_BG }),
                  createCell("Mi Beacon V4/V5, AES-128 Encryption, Cloud MQTT Broker", { bgColor: COLOR_LIGHT_BG }),
                  createCell("Xiaomi IoT Developer Platform Documentation & Reverse-Engineering BTHome.", { bgColor: COLOR_LIGHT_BG })
                ]
              }),
              new TableRow({
                children: [
                  createCell("Application"),
                  createCell("Mobile Client App", { bold: true }),
                  createCell("Mi Home Application (Android v8.x / iOS v8.x)"),
                  createCell("Google Play Store & Apple App Store ID: com.xiaomi.smarthome.")
                ]
              })
            ]
          }),

          h2("2.1 Uraian Bukti Teknis"),
          bullet("Berdasarkan berkas sertifikasi resmi FCC Amerika Serikat (FCC ID: 2AOSD-LYWSD03MMC), pengujian radio menunjukkan perangkat beroperasi pada pita frekuensi 2402 MHz hingga 2480 MHz dengan 40 kanal modulasi GFSK. Daya keluaran puncak terukur (Peak Conducted Output Power) adalah +4.2 dBm (~2.63 mW) dengan gain antena PCB sebesar +0.5 dBi.", { boldPrefix: "1. Sertifikasi FCC ID: 2AOSD-LYWSD03MMC: " }),
          bullet("Pemerintah Indonesia melalui Kementerian Komunikasi dan Informatika (Kominfo / SDPPI) menerbitkan sertifikat nomor 67186/SDPPI/2020 kepada PT. Xiaomi Technology Indonesia. Hal ini membuktikan bahwa perangkat telah memenuhi baku mutu transmisi frekuensi nirkabel yang sah di wilayah Republik Indonesia.", { boldPrefix: "2. Sertifikasi Postel SDPPI Indonesia: " }),
          bullet("Hasil pembongkaran perangkat (hardware teardown) memperlihatkan papan PCB sirkuit ganda yang sangat minimalis dan efisien. Di atas PCB terdapat satu chip utama bermerek Telink TLSR8251F512ET. Datasheet pabrikan (Telink Semiconductor) mengonfirmasi bahwa chip ini memiliki konsumsi arus deep sleep serendah 0.7 - 1.2 uA dengan internal SRAM retention dan internal DC-DC buck converter terintegrasi, menghilangkan kebutuhan IC voltage regulator eksternal sehingga tidak ada daya yang terbuang sia-sia.", { boldPrefix: "3. Datasheet & Teardown SoC Telink TLSR8251: " }),
          bullet("IC sensor suhu dan kelembaban ditandai dengan kode SMD '3C' yang merupakan identitas resmi pabrikan Sensirion AG (Swiss) untuk seri SHTC3. Datasheet Sensirion menyatakan konsumsi arus pengukuran hanya 0.15 mA selama 12.1 ms, dan konsumsi arus mode siaga (sleep mode) hanya 0.2 uA. Sensor berkomunikasi melalui jalur serial I2C standard-mode (100 kHz) dan fast-mode (400 kHz) pada alamat I2C 0x70.", { boldPrefix: "4. Datasheet Sensor Sensirion SHTC3: " }),

          // Page break
          new Paragraph({ pageBreakBefore: true }),

          // BAGIAN 3
          h1("BAGIAN 3: PENERAPAN METODOLOGI DESAIN IOT (LANGKAH 1, 3, DAN 6)"),
          p("Mengacu pada metodologi perancangan sistem IoT standar industri oleh Arshdeep Bahga dan Vijay Madisetti ('Internet of Things: A Hands-On Approach', 2014), berikut adalah susunan ulang perancangan untuk Langkah 1, Langkah 3, dan Langkah 6."),

          h2("3.1 Langkah 1: Purpose & Requirements Specification"),
          pMulti([
            { text: "A. Tujuan Sistem (Purpose): ", bold: true },
            { text: "Menyediakan pemantauan kondisi suhu udara dan kelembaban relatif dalam ruang hunian secara mandiri, akurat, real-time, berdaya ultra-rendah, serta terintegrasi mulus ke dalam platform otomasi rumah cerdas guna meningkatkan kenyamanan termal dan efisiensi pemakaian energi." }
          ]),
          pMulti([
            { text: "B. Perilaku Sistem (Behavior): ", bold: true },
            { text: "Perangkat membaca sensor lingkungan secara periodik, menampilkan hasil pembacaan di layar LCD secara lokal, serta mengemas data tersebut ke dalam frame paket nirkabel BLE Advertising (Mi Beacon). Paket ini dipancarkan secara berkala sehingga gateway terdekat dapat menangkapnya dan meneruskannya ke server cloud tanpa memerlukan proses pairing nirkabel yang memakan waktu dan energi." }
          ]),
          pMulti([
            { text: "C. Persyaratan Fungsional (Functional Requirements):", bold: true }
          ]),
          bullet("Sistem mampu mengukur temperatur pada rentang 0.0°C hingga 60.0°C dan kelembaban relatif 0% hingga 99% RH.", { boldPrefix: "FR-01: " }),
          bullet("Sistem wajib menampilkan angka suhu, kelembaban, dan ikon ekspresi kenyamanan (kenyamanan termal) pada layar LCD fisik.", { boldPrefix: "FR-02: " }),
          bullet("Sistem mampu memancarkan paket telemetri nirkabel BLE Advertising berkala berisi payload terenkripsi identitas perangkat, suhu, kelembaban, dan status baterai.", { boldPrefix: "FR-03: " }),
          bullet("Sistem mendukung integrasi cloud melalui gateway untuk pemicu otomatisasi (automation rule trigger) dan perekaman data historis.", { boldPrefix: "FR-04: " }),

          pMulti([
            { text: "D. Persyaratan Non-Fungsional Terukur (Minimal 3 Terukur):", bold: true }
          ]),
          bullet("Node sensor harus dapat beroperasi terus-menerus selama minimal 12 bulan (1 tahun kalender) hanya dengan menggunakan 1 unit baterai koin CR2032 (kapasitas nominal 220 mAh) pada kondisi operasional ruangan normal (20–30°C).", { boldPrefix: "NFR-01 (Masa Pakai Baterai): " }),
          bullet("Pengukuran temperatur harus memiliki akurasi deviasi maksimal ±0.3°C pada rentang 10°C–40°C dengan resolusi pembacaan 0.1°C; pengukuran kelembaban memiliki toleransi maksimal ±3% RH pada rentang 20%–80% RH dengan resolusi 1% RH.", { boldPrefix: "NFR-02 (Akurasi & Resolusi): " }),
          bullet("Layar LCD lokal harus memperbarui angka pembacaan maksimal setiap 1.0 detik (latensi persepsi instan), dan transmisi siaran nirkabel RF harus diperbarui maksimal 10 detik saat terjadi perubahan nilai delta > 0.5°C atau kelembaban > 5% RH, serta maksimal 10 menit saat kondisi statis.", { boldPrefix: "NFR-03 (Latensi Pembaruan Data): " }),
          bullet("Dimensi fisik bodi perangkat tidak boleh melebihi 45 mm x 45 mm x 13 mm dengan bobot total maksimal 25 gram (termasuk baterai) agar dapat ditempelkan di dinding menggunakan perekat ganda tanpa risiko terjatuh.", { boldPrefix: "NFR-04 (Ergonomi & Form Factor): " }),

          h2("3.2 Langkah 3: Domain Model Specification"),
          p("Spesifikasi Domain Model memetakan seluruh entitas dunia nyata, representasi digital, perangkat keras, sumber daya, dan layanan ke dalam relasi ontologi sistem:"),

          bullet("Ruang hunian fisik (kamar tidur, ruang keluarga, ruang kerja), atmosfer udara sekitar dengan parameter termodinamika suhu (°C) dan uap air (% RH).", { boldPrefix: "1. Physical Entities: " }),
          bullet("Representasi status digital di Mi Cloud dan aplikasi Mi Home (Device ID, AmbientTemperature, RelativeHumidity, BatteryPercentage, ComfortIndex, Timestamp).", { boldPrefix: "2. Virtual Entities: " }),
          bullet("Node Sensor LYWSD03MMC (SoC Telink TLSR8251 + SHTC3), Xiaomi Smart Multimode Gateway (ZNDMWG02LM), dan Smartphone Pengguna.", { boldPrefix: "3. Devices: " }),
          bullet("On-device memory (Register I2C, buffer iklan BLE, registers SRAM dengan retensi); Network resource (Topic MQTT '/miio/report', Endpoint REST Cloud API).", { boldPrefix: "4. Resources: " }),
          bullet("Sensing Service (akuisisi data dari SHTC3), LCD Rendering Service (penulisan segmen display), BLE Beaconing Service (pemancaran paket nirkabel), Cloud Ingestion Service (pengumpulan data di server), Alert & Automation Service (eksekusi aksi jika batas ambang terlampaui).", { boldPrefix: "5. Services: " }),

          h2("3.3 Langkah 6: IoT Level Specification (Level 1–6)"),
          callout("KLASIFIKASI TINGKAT IOT: IOT LEVEL 5", "Berdasarkan taksonomi 6 tingkat arsitektur IoT menurut Bahga & Madisetti, sistem komersial Xiaomi Mijia LYWSD03MMC termasuk ke dalam kategori IOT LEVEL 5 (Multiple Nodes, Single Coordinator/Gateway Node, Centralized Cloud Database & Cloud Analytics)."),
          p("Justifikasi mendalam mengapa sistem ini merupakan IoT Level 5:"),
          bullet("Dalam perancangan smart home, biasanya dipasang beberapa node LYWSD03MMC di berbagai ruangan (kamar tidur 1, kamar tidur 2, ruang tamu, dapur).", { boldPrefix: "1. Karakteristik Multiple End-Nodes: " }),
          bullet("Karena menggunakan BLE berdaya sangat rendah, node sensor tidak dapat berkomunikasi langsung menggunakan protokol IP/Internet. Oleh karena itu, diperlukan satu simpul Koordinator (Coordinator / Gateway Node), yaitu Xiaomi Smart Gateway / Smart Speaker. Koordinator ini bertugas menghimpun (mengagregasi) seluruh paket BLE dari berbagai sensor di sekelilingnya, melakukan translasi protokol menjadi paket TCP/IP, lalu mengirimkannya melalui koneksi Wi-Fi/Ethernet ke internet.", { boldPrefix: "2. Keberadaan Simpul Koordinator (Gateway Node): " }),
          bullet("Seluruh data pengukuran dari berbagai node disimpan secara terpusat pada basis data cloud Xiaomi (Mi Cloud) dan diproses oleh mesin analitik cloud untuk memicu automasi antarperangkat dan menyajikan grafik riwayat ke smartphone pengguna dari mana saja (akses jarak jauh).", { boldPrefix: "3. Basis Data & Analitik di Cloud: " }),
          bullet("Level 1 hanya terdiri dari satu simpul dengan penyimpanan dan aplikasi lokal; Level 2 adalah satu simpul yang mengirim data ke cloud; Level 3 adalah satu simpul dengan analitik di cloud; Level 4 memiliki banyak simpul yang masing-masing mengirim langsung ke cloud (misal sensor berkoneksi Wi-Fi/4G langsung tanpa koordinator); Level 6 menggunakan arsitektur Big Data terdistribusi multi-cloud. Maka, kehadiran 'Node Koordinator/Gateway Perantara' pada topologi multi-node BLE ini secara mutlak mendefinisikan sistem sebagai IoT Level 5.", { boldPrefix: "4. Eliminasi Level Lainnya: " }),

          // Page break
          new Paragraph({ pageBreakBefore: true }),

          // BAGIAN 4
          h1("BAGIAN 4: ANGGARAN ENERGI NODE DAN ESTIMASI UMUR BATERAI"),
          p("Mengacu pada format perhitungan anggaran energi node (sebagaimana dicontohkan pada Slide 40 materi kuliah Desain & Aplikasi IoT), analisis dilakukan dengan menghitung profil konsumsi arus pada setiap fasa operasional perangkat dalam satu siklus waktu periodik."),

          h2("4.1 Karakteristik Catu Daya"),
          bullet("Baterai koin Lithium Manganese Dioxide (Li/MnO2) tipe CR2032 (tegangan nominal 3.0 V).", { boldPrefix: "Tipe Baterai: " }),
          bullet("220 mAh = 220,000 uAh (pada pelepasan arus rendah konstan hingga cut-off 2.0 V).", { boldPrefix: "Kapasitas Nominal (C_nom): " }),
          bullet("Ditetapkan η = 0.85 (85%) untuk mengakomodasi self-discharge kimia baterai (~1% per tahun) dan penurunan efisiensi pada suhu lingkungan bervariasi.", { boldPrefix: "Faktor Derating / Efisiensi (η): " }),
          bullet("C_eff = 220 mAh x 0.85 = 187 mAh = 187,000 uAh.", { boldPrefix: "Kapasitas Efektif (C_eff): " }),

          h2("4.2 Dekomposisi Fasa Operasional (Siklus T = 10 Detik)"),
          p("Perangkat dirancang dengan siklus kerja (duty cycle) yang sangat rendah. Satu siklus waktu periodik berlangsung selama T_cycle = 10 detik (10,000 ms), yang terbagi ke dalam 4 tahapan / fasa kerja:"),

          new Table({
            width: { size: 9360, type: WidthType.DXA },
            rows: [
              new TableRow({
                children: [
                  createCell("Fasa Operasional (State)", { isHeader: true, width: 2200 }),
                  createCell("Aktivitas Perangkat Keras", { isHeader: true, width: 3360 }),
                  createCell("Arus (I)", { isHeader: true, width: 1800, align: AlignmentType.RIGHT }),
                  createCell("Durasi (t)", { isHeader: true, width: 2000, align: AlignmentType.RIGHT })
                ]
              }),
              new TableRow({
                children: [
                  createCell("State 1: Deep Sleep", { bold: true }),
                  createCell("MCU sleep mode (timer aktif, retention ON), SHTC3 standby, LCD static segment bias"),
                  createCell("2.20 uA\n(0.0022 mA)", { align: AlignmentType.RIGHT }),
                  createCell("9,950 ms\n(9.950 s)", { align: AlignmentType.RIGHT })
                ]
              }),
              new TableRow({
                children: [
                  createCell("State 2: Sensor Read", { bold: true, bgColor: COLOR_LIGHT_BG }),
                  createCell("MCU wakeup, clock 24MHz aktif, akuisisi I2C SHTC3 measurement mode", { bgColor: COLOR_LIGHT_BG }),
                  createCell("4.15 mA\n(4,150 uA)", { align: AlignmentType.RIGHT, bgColor: COLOR_LIGHT_BG }),
                  createCell("12 ms\n(0.012 s)", { align: AlignmentType.RIGHT, bgColor: COLOR_LIGHT_BG })
                ]
              }),
              new TableRow({
                children: [
                  createCell("State 3: Data Processing", { bold: true }),
                  createCell("Konversi rumus data biner, pembaruan frame register LCD lokal"),
                  createCell("4.00 mA\n(4,000 uA)", { align: AlignmentType.RIGHT }),
                  createCell("3 ms\n(0.003 s)", { align: AlignmentType.RIGHT })
                ]
              }),
              new TableRow({
                children: [
                  createCell("State 4: BLE Broadcast TX", { bold: true, bgColor: COLOR_LIGHT_BG }),
                  createCell("Radio TX aktif pada kanal 37, 38, 39 (daya pancar +0 dBm, 3 paket siaran)", { bgColor: COLOR_LIGHT_BG }),
                  createCell("9.50 mA\n(9,500 uA)", { align: AlignmentType.RIGHT, bgColor: COLOR_LIGHT_BG }),
                  createCell("5 ms\n(0.005 s)", { align: AlignmentType.RIGHT, bgColor: COLOR_LIGHT_BG })
                ]
              }),
              new TableRow({
                children: [
                  createCell("TOTAL SIKLUS", { isHeader: true, colSpan: 3 }),
                  createCell("10,000 ms (10.0 s)", { isHeader: true, align: AlignmentType.RIGHT })
                ]
              })
            ]
          }),

          h2("4.3 Perhitungan Matematis Muatan Listrik dan Umur Baterai"),
          p("Muatan listrik total dalam satu siklus (Q_cycle) dihitung dengan menjumlahkan hasil kali arus dan durasi pada masing-masing fasa:"),
          p("Q_cycle = Σ (I_i x t_i) = Q_sleep + Q_read + Q_proc + Q_tx", { italic: true, bold: true }),

          bullet("Q_sleep = 2.20 uA x 9.950 s = 21.890 uAs (microampere-detik)", { boldPrefix: "• Muatan State 1 (Sleep): " }),
          bullet("Q_read = 4,150 uA x 0.012 s = 49.800 uAs", { boldPrefix: "• Muatan State 2 (Sensing): " }),
          bullet("Q_proc = 4,000 uA x 0.003 s = 12.000 uAs", { boldPrefix: "• Muatan State 3 (Processing): " }),
          bullet("Q_tx = 9,500 uA x 0.005 s = 47.500 uAs", { boldPrefix: "• Muatan State 4 (BLE TX): " }),

          p("Total muatan per siklus 10 detik:", { bold: true }),
          p("Q_cycle = 21.890 + 49.800 + 12.000 + 47.500 = 131.190 uAs", { bold: true, size: 12, color: COLOR_PRIMARY }),

          p("Arus Rata-rata Siklus Operasional (I_avg):"),
          p("I_avg = Q_cycle / T_cycle = 131.190 uAs / 10 s = 13.119 uA  (~ 0.01312 mA)", { bold: true, size: 12, color: COLOR_SECONDARY }),

          p("Estimasi Masa Pakai Baterai (Battery Lifetime):"),
          bullet("Lifetime (Jam) = C_eff / I_avg = 187,000 uAh / 13.119 uA ≈ 14,254.1 Jam", { boldPrefix: "1. Dalam Satuan Jam: " }),
          bullet("Lifetime (Hari) = 14,254.1 Jam / 24 Jam/Hari ≈ 593.9 Hari", { boldPrefix: "2. Dalam Satuan Hari: " }),
          bullet("Lifetime (Bulan) = 593.9 Hari / 30.416 Hari/Bulan ≈ 19.53 Bulan", { boldPrefix: "3. Dalam Satuan Bulan: " }),
          bullet("Lifetime (Tahun) = 593.9 Hari / 365 Hari/Tahun ≈ 1.63 Tahun (~ 19.5 Bulan)", { boldPrefix: "4. Dalam Satuan Tahun: " }),

          callout("KESIMPULAN PERHITUNGAN BATERAI", "Berdasarkan kalkulasi saintifik, node LYWSD03MMC memiliki estimasi umur baterai sebesar 1.63 tahun (sekitar 19.5 bulan). Nilai ini memvalidasi klaim resmi spesifikasi pabrikan Xiaomi yang menyatakan masa pakai '1 tahun' dengan menyediakan safety margin sebesar ~38% untuk mengantisipasi baterai berkualitas rendah atau suhu dingin ekstrem."),

          // Page break
          new Paragraph({ pageBreakBefore: true }),

          // BAGIAN 5
          h1("BAGIAN 5: ANALISIS KRITIS (1 HALAMAN PENUH)"),
          p("Sebagai mahasiswa Teknik Komputer, analisis kritis tidak hanya mengapresiasi keunggulan desain komersial Xiaomi LYWSD03MMC dalam hal efisiensi biaya dan daya, namun juga mengidentifikasi kelemahan mendasar dalam aspek arsitektur, keamanan, keandalan, dan ketergantungan ekosistem, serta merumuskan usulan modifikasi konkret."),

          h2("5.1 Kelemahan Rancangan Eksisting"),
          bullet("Perangkat LYWSD03MMC bergantung penuh pada gateway perantara Xiaomi (Hub BLE) untuk dapat terhubung ke internet. Pengguna yang tidak memiliki hub Xiaomi hanya dapat membaca data secara jarak dekat via Bluetooth ponsel. Ketergantungan ini menciptakan 'walled-garden vendor lock-in', di mana integrasi lintas platform (seperti Google Home atau Apple HomeKit) menjadi sangat lambat, tidak langsung, dan terputus jika server Xiaomi Cloud mengalami pemeliharaan (downtime).", { boldPrefix: "1. Ketergantungan Ekosistem Cloud Proprietary & Latensi Gateway: " }),
          bullet("Paket siaran Mi Beacon secara default memancarkan data suhu dan kelembaban tanpa enkripsi muatan penuh pada lapisan iklan BLE (hanya menggunakan checksum sederhana pada beberapa versi firmware). Akibatnya, penyerang di sekitar lokasi dapat dengan mudah melakukan sniffing / eavesdropping terhadap kondisi kenyamanan ruangan pengguna atau bahkan melakukan spoofing data suhu palsu untuk mengelabui otomasi pendingin ruangan.", { boldPrefix: "2. Celah Keamanan Protokol Nirkabel & Spoofing: " }),
          bullet("Node sensor tidak dilengkapi memori non-volatile eksternal (seperti SPI Flash atau EEPROM) untuk pencatatan mandiri (on-board data logging). Jika koneksi ke gateway terputus selama beberapa hari (misalnya karena mati listrik atau router Wi-Fi bermasalah), seluruh rekaman telemetri suhu dan kelembaban selama periode tersebut hilang permanen karena node tidak memiliki buffer penyimpan.", { boldPrefix: "3. Ketiadaan On-Board Data Logging saat Jaringan Putus: " }),
          bullet("Casing plastik ABS perangkat memiliki celah ventilasi terbuka di bagian belakang tanpa lapisan conformal coating pada PCB dan tanpa sertifikasi Ingress Protection (IP rating). Kondisi ini menyebabkan perangkat rentan mengalami korosi atau short-circuit jika ditempatkan di area berkelembaban tinggi seperti kamar mandi, rumah kaca pertanian (greenhouse), atau area outdoor.", { boldPrefix: "4. Kerapuhan Lingkungan Fisik (Non-Weatherproof): " }),

          h2("5.2 Usulan Rekayasa Perbaikan & Modifikasi Arsitektur"),
          p("Untuk mengatasi keempat kelemahan di atas, diajukan 4 usulan rekayasa modifikasi konkret sebagai bentuk peningkatan desain (redesign):"),

          bullet("Mengganti firmware BLE proprietary dengan protokol standar terbuka berbasis Matter-over-Thread (IEEE 802.15.4 pada frekuensi 2.4 GHz). Thread menghadirkan topologi mesh IP berdaya rendah (IPv6 addressable) yang dapat berkomunikasi langsung secara lokal (local-first communication) ke smart speaker/border router mana pun (Google Nest, Apple HomePod, Amazon Echo) tanpa ketergantungan cloud pihak ketiga, memangkas latensi otomasi dari 1.5–3 detik menjadi kurang dari 100 ms.", { boldPrefix: "1. Migrasi ke Standar Terbuka Matter-over-Thread: " }),
          bullet("Menerapkan kriptografi berstandar militer AES-CCM 128-bit terakselerasi perangkat keras dengan mekanisme rolling monotonic counter dan ephemeral key. Hal ini mencegah serangan replay attack, manipulasi paket data broadcast, serta menjamin kerahasiaan telemetri penghuni ruangan.", { boldPrefix: "2. Penguatan Enkripsi End-to-End & Anti-Replay: " }),
          bullet("Menambahkan IC memori SPI EEPROM berdaya ultra-rendah 64 KB (misalnya Microchip 24AA64) atau FRAM (Fujitsu MB85RC) yang hanya mengonsumsi arus ~1 uA saat standby. Memori ini difungsikan sebagai buffer sirkular ring yang mampu menyimpan riwayat data hingga 30 hari saat node offline. Saat koneksi gateway pulih, node melakukan sinkronisasi data backfill otomatis.", { boldPrefix: "3. Penambahan On-Board Non-Volatile Data Logger: " }),
          bullet("Menyematkan panel surya mini berbasis Amorphous Silicon (PV Cell) berukuran 30 mm x 10 mm pada bezel depan casing yang dipasangkan dengan superkapasitor 0.22 F atau baterai isi ulang LTO (Lithium Titanate). Panel surya dalam ruangan (indoor lighting 200–500 lux) mampu menghasilkan daya 10–25 uW, cukup untuk menopang kebutuhan rata-rata perangkat (13.1 uW), mewujudkan node sensor mandiri energi sejati tanpa perlu penggantian baterai koin berkala (Zero-Battery Maintenance / Self-Powered IoT).", { boldPrefix: "4. Integrasi Indoor Energy Harvesting: " }),

          // Page break
          new Paragraph({ pageBreakBefore: true }),

          // DAFTAR PUSTAKA
          h1("DAFTAR PUSTAKA & REFERENSI RESMI"),
          bullet("Bahga, A., & Madisetti, V. (2014). Internet of Things: A Hands-On Approach. Universities Press (India) Pvt. Ltd. (Metodologi Desain Langkah 1, 3, 6, dan Klasifikasi IoT Level 1–6).", { size: 10 }),
          bullet("Federal Communications Commission (FCC). (2019). Test Report for Digital Transmission System (DTS) - FCC ID: 2AOSD-LYWSD03MMC. Miaomiaoce Technology (Beijing) Co., Ltd. Shenzhen BCTC Testing Co., Ltd.", { size: 10 }),
          bullet("Kementerian Komunikasi dan Informatika Republik Indonesia (Ditjen SDPPI). (2020). Sertifikat Pengujian Alat dan Perangkat Telekomunikasi No: 67186/SDPPI/2020. PT. Xiaomi Technology Indonesia.", { size: 10 }),
          bullet("Sensirion AG. (2019). Datasheet SHTC3: Humidity and Temperature Sensor IC. Stafa, Switzerland. Document Version 1.", { size: 10 }),
          bullet("Telink Semiconductor. (2020). Datasheet for TLSR8258/TLSR8251: Wireless BLE SoC with 32-bit MCU, BLE 5.0, Flash, and Audio. Shanghai, China. Document ID: DS-TLSR8258-E13.", { size: 10 }),
          bullet("Bluetooth SIG. (2021). Bluetooth Core Specification Version 5.2: Low Energy Advertising Extensions and Periodic Advertising.", { size: 10 }),
          bullet("Matter Specification. (2023). Matter Core Specification Release 1.2. Connectivity Standards Alliance (CSA).", { size: 10 })
        ]
      }
    ]
  });

  const buffer = await Packer.toBuffer(doc);
  const outPath = path.join(__dirname, "Tugas1_Desain_Aplikasi_IoT_5024241050.docx");
  fs.writeFileSync(outPath, buffer);
  console.log("Document successfully written to:", outPath);
}

buildDocx().catch(err => {
  console.error("Error generating docx:", err);
  process.exit(1);
});
