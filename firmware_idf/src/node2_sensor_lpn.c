/* =========================================================================
 * DESIOT ITS SURABAYA - NODE 2: SENSOR KELEMBAPAN (LOW POWER NODE / LPN)
 * Framework : ESP-IDF Murni (Tanpa Arduino, Tanpa Hack Wrapper)
 * Hardware  : ESP32-S3 DevKitC-1, Capacitive Soil Moisture Sensor v1.2
 * Peran     : LPN (Membaca ADC, Mengirim Telemetri ke Gateway, Light Sleep)
 * ========================================================================= */

#include <stdio.h>
#include <string.h>
#include <inttypes.h>

#include "esp_log.h"
#include "esp_sleep.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_adc/adc_oneshot.h"

#include "esp_ble_mesh_defs.h"
#include "esp_ble_mesh_common_api.h"
#include "esp_ble_mesh_networking_api.h"
#include "esp_ble_mesh_provisioning_api.h"
#include "esp_ble_mesh_config_model_api.h"
#include "esp_ble_mesh_low_power_api.h"

#include "mesh_common.h"
#include "ble_mesh_init.h"

#define TAG "NODE2_SENSOR_LPN"

// Device UUID untuk Node 2 (Byte ke-15 diakhiri 0x02)
static uint8_t dev_uuid[16] = {
    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
    0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x02
};

static bool is_node_provisioned = false;
static bool is_appkey_bound = false;
static uint32_t cycle_count = 0;

// Handle ADC OneShot
static adc_oneshot_unit_handle_t adc1_handle;

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

// Vendor Model Opcode
static esp_ble_mesh_model_op_t vnd_op[] = {
    ESP_BLE_MESH_MODEL_OP(ESP_BLE_MESH_VND_MODEL_OP_SENSOR_STATUS, 1),
    ESP_BLE_MESH_MODEL_OP_END,
};

ESP_BLE_MESH_MODEL_PUB_DEFINE(vnd_pub, 3 + 1, ROLE_NODE);

static esp_ble_mesh_model_t root_models[] = {
    ESP_BLE_MESH_MODEL_CFG_SRV(&config_server),
};

static esp_ble_mesh_model_t vnd_models[] = {
    ESP_BLE_MESH_VENDOR_MODEL(CID_ESP, 0x0002, vnd_op, &vnd_pub, NULL),
};

static esp_ble_mesh_elem_t elements[] = {
    ESP_BLE_MESH_ELEMENT(0, root_models, vnd_models),
};

static esp_ble_mesh_comp_t composition = {
    .cid = CID_ESP,
    .element_count = ARRAY_SIZE(elements),
    .elements = elements,
};

static esp_ble_mesh_prov_t prov = {
    .uuid = dev_uuid,
};

// Inisialisasi ADC OneShot ESP-IDF untuk GPIO 4 (ADC1_CH3)
static void init_adc_hardware(void)
{
    adc_oneshot_unit_init_cfg_t init_config1 = {
        .unit_id = ADC_UNIT_1,
    };
    ESP_ERROR_CHECK(adc_oneshot_new_unit(&init_config1, &adc1_handle));

    adc_oneshot_chan_cfg_t config = {
        .bitwidth = ADC_BITWIDTH_DEFAULT,
        .atten = ADC_ATTEN_DB_12,
    };
    ESP_ERROR_CHECK(adc_oneshot_config_channel(adc1_handle, ADC_CHANNEL_3, &config));
    ESP_LOGI(TAG, "ADC1 Channel 3 (GPIO 4) berhasil diinisialisasi");
}

// Baca Sensor Kelembapan dengan Filter Rata-rata 10 Sampel
static int read_soil_moisture_filtered(void)
{
    int raw_val = 0;
    long sum = 0;
    const int SAMPLES = 10;

    for (int i = 0; i < SAMPLES; i++) {
        ESP_ERROR_CHECK(adc_oneshot_read(adc1_handle, ADC_CHANNEL_3, &raw_val));
        sum += raw_val;
        vTaskDelay(pdMS_TO_TICKS(10));
    }
    return (int)(sum / SAMPLES);
}

// Kirim Data Telemetri ke Node 4 (Gateway) via BLE Mesh
static void send_sensor_telemetry_to_gateway(uint16_t adc_val)
{
    esp_ble_mesh_msg_ctx_t ctx = {
        .net_idx = ESP_BLE_MESH_NET_IDX,
        .app_idx = ESP_BLE_MESH_APP_IDX,
        .addr = ADDR_GATEWAY_NODE, // Target: 0x0001
        .send_ttl = 7,
    };

    esp_err_t err = esp_ble_mesh_server_model_send_msg(&vnd_models[0], &ctx,
                                                       ESP_BLE_MESH_VND_MODEL_OP_SENSOR_DATA,
                                                       sizeof(adc_val), (uint8_t *)&adc_val);
    if (err == ESP_OK) {
        ESP_LOGI(TAG, "[NODE 2 -> GATEWAY] Paket telemetri (%u) berhasil dikirim ke Mesh", adc_val);
    } else {
        ESP_LOGE(TAG, "[NODE 2 -> GATEWAY] Gagal kirim paket: %s", esp_err_to_name(err));
    }
}

// Callback Provisioning
static void ble_mesh_prov_cb(esp_ble_mesh_prov_cb_event_t event,
                             esp_ble_mesh_prov_cb_param_t *param)
{
    switch (event) {
    case ESP_BLE_MESH_NODE_PROV_ENABLE_COMP_EVT:
        ESP_LOGI(TAG, "[NODE 2] Beacon Unprovisioned aktif, menunggu Provisioner (Node 4)...");
        break;
    case ESP_BLE_MESH_NODE_PROV_COMPLETE_EVT:
        is_node_provisioned = true;
        ESP_LOGI(TAG, "==================================================");
        ESP_LOGI(TAG, "[NODE 2] PROVISIONING BERHASIL! Addr: 0x%04X", param->node_prov_complete.addr);
        ESP_LOGI(TAG, "[NODE 2] Mengaktifkan Low Power Node (LPN) mode...");
        ESP_LOGI(TAG, "==================================================");
        esp_ble_mesh_lpn_enable();
        break;
    case ESP_BLE_MESH_NODE_PROV_RESET_EVT:
        is_node_provisioned = false;
        is_appkey_bound = false;
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
            is_appkey_bound = true;
            ESP_LOGI(TAG, "[NODE 2] AppKey berhasil di-bind ke Vendor Sensor Model!");
        }
    }
}

// Task Siklus Baca Sensor dan Light Sleep
static void lpn_sensor_cycle_task(void *arg)
{
    while (1) {
        // Tunggu hingga node terprovisi dan AppKey terikat
        if (!is_node_provisioned || !is_appkey_bound) {
            vTaskDelay(pdMS_TO_TICKS(1000));
            continue;
        }

        cycle_count++;
        ESP_LOGI(TAG, "--------------------------------------------------");
        ESP_LOGI(TAG, "DESIOT ITS - NODE 2: SENSOR KELEMBAPAN (LPN)");
        ESP_LOGI(TAG, "Siklus Kerja (Cycle Count): #%" PRIu32, cycle_count);

        // 1. Baca Sensor Kelembapan
        int moisture_adc = read_soil_moisture_filtered();
        const char *status_tanah = (moisture_adc >= SOIL_DRY_THRESHOLD) ? "KERING (Butuh Penyiraman)" :
                                   ((moisture_adc <= SOIL_WET_THRESHOLD) ? "BASAH (Cukup Air)" : "OPTIMAL (Normal)");

        ESP_LOGI(TAG, "[SENSOR] Nilai ADC: %d | Status: %s", moisture_adc, status_tanah);

        // 2. Kirim Telemetri ke Gateway via BLE Mesh
        send_sensor_telemetry_to_gateway((uint16_t)moisture_adc);

        // Beri jeda 500ms agar pengiriman radio selesai dengan aman
        vTaskDelay(pdMS_TO_TICKS(500));

        // 3. Jeda Pengukuran (5 detik untuk responsivitas pengujian real-time)
        ESP_LOGI(TAG, "[SENSOR] Jeda 5 detik sebelum pengukuran berikutnya...");
        ESP_LOGI(TAG, "--------------------------------------------------");
        vTaskDelay(pdMS_TO_TICKS(5000));
    }
}

void app_main(void)
{
    esp_err_t err;

    ESP_LOGI(TAG, "Memulai Node 2 (Sensor Kelembapan LPN)...");

    // 1. Inisialisasi Hardware ADC Sensor
    init_adc_hardware();

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

    // 5. Inisialisasi BLE Mesh
    err = esp_ble_mesh_init(&prov, &composition);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Gagal inisialisasi BLE Mesh: %s", esp_err_to_name(err));
        return;
    }

    // 6. Cek Status NVS: Apakah Node sudah pernah diprovisi sebelumnya?
    if (esp_ble_mesh_node_is_provisioned()) {
        ESP_LOGI(TAG, "==================================================");
        ESP_LOGI(TAG, "[NODE 2] Node sudah terprovisi di NVS! Langsung aktif.");
        ESP_LOGI(TAG, "==================================================");
        is_node_provisioned = true;
        is_appkey_bound = true;
    } else {
        err = esp_ble_mesh_node_prov_enable(ESP_BLE_MESH_PROV_ADV | ESP_BLE_MESH_PROV_GATT);
        if (err != ESP_OK) {
            ESP_LOGE(TAG, "Gagal aktifkan unprov advertising: %s", esp_err_to_name(err));
            return;
        }
        ESP_LOGI(TAG, "[NODE 2] Beacon Unprovisioned aktif, menunggu Provisioner (Node 4)...");
    }

    // 7. Jalankan Task Siklus Sensor
    xTaskCreate(lpn_sensor_cycle_task, "lpn_task", 4096, NULL, 5, NULL);
}
