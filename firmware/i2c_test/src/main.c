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

#include "config.h"
#include "mpu6050.h"
#include "hmc5883l.h"

LOG_MODULE_REGISTER(app);

/* 1000 msec = 1 sec */
#define SLEEP_TIME_MS   1000

#define I2C_NODE DT_NODELABEL(i2c0)
// #define BUTTONS_NODE DT_NODELABEL(button)
static const struct device *i2c_dev = DEVICE_DT_GET(I2C_NODE);

static uint8_t  i2c_buf[6];
static uint16_t acc_data[3];
static uint16_t gyro_data[3];
static uint16_t mag_data[3];


void main(void) {
	int ret;
	if( !(ret = device_is_ready(i2c_dev)) ) {
		LOG_ERR("I2C device not ready, returned with code %d", ret);
	} else {
		LOG_DBG("I2C device is ready");
	}

	MPU_init(i2c_dev);
	HMC_init(i2c_dev);

	while(true) {
		k_msleep(SLEEP_TIME_MS);
	
		ret = MPU_read_acc(acc_data);
		if(ret) {
			LOG_ERR("Error while reading acc");
			// continue;
		}

		ret = MPU_read_gyro(gyro_data);
		if(ret) {
			LOG_ERR("Error while reading gyro");
			// continue;
		}

		ret = HMC_read_mag(mag_data);
		if(ret) {
			LOG_ERR("Error while reading mag");
			// continue;
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
