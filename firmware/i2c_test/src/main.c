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

/* 1000 msec = 1 sec */
#define SLEEP_TIME_MS   1000

#define I2C_NODE DT_NODELABEL(i2c0)

LOG_MODULE_REGISTER(APP);

static const struct device *i2c_dev = DEVICE_DT_GET(I2C_NODE);

// static uint8_t  i2c_buf[6];
static uint16_t sensor_data[3];


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
	
		ret = MPU_read_acc(sensor_data);
		if(ret) {
			LOG_ERR("Error while reading acc");
			// continue;
		}
		LOG_INF("ACC:  x = %12f, y = %12f, z = %12f", 
		(float)ACC_SCALE_FACTOR*(int16_t)sensor_data[0], 
		(float)ACC_SCALE_FACTOR*(int16_t)sensor_data[1], 
		(float)ACC_SCALE_FACTOR*(int16_t)sensor_data[2]);

		ret = MPU_read_gyro(sensor_data);
		if(ret) {
			LOG_ERR("Error while reading gyro");
			// continue;
		}
		LOG_INF("GYRO: x = %12f, y = %12f, z = %12f", 
		(float)GYRO_SCALE_FACTOR*(int16_t)sensor_data[0], 
		(float)GYRO_SCALE_FACTOR*(int16_t)sensor_data[1], 
		(float)GYRO_SCALE_FACTOR*(int16_t)sensor_data[2]);

		ret = HMC_read_mag(sensor_data);
		if(ret) {
			LOG_ERR("Error while reading mag");
			continue;
		}
		LOG_INF("MAG: x = %6d, y = %6d, z = %6d", 
		(int16_t)sensor_data[0], 
		(int16_t)sensor_data[1], 
		(int16_t)sensor_data[2]);
	}

}
