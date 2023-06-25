#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/uuid.h>
#include <zephyr/bluetooth/gatt.h>
#include <zephyr/bluetooth/hci.h>


#define BT_UUID_REMOTE_SERV_VAL \
    BT_UUID_128_ENCODE(0x21370001, 0x2137, 0x2137, 0x2137, 0x213721372137)
// #define BT_UUID_REMOTE_BUTTON_CHRC_VAL \
//     BT_UUID_128_ENCODE(0x21370002, 0x2137, 0x2137, 0x2137, 0x213721372137)

#define BT_UUID_REMOTE_IMU_CHRC_VAL \
    BT_UUID_128_ENCODE(0x21370005, 0x2137, 0x2137, 0x2137, 0x213721372137)
// #define BT_UUID_REMOTE_GYRO_CHRC_VAL \
//     BT_UUID_128_ENCODE(0x21370003, 0x2137, 0x2137, 0x2137, 0x213721372137)
// #define BT_UUID_REMOTE_MAG_CHRC_VAL \
//     BT_UUID_128_ENCODE(0x21370004, 0x2137, 0x2137, 0x2137, 0x213721372137)

#define BT_UUID_REMOTE_SERVICE     BT_UUID_DECLARE_128(BT_UUID_REMOTE_SERV_VAL)
// #define BT_UUID_REMOTE_BUTTON_CHRC BT_UUID_DECLARE_128(BT_UUID_REMOTE_BUTTON_CHRC_VAL)
#define BT_UUID_REMOTE_IMU_CHRC  BT_UUID_DECLARE_128(BT_UUID_REMOTE_IMU_CHRC_VAL)
// #define BT_UUID_REMOTE_GYRO_CHRC BT_UUID_DECLARE_128(BT_UUID_REMOTE_GYRO_CHRC_VAL)
// #define BT_UUID_REMOTE_MAG_CHRC  BT_UUID_DECLARE_128(BT_UUID_REMOTE_MAG_CHRC_VAL)


int bluetooth_init(struct bt_conn_cb* callbacks);
void set_button_value(int value);
uint8_t* get_buffer_addr(void);