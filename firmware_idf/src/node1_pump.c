/* =========================================================================
 * DESIOT ITS SURABAYA - NODE 1: POMPA AIR DC (GENERIC ONOFF SERVER)
 * Framework : ESP-IDF Murni (Tanpa Arduino, Tanpa Hack Wrapper)
 * Hardware  : ESP32-S3 DevKitC-1, Modul Relay 1-Channel (Active-LOW)
 * Peran     : Generic OnOff Server (Menerima perintah ON/OFF dari Mesh)
 * ========================================================================= */

#include <stdio.h>
#include <string.h>
#include <inttypes.h>

#include "esp_log.h"
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "esp_ble_mesh_defs.h"
#include "esp_ble_mesh_common_api.h"
#include "esp_ble_mesh_networking_api.h"
#include "esp_ble_mesh_provisioning_api.h"
#include "esp_ble_mesh_config_model_api.h"
#include "esp_ble_mesh_generic_model_api.h"

#include "mesh_common.h"
#include "ble_mesh_init.h"

#define TAG "NODE1_PUMP"

// Device UUID untuk Node 1 (Byte ke-15 diakhiri 0x01)
static uint8_t dev_uuid[16] = {
    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
    0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x01
};

// State OnOff Pompa (0 = OFF, 1 = ON)
static uint8_t pump_onoff_state = 0;

// Konfigurasi SIG Config Server
static esp_ble_mesh_cfg_srv_t config_server = {
    .net_transmit = ESP_BLE_MESH_TRANSMIT(2, 20),
    .relay = ESP_BLE_MESH_RELAY_DISABLED,
    .relay_retransmit = ESP_BLE_MESH_TRANSMIT(2, 20),
    .beacon = ESP_BLE_MESH_BEACON_ENABLED,
    .gatt_proxy = ESP_BLE_MESH_GATT_PROXY_ENABLED,
    .friend_state = ESP_BLE_MESH_FRIEND_NOT_SUPPORTED,
    .default_ttl = 7,
};

// Struktur Model Generic OnOff Server
static esp_ble_mesh_gen_onoff_srv_t onoff_server = {
    .rsp_ctrl.get_auto_rsp = ESP_BLE_MESH_SERVER_RSP_BY_APP,
    .rsp_ctrl.set_auto_rsp = ESP_BLE_MESH_SERVER_RSP_BY_APP,
};

ESP_BLE_MESH_MODEL_PUB_DEFINE(onoff_pub, 2 + 1, ROLE_NODE);

static esp_ble_mesh_model_t root_models[] = {
    ESP_BLE_MESH_MODEL_CFG_SRV(&config_server),
    ESP_BLE_MESH_MODEL_GEN_ONOFF_SRV(&onoff_pub, &onoff_server),
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

// Fungsi Kontrol Aktuator Relay Fisik (GPIO 10, Active-LOW)
static void apply_pump_state(uint8_t state, const char* source)
{
    pump_onoff_state = state ? 1 : 0;

    // Active-LOW Relay:
    // state = 1 (ON)  --> GPIO 10 = LOW (0V) -> Relay Klik Menutup -> Pompa Menyala
    // state = 0 (OFF) --> GPIO 10 = HIGH (3.3V) -> Relay Membuka -> Pompa Padam
    gpio_set_level((gpio_num_t)PIN_RELAY_PUMP, pump_onoff_state ? 0 : 1);
    gpio_set_level((gpio_num_t)PIN_STATUS_LED, pump_onoff_state ? 1 : 0);

    ESP_LOGI(TAG, "==================================================");
    ESP_LOGI(TAG, "[NODE 1 - POMPA] Status Pompa: %s (Sumber: %s)",
             pump_onoff_state ? ">>> MENYALA (ON) <<<" : ">>> PADAM (OFF) <<<", source);
    ESP_LOGI(TAG, "[NODE 1 - POMPA] GPIO %d Signal: %s (Active-LOW Mode)",
             PIN_RELAY_PUMP, pump_onoff_state ? "LOW (0V)" : "HIGH (3.3V)");
    ESP_LOGI(TAG, "==================================================");
}

// Inisialisasi GPIO Pin Relay dan Status LED
static void init_relay_hardware(void)
{
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << PIN_RELAY_PUMP) | (1ULL << PIN_STATUS_LED),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&io_conf);

    // Default kondisi awal: Pompa Padam (Relay High)
    apply_pump_state(0, "Inisialisasi Hardware");
}

// Callback Provisioning
static void ble_mesh_prov_cb(esp_ble_mesh_prov_cb_event_t event,
                             esp_ble_mesh_prov_cb_param_t *param)
{
    switch (event) {
    case ESP_BLE_MESH_NODE_PROV_ENABLE_COMP_EVT:
        ESP_LOGI(TAG, "[NODE 1] Beacon Unprovisioned aktif, menunggu Provisioner...");
        break;
    case ESP_BLE_MESH_NODE_PROV_COMPLETE_EVT:
        ESP_LOGI(TAG, "==================================================");
        ESP_LOGI(TAG, "[NODE 1] PROVISIONING SELESAI!");
        ESP_LOGI(TAG, "[NODE 1] Unicast Address : 0x%04X", param->node_prov_complete.addr);
        ESP_LOGI(TAG, "[NODE 1] Peran           : GENERIC ONOFF SERVER");
        ESP_LOGI(TAG, "==================================================");
        break;
    case ESP_BLE_MESH_NODE_PROV_RESET_EVT:
        ESP_LOGW(TAG, "[NODE 1] Node di-reset dari jaringan.");
        break;
    default:
        break;
    }
}

// Callback Generic Server (Menerima perintah standar OnOff Get/Set)
static void ble_mesh_generic_server_cb(esp_ble_mesh_generic_server_cb_event_t event,
                                       esp_ble_mesh_generic_server_cb_param_t *param)
{
    switch (event) {
    case ESP_BLE_MESH_GENERIC_SERVER_STATE_CHANGE_EVT:
        if (param->ctx.recv_op == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET ||
            param->ctx.recv_op == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET_UNACK) {
            apply_pump_state(param->value.state_change.onoff_set.onoff, "BLE Mesh Generic OnOff");
        }
        break;
    case ESP_BLE_MESH_GENERIC_SERVER_RECV_GET_MSG_EVT:
        if (param->ctx.recv_op == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_GET) {
            esp_ble_mesh_server_model_send_msg(param->model, &param->ctx,
                                               ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_STATUS,
                                               sizeof(pump_onoff_state), &pump_onoff_state);
        }
        break;
    case ESP_BLE_MESH_GENERIC_SERVER_RECV_SET_MSG_EVT:
        if (param->ctx.recv_op == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET ||
            param->ctx.recv_op == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET_UNACK) {
            apply_pump_state(param->value.set.onoff.onoff, "BLE Mesh Set Message");
            if (param->ctx.recv_op == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET) {
                esp_ble_mesh_server_model_send_msg(param->model, &param->ctx,
                                                   ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_STATUS,
                                                   sizeof(pump_onoff_state), &pump_onoff_state);
            }
        }
        break;
    default:
        break;
    }
}

// Callback Config Server
static void ble_mesh_cfg_server_cb(esp_ble_mesh_cfg_server_cb_event_t event,
                                   esp_ble_mesh_cfg_server_cb_param_t *param)
{
    if (event == ESP_BLE_MESH_CFG_SERVER_STATE_CHANGE_EVT) {
        if (param->ctx.recv_op == ESP_BLE_MESH_MODEL_OP_MODEL_APP_BIND) {
            ESP_LOGI(TAG, "[NODE 1] AppKey berhasil di-bind ke Generic OnOff Server!");
        }
    }
}

void app_main(void)
{
    esp_err_t err;

    ESP_LOGI(TAG, "Memulai inisialisasi Node 1 (Pompa OnOff Server)...");

    // 1. Inisialisasi Hardware Relay Pompa
    init_relay_hardware();

    // 2. Inisialisasi NVS Flash
    err = init_nvs_storage();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Inisialisasi NVS gagal: %s", esp_err_to_name(err));
        return;
    }

    // 3. Inisialisasi Bluetooth Stack
    err = init_bluetooth_stack();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Inisialisasi Bluetooth gagal: %s", esp_err_to_name(err));
        return;
    }

    // 4. Daftarkan Callback Resmi
    esp_ble_mesh_register_prov_callback(ble_mesh_prov_cb);
    esp_ble_mesh_register_config_server_callback(ble_mesh_cfg_server_cb);
    esp_ble_mesh_register_generic_server_callback(ble_mesh_generic_server_cb);

    // 5. Inisialisasi BLE Mesh
    err = esp_ble_mesh_init(&prov, &composition);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Gagal inisialisasi BLE Mesh: %s", esp_err_to_name(err));
        return;
    }

    // 6. Cek Status NVS: Apakah Node sudah pernah diprovisi sebelumnya?
    if (esp_ble_mesh_node_is_provisioned()) {
        ESP_LOGI(TAG, "==================================================");
        ESP_LOGI(TAG, "[NODE 1] Node sudah terprovisi di NVS! Langsung aktif.");
        ESP_LOGI(TAG, "==================================================");
    } else {
        err = esp_ble_mesh_node_prov_enable(ESP_BLE_MESH_PROV_ADV | ESP_BLE_MESH_PROV_GATT);
        if (err != ESP_OK) {
            ESP_LOGE(TAG, "Gagal aktifkan unprov advertising: %s", esp_err_to_name(err));
            return;
        }
        ESP_LOGI(TAG, "[NODE 1] Beacon Unprovisioned aktif, menunggu Provisioner (Node 4)...");
    }

    ESP_LOGI(TAG, "[NODE 1] Siaga menerima perintah Generic OnOff dari Jaringan Mesh.");
}
