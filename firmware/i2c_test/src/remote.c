#include "remote.h"

#define LOG_MODULE_NAME remote
LOG_MODULE_REGISTER(remote);

static K_SEM_DEFINE(bt_init_ok, 1, 1); // i dunno what it does

#define DEVICE_NAME CONFIG_BT_DEVICE_NAME
#define DEVICE_NAME_LEN (sizeof(DEVICE_NAME - 1) )

static const struct bt_data ad[] = {
    BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
    BT_DATA(BT_DATA_NAME_COMPLETE, DEVICE_NAME, DEVICE_NAME_LEN)
};

static const struct bt_data sd[] = {
    BT_DATA_BYTES(BT_DATA_UUID128_ALL, BT_UUID_REMOTE_SERV_VAL)
};

BT_GATT_SERVICE_DEFINE(remote_srv, 
BT_GATT_PRIMARY_SERVICE(BT_UUID_REMOTE_SERVICE),
);

/* ========== CALLBACKS =========== */
void bt_ready(int err) {
    if(err) {
        LOG_ERR("bt_enable returned %d", err);
    } else {
        LOG_DBG("bluetooth enabled");
    }
    k_sem_give(&bt_init_ok);
}


int bluetooth_init(struct bt_conn_cb* callbacks) {
    int err;
    LOG_INF("Initializing bluetooth");

    if(callbacks != NULL) {
        bt_conn_cb_register(callbacks);
    } else {
        return NRFX_ERROR_NULL;
    }

    err = bt_enable(bt_ready);
    if(err) { 
        LOG_ERR("bt_enable returned %d", err);
        return err;
    }

    k_sem_take(&bt_init_ok, K_FOREVER);

    err = bt_le_adv_start(BT_LE_ADV_CONN, ad, ARRAY_SIZE(ad), sd, ARRAY_SIZE(sd));
    if(err) {
        LOG_ERR("Couldn't start advertising (err: %d)", err);
        return err;
    }
    LOG_INF("Bluetooth started advertising");

    return err;
}