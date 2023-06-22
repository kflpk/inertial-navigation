#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/uuid.h>
#include <zephyr/bluetooth/gatt.h>
#include <zephyr/bluetooth/hci.h>


#define BT_UUID_REMOTE_SERV_VAL \
    BT_UUID_128_ENCODE(0xE9EA0001, 0xE19B, 0x482D, 0x9293, 0xC7907585FC48)

#define BT_UUID_REMOTE_SERVICE BT_UUID_DECLARE_128(BT_UUID_REMOTE_SERV_VAL)

int bluetooth_init(struct bt_conn_cb* callbacks);