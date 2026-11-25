/* =========================================================================
 * DESIOT ITS SURABAYA - NODE 4: PROVISIONER + PROXY + GATEWAY WI-FI MQTT
 * Framework : ESP-IDF Murni (Tanpa Arduino, Tanpa Hack Wrapper)
 * Hardware  : ESP32-S3 DevKitC-1
 * Peran     : Provisioner BLE Mesh, Gateway Wi-Fi, dan Client MQTT
 * ========================================================================= */

#include <stdio.h>
#include <string.h>
#include <inttypes.h>

#include "esp_log.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_netif.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "mqtt_client.h"

#include "esp_ble_mesh_defs.h"
#include "esp_ble_mesh_common_api.h"
#include "esp_ble_mesh_networking_api.h"
#include "esp_ble_mesh_provisioning_api.h"
#include "esp_ble_mesh_config_model_api.h"
#include "esp_ble_mesh_generic_model_api.h"

#include "mesh_common.h"
#include "ble_mesh_init.h"

#define TAG "NODE4_GATEWAY"

// AppKey & NetKey Standar BLE Mesh
static const uint8_t mesh_net_key[16] = {
    0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88,
    0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x00
};

static const uint8_t mesh_app_key[16] = {
    0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x00, 0x11,
    0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99
};

// Device UUID untuk Node 4 (Provisioner)
static uint8_t dev_uuid[16] = {
    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
    0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x04
};

// Status Wi-Fi dan MQTT
static EventGroupHandle_t wifi_event_group;
#define WIFI_CONNECTED_BIT BIT0
static esp_mqtt_client_handle_t mqtt_client = NULL;
static bool mqtt_connected = false;

// State Otomasi Edge di Gateway (Mandiri tanpa host / Single Point of Failure)
static bool edge_auto_mode = true;          // Default: Edge Autonomy AKTIF
static int8_t current_pump_state = -1;      // Status pompa terakhir (0 = OFF, 1 = ON, -1 = Belum diset)

// Transaction ID counter
static uint8_t client_tid = 0;

// Konfigurasi SIG Config Server & Client
static esp_ble_mesh_cfg_srv_t config_server = {
    .net_transmit = ESP_BLE_MESH_TRANSMIT(2, 20),
    .relay = ESP_BLE_MESH_RELAY_DISABLED,
    .relay_retransmit = ESP_BLE_MESH_TRANSMIT(2, 20),
    .beacon = ESP_BLE_MESH_BEACON_ENABLED,
    .gatt_proxy = ESP_BLE_MESH_GATT_PROXY_ENABLED,
    .friend_state = ESP_BLE_MESH_FRIEND_NOT_SUPPORTED,
    .default_ttl = 7,
};

static esp_ble_mesh_client_t config_client;
static esp_ble_mesh_client_t onoff_client;

ESP_BLE_MESH_MODEL_PUB_DEFINE(onoff_cli_pub, 2 + 1, ROLE_NODE);

// Vendor Model Opcode untuk Menerima Telemetri dari Node 2
static esp_ble_mesh_model_op_t vnd_op[] = {
    ESP_BLE_MESH_MODEL_OP(ESP_BLE_MESH_VND_MODEL_OP_SENSOR_DATA, 2),
    ESP_BLE_MESH_MODEL_OP_END,
};

static esp_ble_mesh_model_t root_models[] = {
    ESP_BLE_MESH_MODEL_CFG_SRV(&config_server),
    ESP_BLE_MESH_MODEL_CFG_CLI(&config_client),
    ESP_BLE_MESH_MODEL_GEN_ONOFF_CLI(&onoff_cli_pub, &onoff_client),
};

static esp_ble_mesh_model_t vnd_models[] = {
    ESP_BLE_MESH_VENDOR_MODEL(CID_ESP, 0x0001, vnd_op, NULL, NULL),
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
    .prov_unicast_addr = ADDR_GATEWAY_NODE, // 0x0001
    .prov_start_address = 0x0002,
    .uuid = dev_uuid,
};

// Forward declaration
static void send_mesh_onoff_to_node1(uint8_t state);

// Callback Wi-Fi Event
static void wifi_event_handler(void* arg, esp_event_base_t event_base,
                               int32_t event_id, void* event_data)
{
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        ESP_LOGW(TAG, "Wi-Fi terputus, mencoba menghubungkan kembali...");
        esp_wifi_connect();
        xEventGroupClearBits(wifi_event_group, WIFI_CONNECTED_BIT);
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t* event = (ip_event_got_ip_t*) event_data;
        ESP_LOGI(TAG, "Wi-Fi Terhubung! Alamat IP: " IPSTR, IP2STR(&event->ip_info.ip));
        xEventGroupSetBits(wifi_event_group, WIFI_CONNECTED_BIT);
    }
}

// Inisialisasi Wi-Fi Station
static void init_wifi_station(void)
{
    wifi_event_group = xEventGroupCreate();
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    esp_event_handler_instance_t instance_any_id;
    esp_event_handler_instance_t instance_got_ip;
    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT,
                                                        ESP_EVENT_ANY_ID,
                                                        &wifi_event_handler,
                                                        NULL,
                                                        &instance_any_id));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT,
                                                        IP_EVENT_STA_GOT_IP,
                                                        &wifi_event_handler,
                                                        NULL,
                                                        &instance_got_ip));

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID_CONFIG,
            .password = WIFI_PASS_CONFIG,
            .threshold.authmode = WIFI_AUTH_OPEN,
        },
    };
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());
    ESP_LOGI(TAG, "Wi-Fi Station diinisialisasi untuk SSID: %s", WIFI_SSID_CONFIG);
}

// Callback Event MQTT
static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data)
{
    esp_mqtt_event_handle_t event = event_data;

    switch ((esp_mqtt_event_id_t)event_id) {
    case MQTT_EVENT_CONNECTED:
        ESP_LOGI(TAG, "MQTT Terhubung ke Mosquitto Broker (%s)!", MQTT_BROKER_URL_CONFIG);
        mqtt_connected = true;
        // Berlangganan (Subscribe) ke topik perintah pompa & mode dari komputer host
        esp_mqtt_client_subscribe(mqtt_client, MQTT_TOPIC_PUMP_SET, 0);
        esp_mqtt_client_subscribe(mqtt_client, MQTT_TOPIC_MODE_SET, 0);
        ESP_LOGI(TAG, "Subscribed ke topik: %s dan %s", MQTT_TOPIC_PUMP_SET, MQTT_TOPIC_MODE_SET);

        // Publish pesan status awal
        esp_mqtt_client_publish(mqtt_client, "desiot/kebun/gateway", "{\"status\":\"online\"}", 0, 1, 0);
        {
            char init_status[64];
            snprintf(init_status, sizeof(init_status), "{\"pump_state\":%d,\"auto_mode\":%s}",
                     current_pump_state >= 0 ? current_pump_state : 0,
                     edge_auto_mode ? "true" : "false");
            esp_mqtt_client_publish(mqtt_client, MQTT_TOPIC_PUMP_STATE, init_status, 0, 1, 0);
        }
        break;

    case MQTT_EVENT_DISCONNECTED:
        ESP_LOGW(TAG, "MQTT Terputus dari Broker");
        mqtt_connected = false;
        break;

    case MQTT_EVENT_DATA:
        ESP_LOGI(TAG, "Pesan MQTT Masuk [Topik: %.*s]: %.*s",
                 event->topic_len, event->topic, event->data_len, event->data);

        // 1. Periksa jika ada perintah ubah mode (OTOMATIS / MANUAL) dari HMI Dashboard
        if (strncmp(event->topic, MQTT_TOPIC_MODE_SET, event->topic_len) == 0) {
            char m_buf[64];
            if (strstr(event->data, "\"auto\": true") || strstr(event->data, "\"auto\":true") ||
                strstr(event->data, "\"auto\": 1") || strstr(event->data, "\"auto\":1")) {
                edge_auto_mode = true;
                ESP_LOGW(TAG, "[HMI OVERRIDE] Mode diubah ke OTOMATIS (Edge Autonomy Aktif)");
                snprintf(m_buf, sizeof(m_buf), "{\"pump_state\":%d,\"auto_mode\":true}",
                         current_pump_state >= 0 ? current_pump_state : 0);
                esp_mqtt_client_publish(mqtt_client, MQTT_TOPIC_PUMP_STATE, m_buf, 0, 1, 0);
            } else if (strstr(event->data, "\"auto\": false") || strstr(event->data, "\"auto\":false") ||
                       strstr(event->data, "\"auto\": 0") || strstr(event->data, "\"auto\":0")) {
                edge_auto_mode = false;
                ESP_LOGW(TAG, "[HMI OVERRIDE] Mode diubah ke MANUAL (Edge Autonomy Nonaktif)");
                snprintf(m_buf, sizeof(m_buf), "{\"pump_state\":%d,\"auto_mode\":false}",
                         current_pump_state >= 0 ? current_pump_state : 0);
                esp_mqtt_client_publish(mqtt_client, MQTT_TOPIC_PUMP_STATE, m_buf, 0, 1, 0);
            }
        }
        // 2. Periksa jika ada perintah kontrol manual pompa dari HMI Dashboard
        else if (strncmp(event->topic, MQTT_TOPIC_PUMP_SET, event->topic_len) == 0) {
            char p_buf[64];
            edge_auto_mode = false; // Override manual otomatis mematikan otomasi edge
            if (strstr(event->data, "\"state\": 1") || strstr(event->data, "\"state\":1") || strstr(event->data, "1")) {
                ESP_LOGI(TAG, "[HMI MANUAL OVERRIDE] Menerima perintah Pompa ON");
                current_pump_state = 1;
                send_mesh_onoff_to_node1(1);
                snprintf(p_buf, sizeof(p_buf), "{\"pump_state\":1,\"auto_mode\":false}");
                esp_mqtt_client_publish(mqtt_client, MQTT_TOPIC_PUMP_STATE, p_buf, 0, 1, 0);
            } else if (strstr(event->data, "\"state\": 0") || strstr(event->data, "\"state\":0") || strstr(event->data, "0")) {
                ESP_LOGI(TAG, "[HMI MANUAL OVERRIDE] Menerima perintah Pompa OFF");
                current_pump_state = 0;
                send_mesh_onoff_to_node1(0);
                snprintf(p_buf, sizeof(p_buf), "{\"pump_state\":0,\"auto_mode\":false}");
                esp_mqtt_client_publish(mqtt_client, MQTT_TOPIC_PUMP_STATE, p_buf, 0, 1, 0);
            }
        }
        break;

    default:
        break;
    }
}

// Inisialisasi MQTT Client
static void init_mqtt_client(void)
{
    esp_mqtt_client_config_t mqtt_cfg = {
        .broker.address.uri = MQTT_BROKER_URL_CONFIG,
    };
    mqtt_client = esp_mqtt_client_init(&mqtt_cfg);
    esp_mqtt_client_register_event(mqtt_client, ESP_EVENT_ANY_ID, mqtt_event_handler, NULL);
    esp_mqtt_client_start(mqtt_client);
}

// Tracking ID & Alamat Node Mesh
static uint8_t pending_prov_target_id = 0x01;
static uint16_t actual_pump_addr = 0x0003;
static uint16_t actual_sensor_addr = 0x0004;

// Fungsi helper mengikat model ke AppKey pada node target
static void bind_model_to_node(uint16_t addr, uint16_t model_id, uint16_t company_id)
{
    esp_ble_mesh_cfg_client_set_state_t set_state = {0};
    set_state.model_app_bind.element_addr = addr;
    set_state.model_app_bind.model_app_idx = ESP_BLE_MESH_APP_IDX;
    set_state.model_app_bind.model_id = model_id;
    set_state.model_app_bind.company_id = company_id;

    esp_ble_mesh_client_common_param_t common = {
        .opcode = ESP_BLE_MESH_MODEL_OP_MODEL_APP_BIND,
        .model = config_client.model,
        .ctx.net_idx = ESP_BLE_MESH_NET_IDX,
        .ctx.app_idx = ESP_BLE_MESH_APP_IDX,
        .ctx.addr = addr,
        .ctx.send_ttl = 7,
        .msg_role = ROLE_PROVISIONER,
    };
    esp_ble_mesh_config_client_set_state(&common, &set_state);
}

// Kirim Perintah Generic OnOff Set ke Node 1 via BLE Mesh
static void send_mesh_onoff_to_node1(uint8_t state)
{
    esp_ble_mesh_generic_client_set_state_t set_state = {
        .onoff_set.op_en = false,
        .onoff_set.onoff = state,
        .onoff_set.tid = client_tid++,
    };

    // Kirim Unacknowledged (SET_UNACK) ke alamat pompa aktual
    esp_ble_mesh_client_common_param_t common = {
        .opcode = ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET_UNACK,
        .model = onoff_client.model,
        .ctx.net_idx = ESP_BLE_MESH_NET_IDX,
        .ctx.app_idx = ESP_BLE_MESH_APP_IDX,
        .ctx.addr = actual_pump_addr,
        .ctx.send_ttl = 7,
        .ctx.send_rel = false,
        .msg_timeout = 0,
        .msg_role = ROLE_PROVISIONER,
    };

    esp_err_t err = esp_ble_mesh_generic_client_set_state(&common, &set_state);
    if (err == ESP_OK) {
        ESP_LOGI(TAG, "[NODE 4 -> ADDR 0x%04X] Mengirim Generic OnOff Set: %d", actual_pump_addr, state);
    } else {
        ESP_LOGE(TAG, "[NODE 4 -> ADDR 0x%04X] Gagal kirim: %s", actual_pump_addr, esp_err_to_name(err));
    }

    // Juga kirim ke 0x0002 jika actual_pump_addr != 0x0002 sebagai redundansi
    if (actual_pump_addr != 0x0002) {
        common.ctx.addr = 0x0002;
        esp_ble_mesh_generic_client_set_state(&common, &set_state);
    }
}

// Callback Provisioner BLE Mesh
static void ble_mesh_provisioning_cb(esp_ble_mesh_prov_cb_event_t event,
                                     esp_ble_mesh_prov_cb_param_t *param)
{
    switch (event) {
    case ESP_BLE_MESH_PROVISIONER_PROV_ENABLE_COMP_EVT:
        ESP_LOGI(TAG, "[PROVISIONER] Provisioner aktif. Menambahkan local AppKey...");
        esp_ble_mesh_provisioner_add_local_app_key(mesh_app_key, ESP_BLE_MESH_NET_IDX, ESP_BLE_MESH_APP_IDX);
        break;

    case ESP_BLE_MESH_PROVISIONER_ADD_LOCAL_APP_KEY_COMP_EVT:
        ESP_LOGI(TAG, "[PROVISIONER] Local AppKey selesai (err %d). Mengikat ke OnOff Client...",
                 param->provisioner_add_app_key_comp.err_code);
        if (param->provisioner_add_app_key_comp.err_code == ESP_OK) {
            esp_ble_mesh_provisioner_bind_app_key_to_local_model(ADDR_GATEWAY_NODE, ESP_BLE_MESH_APP_IDX,
                                                                 ESP_BLE_MESH_MODEL_ID_GEN_ONOFF_CLI, ESP_BLE_MESH_CID_NVAL);
        }
        break;

    case ESP_BLE_MESH_PROVISIONER_BIND_APP_KEY_TO_MODEL_COMP_EVT:
        ESP_LOGI(TAG, "[PROVISIONER] Local model (0x%04X, CID 0x%04X) selesai diikat ke AppKey (err %d)",
                 param->provisioner_bind_app_key_to_model_comp.model_id,
                 param->provisioner_bind_app_key_to_model_comp.company_id,
                 param->provisioner_bind_app_key_to_model_comp.err_code);
        if (param->provisioner_bind_app_key_to_model_comp.model_id == ESP_BLE_MESH_MODEL_ID_GEN_ONOFF_CLI) {
            // Lanjutkan ikat Local Vendor Model (0x0001, CID_ESP) untuk menerima telemetri Sensor Node 2
            esp_ble_mesh_provisioner_bind_app_key_to_local_model(ADDR_GATEWAY_NODE, ESP_BLE_MESH_APP_IDX,
                                                                 0x0001, CID_ESP);
        } else if (param->provisioner_bind_app_key_to_model_comp.model_id == 0x0001) {
            ESP_LOGI(TAG, "[PROVISIONER] Semua local model siap! Memastikan bind OnOff Server ke Node 1...");
            bind_model_to_node(0x0003, ESP_BLE_MESH_MODEL_ID_GEN_ONOFF_SRV, ESP_BLE_MESH_CID_NVAL);
            bind_model_to_node(0x0002, ESP_BLE_MESH_MODEL_ID_GEN_ONOFF_SRV, ESP_BLE_MESH_CID_NVAL);
        }
        break;

    case ESP_BLE_MESH_PROVISIONER_RECV_UNPROV_ADV_PKT_EVT: {
        uint8_t target_id = param->provisioner_recv_unprov_adv_pkt.dev_uuid[15];
        pending_prov_target_id = target_id;
        uint16_t assign_addr = 0x0000;

        if (target_id == 0x01) {
            assign_addr = ADDR_PUMP_NODE;         // 0x0002 (Node 1)
        } else if (target_id == 0x02) {
            assign_addr = ADDR_SENSOR_NODE;       // 0x0003 (Node 2)
        } else if (target_id == 0x03) {
            assign_addr = ADDR_RELAY_FRIEND_NODE; // 0x0004 (Node 3)
        }

        if (assign_addr != 0x0000) {
            ESP_LOGI(TAG, "[PROVISIONER] Menemukan Device target (ID: 0x%02X). Memulai Provisioning...",
                     target_id);

            esp_ble_mesh_unprov_dev_add_t add_dev = {0};
            memcpy(add_dev.addr, param->provisioner_recv_unprov_adv_pkt.addr, BD_ADDR_LEN);
            add_dev.addr_type = (esp_ble_mesh_addr_type_t)param->provisioner_recv_unprov_adv_pkt.addr_type;
            memcpy(add_dev.uuid, param->provisioner_recv_unprov_adv_pkt.dev_uuid, 16);
            add_dev.oob_info = param->provisioner_recv_unprov_adv_pkt.oob_info;
            add_dev.bearer = (esp_ble_mesh_prov_bearer_t)param->provisioner_recv_unprov_adv_pkt.bearer;

            esp_ble_mesh_provisioner_add_unprov_dev(&add_dev,
                (esp_ble_mesh_dev_add_flag_t)(ADD_DEV_RM_AFTER_PROV_FLAG | ADD_DEV_START_PROV_NOW_FLAG | ADD_DEV_FLUSHABLE_DEV_FLAG));
        }
        break;
    }

    case ESP_BLE_MESH_PROVISIONER_PROV_COMPLETE_EVT: {
        uint16_t unicast_addr = param->provisioner_prov_complete.unicast_addr;
        ESP_LOGI(TAG, "==================================================");
        ESP_LOGI(TAG, "[PROVISIONER] Provisioning Sukses untuk Node: 0x%04X (ID: 0x%02X)!",
                 unicast_addr, pending_prov_target_id);
        ESP_LOGI(TAG, "==================================================");

        if (pending_prov_target_id == 0x01) {
            actual_pump_addr = unicast_addr;
            ESP_LOGI(TAG, "[PROVISIONER] Node 1 (Pompa) terdaftar di Address: 0x%04X", actual_pump_addr);
        } else if (pending_prov_target_id == 0x02) {
            actual_sensor_addr = unicast_addr;
            ESP_LOGI(TAG, "[PROVISIONER] Node 2 (Sensor) terdaftar di Address: 0x%04X", actual_sensor_addr);
        }

        // Distribusikan AppKey ke Node yang baru terprovisi
        esp_ble_mesh_cfg_client_set_state_t set_state = {0};
        set_state.app_key_add.net_idx = ESP_BLE_MESH_NET_IDX;
        set_state.app_key_add.app_idx = ESP_BLE_MESH_APP_IDX;
        memcpy(set_state.app_key_add.app_key, mesh_app_key, 16);

        esp_ble_mesh_client_common_param_t common = {
            .opcode = ESP_BLE_MESH_MODEL_OP_APP_KEY_ADD,
            .model = config_client.model,
            .ctx.net_idx = ESP_BLE_MESH_NET_IDX,
            .ctx.app_idx = ESP_BLE_MESH_APP_IDX,
            .ctx.addr = unicast_addr,
            .ctx.send_ttl = 7,
            .msg_role = ROLE_PROVISIONER,
        };
        esp_ble_mesh_config_client_set_state(&common, &set_state);
        break;
    }

    default:
        break;
    }
}

// Callback Config Client (Konfirmasi AppKey Add & Bind Model)
static void ble_mesh_cfg_client_cb(esp_ble_mesh_cfg_client_cb_event_t event,
                                   esp_ble_mesh_cfg_client_cb_param_t *param)
{
    if (event == ESP_BLE_MESH_CFG_CLIENT_SET_STATE_EVT) {
        if (param->params->opcode == ESP_BLE_MESH_MODEL_OP_APP_KEY_ADD) {
            uint16_t target_addr = param->params->ctx.addr;
            ESP_LOGI(TAG, "[PROVISIONER] AppKey berhasil diterima node 0x%04X! Mengikat Model App...",
                     target_addr);

            // Ikat Model yang tepat berdasarkan tipe Node
            if (pending_prov_target_id == 0x02) {
                ESP_LOGI(TAG, "[PROVISIONER] Mengikat Vendor Sensor Model ke Node Sensor (0x%04X)...", target_addr);
                bind_model_to_node(target_addr, 0x0002, CID_ESP);
            } else if (pending_prov_target_id == 0x01 || target_addr == actual_pump_addr || target_addr == 0x0003 || target_addr == 0x0002) {
                ESP_LOGI(TAG, "[PROVISIONER] Mengikat Generic OnOff Server ke Node Pompa (0x%04X)...", target_addr);
                bind_model_to_node(target_addr, ESP_BLE_MESH_MODEL_ID_GEN_ONOFF_SRV, ESP_BLE_MESH_CID_NVAL);
            }
        } else if (param->params->opcode == ESP_BLE_MESH_MODEL_OP_MODEL_APP_BIND) {
            ESP_LOGI(TAG, "[PROVISIONER] Model pada node 0x%04X selesai diikat (Status: 0x%02X)!",
                     param->params->ctx.addr, param->status_cb.model_app_status.status);
        }
    }
}

// Callback Generic Client (Menerima status konfirmasi dari Pompa Node 1)
static void ble_mesh_generic_client_cb(esp_ble_mesh_generic_client_cb_event_t event,
                                       esp_ble_mesh_generic_client_cb_param_t *param)
{
    if (event == ESP_BLE_MESH_GENERIC_CLIENT_GET_STATE_EVT ||
        event == ESP_BLE_MESH_GENERIC_CLIENT_SET_STATE_EVT) {
        if (param->params->opcode == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_STATUS) {
            uint8_t state = param->status_cb.onoff_status.present_onoff;
            ESP_LOGI(TAG, "[STATUS MESH] Konfirmasi Pompa Node 1: %s", state ? "MENYALA (ON)" : "PADAM (OFF)");

            if (mqtt_connected) {
                char payload[64];
                snprintf(payload, sizeof(payload), "{\"node\":1,\"pump_state\":%d,\"source\":\"mesh_status\"}", state);
                esp_mqtt_client_publish(mqtt_client, MQTT_TOPIC_PUMP_STATE, payload, 0, 1, 0);
            }
        }
    }
}

// Callback Custom / Vendor Model (Menerima Telemetri Sensor dari Node 2)
static void ble_mesh_custom_model_cb(esp_ble_mesh_model_cb_event_t event,
                                     esp_ble_mesh_model_cb_param_t *param)
{
    if (event == ESP_BLE_MESH_MODEL_OPERATION_EVT) {
        if (param->model_operation.opcode == ESP_BLE_MESH_VND_MODEL_OP_SENSOR_DATA) {
            uint16_t raw_adc = *(uint16_t *)param->model_operation.msg;
            const char* status_str = (raw_adc >= SOIL_DRY_THRESHOLD) ? "KERING" :
                                     ((raw_adc <= SOIL_WET_THRESHOLD) ? "BASAH" : "OPTIMAL");

            ESP_LOGI(TAG, "==================================================");
            ESP_LOGI(TAG, "[TELEMETRI DARI NODE 2] Nilai ADC: %d | Status: %s", raw_adc, status_str);
            ESP_LOGI(TAG, "==================================================");

            // 1. Edge Autonomy Logic (Otonom di ESP32 Gateway - Bebas dari Single Point of Failure Laptop/Host)
            if (edge_auto_mode) {
                if (raw_adc >= SOIL_DRY_THRESHOLD && current_pump_state != 1) {
                    ESP_LOGW(TAG, ">>> [EDGE AUTONOMY] Tanah KERING (ADC: %d >= %d)! Mengirim OnOff Set (1) ke Node 1...",
                             raw_adc, SOIL_DRY_THRESHOLD);
                    send_mesh_onoff_to_node1(1);
                    current_pump_state = 1;
                    if (mqtt_connected) {
                        char p_buf[64];
                        snprintf(p_buf, sizeof(p_buf), "{\"pump_state\":1,\"auto_mode\":true}");
                        esp_mqtt_client_publish(mqtt_client, MQTT_TOPIC_PUMP_STATE, p_buf, 0, 1, 0);
                    }
                } else if (raw_adc <= SOIL_WET_THRESHOLD && current_pump_state != 0) {
                    ESP_LOGW(TAG, ">>> [EDGE AUTONOMY] Tanah BASAH (ADC: %d <= %d)! Mengirim OnOff Set (0) ke Node 1...",
                             raw_adc, SOIL_WET_THRESHOLD);
                    send_mesh_onoff_to_node1(0);
                    current_pump_state = 0;
                    if (mqtt_connected) {
                        char p_buf[64];
                        snprintf(p_buf, sizeof(p_buf), "{\"pump_state\":0,\"auto_mode\":true}");
                        esp_mqtt_client_publish(mqtt_client, MQTT_TOPIC_PUMP_STATE, p_buf, 0, 1, 0);
                    }
                }
            } else {
                ESP_LOGI(TAG, "[EDGE] Mode MANUAL aktif (HMI Override). Mengabaikan otomasi sensor.");
            }

            // 2. Teruskan telemetri ke Broker MQTT untuk HMI Dashboard (jika terhubung)
            if (mqtt_connected) {
                char payload[128];
                snprintf(payload, sizeof(payload),
                         "{\"node\":2,\"raw_adc\":%d,\"status\":\"%s\"}", raw_adc, status_str);
                esp_mqtt_client_publish(mqtt_client, MQTT_TOPIC_SENSOR, payload, 0, 1, 0);
                ESP_LOGI(TAG, "[GATEWAY -> MQTT] Telemetri dipublish ke topik: %s", MQTT_TOPIC_SENSOR);
            }
        }
    }
}

void app_main(void)
{
    esp_err_t err;

    ESP_LOGI(TAG, "Memulai Node 4 (Provisioner & Wi-Fi MQTT Gateway)...");

    // 1. Inisialisasi NVS Flash
    err = init_nvs_storage();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Inisialisasi NVS gagal: %s", esp_err_to_name(err));
        return;
    }

    // 2. Inisialisasi Wi-Fi Station
    init_wifi_station();

    // 3. Inisialisasi MQTT Client
    init_mqtt_client();

    // 4. Inisialisasi Bluetooth Stack
    err = init_bluetooth_stack();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Inisialisasi Bluetooth gagal: %s", esp_err_to_name(err));
        return;
    }

    // 5. Daftarkan Callback Resmi BLE Mesh
    esp_ble_mesh_register_prov_callback(ble_mesh_provisioning_cb);
    esp_ble_mesh_register_config_client_callback(ble_mesh_cfg_client_cb);
    esp_ble_mesh_register_generic_client_callback(ble_mesh_generic_client_cb);
    esp_ble_mesh_register_custom_model_callback(ble_mesh_custom_model_cb);

    // 6. Inisialisasi BLE Mesh Provisioner
    err = esp_ble_mesh_init(&prov, &composition);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Gagal inisialisasi BLE Mesh Provisioner: %s", esp_err_to_name(err));
        return;
    }

    // 7. Aktifkan Provisioner PB-ADV & PB-GATT
    err = esp_ble_mesh_provisioner_prov_enable(ESP_BLE_MESH_PROV_ADV | ESP_BLE_MESH_PROV_GATT);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Gagal aktifkan Provisioner: %s", esp_err_to_name(err));
        return;
    }

    ESP_LOGI(TAG, "Node 4 Gateway (Provisioner + Wi-Fi MQTT) SIAGA BEROPERASI.");
}
