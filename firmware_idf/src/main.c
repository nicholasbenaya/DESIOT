/* =========================================================================
 * DESIOT ITS SURABAYA - FIRMWARE ESP-IDF MURNI
 * Multi-Target Entry Point
 * ========================================================================= */

#if defined(CONFIG_NODE_3_RELAY_FRIEND)
#include "node3_relay_friend.c"
#elif defined(CONFIG_NODE_1_PUMP)
#include "node1_pump.c"
#elif defined(CONFIG_NODE_2_SENSOR_LPN)
#include "node2_sensor_lpn.c"
#elif defined(CONFIG_NODE_4_GATEWAY)
#include "node4_gateway.c"
#else
#include "node3_relay_friend.c" // Default fallback
#endif
