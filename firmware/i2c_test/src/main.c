/*
 * Copyright (c) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/i2c.h>
#include <zephyr/logging/log.h>
#include <dk_buttons_and_leds.h>

#include "config.h"
#include "mpu6050.h"
#include "hmc5883l.h"
#include "remote.h"
#include "callbacks.h"

#define SLEEP_TIME_MS   1000
#define I2C_NODE DT_NODELABEL(i2c0)
#define BT_STATUS_LED DK_LED1

LOG_MODULE_REGISTER(app);


static const struct device *i2c_dev = DEVICE_DT_GET(I2C_NODE);
static uint8_t  i2c_buf[6];
static uint16_t acc_data[3];
static uint16_t gyro_data[3];
static uint16_t mag_data[3];
static struct bt_conn* current_conn;


void button_handler(uint32_t button_state, uint32_t has_changed) {
	if(button_state & has_changed) {
		switch(has_changed) {
			case DK_BTN1_MSK:
				dk_set_led(DK_LED1, 1);
			break;
			case DK_BTN2_MSK:
				dk_set_led(DK_LED2, 1);
			break;
			case DK_BTN3_MSK:
				dk_set_led(DK_LED3, 1);
			break;
			case DK_BTN4_MSK:
				dk_set_led(DK_LED4, 1);
			break;
		}
	}
}

void init_buttons_and_leds() {
	int ret;
	ret = dk_buttons_init(button_handler);
	if(ret) {
		LOG_ERR("Couldn't init buttons, err: %d", ret);
	}
	ret = dk_leds_init();
	if(ret) {
		LOG_ERR("Couldn't init LEDs, err: %d", ret);
	}
}
void on_connected(struct bt_conn* conn, uint32_t err) {
    if(err) {
        LOG_ERR("connection err: %d", err);
		return;
    }
	LOG_INF("Bluetooth connected");
	current_conn = bt_conn_ref(conn);
	dk_set_led_on(BT_STATUS_LED);
}

void on_disconnected(struct bt_conn* conn, uint32_t reason) {
	LOG_INF("Disconnected, reason: 0x%x", reason);
	dk_set_led_off(BT_STATUS_LED);
	if(current_conn) {
		bt_conn_unref(current_conn);
		current_conn = NULL;
	}
}

struct bt_conn_cb bluetooth_callbacks = {
	.connected = on_connected,
	.disconnected = on_disconnected
};

void main(void) {
	int ret;
	
	if( !(ret = device_is_ready(i2c_dev)) ) {
		LOG_ERR("I2C device not ready, returned with code %d", ret);
	} else {
		LOG_DBG("I2C device is ready");
	}

	init_buttons_and_leds();
	MPU_init(i2c_dev);
	HMC_init(i2c_dev);
	ret = bluetooth_init(&bluetooth_callbacks);

	while(true) {
		k_msleep(SLEEP_TIME_MS);
	
		ret = MPU_read_acc(acc_data);
		if(ret) {
			LOG_ERR("Error while reading acc");
		}

		ret = MPU_read_gyro(gyro_data);
		if(ret) {
			LOG_ERR("Error while reading gyro");
		}

		ret = HMC_read_mag(mag_data);
		if(ret) {
			LOG_ERR("Error while reading mag");
		}

		LOG_INF("acc:  %f, %f, %f", 
		(float)(ACC_SCALE_FACTOR)*(int16_t)acc_data[0], 
		(float)(ACC_SCALE_FACTOR)*(int16_t)acc_data[1], 
		(float)(ACC_SCALE_FACTOR)*(int16_t)acc_data[2]);

		LOG_INF("gyro: %f, %f, %f",
		(float)(GYRO_SCALE_FACTOR)*(int16_t)gyro_data[0], 
		(float)(GYRO_SCALE_FACTOR)*(int16_t)gyro_data[1], 
		(float)(GYRO_SCALE_FACTOR)*(int16_t)gyro_data[2]);

		LOG_INF("mag:  %f, %f, %f", 
		(float)(MAG_SCALE_FACTOR)*(int16_t)mag_data[0],
		(float)(MAG_SCALE_FACTOR)*(int16_t)mag_data[1],
		(float)(MAG_SCALE_FACTOR)*(int16_t)mag_data[2]);

	}

}
