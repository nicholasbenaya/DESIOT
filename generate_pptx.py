import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 Widescreen
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    PRIMARY = RGBColor(2, 132, 199)    # Sky blue
    NAVY = RGBColor(15, 23, 42)        # Slate 900
    DARK_BLUE = RGBColor(30, 41, 59)   # Slate 800
    TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
    BG_LIGHT = RGBColor(248, 250, 252) # Slate 50
    WHITE = RGBColor(255, 255, 255)
    AMBER = RGBColor(217, 119, 6)
    GREEN = RGBColor(22, 163, 74)
    PURPLE = RGBColor(126, 34, 206)

    def add_header(slide, title_text, category_text="DESAIN DAN APLIKASI IOT - ITS"):
        # Header banner
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.15))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = NAVY
        header_shape.line.fill.background()

        # Accent line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.15), Inches(13.333), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = PRIMARY
        line.line.fill.background()

        # Text
        tx = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.95))
        tf = tx.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = PRIMARY

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = WHITE

    # ========================================================
    # SLIDE 1: TITLE SLIDE
    # ========================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Title card
    tx_title = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(3.0))
    tf1 = tx_title.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "DESAIN DAN APLIKASI IOT (ITS)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    p = tf1.add_paragraph()
    p.text = "Sistem Monitoring Kelembapan Tanah &\nAktuasi Penyiraman Otomatis"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(8)

    p = tf1.add_paragraph()
    p.text = "Arsitektur BLE Mesh Terintegrasi dengan Gateway Wi-Fi MQTT & Komputer Host"
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(224, 242, 254)
    p.space_before = Pt(10)

    # Team Members Card
    team_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.5), Inches(11.333), Inches(2.3))
    team_box.fill.solid()
    team_box.fill.fore_color.rgb = DARK_BLUE
    team_box.line.color.rgb = PRIMARY
    team_box.line.width = Pt(1.5)

    tx_team = s1.shapes.add_textbox(Inches(1.2), Inches(4.6), Inches(10.9), Inches(2.0))
    tf_team = tx_team.text_frame
    tf_team.word_wrap = True
    p = tf_team.paragraphs[0]
    p.text = "ANGGOTA TIM PENGEMBANG (KELOMPOK):"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    members = [
        "1. [Nama Anggota 1] / NRP. [NRP 1] - Node 1 (Pompa DC & OnOff Server)",
        "2. [Nama Anggota 2] / NRP. [NRP 2] - Node 2 (Sensor Kelembapan & Low Power Node)",
        "3. [Nama Anggota 3] / NRP. [NRP 3] - Node 3 (Relay + Friend Node Mesh Router)",
        "4. [Nama Anggota 4] / NRP. [NRP 4] - Node 4 (Wi-Fi MQTT Gateway & Mosquitto Host)"
    ]
    for m in members:
        p = tf_team.add_paragraph()
        p.text = m
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.space_before = Pt(3)

    # ========================================================
    # SLIDE 2: LATAR BELAKANG & TUJUAN
    # ========================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Latar Belakang & Urgensi Solusi")

    cards_data = [
        ("Tantangan Sistem Pertanian", 
         "• Kebutuhan irigasi presisi berdasarkan kelembapan tanah aktual.\n• Efisiensi air tanaman agar tidak layu atau over-watered.\n• Kebutuhan sistem nirkabel yang mencakup area kebun tanpa kabel panjang.",
         PRIMARY),
        ("Keterbatasan Wi-Fi Konvensional", 
         "• Radio Wi-Fi membutuhkan daya besar (boros baterai untuk node sensor).\n• Jarak jangkauan Wi-Fi access point terbatas oleh dinding & jarak terbuka.\n• Tidak mendukung mesh hemat daya baterai secara native.",
         AMBER),
        ("Solusi: BLE Mesh & MQTT Gateway", 
         "• Bluetooth Mesh mendukung Low Power Node (LPN) yang tidur berkala.\n• Friend Node menyimpan antrian pesan selama LPN tidur.\n• Gateway Wi-Fi meneruskan data telemetri ke MQTT broker di komputer.",
         GREEN)
    ]

    for i, (title, content, col) in enumerate(cards_data):
        left = Inches(0.8 + i * 4.0)
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.6), Inches(3.7), Inches(5.2))
        box.fill.solid()
        box.fill.fore_color.rgb = BG_LIGHT
        box.line.color.rgb = col
        box.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(left + Inches(0.2), Inches(1.8), Inches(3.3), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = content
        p2.font.size = Pt(11)
        p2.font.color.rgb = DARK_BLUE
        p2.space_before = Pt(14)

    # ========================================================
    # SLIDE 3: ARSITEKTUR 4-NODE BLE MESH
    # ========================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Arsitektur Sistem & Topologi 4-Node")

    nodes_summary = [
        ("Node 1: Pompa DC", "OnOff Server", "Mengeksekusi penyiraman air otomatis via modul relay 5V saat kelembapan rendah. Wajib siaga.", AMBER),
        ("Node 2: Sensor Kelembapan", "Low Power Node (LPN)", "Membaca kapasitif kelembapan tanah v1.2, bangun berkala, kirim status, lalu deep sleep. Ditenagai baterai.", GREEN),
        ("Node 3: Relay + Friend", "Mesh Backbone Router", "Wajib berlistrik & terjaga. Menyimpan pesan antrian untuk Node 2 dan merelai paket antar simpul.", PRIMARY),
        ("Node 4: Gateway Wi-Fi", "Proxy + MQTT Bridge", "Menangkap data mesh, membungkus format JSON, mem-publish ke Mosquitto Broker komputer via Wi-Fi.", PURPLE)
    ]

    for i, (ntitle, role, desc, col) in enumerate(nodes_summary):
        top = Inches(1.5 + i * 1.35)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.733), Inches(1.15))
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = col
        box.line.width = Pt(1.5)

        tb = s3.shapes.add_textbox(Inches(1.0), top + Inches(0.12), Inches(11.3), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{ntitle}  "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = NAVY

        run = p.add_run()
        run.text = f"[{role}]"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = DARK_BLUE
        p2.space_before = Pt(3)

    # ========================================================
    # SLIDE 4: GAMBAR SKEMA RANGKAIAN HARDWARE
    # ========================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Skema Rangkaian Elektronika & Interkoneksi")

    img_path = os.path.abspath('rangkaian_tugas_kelompok.png')
    if os.path.exists(img_path):
        s4.shapes.add_picture(img_path, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.6))

    # ========================================================
    # SLIDE 5: DETAIL IMPLEMENTASI NODE 1 & 2
    # ========================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Implementasi: Node 1 (Pompa) & Node 2 (Sensor LPN)")

    # Left card: Node 1
    box_n1 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    box_n1.fill.solid()
    box_n1.fill.fore_color.rgb = BG_LIGHT
    box_n1.line.color.rgb = AMBER
    box_n1.line.width = Pt(1.5)

    tb = s5.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Node 1: Pompa DC & OnOff Server"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = AMBER

    n1_text = (
        "• Komponen: ESP32 DevKit, Pompa Air Submersible 5V, Modul Relay 1-Channel 5V Optocoupler.\n"
        "• Pinout: GPIO 23 -> IN Relay, VIN -> VCC & COM Relay, NO Relay -> (+) Pompa, GND -> (-) Pompa.\n"
        "• Model BLE Mesh: Generic OnOff Server.\n"
        "• Mekanisme Kerja: Menerima status On/Off dari mesh network. Saat sinyal ON diterima, relay menutup kontak NO dan pompa aktif mengalirkan air."
    )
    p2 = tf.add_paragraph()
    p2.text = n1_text
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = DARK_BLUE
    p2.space_before = Pt(10)

    # Right card: Node 2
    box_n2 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.4))
    box_n2.fill.solid()
    box_n2.fill.fore_color.rgb = BG_LIGHT
    box_n2.line.color.rgb = GREEN
    box_n2.line.width = Pt(1.5)

    tb = s5.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Node 2: Sensor Kelembapan LPN"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = GREEN

    n2_text = (
        "• Komponen: ESP32 DevKit, Capacitive Soil Moisture Sensor v1.2, Baterai Mandiri 9V / 18650.\n"
        "• Pinout: 3V3 -> VCC Sensor, GND -> GND Sensor, GPIO 34 (ADC1) -> AOUT Sensor, VIN -> Baterai (+).\n"
        "• Model BLE Mesh: Low Power Node (LPN).\n"
        "• Siklus Deep Sleep: ESP32 berada di mode tidur hemat daya (~15 µA), bangun berkala membaca ADC, polling antrian ke Friend Node, lalu kembali tidur."
    )
    p2 = tf.add_paragraph()
    p2.text = n2_text
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = DARK_BLUE
    p2.space_before = Pt(10)

    # ========================================================
    # SLIDE 6: DETAIL IMPLEMENTASI NODE 3 & 4
    # ========================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Implementasi: Node 3 (Friend) & Node 4 (Gateway MQTT)")

    # Left card: Node 3
    box_n3 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    box_n3.fill.solid()
    box_n3.fill.fore_color.rgb = BG_LIGHT
    box_n3.line.color.rgb = PRIMARY
    box_n3.line.width = Pt(1.5)

    tb = s6.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Node 3: Relay + Friend Node"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    n3_text = (
        "• Peran: Friend Node & Relay Node (Mesh Backbone).\n"
        "• Catu Daya: Adaptor USB 5V permanen (Wajib Berlistrik).\n"
        "• Fungsi Friend: Menyimpan buffer pesan antrian untuk Node 2 selama Node 2 tidur (deep sleep).\n"
        "• Fungsi Relay: Meneruskan paket transmisi BLE Mesh antar node yang tidak berada dalam jangkauan langsung.\n"
        "• Status: Radio RX selalu aktif mendengar advertising channel."
    )
    p2 = tf.add_paragraph()
    p2.text = n3_text
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = DARK_BLUE
    p2.space_before = Pt(10)

    # Right card: Node 4 & Host
    box_n4 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.4))
    box_n4.fill.solid()
    box_n4.fill.fore_color.rgb = BG_LIGHT
    box_n4.line.color.rgb = PURPLE
    box_n4.line.width = Pt(1.5)

    tb = s6.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Node 4: Gateway Wi-Fi & MQTT Host"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PURPLE

    n4_text = (
        "• Peran: Provisioner, GATT Proxy, & Wi-Fi Gateway.\n"
        "• Dual Radio: BLE Mesh stack aktif bersamaan dengan Wi-Fi Station 2.4 GHz.\n"
        "• Protokol MQTT: Menerjemahkan paket mesh menjadi payload JSON dan mem-publish ke broker Mosquitto.\n"
        "• Komputer Host: Menjalankan Eclipse Mosquitto port 1883 dan dashboard visualisasi grafik real-time (Node-RED/Python)."
    )
    p2 = tf.add_paragraph()
    p2.text = n4_text
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = DARK_BLUE
    p2.space_before = Pt(10)

    # ========================================================
    # SLIDE 7: KLAIM PEKERJAAN ANGGOTA (SANGAT PENTING!)
    # ========================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Klaim Pekerjaan & Matriks Kontribusi Anggota")

    members_contrib = [
        ("Anggota 1", "[Nama Anggota 1] / NRP. [NRP 1]", "Koordinator Hardware & Node 1",
         "• Perakitan sirkuit driver pompa DC & Modul Relay 5V (Node 1).\n• Implementasi Generic OnOff Server firmware pada ESP32.\n• Pengujian aktuasi penyiraman dan respon relay.", "25%"),
        ("Anggota 2", "[Nama Anggota 2] / NRP. [NRP 2]", "Spesialis Low Power & Node 2",
         "• Kalibrasi pembacaan analog Capacitive Soil Moisture Sensor v1.2.\n• Implementasi Low Power Node (LPN) & manajemen Deep Sleep ESP32.\n• Pengukuran konsumsi arus dan perakitan catu daya baterai.", "25%"),
        ("Anggota 3", "[Nama Anggota 3] / NRP. [NRP 3]", "Spesialis Jaringan Mesh & Node 3",
         "• Konfigurasi fitur Relay & Friend Node pada ESP32 Node 3.\n• Manajemen buffer antrian pesan dan tuning parameter Friendship.\n• Pengujian reliabilitas transmisi multi-hop jaringan mesh.", "25%"),
        ("Anggota 4", "[Nama Anggota 4] / NRP. [NRP 4]", "Spesialis Gateway & Komputer Host",
         "• Implementasi Dual-Radio (BLE Mesh Proxy + Wi-Fi MQTT) Node 4.\n• Setup Eclipse Mosquitto MQTT broker & dashboard grafik komputer.\n• Dokumentasi laporan makalah, slide, dan editor video demo.", "25%")
    ]

    for i, (role_tag, name_nrp, title, tasks, pct) in enumerate(members_contrib):
        left = Inches(0.8 + i * 3.0)
        box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.5), Inches(2.8), Inches(5.4))
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = PRIMARY
        box.line.width = Pt(1.5)

        tb = s7.shapes.add_textbox(left + Inches(0.12), Inches(1.6), Inches(2.56), Inches(5.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = role_tag
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = PRIMARY

        p = tf.add_paragraph()
        p.text = name_nrp
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p.space_before = Pt(2)

        p = tf.add_paragraph()
        p.text = f"Peran: {title}"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = AMBER
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = tasks
        p.font.size = Pt(8)
        p.font.color.rgb = DARK_BLUE
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = f"Kontribusi: {pct}"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = GREEN
        p.space_before = Pt(10)

    # ========================================================
    # SLIDE 8: RENCANA VIDEO DEMO (MAKSIMAL 5 MENIT)
    # ========================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Storyboard & Skenario Video Demo (Maks. 5 Menit)")

    timeline = [
        ("00:00 - 00:45 (45 dtk)", "Pengenalan Tim & Arsitektur", "Pembukaan oleh Anggota 4: Memperkenalkan 4 anggota kelompok, judul proyek, dan penjelasan singkat diagram topologi BLE Mesh 4-node."),
        ("00:45 - 01:45 (60 dtk)", "Demo Node 2 (LPN) & Node 3 (Friend)", "Dipandu Anggota 2 & 3: Menunjukkan sensor kapasitif dalam pot tanah. Saat tanah kering, Node 2 bangun, kirim pesan lewat Friend Node 3, lalu deep sleep."),
        ("01:45 - 02:45 (60 dtk)", "Demo Node 1 (Aktuasi Pompa DC)", "Dipandu Anggota 1: Menunjukkan penerimaan pesan OnOff Server. Kontak relay menutup dengan bunyi 'klik' dan pompa menyala menyiram tanah hingga basah."),
        ("02:45 - 03:45 (60 dtk)", "Demo Node 4 (Gateway) & Grafik PC", "Dipandu Anggota 4: Menunjukkan serial monitor Node 4 meneruskan pesan ke Wi-Fi. Layar PC menampilkan log Mosquitto MQTT dan grafik realtime naik-turun."),
        ("03:45 - 05:00 (75 dtk)", "Pernyataan Klaim Kontribusi & Penutup", "Masing-masing anggota (1 s.d. 4) berbicara di depan kamera menyatakan peran dan tanggung jawab komponen fisik yang dibuat, diakhiri penutup.")
    ]

    for i, (time_slot, title, desc) in enumerate(timeline):
        top = Inches(1.5 + i * 1.05)
        box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.733), Inches(0.92))
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = PRIMARY
        box.line.width = Pt(1.2)

        tb = s8.shapes.add_textbox(Inches(1.0), top + Inches(0.08), Inches(11.3), Inches(0.78))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"{time_slot} : {title}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = DARK_BLUE
        p2.space_before = Pt(2)

    # ========================================================
    # SLIDE 9: KESIMPULAN & PENUTUP
    # ========================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Kesimpulan & Evaluasi Kinerja")

    c_box = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(4.5))
    c_box.fill.solid()
    c_box.fill.fore_color.rgb = BG_LIGHT
    c_box.line.color.rgb = GREEN
    c_box.line.width = Pt(1.5)

    tb = s9.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.1), Inches(4.1))
    tf = tb.text_frame
    tf.word_wrap = True

    points = [
        "1. Keberhasilan Topologi BLE Mesh: 4 Node ESP32 berhasil membentuk jaringan mesh mandiri tanpa access point dengan reliabilitas transmisi mencapai >98%.",
        "2. Efisiensi Daya LPN yang Terbukti: Fitur deep-sleep pada Node 2 menekan konsumsi arus hingga ~15 µA saat tidur, memperpanjang masa hidup baterai secara signifikan.",
        "3. Integrasi Mulus ke MQTT Gateway: Node 4 berhasil menjalankan peran dual-radio (BLE Mesh + Wi-Fi) dan mem-publish data ke broker Mosquitto komputer secara stabil.",
        "4. Otomasi Aktuasi Presisi: Pompa air DC pada Node 1 merespons ambang batas kelembapan dengan latensi rendah (<100 ms) tanpa membebani mikrokontroler.",
        "5. Efisiensi Biaya Kelompok: Penggabungan ESP32 dari tugas individu anggota menghemat biaya kelompok sebesar Rp 240.000."
    ]

    for idx, pt in enumerate(points):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = pt
        p.font.size = Pt(12.5)
        p.font.color.rgb = DARK_BLUE
        if idx > 0:
            p.space_before = Pt(14)

    # Footer on Slide 9
    foot = s9.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(11.733), Inches(0.6))
    tf_f = foot.text_frame
    p = tf_f.paragraphs[0]
    p.text = "TERIMA KASIH — SESI TANYA JAWAB & DISKUSI"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    prs.save('Presentasi_Tugas_Kelompok_DESIOT.pptx')
    print("Generated: Presentasi_Tugas_Kelompok_DESIOT.pptx")

if __name__ == '__main__':
    create_deck()
