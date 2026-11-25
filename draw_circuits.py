import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set figure typography
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

def draw_tugas_kelompok():
    fig = plt.figure(figsize=(16, 11), dpi=250, facecolor='#f8fafc')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#f8fafc')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')

    # Title Banner
    title_box = FancyBboxPatch((0.5, 10.15), 15.0, 0.72, boxstyle="round,pad=0.1,rounding_size=0.15",
                               ec="#0284c7", fc="#0284c7", lw=1.5)
    ax.add_patch(title_box)
    ax.text(8.0, 10.53, "SKEMA RANGKAIAN ELEKTRONIKA & TOPOLOGI BLE MESH: TUGAS KELOMPOK", 
            color='white', fontsize=12.5, fontweight='bold', ha='center', va='center')
    ax.text(8.0, 10.28, "Mata Kuliah: Desain dan Aplikasi IoT - Institut Teknologi Sepuluh Nopember (ITS)", 
            color='#e0f2fe', fontsize=8.5, ha='center', va='center')

    # =============================================================
    # PANEL 1: NODE 1 - POMPA DC (ONOFF SERVER)
    # =============================================================
    p1 = FancyBboxPatch((0.5, 5.25), 7.2, 4.6, boxstyle="round,pad=0.15,rounding_size=0.2",
                        ec="#cbd5e1", fc="#ffffff", lw=1.5)
    ax.add_patch(p1)
    header1 = FancyBboxPatch((0.5, 9.35), 7.2, 0.5, boxstyle="round,pad=0.08,rounding_size=0.15",
                             ec="#d97706", fc="#fef3c7", lw=1)
    ax.add_patch(header1)
    ax.text(0.7, 9.6, "NODE 1: AKTUATOR POMPA AIR DC", fontsize=9.2, fontweight='bold', color="#92400e")
    ax.text(7.5, 9.6, "[ OnOff Server | Wajib Siaga ]", fontsize=8, fontweight='bold', color="#b45309", ha='right')

    # ESP32 Box (Node 1)
    esp1 = FancyBboxPatch((0.8, 6.3), 2.2, 2.7, boxstyle="round,pad=0.1,rounding_size=0.12",
                          ec="#334155", fc="#1e293b", lw=1.5)
    ax.add_patch(esp1)
    ax.text(1.9, 8.65, "ESP32-S3", color='white', fontsize=9.5, fontweight='bold', ha='center')
    ax.text(1.9, 8.4, "DevKitC-1", color='#94a3b8', fontsize=7, ha='center')
    ax.text(1.9, 6.6, "[ Power: USB 5V ]", color='#38bdf8', fontsize=6.8, ha='center')
    
    # ESP1 Pins
    pins_esp1 = [
        ("GND (Common)", 7.4, "#0f172a"),
        ("GPIO 10", 6.9, "#10b981")
    ]
    for label, y, col in pins_esp1:
        ax.plot([3.0, 3.2], [y, y], color=col, lw=2.5)
        ax.text(2.9, y, label, color='white', fontsize=7.2, ha='right', va='center', fontweight='bold')

    # Relay Module Box
    relay = FancyBboxPatch((3.7, 6.5), 2.1, 2.4, boxstyle="round,pad=0.1,rounding_size=0.12",
                           ec="#0284c7", fc="#f0f9ff", lw=1.5)
    ax.add_patch(relay)
    ax.text(4.75, 8.6, "MODUL RELAY 5V", color='#0369a1', fontsize=8, fontweight='bold', ha='center')
    ax.text(4.75, 8.35, "(Optocoupler Driver)", color='#0284c7', fontsize=6.5, ha='center')

    # Relay Left Pins
    ax.text(3.8, 8.0, "VCC", fontsize=7.2, fontweight='bold', color='#ef4444')
    ax.text(3.8, 7.4, "GND", fontsize=7.2, fontweight='bold', color='#0f172a')
    ax.text(3.8, 6.9, "IN", fontsize=7.2, fontweight='bold', color='#10b981')

    # Relay Right Pins
    ax.text(5.6, 8.0, "NO", fontsize=7.2, fontweight='bold', color='#ea580c', ha='right')
    ax.text(5.6, 7.4, "COM", fontsize=7.2, fontweight='bold', color='#ef4444', ha='right')
    ax.text(5.6, 6.8, "NC", fontsize=7.2, fontweight='bold', color='#94a3b8', ha='right')

    # Wires ESP1 to Relay
    ax.plot([3.2, 3.7], [7.4, 7.4], color='#0f172a', lw=2)  # GND to GND
    ax.plot([3.2, 3.7], [6.9, 6.9], color='#10b981', lw=2)  # GPIO10 to IN

    # DC Pump Box
    pump = FancyBboxPatch((6.1, 6.5), 1.4, 2.4, boxstyle="round,pad=0.1,rounding_size=0.12",
                          ec="#059669", fc="#ecfdf5", lw=1.5)
    ax.add_patch(pump)
    ax.text(6.8, 8.55, "POMPA DC", color='#047857', fontsize=7.8, fontweight='bold', ha='center')
    ax.text(6.8, 8.3, "Submersible", color='#059669', fontsize=6.8, ha='center')
    ax.text(6.8, 7.6, "[ Motor 5V ]", color='#10b981', fontsize=7.5, ha='center')
    ax.text(6.4, 6.85, "(+)", color='#ef4444', fontsize=7, fontweight='bold')
    ax.text(7.2, 6.85, "(-)", color='#0f172a', fontsize=7, fontweight='bold', ha='right')

    # External 5V Power Box for Relay and Pump
    pwr_box = FancyBboxPatch((3.7, 5.4), 3.8, 0.85, boxstyle="round,pad=0.08,rounding_size=0.1",
                             ec="#ef4444", fc="#fee2e2", lw=1.2)
    ax.add_patch(pwr_box)
    ax.text(5.6, 5.95, "CATU DAYA EKSTERNAL 5V (Adaptor / Power Bank)", color='#991b1b', fontsize=6.8, fontweight='bold', ha='center')
    ax.text(5.6, 5.65, "+5V -> VCC & COM Relay | GND -> Common Ground", color='#b91c1c', fontsize=6.2, ha='center')

    # Wiring Power to Relay & Pump
    ax.plot([4.2, 4.2, 3.7], [6.25, 8.0, 8.0], color='#ef4444', lw=1.8) # +5V to VCC Relay
    ax.plot([5.0, 5.0, 5.8], [6.25, 7.4, 7.4], color='#ef4444', lw=1.8) # +5V to COM Relay
    ax.plot([5.8, 6.4], [8.0, 8.0], color='#ea580c', lw=2) # NO to Pump (+)
    ax.plot([7.0, 7.0, 6.6], [6.7, 5.8, 5.8], color='#0f172a', lw=1.8) # Pump (-) to GND
    ax.plot([3.45, 3.45, 3.7], [7.4, 5.8, 5.8], color='#0f172a', lw=1.8, ls=':') # Common ground

    ax.text(4.1, 5.15, "Best Practice: Sinyal kontrol dari GPIO 10 ESP32-S3. Daya motor pompa diambil mandiri\ndari adaptor 5V (Common Ground) agar ESP32-S3 bebas dari brownout reset.", 
            fontsize=6.6, color='#475569', ha='center')

    # =============================================================
    # PANEL 2: NODE 2 - SENSOR KELEMBAPAN (LOW POWER NODE)
    # =============================================================
    p2 = FancyBboxPatch((8.3, 5.25), 7.2, 4.6, boxstyle="round,pad=0.15,rounding_size=0.2",
                        ec="#cbd5e1", fc="#ffffff", lw=1.5)
    ax.add_patch(p2)
    header2 = FancyBboxPatch((8.3, 9.35), 7.2, 0.5, boxstyle="round,pad=0.08,rounding_size=0.15",
                             ec="#16a34a", fc="#dcfce7", lw=1)
    ax.add_patch(header2)
    ax.text(8.5, 9.6, "NODE 2: SENSOR KELEMBAPAN", fontsize=9.2, fontweight='bold', color="#15803d")
    ax.text(15.3, 9.6, "[ Low Power Node | Tidur & Bangun Berkala ]", fontsize=8, fontweight='bold', color="#166534", ha='right')

    # ESP32 Box (Node 2)
    esp2 = FancyBboxPatch((8.6, 6.6), 2.2, 2.4, boxstyle="round,pad=0.1,rounding_size=0.12",
                          ec="#334155", fc="#1e293b", lw=1.5)
    ax.add_patch(esp2)
    ax.text(9.7, 8.65, "ESP32-S3", color='white', fontsize=9.5, fontweight='bold', ha='center')
    ax.text(9.7, 8.4, "DevKitC-1", color='#94a3b8', fontsize=7, ha='center')
    ax.text(9.7, 6.9, "[ Deep Sleep Active ]", color='#a7f3d0', fontsize=6.5, ha='center')

    # ESP2 Pins Right
    pins_esp2 = [
        ("3V3 (Out)", 8.1, "#ef4444"),
        ("GND", 7.6, "#0f172a"),
        ("GPIO 4 (ADC1)", 7.1, "#3b82f6"),
    ]
    for label, y, col in pins_esp2:
        ax.plot([10.8, 11.1], [y, y], color=col, lw=2.5)
        ax.text(10.7, y, label, color='white', fontsize=7, ha='right', va='center', fontweight='bold')

    # Battery Box (Below ESP2)
    bat = FancyBboxPatch((8.6, 5.4), 2.2, 0.95, boxstyle="round,pad=0.08,rounding_size=0.1",
                         ec="#b45309", fc="#fef3c7", lw=1.2)
    ax.add_patch(bat)
    ax.text(9.7, 6.05, "BATERAI MANDIRI", color='#92400e', fontsize=7.2, fontweight='bold', ha='center')
    ax.text(9.7, 5.8, "9V / 18650 / 3x AA", color='#b45309', fontsize=6.5, ha='center')
    ax.text(9.7, 5.55, "+ (Merah) -> VIN | - (Hitam) -> GND", color='#78350f', fontsize=5.8, ha='center')

    # Battery wires going up to ESP2
    ax.plot([8.8, 8.8], [6.35, 6.6], color='#ef4444', lw=2) # Red to VIN
    ax.text(8.8, 6.75, "VIN", color='white', fontsize=6, fontweight='bold', ha='center')
    ax.plot([10.5, 10.5], [6.35, 6.6], color='#0f172a', lw=2) # Black to GND
    ax.text(10.5, 6.75, "GND", color='white', fontsize=6, fontweight='bold', ha='center')

    # Soil Sensor Box
    sensor = FancyBboxPatch((11.5, 6.4), 3.6, 2.6, boxstyle="round,pad=0.1,rounding_size=0.12",
                            ec="#0284c7", fc="#f0f9ff", lw=1.5)
    ax.add_patch(sensor)
    ax.text(13.3, 8.6, "CAPACITIVE SOIL MOISTURE", color='#0369a1', fontsize=7.8, fontweight='bold', ha='center')
    ax.text(13.3, 8.35, "Sensor Kelembapan v1.2", color='#0284c7', fontsize=6.8, ha='center')

    # Sensor Pins
    ax.text(11.7, 8.1, "VCC (3.3V)", fontsize=7, fontweight='bold', color='#ef4444')
    ax.text(11.7, 7.6, "GND", fontsize=7, fontweight='bold', color='#0f172a')
    ax.text(11.7, 7.1, "AOUT (Analog)", fontsize=7, fontweight='bold', color='#3b82f6')

    # Wiring ESP2 to Sensor
    ax.plot([11.1, 11.6], [8.1, 8.1], color='#ef4444', lw=2)
    ax.plot([11.1, 11.6], [7.6, 7.6], color='#0f172a', lw=2)
    ax.plot([11.1, 11.6], [7.1, 7.1], color='#3b82f6', lw=2)

    # Probe illustration
    probe = FancyBboxPatch((12.5, 6.6), 1.6, 1.2, boxstyle="round,pad=0.05,rounding_size=0.08",
                           ec="#94a3b8", fc="#e2e8f0", lw=1)
    ax.add_patch(probe)
    ax.text(13.3, 7.25, "[ Bilah PCB ]", color='#475569', fontsize=6.5, ha='center')
    ax.text(13.3, 6.95, "Tancap ke Tanah", color='#64748b', fontsize=6, ha='center')

    ax.text(13.3, 5.5, "LPN Life-Cycle: ESP32 deep-sleep (hemat baterai),\nbangun berkala membaca ADC AOUT, lalu broadcast ke Node 3.", 
            fontsize=6.8, color='#475569', ha='center')

    # =============================================================
    # PANEL 3: NODE 3 - RELAY + FRIEND (BLE MESH ROUTER)
    # =============================================================
    p3 = FancyBboxPatch((0.5, 0.4), 7.2, 4.5, boxstyle="round,pad=0.15,rounding_size=0.2",
                        ec="#cbd5e1", fc="#ffffff", lw=1.5)
    ax.add_patch(p3)
    header3 = FancyBboxPatch((0.5, 4.35), 7.2, 0.5, boxstyle="round,pad=0.08,rounding_size=0.15",
                             ec="#0284c7", fc="#e0f2fe", lw=1)
    ax.add_patch(header3)
    ax.text(0.7, 4.6, "NODE 3: RELAY + FRIEND NODE", fontsize=9.2, fontweight='bold', color="#0369a1")
    ax.text(7.5, 4.6, "[ Wajib Terjaga & Wajib Berlistrik ]", fontsize=8, fontweight='bold', color="#0284c7", ha='right')

    # ESP32 Box (Node 3)
    esp3 = FancyBboxPatch((0.9, 1.3), 2.5, 2.7, boxstyle="round,pad=0.1,rounding_size=0.12",
                          ec="#334155", fc="#1e293b", lw=1.5)
    ax.add_patch(esp3)
    ax.text(2.15, 3.65, "ESP32-S3", color='white', fontsize=9.5, fontweight='bold', ha='center')
    ax.text(2.15, 3.4, "DevKitC-1", color='#94a3b8', fontsize=7, ha='center')
    ax.text(2.15, 2.7, "PERAN BLE MESH:", color='#38bdf8', fontsize=7, fontweight='bold', ha='center')
    ax.text(2.15, 2.35, "1. Friend Node", color='white', fontsize=7, ha='center')
    ax.text(2.15, 2.05, "2. Relay Node", color='white', fontsize=7, ha='center')
    ax.text(2.15, 1.6, "[ Power: USB Adaptor ]", color='#fbbf24', fontsize=6.8, ha='center')

    # Explanatory card
    exp3 = FancyBboxPatch((3.7, 1.3), 3.7, 2.7, boxstyle="round,pad=0.1,rounding_size=0.12",
                          ec="#cbd5e1", fc="#f8fafc", lw=1)
    ax.add_patch(exp3)
    ax.text(5.55, 3.6, "Tugas Utama Node 3 di Topologi:", color='#0f172a', fontsize=7.8, fontweight='bold', ha='center')
    ax.text(3.9, 3.15, "• Friend Node: Menyimpan antrian pesan", color='#334155', fontsize=7)
    ax.text(3.9, 2.85, "  untuk Node 2 yang sedang deep sleep.", color='#64748b', fontsize=6.5)
    ax.text(3.9, 2.45, "• Relay Node: Meneruskan paket antar simpul", color='#334155', fontsize=7)
    ax.text(3.9, 2.15, "  (Node 2 ke Node 1 & Node 4).", color='#64748b', fontsize=6.5)
    ax.text(3.9, 1.65, "• Wajib terhubung ke listrik terus-menerus", color='#b91c1c', fontsize=7, fontweight='bold')
    ax.text(3.9, 1.4, "  karena radio scanning harus selalu aktif.", color='#b91c1c', fontsize=6.5)

    ax.text(4.1, 0.7, "Koneksi Radio: BLE Mesh (2.4 GHz Advertising Bearer)", 
            fontsize=6.8, color='#0284c7', ha='center', fontweight='bold')

    # =============================================================
    # PANEL 4: NODE 4 - GATEWAY WI-FI & MQTT BROKER
    # =============================================================
    p4 = FancyBboxPatch((8.3, 0.4), 7.2, 4.5, boxstyle="round,pad=0.15,rounding_size=0.2",
                        ec="#cbd5e1", fc="#ffffff", lw=1.5)
    ax.add_patch(p4)
    header4 = FancyBboxPatch((8.3, 4.35), 7.2, 0.5, boxstyle="round,pad=0.08,rounding_size=0.15",
                             ec="#7e22ce", fc="#f3e8ff", lw=1)
    ax.add_patch(header4)
    ax.text(8.5, 4.6, "NODE 4: PROVISIONER + PROXY + GATEWAY", fontsize=9.2, fontweight='bold', color="#7e22ce")
    ax.text(15.3, 4.6, "[ Wi-Fi Gateway MQTT ]", fontsize=8, fontweight='bold', color="#6b21a8", ha='right')

    # ESP32 Box (Node 4)
    esp4 = FancyBboxPatch((8.7, 1.3), 2.5, 2.7, boxstyle="round,pad=0.1,rounding_size=0.12",
                          ec="#334155", fc="#1e293b", lw=1.5)
    ax.add_patch(esp4)
    ax.text(9.95, 3.65, "ESP32-S3", color='white', fontsize=9.5, fontweight='bold', ha='center')
    ax.text(9.95, 3.4, "DevKitC-1", color='#94a3b8', fontsize=7, ha='center')
    ax.text(9.95, 2.7, "DUAL RADIO:", color='#a855f7', fontsize=7, fontweight='bold', ha='center')
    ax.text(9.95, 2.35, "1. BLE Mesh Proxy", color='white', fontsize=7, ha='center')
    ax.text(9.95, 2.05, "2. Wi-Fi Station", color='white', fontsize=7, ha='center')
    ax.text(9.95, 1.6, "[ Power: USB 5V ]", color='#fbbf24', fontsize=6.8, ha='center')

    # Wi-Fi Arrow
    arrow_wifi = FancyArrowPatch((11.4, 2.65), (12.3, 2.65),
                                 connectionstyle="arc3,rad=0", color="#7e22ce",
                                 arrowstyle="simple,tail_width=2.5,head_width=7,head_length=7")
    ax.add_patch(arrow_wifi)
    ax.text(11.85, 2.95, "Wi-Fi TCP/IP\nMQTT (1883)", color='#7e22ce', fontsize=6.5, ha='center', fontweight='bold')

    # Computer Box (Mosquitto + Grafik)
    pc = FancyBboxPatch((12.5, 1.3), 2.6, 2.7, boxstyle="round,pad=0.1,rounding_size=0.12",
                        ec="#334155", fc="#f1f5f9", lw=1.5)
    ax.add_patch(pc)
    ax.text(13.8, 3.65, "KOMPUTER / LAPTOP", color='#0f172a', fontsize=7.8, fontweight='bold', ha='center')
    ax.text(13.8, 3.35, "(Local MQTT Broker)", color='#64748b', fontsize=6.5, ha='center')
    
    soft1 = FancyBboxPatch((12.7, 2.4), 2.2, 0.65, boxstyle="round,pad=0.05,rounding_size=0.08",
                           ec="#0284c7", fc="#e0f2fe", lw=1)
    ax.add_patch(soft1)
    ax.text(13.8, 2.7, "Eclipse Mosquitto", color='#0369a1', fontsize=7, fontweight='bold', ha='center')
    ax.text(13.8, 2.52, "Port: 1883", color='#0284c7', fontsize=6, ha='center')

    soft2 = FancyBboxPatch((12.7, 1.55), 2.2, 0.65, boxstyle="round,pad=0.05,rounding_size=0.08",
                           ec="#16a34a", fc="#dcfce7", lw=1)
    ax.add_patch(soft2)
    ax.text(13.8, 1.85, "Visualisasi Grafik", color='#15803d', fontsize=7, fontweight='bold', ha='center')
    ax.text(13.8, 1.67, "Node-RED / Python", color='#16a34a', fontsize=6, ha='center')

    ax.text(11.9, 0.7, "Node 4 menerima paket BLE Mesh, konversi ke format JSON,\ndan publish ke topic MQTT untuk digambar pada grafik komputer.", 
            fontsize=6.8, color='#475569', ha='center')

    # =============================================================
    # WIRELESS TOPOLOGY OVERLAY ARROWS (BETWEEN PANELS)
    # =============================================================
    # Node 2 to Node 3: BLE Mesh
    arrow_2_to_3 = FancyArrowPatch((9.7, 5.25), (6.0, 4.9),
                                   connectionstyle="arc3,rad=-0.15", color="#0284c7",
                                   arrowstyle="<->,head_width=5,head_length=5", lw=2, ls='--')
    ax.add_patch(arrow_2_to_3)
    ax.text(7.7, 5.05, "BLE Mesh (LPN - Friend)", color='#0284c7', fontsize=7, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#0284c7", lw=0.8))

    # Node 3 to Node 1: BLE Mesh
    arrow_3_to_1 = FancyArrowPatch((2.2, 4.9), (2.2, 5.25),
                                   connectionstyle="arc3,rad=0", color="#d97706",
                                   arrowstyle="<->,head_width=5,head_length=5", lw=2, ls='--')
    ax.add_patch(arrow_3_to_1)
    ax.text(2.2, 5.08, "BLE Mesh", color='#d97706', fontsize=7, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#d97706", lw=0.8))

    # Node 3 to Node 4: BLE Mesh
    arrow_3_to_4 = FancyArrowPatch((7.7, 2.65), (8.7, 2.65),
                                   connectionstyle="arc3,rad=0", color="#7e22ce",
                                   arrowstyle="<->,head_width=5,head_length=5", lw=2, ls='--')
    ax.add_patch(arrow_3_to_4)
    ax.text(8.2, 2.95, "BLE Mesh\n(Relay)", color='#7e22ce', fontsize=6.5, fontweight='bold', ha='center')

    plt.tight_layout()
    plt.savefig('rangkaian_tugas_kelompok.png', dpi=250, bbox_inches='tight')
    plt.close()
    print("Generated: rangkaian_tugas_kelompok.png")

def draw_tugas_individu():
    fig = plt.figure(figsize=(14, 8), dpi=250, facecolor='#f8fafc')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#f8fafc')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title Banner
    title_box = FancyBboxPatch((0.5, 7.15), 13.0, 0.65, boxstyle="round,pad=0.1,rounding_size=0.15",
                               ec="#059669", fc="#059669", lw=1.5)
    ax.add_patch(title_box)
    ax.text(7.0, 7.5, "SKEMA RANGKAIAN: TUGAS INDIVIDU (ESP32 + BLYNK + THINGSPEAK)", 
            color='white', fontsize=12, fontweight='bold', ha='center', va='center')
    ax.text(7.0, 7.27, "Mata Kuliah: Desain dan Aplikasi IoT - Institut Teknologi Sepuluh Nopember (ITS)", 
            color='#d1fae5', fontsize=8, ha='center', va='center')

    # Main Card
    main_box = FancyBboxPatch((0.5, 0.5), 13.0, 6.4, boxstyle="round,pad=0.15,rounding_size=0.2",
                             ec="#cbd5e1", fc="#ffffff", lw=1.5)
    ax.add_patch(main_box)

    # 1. Hardware Box (Left)
    hw_header = FancyBboxPatch((0.8, 6.15), 6.5, 0.5, boxstyle="round,pad=0.08,rounding_size=0.1",
                               ec="#0284c7", fc="#e0f2fe", lw=1)
    ax.add_patch(hw_header)
    ax.text(1.0, 6.4, "BAGIAN 1: RANGKAIAN PERANGKAT KERAS (HARDWARE)", fontsize=8.5, fontweight='bold', color="#0369a1")

    # Sensor (DHT11 / Soil Moisture)
    sensor = FancyBboxPatch((1.0, 2.3), 2.3, 3.5, boxstyle="round,pad=0.1,rounding_size=0.12",
                            ec="#0284c7", fc="#f0f9ff", lw=1.5)
    ax.add_patch(sensor)
    ax.text(2.15, 5.4, "SENSOR", color='#0369a1', fontsize=9, fontweight='bold', ha='center')
    ax.text(2.15, 5.1, "DHT11 / DHT22", color='#0284c7', fontsize=8, fontweight='bold', ha='center')
    ax.text(2.15, 4.85, "(atau Soil Moisture)", color='#64748b', fontsize=7, ha='center')

    # Sensor Pins
    ax.text(3.1, 4.2, "VCC (3.3V)", color='#ef4444', fontsize=7.2, fontweight='bold', ha='right')
    ax.text(3.1, 3.4, "DATA", color='#10b981', fontsize=7.2, fontweight='bold', ha='right')
    ax.text(3.1, 2.6, "GND", color='#0f172a', fontsize=7.2, fontweight='bold', ha='right')

    # ESP32 Box
    esp = FancyBboxPatch((4.5, 1.8), 2.6, 4.0, boxstyle="round,pad=0.1,rounding_size=0.12",
                         ec="#334155", fc="#1e293b", lw=1.5)
    ax.add_patch(esp)
    ax.text(5.8, 5.4, "ESP32", color='white', fontsize=11, fontweight='bold', ha='center')
    ax.text(5.8, 5.15, "DevKit v1", color='#94a3b8', fontsize=7.5, ha='center')

    # ESP Pins Left
    ax.text(4.7, 4.2, "3V3", color='#ef4444', fontsize=7.5, fontweight='bold')
    ax.text(4.7, 3.4, "GPIO 4 / 34", color='#10b981', fontsize=7.5, fontweight='bold')
    ax.text(4.7, 2.6, "GND", color='white', fontsize=7.5, fontweight='bold')

    # Wires Sensor to ESP
    ax.plot([3.2, 4.5], [4.2, 4.2], color='#ef4444', lw=2.5)  # VCC
    ax.plot([3.2, 4.5], [3.4, 3.4], color='#10b981', lw=2.5)  # DATA
    ax.plot([3.2, 4.5], [2.6, 2.6], color='#0f172a', lw=2.5)  # GND

    # USB Power into ESP32
    ax.plot([5.8, 5.8], [1.8, 1.1], color='#3b82f6', lw=3)
    ax.text(5.8, 0.9, "Kabel USB (Data & Power dari Laptop)", color='#1d4ed8', fontsize=7.2, fontweight='bold', ha='center')

    # 2. Cloud Platforms Box (Right)
    cloud_header = FancyBboxPatch((7.6, 6.15), 5.6, 0.5, boxstyle="round,pad=0.08,rounding_size=0.1",
                                 ec="#16a34a", fc="#dcfce7", lw=1)
    ax.add_patch(cloud_header)
    ax.text(7.8, 6.4, "BAGIAN 2: INTEGRASI CLOUD (INTERNET / WI-FI 2.4 GHz)", fontsize=8.5, fontweight='bold', color="#15803d")

    # Wi-Fi Cloud connection arrows
    arrow_cloud1 = FancyArrowPatch((7.2, 4.5), (8.1, 5.0),
                                   connectionstyle="arc3,rad=-0.1", color="#059669",
                                   arrowstyle="simple,tail_width=2.5,head_width=7,head_length=7")
    ax.add_patch(arrow_cloud1)

    arrow_cloud2 = FancyArrowPatch((7.2, 3.2), (8.1, 2.7),
                                   connectionstyle="arc3,rad=0.1", color="#059669",
                                   arrowstyle="simple,tail_width=2.5,head_width=7,head_length=7")
    ax.add_patch(arrow_cloud2)

    ax.text(7.5, 3.85, "Wi-Fi 2.4 GHz\n(Internet)", color='#059669', fontsize=7.5, fontweight='bold', ha='center')

    # Platform 1: Blynk
    blynk = FancyBboxPatch((8.3, 4.1), 4.7, 1.8, boxstyle="round,pad=0.1,rounding_size=0.12",
                           ec="#10b981", fc="#ecfdf5", lw=1.5)
    ax.add_patch(blynk)
    ax.text(10.65, 5.5, "APLIKASI BLYNK (Blynk IoT)", color='#047857', fontsize=8.5, fontweight='bold', ha='center')
    ax.text(8.5, 5.0, "• Protokol: Blynk Library (WebSocket / TCP)", color='#065f46', fontsize=7)
    ax.text(8.5, 4.65, "• Fungsi: Kontrol & Monitoring Real-Time di HP", color='#065f46', fontsize=7)
    ax.text(8.5, 4.3, "• Widget: Gauge, Realtime Value Display, Button", color='#065f46', fontsize=7)

    # Platform 2: ThingSpeak
    ts = FancyBboxPatch((8.3, 1.7), 4.7, 1.8, boxstyle="round,pad=0.1,rounding_size=0.12",
                        ec="#0284c7", fc="#f0f9ff", lw=1.5)
    ax.add_patch(ts)
    ax.text(10.65, 3.1, "THINGSPEAK (MathWorks IoT)", color='#0369a1', fontsize=8.5, fontweight='bold', ha='center')
    ax.text(8.5, 2.6, "• Protokol: HTTP REST API (ThingSpeak.writeFields)", color='#1e40af', fontsize=7)
    ax.text(8.5, 2.25, "• Fungsi: Cloud Data Logging & Time-Series Graph", color='#1e40af', fontsize=7)
    ax.text(8.5, 1.9, "• Output: Grafik tren historis kelembapan/suhu", color='#1e40af', fontsize=7)

    plt.tight_layout()
    plt.savefig('rangkaian_tugas_individu.png', dpi=250, bbox_inches='tight')
    plt.close()
    print("Generated: rangkaian_tugas_individu.png")

if __name__ == '__main__':
    draw_tugas_kelompok()
    draw_tugas_individu()
