#ifndef MESH_COMMON_H
#define MESH_COMMON_H

#include <stdint.h>
#include <esp_ble_mesh_defs.h>

/* =========================================================================
 * DESIOT ITS SURABAYA - BLE MESH & MQTT GATEWAY SYSTEM (ESP-IDF MURNI)
 * Definisi Konstanta, Alamat Unicast, dan Protokol Bersama
 * ========================================================================= */

// Identitas Perusahaan (Espressif Company ID)
#define CID_ESP                         0x02E5

// Indeks Jaringan & Aplikasi BLE Mesh
#define ESP_BLE_MESH_NET_IDX            0x0000
#define ESP_BLE_MESH_APP_IDX            0x0000

// Alamat Unicast Standar
#define ADDR_GATEWAY_NODE               0x0001  // Node 4: Provisioner & Gateway
#define ADDR_PUMP_NODE                  0x0002  // Node 1: Pompa Generic OnOff Server
#define ADDR_SENSOR_NODE                0x0003  // Node 2: Sensor Kelembapan LPN
#define ADDR_RELAY_FRIEND_NODE          0x0004  // Node 3: Relay + Friend Node
#define ADDR_ALL_NODES_GROUP            0xC001  // Group Address Broadcast

// Opcode Vendor Model untuk Sensor Telemetri
#define ESP_BLE_MESH_VND_MODEL_OP_SENSOR_DATA   ESP_BLE_MESH_MODEL_OP_3(0x01, CID_ESP)
#define ESP_BLE_MESH_VND_MODEL_OP_SENSOR_STATUS ESP_BLE_MESH_MODEL_OP_3(0x02, CID_ESP)

// Pinout Hardware ESP32-S3
#define PIN_RELAY_PUMP                  10      // GPIO 10: Relay Pompa (Active-LOW)
#define PIN_SOIL_ANALOG                 4       // GPIO 4: ADC1_CH3 Sensor Kelembapan
#define PIN_STATUS_LED                  2       // GPIO 2: Status Onboard LED

// Ambang Batas Sensor Kelembapan (Kapasitif v1.2)
#define SOIL_DRY_THRESHOLD              2100    // ADC >= 2100 -> Kering (Pompa Butuh ON)
#define SOIL_WET_THRESHOLD              1800    // ADC <= 1800 -> Basah (Pompa Harus OFF)
#define LPN_SLEEP_DURATION_SEC          15      // Durasi Light Sleep berkala LPN

// Kredensial Wi-Fi & MQTT Gateway (Node 4)
#define WIFI_SSID_CONFIG                "WIFI-DTM2"
#define WIFI_PASS_CONFIG                ""
#define MQTT_BROKER_URL_CONFIG          "mqtt://10.3.74.117:1883"
#define MQTT_TOPIC_SENSOR               "desiot/kebun/sensor"
#define MQTT_TOPIC_PUMP_STATE           "desiot/kebun/pompa"
#define MQTT_TOPIC_PUMP_SET             "desiot/kebun/pompa/set"
#define MQTT_TOPIC_MODE_SET             "desiot/kebun/mode/set"

#endif // MESH_COMMON_H
