#!/usr/bin/env python3
"""
=============================================================================
DESIOT ITS SURABAYA - WEB DASHBOARD & AUTOMATION CONTROLLER
Mata Kuliah : Desain dan Aplikasi IoT - Lab A108 FTEIC ITS Surabaya
Arsitektur  : 4x ESP32-S3 BLE Mesh + Wi-Fi MQTT Gateway + Flask Web Interface
=============================================================================
"""

import sys
import time
import json
import threading
from flask import Flask, render_template_string, jsonify, request, Response

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("[ERROR] Library 'paho-mqtt' belum terinstall.")
    print("Silakan jalankan: pip install paho-mqtt flask")
    sys.exit(1)

# Konfigurasi MQTT
BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883

TOPIC_SENSOR = "desiot/kebun/sensor"
TOPIC_PUMP_STATE = "desiot/kebun/pompa"
TOPIC_PUMP_SET = "desiot/kebun/pompa/set"
TOPIC_MODE_SET = "desiot/kebun/mode/set"
TOPIC_GATEWAY = "desiot/kebun/gateway"

SOIL_DRY_THRESHOLD = 2100
SOIL_WET_THRESHOLD = 1800

# State Global Sistem (HMI Monitor)
system_state = {
    "raw_adc": 0,
    "moisture_pct": 0,
    "soil_status": "BELUM TERHUBUNG",
    "pump_state": 0,
    "auto_mode": True,
    "last_sensor_update": "Belum ada",
    "gateway_connected": False,
    "history": [],
    "logs": []
}

state_lock = threading.Lock()
mqtt_client = None

def add_log(msg):
    ts = time.strftime("%H:%M:%S")
    with state_lock:
        system_state["logs"].insert(0, f"[{ts}] {msg}")
        if len(system_state["logs"]) > 25:
            system_state["logs"].pop()

# Callback MQTT
def on_connect(client, userdata, flags, rc, *args):
    code = getattr(rc, "value", rc)
    if code == 0:
        with state_lock:
            system_state["gateway_connected"] = True
        add_log("HMI terhubung ke Mosquitto Broker!")
        client.subscribe(TOPIC_SENSOR)
        client.subscribe(TOPIC_PUMP_STATE)
        client.subscribe(TOPIC_GATEWAY)
        add_log("Subscribed ke topik: sensor, pompa, gateway")
    else:
        add_log(f"Gagal koneksi broker MQTT, code: {rc}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload_str = msg.payload.decode('utf-8', errors='ignore')
    ts = time.strftime("%H:%M:%S")

    try:
        data = json.loads(payload_str)
    except Exception:
        data = {"raw": payload_str}

    if topic == TOPIC_SENSOR:
        adc = data.get("raw_adc", 0)
        # Kalkulasi persentase kelembapan (terbalik: ADC tinggi = kering, ADC rendah = basah)
        # 4095 = 0%, ~1500 = 100%
        pct = max(0, min(100, int((4095 - adc) / (4095 - 1500) * 100)))

        if adc >= SOIL_DRY_THRESHOLD:
            status_text = "KERING"
        elif adc <= SOIL_WET_THRESHOLD:
            status_text = "BASAH"
        else:
            status_text = "OPTIMAL"

        with state_lock:
            system_state["raw_adc"] = adc
            system_state["moisture_pct"] = pct
            system_state["soil_status"] = status_text
            system_state["last_sensor_update"] = ts
            system_state["history"].append({"time": ts, "adc": adc, "pct": pct})
            if len(system_state["history"]) > 30:
                system_state["history"].pop(0)

        add_log(f"Telemetri Node 2: ADC {adc} ({pct}%) -> {status_text}")

    elif topic == TOPIC_PUMP_STATE:
        state = data.get("pump_state", 0)
        auto_mode = data.get("auto_mode", None)
        with state_lock:
            system_state["pump_state"] = state
            if auto_mode is not None:
                system_state["auto_mode"] = bool(auto_mode)
            mode_str = "OTOMATIS (Edge)" if system_state["auto_mode"] else "MANUAL"
        add_log(f"Status Node 1 (Pompa): {'MENYALA (ON)' if state else 'PADAM (OFF)'} [{mode_str}]")

    elif topic == TOPIC_GATEWAY:
        add_log(f"Status Node 4 Gateway: {payload_str}")

def start_mqtt_thread():
    global mqtt_client
    try:
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        mqtt_client = mqtt.Client()

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    def run():
        try:
            mqtt_client.connect(BROKER_HOST, BROKER_PORT, 60)
            mqtt_client.loop_forever()
        except Exception as e:
            add_log(f"MQTT Error: {e}")

    t = threading.Thread(target=run, daemon=True)
    t.start()

# Flask Web App
app = Flask(__name__)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DESIOT ITS - Smart Irrigation Dashboard</title>
    <!-- Google Fonts: Plus Jakarta Sans -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-body: #f4f7fc;
            --bg-card: #ffffff;
            --text-title: #0f172a;
            --text-body: #334155;
            --text-muted: #94a3b8;
            --primary-blue: #2563eb;
            --primary-indigo: #4f46e5;
            --primary-cyan: #0284c7;
            --accent-green: #10b981;
            --accent-red: #f43f5e;
            --border-subtle: #f1f5f9;
            --shadow-card: 0 10px 25px -5px rgba(15, 23, 42, 0.04), 0 8px 10px -6px rgba(15, 23, 42, 0.02);
            --shadow-hover: 0 20px 25px -5px rgba(15, 23, 42, 0.07), 0 10px 10px -5px rgba(15, 23, 42, 0.03);
            --radius-card: 24px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        body {
            background-color: var(--bg-body);
            color: var(--text-body);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            padding: 24px;
        }

        /* 1. Main Dashboard Layout (Centered Container, Nav Rail Omitted) */
        .main-container {
            width: 100%;
            max-width: 1440px;
            display: flex;
            gap: 24px;
            min-width: 0;
        }

        .dashboard-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 24px;
            min-width: 0;
        }

        /* 3. Search Bar & Top Row (Matching Reference) */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #ffffff;
            border-radius: 20px;
            padding: 12px 24px;
            box-shadow: var(--shadow-card);
            border: 1px solid rgba(226, 232, 240, 0.8);
        }

        .search-box {
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--text-muted);
            width: 320px;
        }

        .search-box input {
            border: none;
            outline: none;
            background: transparent;
            font-size: 0.9rem;
            color: var(--text-title);
            width: 100%;
        }

        .search-box input::placeholder {
            color: #94a3b8;
        }

        .top-actions {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .icon-badge-btn {
            width: 40px;
            height: 40px;
            border-radius: 12px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #64748b;
            cursor: pointer;
            position: relative;
            transition: all 0.2s;
        }

        .icon-badge-btn:hover {
            background: #f1f5f9;
            color: #0f172a;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background: #22c55e;
            border-radius: 50%;
            position: absolute;
            top: 8px;
            right: 8px;
            box-shadow: 0 0 6px #22c55e;
        }

        .user-pill {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 4px 12px 4px 6px;
            border-radius: 9999px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
        }

        .user-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 0.8rem;
        }

        /* 4. Page Header */
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 4px;
        }

        .page-title {
            font-size: 1.85rem;
            font-weight: 800;
            color: var(--text-title);
            letter-spacing: -0.5px;
        }

        .date-pill {
            display: flex;
            align-items: center;
            gap: 8px;
            background: #ffffff;
            padding: 8px 16px;
            border-radius: 14px;
            font-size: 0.85rem;
            font-weight: 600;
            color: #64748b;
            box-shadow: var(--shadow-card);
            border: 1px solid rgba(226, 232, 240, 0.8);
        }

        /* 5. Tri-Card Metric Grid (Directly from Reference Photo) */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }

        .metric-card {
            border-radius: var(--radius-card);
            padding: 24px;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 180px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: var(--shadow-card);
        }

        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-hover);
        }

        /* Background Watermark Shapes (Like in reference) */
        .metric-card::after {
            content: '';
            position: absolute;
            right: -20px;
            bottom: -20px;
            width: 140px;
            height: 140px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.18);
            pointer-events: none;
        }

        .metric-card-1 {
            background: linear-gradient(135deg, #c7d2fe 0%, #e0e7ff 100%);
            color: #1e1b4b;
        }

        .metric-card-2 {
            background: linear-gradient(135deg, #bae6fd 0%, #e0f2fe 100%);
            color: #082f49;
        }

        .metric-card-3 {
            background: linear-gradient(135deg, #fbcfe8 0%, #fce7f3 100%);
            color: #701a75;
        }

        .card-icon-box {
            width: 48px;
            height: 48px;
            border-radius: 16px;
            background: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.06);
            margin-bottom: 20px;
        }

        .card-label {
            font-size: 0.95rem;
            font-weight: 700;
            margin-bottom: 4px;
            opacity: 0.9;
        }

        .card-value {
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin-bottom: 6px;
        }

        .card-meta {
            font-size: 0.8rem;
            font-weight: 600;
            opacity: 0.75;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .badge-pill-light {
            background: rgba(255, 255, 255, 0.8);
            padding: 2px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        }

        /* 6. Main Activity Chart Card (Matching Reference) */
        .chart-card {
            background: #ffffff;
            border-radius: var(--radius-card);
            padding: 28px;
            box-shadow: var(--shadow-card);
            border: 1px solid rgba(226, 232, 240, 0.8);
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .chart-title {
            font-size: 1.25rem;
            font-weight: 800;
            color: var(--text-title);
        }

        .chart-tabs {
            display: flex;
            background: #f1f5f9;
            padding: 4px;
            border-radius: 12px;
            gap: 4px;
        }

        .chart-tab {
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 600;
            color: #64748b;
            background: transparent;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
        }

        .chart-tab.active {
            background: #2563eb;
            color: #ffffff;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
        }

        .chart-box {
            height: 250px;
            width: 100%;
            position: relative;
        }

        /* 7. Bottom Split Cards: Recommendation & Treatment Style */
        .bottom-split {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }

        .white-card {
            background: #ffffff;
            border-radius: var(--radius-card);
            padding: 24px;
            box-shadow: var(--shadow-card);
            border: 1px solid rgba(226, 232, 240, 0.8);
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .card-header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .card-header-title {
            font-size: 1.1rem;
            font-weight: 800;
            color: var(--text-title);
        }

        .btn-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 4px;
            width: 100%;
        }

        .btn-action {
            width: 100%;
            min-width: 0;
            padding: 12px 6px;
            border-radius: 14px;
            border: none;
            font-weight: 700;
            font-size: 0.82rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            white-space: nowrap;
            transition: all 0.2s ease;
        }

        .btn-action:hover {
            transform: translateY(-2px);
        }

        .btn-on {
            background: #10b981;
            color: #ffffff;
            box-shadow: 0 6px 16px rgba(16, 185, 129, 0.25);
        }

        .btn-on:hover {
            background: #059669;
            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.35);
        }

        .btn-off {
            background: #f43f5e;
            color: #ffffff;
            box-shadow: 0 6px 16px rgba(244, 63, 94, 0.25);
        }

        .btn-off:hover {
            background: #e11d48;
            box-shadow: 0 8px 20px rgba(244, 63, 94, 0.35);
        }

        .btn-mode-toggle {
            width: 100%;
            padding: 11px 12px;
            border-radius: 14px;
            border: 1px solid #e2e8f0;
            background: #f8fafc;
            color: #475569;
            font-weight: 700;
            font-size: 0.82rem;
            cursor: pointer;
            transition: all 0.2s;
            margin-top: 4px;
            text-align: center;
        }

        .btn-mode-toggle:hover {
            background: #f1f5f9;
            color: #0f172a;
        }

        /* Node Item Lists (Like Doctors / Treatments in Reference) */
        .node-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .node-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 16px;
            border-radius: 16px;
            background: #f8fafc;
            border: 1px solid #f1f5f9;
        }

        .node-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .node-icon-circle {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            font-weight: 700;
        }

        .node-title-box h4 {
            font-size: 0.9rem;
            font-weight: 700;
            color: var(--text-title);
        }

        .node-title-box p {
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .node-tag {
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 8px;
            border-radius: 9999px;
            white-space: nowrap;
            flex-shrink: 0;
        }

        .tag-active {
            background: #dcfce7;
            color: #15803d;
        }

        .tag-router {
            background: #e0f2fe;
            color: #0369a1;
        }

        /* 8. Right Sidebar (Controls & Topology) */
        .right-sidebar {
            width: 360px;
            display: flex;
            flex-direction: column;
            gap: 24px;
            flex-shrink: 0;
        }

        /* Calendar Widget (Matching Top Right of Reference) */
        .calendar-card {
            background: #ffffff;
            border-radius: var(--radius-card);
            padding: 24px;
            box-shadow: var(--shadow-card);
            border: 1px solid rgba(226, 232, 240, 0.8);
        }

        .calendar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
        }

        .calendar-title {
            font-size: 1.1rem;
            font-weight: 800;
            color: var(--text-title);
        }

        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 6px;
            text-align: center;
        }

        .cal-day-name {
            font-size: 0.7rem;
            font-weight: 700;
            color: #94a3b8;
            padding-bottom: 8px;
        }

        .cal-date {
            font-size: 0.8rem;
            font-weight: 600;
            color: #475569;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.15s;
        }

        .cal-date:hover {
            background: #f1f5f9;
        }

        .cal-date.active {
            background: #2563eb;
            color: #ffffff;
            font-weight: 700;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.35);
        }

        .cal-date.muted {
            color: #cbd5e1;
        }

        /* Live Activity Log Widget */
        .logs-card {
            background: #ffffff;
            border-radius: var(--radius-card);
            padding: 24px;
            box-shadow: var(--shadow-card);
            border: 1px solid rgba(226, 232, 240, 0.8);
            display: flex;
            flex-direction: column;
            gap: 14px;
            flex: 1;
            max-height: 480px;
        }

        .log-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
            overflow-y: auto;
            max-height: 380px;
            padding-right: 4px;
        }

        .log-container::-webkit-scrollbar {
            width: 4px;
        }

        .log-container::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }

        .log-entry {
            display: flex;
            gap: 10px;
            padding: 10px 12px;
            border-radius: 12px;
            background: #f8fafc;
            border: 1px solid #f1f5f9;
            font-size: 0.8rem;
            line-height: 1.4;
        }

        .log-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #2563eb;
            margin-top: 5px;
            flex-shrink: 0;
        }

        .log-text {
            color: #334155;
            word-break: break-word;
        }

        .log-time {
            font-weight: 700;
            color: #64748b;
        }
    </style>
</head>
<body>

    <!-- Main Layout Container (Nav Rail Omitted) -->
    <div class="main-container">

        <!-- Center Column -->
        <main class="dashboard-content">

            <!-- Top Search Bar (Matching Reference) -->
            <div class="top-bar">
                <div class="search-box">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    <input type="text" placeholder="Cari sensor, node, event telemetri...">
                </div>
                <div class="top-actions">
                    <div class="icon-badge-btn" title="Status Jaringan">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                        </svg>
                        <span class="pulse-dot"></span>
                    </div>
                    <div class="user-pill">
                        <div class="user-avatar">A108</div>
                        <span style="font-size:0.85rem; font-weight:700; color:#0f172a;">Lab A108 • FTEIC</span>
                    </div>
                </div>
            </div>

            <!-- Page Title Row -->
            <div class="page-header">
                <div>
                    <h1 class="page-title">Dashboard</h1>
                    <p style="font-size: 0.85rem; color: #64748b; font-weight: 500; margin-top: 2px;">
                        Sistem Penyiraman Pintar BLE Mesh • Lab A108 FTEIC ITS
                    </p>
                </div>
                <div class="date-pill">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                    <span id="currentDateText">24 November 2026</span>
                </div>
            </div>

            <!-- 3. Tri-Card Metric Grid (Directly from Reference Photo) -->
            <div class="metric-grid">
                
                <!-- Card 1: Periwinkle / Heart Rate Style -> Soil Moisture -->
                <div class="metric-card metric-card-1">
                    <div>
                        <div class="card-icon-box" style="color: #4f46e5;">
                            <!-- Leaf / Moisture Pulse Icon -->
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"></path>
                                <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"></path>
                            </svg>
                        </div>
                        <div class="card-label">Kelembapan Tanah</div>
                    </div>
                    <div>
                        <div class="card-value" id="valPct">-- %</div>
                        <div class="card-meta">
                            <span>Raw ADC: <b id="valAdc">--</b></span>
                            <span class="badge-pill-light" id="badgeStatus">MEMBACA...</span>
                        </div>
                    </div>
                </div>

                <!-- Card 2: Sky Cyan / Blood Pressure Style -> Pump Actuator -->
                <div class="metric-card metric-card-2">
                    <div>
                        <div class="card-icon-box" style="color: #0284c7;">
                            <!-- Water Droplet / Pump Icon -->
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
                            </svg>
                        </div>
                        <div class="card-label">Status Aktuator Pompa</div>
                    </div>
                    <div>
                        <div class="card-value" id="valPump">PADAM</div>
                        <div class="card-meta">
                            <span>Node 1 Relay (GPIO 10)</span>
                            <span class="badge-pill-light" id="valPumpDetail">Active-LOW</span>
                        </div>
                    </div>
                </div>

                <!-- Card 3: Soft Pink-Violet / Glucose Style -> Control Mode -->
                <div class="metric-card metric-card-3">
                    <div>
                        <div class="card-icon-box" style="color: #c026d3;">
                            <!-- Microchip / Smart Mode Icon -->
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                                <rect x="4" y="4" width="16" height="16" rx="2"></rect>
                                <rect x="9" y="9" width="6" height="6"></rect>
                                <line x1="9" y1="1" x2="9" y2="4"></line>
                                <line x1="15" y1="1" x2="15" y2="4"></line>
                                <line x1="9" y1="20" x2="9" y2="23"></line>
                                <line x1="15" y1="20" x2="15" y2="23"></line>
                                <line x1="20" y1="9" x2="23" y2="9"></line>
                                <line x1="20" y1="14" x2="23" y2="14"></line>
                                <line x1="1" y1="9" x2="4" y2="9"></line>
                                <line x1="1" y1="14" x2="4" y2="14"></line>
                            </svg>
                        </div>
                        <div class="card-label">Mode Kontrol Jaringan</div>
                    </div>
                    <div>
                        <div class="card-value" id="badgeModeText">OTOMATIS</div>
                        <div class="card-meta">
                            <span>Edge Autonomy Node 4</span>
                            <span class="badge-pill-light" id="lastUpdateTime">Online</span>
                        </div>
                    </div>
                </div>

            </div>

            <!-- 4. Activity Chart Card (Matching Reference Line Graph) -->
            <div class="chart-card">
                <div class="chart-header">
                    <div>
                        <div class="chart-title">Aktivitas Kelembapan (ADC Real-Time)</div>
                        <p style="font-size:0.8rem; color:#94a3b8; font-weight:500;">
                            Batas Ambang Otomasi: Kering &ge; 2100 ADC (Pompa ON) | Basah &le; 1800 ADC (Pompa OFF)
                        </p>
                    </div>
                    <div class="chart-tabs">
                        <button class="chart-tab active">Live Stream</button>
                        <button class="chart-tab">Thresholds</button>
                    </div>
                </div>
                <div class="chart-box">
                    <canvas id="moistureChart"></canvas>
                </div>
            </div>

            <!-- 5. Live Activity Feed (Swapped from Right Sidebar to Main Content) -->
            <div class="white-card" style="flex: 1;">
                <div class="card-header-row">
                    <div>
                        <div class="card-header-title">Live Activity & Telemetri Feed</div>
                        <p style="font-size:0.75rem; color:#94a3b8; font-weight:500; margin-top:2px;">
                            Aliran event real-time: paket sensor BLE Mesh, sinyal aktuator relay, dan status jaringan
                        </p>
                    </div>
                    <span class="badge-pill-light" style="background:#f1f5f9; color:#64748b;" id="clockText">--:--:--</span>
                </div>
                <div class="log-container" id="logBox" style="max-height: 220px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px;">
                    <div class="log-entry">
                        <span class="log-dot"></span>
                        <div class="log-text">
                            <span class="log-time">[System]</span> Menghubungkan ke broker MQTT...
                        </div>
                    </div>
                </div>
            </div>

        </main>

        <!-- 3. Right Sidebar (Kendali Aktuator di Atas + Topologi Node di Bawah) -->
        <aside class="right-sidebar">
            
            <!-- Card 1 (Atas, Menggantikan Kalender): Kendali Cepat Aktuator -->
            <div class="white-card">
                <div class="card-header-row">
                    <div class="card-header-title">Kendali Cepat Aktuator</div>
                    <span class="badge-pill-light" style="background:#f1f5f9; color:#475569;" id="hmiStatusBadge">HMI OVERRIDE</span>
                </div>
                <p style="font-size:0.8rem; color:#64748b; line-height: 1.4;">
                    Edge Autonomy aktif di Node 4. Menekan tombol akan meng-override kontrol lokal ke Mode Manual.
                </p>
                <div class="btn-group">
                    <button class="btn-action btn-on" onclick="setPump(1)">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <polygon points="5 3 19 12 5 21 5 3"></polygon>
                        </svg>
                        NYALAKAN (ON)
                    </button>
                    <button class="btn-action btn-off" onclick="setPump(0)">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="6" y="4" width="4" height="16"></rect>
                            <rect x="14" y="4" width="4" height="16"></rect>
                        </svg>
                        PADAMKAN (OFF)
                    </button>
                </div>
                <button class="btn-mode-toggle" id="btnToggleMode" onclick="toggleMode()">
                    Beralih ke Mode Manual
                </button>
            </div>

            <!-- Card 2 (Bawah, Ditukar dengan Live Activity): Topologi 4-Node BLE Mesh -->
            <div class="white-card">
                <div class="card-header-row">
                    <div class="card-header-title">Topologi Node BLE Mesh</div>
                    <span class="badge-pill-light" style="background:#eff6ff; color:#2563eb;">4 Nodes Active</span>
                </div>
                <div class="node-list">
                    <div class="node-item">
                        <div class="node-left">
                            <div class="node-icon-circle" style="background:#dbeafe; color:#1d4ed8;">N4</div>
                            <div class="node-title-box">
                                <h4>Node 4 (Gateway & Provisioner)</h4>
                                <p>0x0001 • Wi-Fi Station & MQTT Gateway</p>
                            </div>
                        </div>
                        <span class="node-tag tag-active">Gateway Active</span>
                    </div>
                    <div class="node-item">
                        <div class="node-left">
                            <div class="node-icon-circle" style="background:#dcfce7; color:#15803d;">N1</div>
                            <div class="node-title-box">
                                <h4>Node 1 (Aktuator Pompa)</h4>
                                <p>0x0002 / 0x0003 • Generic OnOff Server</p>
                            </div>
                        </div>
                        <span class="node-tag tag-active" id="node1Badge">Siaga</span>
                    </div>
                    <div class="node-item">
                        <div class="node-left">
                            <div class="node-icon-circle" style="background:#fef3c7; color:#b45309;">N2</div>
                            <div class="node-title-box">
                                <h4>Node 2 (Sensor Kelembapan LPN)</h4>
                                <p>0x0004 • Vendor Model Telemetry (5s)</p>
                            </div>
                        </div>
                        <span class="node-tag tag-active">Sampling 5s</span>
                    </div>
                    <div class="node-item">
                        <div class="node-left">
                            <div class="node-icon-circle" style="background:#f1f5f9; color:#475569;">N3</div>
                            <div class="node-title-box">
                                <h4>Node 3 (Relay & Friend Node)</h4>
                                <p>0x0005 • Mesh Backbone Router</p>
                            </div>
                        </div>
                        <span class="node-tag tag-router">Router Relaying</span>
                    </div>
                </div>
            </div>

        </aside>

    </div>

    <!-- Script Chart.js & Real-Time Sync -->
    <script>
        // Update Live Clock & Date
        function updateClock() {
            const now = new Date();
            document.getElementById('clockText').innerText = now.toLocaleTimeString();
            const options = { day: 'numeric', month: 'long', year: 'numeric' };
            document.getElementById('currentDateText').innerText = now.toLocaleDateString('id-ID', options);
        }
        setInterval(updateClock, 1000);
        updateClock();

        // Inisialisasi Chart.js dengan Style Estetik Modern
        const ctx = document.getElementById('moistureChart').getContext('2d');

        // Gradient Fill untuk Line Chart
        const fillGradient = ctx.createLinearGradient(0, 0, 0, 250);
        fillGradient.addColorStop(0, 'rgba(37, 99, 235, 0.18)');
        fillGradient.addColorStop(1, 'rgba(37, 99, 235, 0.0)');

        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Nilai ADC (Raw)',
                        data: [],
                        borderColor: '#2563eb',
                        backgroundColor: fillGradient,
                        borderWidth: 2.8,
                        tension: 0.42,
                        fill: true,
                        pointRadius: 3,
                        pointHoverRadius: 6,
                        pointBackgroundColor: '#2563eb',
                        pointBorderColor: '#ffffff',
                        pointBorderWidth: 2
                    },
                    {
                        label: 'Batas Kering (2100)',
                        data: [],
                        borderColor: 'rgba(244, 63, 94, 0.4)',
                        borderWidth: 1.5,
                        borderDash: [5, 5],
                        pointRadius: 0,
                        fill: false
                    },
                    {
                        label: 'Batas Basah (1800)',
                        data: [],
                        borderColor: 'rgba(16, 185, 129, 0.4)',
                        borderWidth: 1.5,
                        borderDash: [5, 5],
                        pointRadius: 0,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', size: 11 } }
                    },
                    y: {
                        min: 1000,
                        max: 4095,
                        grid: { color: '#f1f5f9', borderDash: [4, 4] },
                        ticks: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', size: 11 } }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        align: 'end',
                        labels: {
                            boxWidth: 8,
                            boxHeight: 8,
                            usePointStyle: true,
                            pointStyle: 'circle',
                            color: '#64748b',
                            font: { family: 'Plus Jakarta Sans', size: 11, weight: '600' }
                        }
                    },
                    tooltip: {
                        backgroundColor: '#0f172a',
                        titleFont: { family: 'Plus Jakarta Sans', weight: '700' },
                        bodyFont: { family: 'Plus Jakarta Sans' },
                        padding: 10,
                        cornerRadius: 12
                    }
                }
            }
        });

        // HMI Action Handlers
        function setPump(state) {
            fetch('/api/pump', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ state: state })
            });
        }

        function toggleMode() {
            fetch('/api/toggle_mode', { method: 'POST' });
        }

        // Real-Time Polling Setiap 1 Detik
        async function fetchData() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();

                // 1. Update Sensor Card (Periwinkle Card)
                document.getElementById('valPct').innerText = data.moisture_pct + ' %';
                document.getElementById('valAdc').innerText = data.raw_adc;
                const badgeStatus = document.getElementById('badgeStatus');
                badgeStatus.innerText = data.soil_status;

                // 2. Update Pump Card (Sky Cyan Card)
                const valPump = document.getElementById('valPump');
                const valPumpDetail = document.getElementById('valPumpDetail');
                const node1Badge = document.getElementById('node1Badge');
                if (data.pump_state === 1) {
                    valPump.innerText = 'MENYALA';
                    valPump.style.color = '#0284c7';
                    valPumpDetail.innerText = 'Menyiram Aktif';
                    node1Badge.innerText = 'Menyala (ON)';
                    node1Badge.className = 'node-tag tag-active';
                } else {
                    valPump.innerText = 'PADAM';
                    valPump.style.color = 'inherit';
                    valPumpDetail.innerText = 'Relay Standby';
                    node1Badge.innerText = 'Padam (OFF)';
                    node1Badge.className = 'node-tag';
                }

                // 3. Update Mode Card (Pink/Violet Card)
                const badgeModeText = document.getElementById('badgeModeText');
                const btnToggleMode = document.getElementById('btnToggleMode');
                const hmiStatusBadge = document.getElementById('hmiStatusBadge');
                if (data.auto_mode) {
                    badgeModeText.innerText = 'OTOMATIS';
                    btnToggleMode.innerText = 'Ubah ke Mode Manual (HMI Override)';
                    hmiStatusBadge.innerText = 'OTOMASI EDGE';
                    hmiStatusBadge.style.background = '#dcfce7';
                    hmiStatusBadge.style.color = '#15803d';
                } else {
                    badgeModeText.innerText = 'MANUAL';
                    btnToggleMode.innerText = 'Ubah ke Mode Otomatis (Edge)';
                    hmiStatusBadge.innerText = 'HMI MANUAL';
                    hmiStatusBadge.style.background = '#fee2e2';
                    hmiStatusBadge.style.color = '#b91c1c';
                }

                document.getElementById('lastUpdateTime').innerText = data.last_sensor_update || 'Live';

                // 4. Update Chart Data
                if (data.history && data.history.length > 0) {
                    chart.data.labels = data.history.map(h => h.time);
                    chart.data.datasets[0].data = data.history.map(h => h.adc);
                    // Garis ambang batas statis untuk referensi visual
                    chart.data.datasets[1].data = data.history.map(() => 2100);
                    chart.data.datasets[2].data = data.history.map(() => 1800);
                    chart.update('none');
                }

                // 5. Update Activity Feed
                const logBox = document.getElementById('logBox');
                if (data.logs && data.logs.length > 0) {
                    logBox.innerHTML = data.logs.map(logStr => {
                        const match = logStr.match(/^\\[([^\\]]+)\\]\\s*(.*)$/);
                        const time = match ? match[1] : '';
                        const msg = match ? match[2] : logStr;
                        return `
                            <div class="log-entry">
                                <span class="log-dot"></span>
                                <div class="log-text">
                                    <span class="log-time">[${time}]</span> ${msg}
                                </div>
                            </div>
                        `;
                    }).join('');
                }

            } catch (err) {
                console.error("Gagal sinkronisasi data:", err);
            }
        }

        setInterval(fetchData, 1000);
        fetchData();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/status")
def get_status():
    with state_lock:
        return jsonify(system_state)

@app.route("/api/pump", methods=["POST"])
def control_pump():
    data = request.get_json() or {}
    state = int(data.get("state", 0))
    if mqtt_client:
        payload = json.dumps({"state": state})
        mqtt_client.publish(TOPIC_PUMP_SET, payload)
        add_log(f"[HMI MANUAL OVERRIDE] Mengirim perintah pompa: {'ON' if state else 'OFF'}")
    return jsonify({"status": "ok", "state": state})

@app.route("/api/toggle_mode", methods=["POST"])
def toggle_mode():
    with state_lock:
        target_mode = not system_state["auto_mode"]
    if mqtt_client:
        payload = json.dumps({"auto": target_mode})
        mqtt_client.publish(TOPIC_MODE_SET, payload)
        add_log(f"[HMI OVERRIDE] Mengirim perintah ubah mode ke Gateway: {'OTOMATIS' if target_mode else 'MANUAL'}")
    return jsonify({"status": "ok", "target_mode": target_mode})

def main():
    print("==================================================")
    print("  DESIOT ITS SURABAYA - WEB DASHBOARD SERVER      ")
    print("  Membuka koneksi ke Mosquitto Broker...         ")
    print("==================================================")
    start_mqtt_thread()

    print("\n>>> WEB DASHBOARD BERJALAN! <<<")
    print("Silakan buka di browser Anda: http://localhost:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    main()
