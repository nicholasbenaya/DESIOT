/* =========================================================================
 * DESIOT ITS SURABAYA - NODE 3: RELAY + FRIEND NODE
 * Framework : ESP-IDF Murni (Tanpa Arduino, Tanpa Hack Wrapper)
 * Hardware  : ESP32-S3 DevKitC-1
 * Peran     : Relay paket mesh antar node & Friend Node (cache pesan LPN)
 * ========================================================================= */

#include <stdio.h>
#include <string.h>
#include <inttypes.h>

#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "esp_ble_mesh_defs.h"
#include "esp_ble_mesh_common_api.h"
#include "esp_ble_mesh_networking_api.h"
#include "esp_ble_mesh_provisioning_api.h"
#include "esp_ble_mesh_config_model_api.h"

#include "mesh_common.h"
#include "ble_mesh_init.h"

#define TAG "NODE3_RELAY_FRIEND"

// Device UUID untuk Node 3 (Byte ke-15 diakhiri 0x03)
static uint8_t dev_uuid[16] = {
    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
    0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x03
};

// Konfigurasi Standar SIG Config Server
static esp_ble_mesh_cfg_srv_t config_server = {
    .net_transmit = ESP_BLE_MESH_TRANSMIT(1, 40),      // Retransmit 1 kali, interval 40ms (mencegah tabrakan RF)
    .relay = ESP_BLE_MESH_RELAY_ENABLED,               // FITUR RELAY AKTIF
    .relay_retransmit = ESP_BLE_MESH_TRANSMIT(1, 40),  // Meneruskan paket 1 kali, interval 40ms (mencegah tabrakan RF)
    .beacon = ESP_BLE_MESH_BEACON_ENABLED,
    .gatt_proxy = ESP_BLE_MESH_GATT_PROXY_ENABLED,
    .friend_state = ESP_BLE_MESH_FRIEND_ENABLED,       // FITUR FRIEND NODE AKTIF
    .default_ttl = 7,
};

static esp_ble_mesh_model_t root_models[] = {
    ESP_BLE_MESH_MODEL_CFG_SRV(&config_server),
};

static esp_ble_mesh_elem_t elements[] = {
    ESP_BLE_MESH_ELEMENT(0, root_models, ESP_BLE_MESH_MODEL_NONE),
};

static esp_ble_mesh_comp_t composition = {
    .cid = CID_ESP,
    .element_count = ARRAY_SIZE(elements),
    .elements = elements,
};

static esp_ble_mesh_prov_t prov = {
    .uuid = dev_uuid,
};

static bool is_node_provisioned = false;
static uint16_t node_unicast_addr = 0x0000;

// Callback Provisioning BLE Mesh
static void ble_mesh_prov_cb(esp_ble_mesh_prov_cb_event_t event,
                             esp_ble_mesh_prov_cb_param_t *param)
{
    switch (event) {
    case ESP_BLE_MESH_NODE_PROV_ENABLE_COMP_EVT:
        ESP_LOGI(TAG, "[NODE 3] Beacon Unprovisioned aktif, menunggu Provisioner (Node 4)...");
        break;
    case ESP_BLE_MESH_NODE_PROV_COMPLETE_EVT:
        node_unicast_addr = param->node_prov_complete.addr;
        is_node_provisioned = true;
        ESP_LOGI(TAG, "==================================================");
        ESP_LOGI(TAG, "[NODE 3] PROVISIONING BERHASIL!");
        ESP_LOGI(TAG, "[NODE 3] Unicast Address : 0x%04X", node_unicast_addr);
        ESP_LOGI(TAG, "[NODE 3] NetKey Index    : 0x%04X", param->node_prov_complete.net_idx);
        ESP_LOGI(TAG, "[NODE 3] Peran Aktif     : RELAY + FRIEND NODE");
        ESP_LOGI(TAG, "==================================================");
        break;
    case ESP_BLE_MESH_NODE_PROV_RESET_EVT:
        ESP_LOGW(TAG, "[NODE 3] Node di-reset dari jaringan Mesh.");
        is_node_provisioned = false;
        break;
    default:
        break;
    }
}

// Callback Konfigurasi Server (saat Node 4 mengonfigurasi fitur)
static void ble_mesh_cfg_server_cb(esp_ble_mesh_cfg_server_cb_event_t event,
                                   esp_ble_mesh_cfg_server_cb_param_t *param)
{
    if (event == ESP_BLE_MESH_CFG_SERVER_STATE_CHANGE_EVT) {
        switch (param->ctx.recv_op) {
        case ESP_BLE_MESH_MODEL_OP_APP_KEY_ADD:
            ESP_LOGI(TAG, "[NODE 3] AppKey berhasil ditambahkan oleh Provisioner (AppIdx: 0x%04X)",
                     param->value.state_change.appkey_add.app_idx);
            break;
        case ESP_BLE_MESH_MODEL_OP_MODEL_APP_BIND:
            ESP_LOGI(TAG, "[NODE 3] Model AppKey berhasil di-bind oleh Provisioner");
            break;
        default:
            break;
        }
    }
}

// Task Periodic Status Monitor
static void status_heartbeat_task(void *arg)
{
    uint32_t uptime_sec = 0;
    while (1) {
        vTaskDelay(pdMS_TO_TICKS(10000));
        uptime_sec += 10;

        ESP_LOGI(TAG, "--------------------------------------------------");
        ESP_LOGI(TAG, "DESIOT ITS - NODE 3 (RELAY + FRIEND NODE)");
        ESP_LOGI(TAG, "Uptime: %" PRIu32 " detik | Status: %s",
                 uptime_sec, is_node_provisioned ? "TERPROVISI (ONLINE)" : "SIAGA MENUNGGU PROVISIONER");
        ESP_LOGI(TAG, "Fitur Relay  : AKTIF (RX Continuous Scan & Flood Retransmit)");
        ESP_LOGI(TAG, "Fitur Friend : AKTIF (Siaga Menerima Permintaan Friendship)");
        ESP_LOGI(TAG, "--------------------------------------------------");
    }
}

void app_main(void)
{
    esp_err_t err;

    ESP_LOGI(TAG, "Memulai inisialisasi Node 3 (ESP-IDF Murni)...");

    // 1. Inisialisasi NVS Flash (Wajib untuk BLE Mesh)
    err = init_nvs_storage();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Inisialisasi NVS gagal: %s", esp_err_to_name(err));
        return;
    }

    // 2. Inisialisasi Bluetooth Controller & Bluedroid Host Stack
    err = init_bluetooth_stack();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Inisialisasi Bluetooth gagal: %s", esp_err_to_name(err));
        return;
    }

    // 3. Daftarkan Callback Resmi ESP-BLE-MESH
    err = esp_ble_mesh_register_prov_callback(ble_mesh_prov_cb);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Gagal register prov callback: %s", esp_err_to_name(err));
        return;
    }

    err = esp_ble_mesh_register_config_server_callback(ble_mesh_cfg_server_cb);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Gagal register cfg server callback: %s", esp_err_to_name(err));
        return;
    }

    // 4. Inisialisasi Core BLE Mesh Node
    err = esp_ble_mesh_init(&prov, &composition);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Gagal inisialisasi BLE Mesh: %s", esp_err_to_name(err));
        return;
    }

    // 5. Cek Status NVS: Apakah Node sudah pernah diprovisi sebelumnya?
    if (esp_ble_mesh_node_is_provisioned()) {
        ESP_LOGI(TAG, "==================================================");
        ESP_LOGI(TAG, "[NODE 3] Node sudah terprovisi di NVS! Langsung aktif.");
        ESP_LOGI(TAG, "==================================================");
        is_node_provisioned = true;
    } else {
        err = esp_ble_mesh_node_prov_enable(ESP_BLE_MESH_PROV_ADV | ESP_BLE_MESH_PROV_GATT);
        if (err != ESP_OK) {
            ESP_LOGE(TAG, "Gagal aktifkan unprov advertising: %s", esp_err_to_name(err));
            return;
        }
        ESP_LOGI(TAG, "[NODE 3] Beacon Unprovisioned aktif, menunggu Provisioner (Node 4)...");
    }

    ESP_LOGI(TAG, "Node 3 siap beroperasi.");

    // 6. Jalankan FreeRTOS Task Pemantauan Heartbeat
    xTaskCreate(status_heartbeat_task, "status_task", 3072, NULL, 5, NULL);
}
